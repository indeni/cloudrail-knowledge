import os
from functools import lru_cache
from typing import Dict, Optional, List
from cfn_tools import ODict
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_utils import CloudformationUtils
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_info import CloudformationResourceInfo
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_transform_context import CloudformationTransformContext
from cloudrail.knowledge.context.aws.cloudformation.intrinsic_functions.cloudformation_intrinsic_functions import CloudformationFunction, FunctionsFactory


class CloudformationMetadataParser:
    EXTRA_PARAMS: list = ['region', 'account_id', 'stack_name', 'iac_type', 'cloud_provider', 'cfn_template_file_name']

    def __init__(self, cfn_template_file: str, logical_to_physical_id_map: Dict[str, str],
                 cfn_template_params: dict, logical_id_to_resource_info_map: Dict[str, CloudformationResourceInfo],
                 scanner_context: AwsEnvironmentContext = None) -> None:
        super().__init__()
        self._logical_to_physical_id_map: Dict[str, str] = logical_to_physical_id_map or {}
        self._cfn_template_dict: dict = CloudformationUtils.load_cfn_template(cfn_template_file)
        self._cfn_template_params: dict = cfn_template_params or {}
        if 'cfn_template_file_name' not in self._cfn_template_params:
            self._cfn_template_params['cfn_template_file_name'] = os.path.basename(cfn_template_file)
        self.logical_id_to_resource_info_map: Dict[str, CloudformationResourceInfo] = logical_id_to_resource_info_map
        self._init_template_param_map()
        self._cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, dict]] = self._create_resources_by_type_map()
        self._cfn_transform_context: CloudformationTransformContext = self._create_transform_context(scanner_context)

    def _create_transform_context(self, scanner_context: AwsEnvironmentContext) -> CloudformationTransformContext:
        cfn_resources_by_type_map: Dict[CloudformationResourceType, AliasesDict[Mergeable]] = {}
        if scanner_context:
            cfn_resources_by_type_map = self._create_cfn_resources_by_type_map(scanner_context)
        references_map: dict = self._logical_to_physical_id_map.copy()
        references_map.update(self._cfn_template_params)
        cfn_resources_map: Dict[str, dict] = {logical_id: cfn_resource for entry in self._cfn_by_type_map.values()
                                              for logical_id, cfn_resource in entry.items()}

        pseudo_params: dict = self._create_pseudo_params_map(references_map, scanner_context)
        references_map.update(pseudo_params)
        return CloudformationTransformContext(logical_to_physical_id_map=self._logical_to_physical_id_map,
                                              cfn_template_params=self._cfn_template_params,
                                              cfn_by_type_map=self._cfn_by_type_map,
                                              cfn_resources_by_type_map=cfn_resources_by_type_map,
                                              cfn_template_dict=self._cfn_template_dict,
                                              references_map=references_map,
                                              cfn_resources_map=cfn_resources_map,
                                              availability_zones=self._create_region_to_azs_map(scanner_context))

    def parse(self, iac_url_template: Optional[str], salt: Optional[str]) -> dict:
        self._transform_mappings()
        self._transform_conditions()
        self._remove_resources_by_condition()
        self._transform_resources()
        self._set_resource_state()
        self._set_extra_data(iac_url_template, salt)
        return self._cfn_by_type_map.copy()

    def _remove_resources_by_condition(self):
        all_resources: dict = self._get_resources()
        all_conditions: dict = self._get_conditions()
        for resource_name in list(all_resources.keys()):
            resource: dict = all_resources[resource_name]
            if 'Condition' in resource:
                resource['Condition'] = all_conditions.get(resource['Condition'])
                if not resource.get('Condition'):
                    del all_resources[resource_name]
                    resource_type: CloudformationResourceType = CloudformationResourceType(resource['Type'])
                    del self._cfn_by_type_map[resource_type][resource_name]
                    if not self._cfn_by_type_map[resource_type]:
                        del self._cfn_by_type_map[resource_type]

    def _add_physical_id(self, cfn_resource: dict):
        logical_id: str = cfn_resource['logical_id']
        if physical_id := self._logical_to_physical_id_map.get(logical_id):
            cfn_resource['physical_id'] = physical_id

    def _create_resources_by_type_map(self) -> Dict[CloudformationResourceType, Dict[str, dict]]:
        cfn_resources: ODict = self._get_resources()
        cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, dict]] = {}
        for logical_id, cfn_res in cfn_resources.items():
            cfn_res['logical_id'] = logical_id
            cfn_type: CloudformationResourceType = cfn_res.get('Type')
            if cfn_type not in cfn_by_type_map:
                cfn_by_type_map[cfn_type] = {}
            self._inject_extra_params(cfn_res)
            self._add_physical_id(cfn_res)
            cfn_by_type_map[cfn_type][logical_id] = cfn_res
        return cfn_by_type_map

    def _get_resources(self) -> ODict:
        return self._cfn_template_dict.get('Resources', ODict())

    def _get_conditions(self) -> ODict:
        return self._cfn_template_dict.get('Conditions', ODict())

    def _get_mappings(self) -> ODict:
        return self._cfn_template_dict.get('Mappings', ODict())

    def get_cfn_template_as_dict(self) -> dict:
        return self._cfn_template_dict.copy()

    def _inject_extra_params(self, cfn_resource: dict) -> None:
        cfn_resource.update(self._get_allowed_cfn_params())

    @lru_cache
    def _get_allowed_cfn_params(self) -> dict:
        return {param_name: self._cfn_template_params[param_name] for param_name in self.EXTRA_PARAMS
                if param_name in self._cfn_template_params}

    def _init_template_param_map(self):
        for param_name, param_attr in self._get_parameters().items():
            if param_name not in self._cfn_template_params:
                default_value = param_attr.get('Default', None)
                if default_value:
                    self._cfn_template_params[param_name] = default_value
                else:
                    raise Exception(f'Missing template parameter={param_name}')

    def _get_parameters(self) -> ODict:
        return self._cfn_template_dict.get('Parameters', ODict())

    def _transform_conditions(self):
        conditions: dict = self._get_conditions()
        for name, expression in conditions.items():
            CloudformationFunction.transform_and_set(name, expression, conditions, self._cfn_transform_context)

    def _transform_resources(self):
        resources: dict = self._get_resources()
        for resource in resources.values():
            properties: dict = resource.get('Properties', {})
            self._cfn_template_crawler(current_node=properties, parent_node=resources)

            for property_name, property_value in properties.copy().items():
                if property_value == 'AWS::NoValue':
                    del properties[property_name]

    def _transform_mappings(self):
        mappings: dict = self._get_mappings()
        for map_name, map_value in mappings.items():
            CloudformationFunction.transform_and_set(map_name, map_value, mappings, self._cfn_transform_context)

    def _set_extra_data(self, iac_url_template: Optional[str], salt: Optional[str]):
        for resource in self._get_resources().values():
            if iac_url_template:
                resource['iac_url_template'] = iac_url_template
            if salt and resource.get('Properties'):
                resource['Properties']['salt'] = salt

    def _set_resource_state(self):
        logical_id_to_resource_map: Dict[str, dict] = {logical_id: resource for resources_map in self._cfn_transform_context.cfn_by_type_map.values()
                                                       for logical_id, resource in resources_map.items()}

        for logical_id, resource in logical_id_to_resource_map.items():
            if logical_id in self._cfn_transform_context.logical_to_physical_id_map:
                resource['iac_action'] = IacActionType.UPDATE
            else:
                resource['iac_action'] = IacActionType.CREATE

        res_type_by_physical_id_map: Dict[str, CloudformationResourceType] = \
            {res.get_id(): res_type for res_type, res_map in self._cfn_transform_context.cfn_resources_by_type_map.items()
             for res in res_map.values()}
        deleted_resources_map: Dict[CloudformationResourceType, Dict[str, Dict]] = {}

        for logical_id, physical_id in self._cfn_transform_context.logical_to_physical_id_map.items():
            if logical_id not in logical_id_to_resource_map:
                res_type_str: str = res_type_by_physical_id_map.get(physical_id)
                if res_type_str:
                    res_type: CloudformationResourceType = CloudformationResourceType(res_type_str)
                    if res_type not in deleted_resources_map:
                        deleted_resources_map[res_type] = {}
                    deleted_resources_map[res_type][logical_id] = {
                        'Type': res_type,
                        'logical_id': logical_id,
                        'physical_id': physical_id,
                        'iac_action': IacActionType.DELETE
                        }
                    self._inject_extra_params(deleted_resources_map[res_type][logical_id])

        for res_type, resources in deleted_resources_map.items():
            if res_type not in self._cfn_by_type_map:
                self._cfn_by_type_map[res_type] = {}
            self._cfn_by_type_map[res_type].update(resources)

    @staticmethod
    def _create_pseudo_params_map(references_map: dict, scanner_context: AwsEnvironmentContext):
        stack_info: Optional[CloudformationResourceInfo] = None
        if scanner_context:
            stack_info: CloudformationResourceInfo = next(iter(res_info for res_info in scanner_context.cfn_resources_info if
                                                               res_info.stack_name == references_map.get('stack_name') and
                                                               res_info.region == references_map.get('region')), None)
        return {
            'AWS::Region': references_map.get('region'),
            'AWS::AccountId': references_map.get('account_id'),
            'AWS::NotificationARNs': [],  # todo - get actual arns list
            'AWS::NoValue': 'AWS::NoValue',
            'AWS::Partition': 'aws',  # todo - implement get partition by region
            'AWS::StackId': (stack_info and stack_info.stack_id),
            'AWS::StackName': references_map.get('stack_name'),
            'AWS::URLSuffix': 'amazonaws.com'  # todo - implement get url suffix by region
        }

    @staticmethod
    def _create_region_to_azs_map(scanner_context: AwsEnvironmentContext) -> dict:
        availability_zones: Dict[str, List[str]] = {}
        if scanner_context:
            for zone in scanner_context.availability_zones.values():
                if zone.region not in availability_zones:
                    availability_zones[zone.region] = []
                availability_zones[zone.region].append(zone.zone_name)

            for zones in availability_zones.values():
                zones.sort()
        return availability_zones

    @staticmethod
    def _create_cfn_resources_by_type_map(scanner_context: AwsEnvironmentContext) -> Dict[CloudformationResourceType, AliasesDict[Mergeable]]:
        return {
            CloudformationResourceType.VPC: scanner_context.vpcs,
            CloudformationResourceType.EC2_INSTANCE: AliasesDict(*scanner_context.ec2s),
            CloudformationResourceType.SECURITY_GROUP: scanner_context.security_groups,
            CloudformationResourceType.S3_BUCKET: scanner_context.s3_buckets,
            CloudformationResourceType.ATHENA_WORKGROUP: AliasesDict(*scanner_context.athena_workgroups),
            CloudformationResourceType.INTERNET_GATEWAY: AliasesDict(*scanner_context.internet_gateways),
            CloudformationResourceType.VPC_GATEWAY_ATTACHMENT: scanner_context.vpc_gateway_attachment,
            CloudformationResourceType.ROUTE_TABLE: scanner_context.route_tables,
            CloudformationResourceType.ROUTE: AliasesDict(*scanner_context.routes),
            CloudformationResourceType.SUBNET_ROUTE_TABLE_ASSOCIATION: AliasesDict(*scanner_context.route_table_associations),
            CloudformationResourceType.ELASTIC_LOAD_BALANCER: AliasesDict(*scanner_context.load_balancers),
            CloudformationResourceType.ELASTIC_LOAD_BALANCER_LISTENER: AliasesDict(*scanner_context.load_balancer_listeners),
            CloudformationResourceType.API_GATEWAY_V2: AliasesDict(*scanner_context.api_gateways_v2),
            CloudformationResourceType.API_GATEWAY_V2_VPC_LINK: AliasesDict(*scanner_context.api_gateway_v2_vpc_links),
            CloudformationResourceType.API_GATEWAY_V2_INTEGRATION: AliasesDict(*scanner_context.api_gateway_v2_integrations),
            CloudformationResourceType.SUBNET: scanner_context.subnets,
            CloudformationResourceType.CLOUDTRAIL: AliasesDict(*scanner_context.cloudtrail),
            CloudformationResourceType.CODEBUILD_REPORTGROUP: AliasesDict(*scanner_context.codebuild_report_groups),
            CloudformationResourceType.BATCH_COMPUTE_ENVIRONMENT: AliasesDict(*scanner_context.batch_compute_environments)
        }

    def _cfn_template_crawler(self, current_node, parent_node, current_key: str = None):
        for child_key, child_node in current_node.items():
            if FunctionsFactory.has_function(child_key):
                value = CloudformationFunction.transform(current_node, self._cfn_transform_context)
                if isinstance(parent_node, dict):
                    parent_node[current_key] = value
                else:
                    parent_node.remove(current_node)
                    parent_node.append(value)

            elif isinstance(child_node, dict):
                self._cfn_template_crawler(child_node, current_node, child_key)
            elif isinstance(child_node, list):
                for item in list(child_node):
                    if isinstance(item, (dict, list)):
                        self._cfn_template_crawler(item, child_node, child_key)
