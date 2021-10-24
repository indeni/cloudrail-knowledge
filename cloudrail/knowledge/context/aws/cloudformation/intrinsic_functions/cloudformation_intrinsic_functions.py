import base64
import re
from abc import abstractmethod
from typing import Union, Tuple
from cfn_tools import ODict
from cloudrail.knowledge.utils.utils import flat_list
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_transform_context import CloudformationTransformContext
from cloudrail.knowledge.context.aws.cloudformation.intrinsic_functions.cloudformation_resource_attributes_mapper import CloudformationResourceAttributesMapper


class CloudformationFunction:

    @abstractmethod
    def action(self, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        pass

    @classmethod
    def is_all_values_valid(cls, *values) -> bool:
        for val in flat_list(values):
            if isinstance(val, list):
                result = all(cls.is_all_values_valid(item) for item in val)
                if not result:
                    return False
            elif isinstance(val, dict):
                dict_values = list(val.keys()) + list(val.values())
                result = all(cls.is_all_values_valid(item) for item in dict_values)
                if not result:
                    return False
            elif isinstance(val, str):
                if val != 'Condition' and (FunctionsFactory.has_function(val) or val.startswith('Fn::')):
                    return False
        return True

    @staticmethod
    def get_first_val(node: dict) -> Tuple:
        for key, value in node.items():
            return key, value

    @classmethod
    def transform_and_set(cls, key: str, node: Union[dict, list], parent_node: dict,
                          cfn_transform_context: CloudformationTransformContext):
        val = cls.transform(node, cfn_transform_context)
        if val is not None:
            parent_node[key] = val

    @staticmethod
    def transform(node, cfn_transform_context: CloudformationTransformContext):
        if isinstance(node, dict):
            func_name, func_expression = CloudformationFunction.get_first_val(node)
            if FunctionsFactory.has_function(func_name):
                func: CloudformationFunction = FunctionsFactory.get_function(func_name)
                val = func.action(func_name, func_expression, cfn_transform_context)
                if val is not None:
                    return val
        return node


class CloudformationRefFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        return cfn_transform_context.references_map.get(node, node)


class CloudformationGetAttFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        if cfn_resource := cfn_transform_context.cfn_resources_map.get(node[0]):
            property_value: str = cfn_resource.get('Properties', {}).get(node[1])
            if property_value := cls.transform(property_value, cfn_transform_context):
                return property_value
            else:
                cfn_resource: dict = cfn_transform_context.cfn_resources_map[node[0]]
                physical_id: str = cfn_transform_context.logical_to_physical_id_map.get(cfn_resource['logical_id'])
                if physical_id:
                    aws_resource = cfn_transform_context.cfn_resources_by_type_map\
                        .get(cfn_resource['Type'], {})\
                        .get(physical_id)  # all context resources should be in aliases dict with aws resource id as alias
                    if attr_value := CloudformationResourceAttributesMapper.get_attribute(aws_resource, node[1]):
                        return attr_value
        return f'{node[0]}.{node[1]}'


class CloudformationFIndInMapFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        map_name: str = cls.transform(node[0], cfn_transform_context)
        map_key: str = cls.transform(node[1], cfn_transform_context)
        map_sub_key: str = cls.transform(node[2], cfn_transform_context)
        if cls.is_all_values_valid(map_name, map_key, map_sub_key):
            mappings: dict = cfn_transform_context.cfn_template_dict.get('Mappings', {})
            return mappings.get(map_name, {}).get(map_key, {}).get(map_sub_key)
        else:
            return node


class CloudformationJoinFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        delimiter: str = cls.transform(node[0], cfn_transform_context)
        join_values: list = [cls.transform(val, cfn_transform_context) for val in node[1]]
        if cls.is_all_values_valid(join_values):
            return delimiter.join(join_values)
        else:
            return node


class CloudformationSplitFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        delimiter: str = cls.transform(node[0], cfn_transform_context)
        source = cls.transform(node[1], cfn_transform_context)
        if isinstance(source, str):
            split_values: list = source.split(delimiter)
            if cls.is_all_values_valid(split_values):
                return split_values
        return node


class CloudformationBase64Function(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        val = cls.transform(node, cfn_transform_context)
        if cls.is_all_values_valid(val):
            message_bytes = val.encode('ascii')
            return base64.b64encode(message_bytes)
        return node


class CloudformationEqualsConditionFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        val_1 = cls.transform(node[0], cfn_transform_context)
        val_2 = cls.transform(node[1], cfn_transform_context)
        if cls.is_all_values_valid(val_1, val_2):
            return val_1 == val_2
        else:
            return node

    @classmethod
    def get_value(cls, key: str, item):
        if isinstance(item, dict):
            return cls.get_first_val(item)
        else:
            return key, item


class BaseCloudformationConditionFunction(CloudformationFunction):

    @abstractmethod
    def action(self, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        pass

    @classmethod
    def get_condition_result(cls, condition_name_or_expression: Union[str, dict],
                             cfn_transform_context: CloudformationTransformContext):
        result = None
        if isinstance(condition_name_or_expression, list):
            condition_name_or_expression = condition_name_or_expression[0]
        if isinstance(condition_name_or_expression, str):
            result = cfn_transform_context.cfn_template_dict.get('Conditions', {}).get(condition_name_or_expression)
        if not isinstance(result, bool):
            result = cls.transform(result or condition_name_or_expression, cfn_transform_context)
        return result


class CloudformationIfConditionFunction(CloudformationFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        condition = cls.transform(node[0], cfn_transform_context)
        val_1 = cls.transform(node[1], cfn_transform_context)
        val_2 = cls.transform(node[2], cfn_transform_context)
        if cls.is_all_values_valid(condition, val_1, val_2):
            return val_1 if cfn_transform_context.cfn_template_dict.get('Conditions', {}).get(condition) else val_2
        else:
            return node


class CloudformationConditionFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        return cls.get_condition_result(node, cfn_transform_context)


class CloudformationNotConditionFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        val = cls.get_condition_result(node, cfn_transform_context)
        if cls.is_all_values_valid(val):
            return not val
        else:
            return node


class CloudformationAndConditionFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        conditions_results: list = []
        for condition in node:
            conditions_results.append(cls.get_condition_result(condition, cfn_transform_context))
        if cls.is_all_values_valid(conditions_results):
            return all(conditions_results)
        else:
            return node


class CloudformationOrConditionFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        conditions_results: list = []
        for condition in node:
            conditions_results.append(cls.get_condition_result(condition, cfn_transform_context))
        if cls.is_all_values_valid(conditions_results):
            return any(conditions_results)
        else:
            return node


class CloudformationSelectFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        if isinstance(node, list):
            val = None
            if not (isinstance(node[1], list) and node[0].isnumeric()):
                val = cls.transform(node[1], cfn_transform_context)
            if isinstance(val, list):
                if val:
                    return val[int(node[0])]
                return None
        return node


class CloudformationSubFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        pattern: str = '\\${.*?}'
        key_val_map: dict = {}
        sub_str: str = None

        if isinstance(node, list) and isinstance(node[0], str):
            sub_str = node[0]
            for index in range(1, len(node)):
                key, val = cls.get_first_val(node[index])
                val = cls.transform(val, cfn_transform_context)
                key_val_map.update({key: val})
        elif isinstance(node, str):
            sub_str = node

        if sub_str:
            for pattern_found in re.findall(pattern, sub_str):
                repl_key = cls._clear_inject_pattern(pattern_found)

                if repl_key in key_val_map:
                    repl_val = key_val_map[repl_key]
                elif '.' in repl_key:
                    repl_val = cls._transform_get_att(repl_key, cfn_transform_context)
                else:
                    repl_val = cfn_transform_context.references_map.get(repl_key, repl_key)
                sub_str = sub_str.replace(pattern_found, repl_val)
            return sub_str
        else:
            return node

    @staticmethod
    def _clear_inject_pattern(source: str) -> str:
        return source.replace('$', '').replace('{', '').replace('}', '')

    @classmethod
    def _transform_get_att(cls, repl_key: str, cfn_transform_context: CloudformationTransformContext):
        return cls.transform(ODict([['Fn::GetAtt', repl_key.split('.')]]), cfn_transform_context)


class CloudformationGetAZsFunction(BaseCloudformationConditionFunction):

    @classmethod
    def action(cls, key: str, node: dict, cfn_transform_context: CloudformationTransformContext):
        val = None
        if not isinstance(node, str):
            val = cls.transform(node, cfn_transform_context)
        if isinstance(node, str):
            val = node
        if isinstance(val, str):
            if val == '':
                val = 'AWS::Region'
            val = cfn_transform_context.references_map.get(val)
            return cfn_transform_context.availability_zones.get(val, [])
        else:
            return node


class FunctionsFactory:
    _INTRINSIC_FUNCTIONS_MAP = {
        'Ref': CloudformationRefFunction,
        'Fn::GetAtt': CloudformationGetAttFunction,
        'Fn::FindInMap': CloudformationFIndInMapFunction,
        'Fn::Join': CloudformationJoinFunction,
        'Fn::Split': CloudformationSplitFunction,
        'Fn::Base64': CloudformationBase64Function,
        'Fn::Equals': CloudformationEqualsConditionFunction,
        'Fn::If': CloudformationIfConditionFunction,
        'Condition': CloudformationConditionFunction,
        'Fn::Not': CloudformationNotConditionFunction,
        'Fn::And': CloudformationAndConditionFunction,
        'Fn::Or': CloudformationOrConditionFunction,
        'Fn::Select': CloudformationSelectFunction,
        'Fn::Sub': CloudformationSubFunction,
        'Fn::GetAZs': CloudformationGetAZsFunction
    }

    @classmethod
    def get_function(cls, key) -> CloudformationFunction:
        return cls._INTRINSIC_FUNCTIONS_MAP.get(key)

    @classmethod
    def has_function(cls, key) -> bool:
        return key in cls._INTRINSIC_FUNCTIONS_MAP.keys()
