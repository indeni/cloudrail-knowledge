import dataclasses
import json
import logging
from abc import abstractmethod
from enum import Enum
from typing import List, Union, Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import LambdaAlias
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.drift_detection.drift_detection_result import DriftDetectionResult, Drift
from cloudrail.knowledge.utils.utils import hash_list
from deepdiff import DeepDiff


class BaseEnvironmentContextDriftDetector:

    @classmethod
    def find_drifts(cls, cm_context, tf_context_before, tf_context_after, workspace_id):
        drifts_before = cls._compare_environments(cm_context, tf_context_before)
        drifts_after = cls._compare_environments(cm_context, tf_context_after)
        drifts = cls._find_mutual_drifts(drifts_before, drifts_after)
        return DriftDetectionResult(drifts, cls._calculate_iac_coverage(cm_context, tf_context_after), workspace_id)

    @classmethod
    @abstractmethod
    def get_excluded_attributes(cls):
        pass

    @classmethod
    def _compare_entities(cls, attr: str, olds: Union[List[Mergeable], AliasesDict[Mergeable], dict],
                          news: Union[List[Mergeable], AliasesDict[Mergeable], dict]) -> List[Drift]:
        logging.info(f'comparing {attr}..')
        drifts = {}
        if isinstance(olds, (list, set)):
            identity_func = lambda x: x
            iterable = identity_func
            mergeable = identity_func
        elif isinstance(olds, dict):
            iterable = dict.items
            mergeable = lambda tpl: tpl[1]
        elif isinstance(olds, AliasesDict):
            iterable = AliasesDict.values
            mergeable = lambda x: x
        else:
            raise NotImplementedError(f"Merging components of type {type(olds).__name__} is not supported")

        if new := next((x for x in iterable(news)), None):
            if mergeable(new).get_keys() is None:
                logging.warning(f'An entity of type {type(new).__name__} did not implement "get_keys" method and therefore all new entities '
                                f'will overwrite old entities')

        for new in iterable(news):
            state = mergeable(new).iac_state
            if state:
                if isinstance(mergeable(new), LambdaAlias):
                    continue
                old = next((old for old in iterable(olds) if hash_list(mergeable(old).get_keys()) == hash_list(mergeable(new).get_keys())), None)
                if old:
                    if drift := cls._compare_entity(mergeable(new), mergeable(old)):
                        drifts[drift.resource_id] = drift
                else:
                    logging.warning(f'missing entity in live env {mergeable(new).iac_state.address}')
        return list(drifts.values())

    @classmethod
    def _compare_environments(cls, cm_ctx: BaseEnvironmentContext, tf_ctx: BaseEnvironmentContext) -> List[Drift]:
        drifts = []
        for attr in dir(cm_ctx):
            if not callable(getattr(cm_ctx, attr)) and not attr.startswith('_'):
                old_values = getattr(cm_ctx, attr)
                new_values = getattr(tf_ctx, attr)
                values = old_values or new_values
                if not values:
                    continue
                if isinstance(values, list):
                    values_class = values[0].__class__
                    if issubclass(values_class, Mergeable):
                        drifts.extend(cls._compare_entities(attr, old_values, new_values))
                if isinstance(values, dict):
                    values_class = list(values.values())[0].__class__
                    if issubclass(values_class, Mergeable):
                        drifts.extend(cls._compare_entities(attr, old_values, new_values))
                if isinstance(values, AliasesDict):
                    drifts.extend(cls._compare_entities(attr, old_values.values(), new_values.values()))
        return drifts

    @classmethod
    def _compare_entity(cls, tf_entity: Mergeable, cm_entity: Mergeable) -> Optional[Drift]:
        tf_dict = cls._to_simple_dict(tf_entity)
        cm_dict = cls._to_simple_dict(cm_entity)
        cls._filter_fields(tf_dict, cm_dict)
        diff = DeepDiff(tf_dict, cm_dict, ignore_order=True)
        if diff:
            return Drift(tf_entity.get_type(),
                         tf_entity.iac_state.address,
                         tf_dict,
                         cm_dict,
                         tf_entity.iac_state.resource_metadata and dataclasses.asdict(tf_entity.iac_state.resource_metadata),
                         str(diff),
                         cm_entity.get_cloud_resource_url(),
                         tf_entity.iac_state.iac_resource_url,
                         tf_entity.get_id())
        return None

    @classmethod
    def _to_simple_dict(cls, entity: Mergeable, max_depth=2) -> dict:
        res = {}
        excluded_attrs = cls.get_excluded_attributes()
        for attr in dir(entity):
            if callable(getattr(entity, attr)) or attr.startswith('_'):
                continue
            if attr in excluded_attrs:
                continue
            if 'default' in attr:
                continue
            value = getattr(entity, attr)
            if value is None:
                continue
            if isinstance(value, str):
                try:
                    dic_value = json.loads(value)
                    res[attr] = dic_value
                    continue
                except Exception:
                    pass
            if isinstance(value, (str, int, bool)):
                res[attr] = value
                continue
            if isinstance(value, Enum):
                res[attr] = value.value
            if value and isinstance(value, list):
                if isinstance(value[0], (str, int, bool, dict, tuple, list)):
                    res[attr] = value
                elif isinstance(value[0], Enum):
                    res[attr] = [v.value for v in value]
                elif (isinstance(value[0], Mergeable) and not value[0].is_standalone()) \
                        or not isinstance(value[0], Mergeable):
                    if max_depth > 0:
                        res[attr] = [cls._to_simple_dict(v, max_depth - 1) for v in value]
                continue
            if value and isinstance(value, set):
                head = value.pop()
                value.add(head)
                if isinstance(head, (str, int, bool)):
                    res[attr] = list(value)
                elif isinstance(head, Enum):
                    res[attr] = [v.value for v in value]
                elif (isinstance(head, Mergeable) and not head.is_standalone()) \
                        or not isinstance(head, Mergeable):
                    if max_depth > 0:
                        res[attr] = [cls._to_simple_dict(v, max_depth - 1) for v in value]
                continue
            if value and isinstance(value, dict):
                val = list(value.values())[0]
                if isinstance(val, (str, int, bool)):
                    res[attr] = value
                elif isinstance(val, Enum):
                    res[attr] = {k: v.value for k, v in value.items()}
                elif (isinstance(val, Mergeable) and not val.is_standalone()) \
                        or not isinstance(val, Mergeable):
                    if max_depth > 0:
                        res[attr] = {k: cls._to_simple_dict(v, max_depth - 1) for k, v in value.items()}
                continue
            if (isinstance(value, Mergeable) and not value.is_standalone()) or not isinstance(value, Mergeable):
                if max_depth > 0:
                    res[attr] = cls._to_simple_dict(value, max_depth - 1)
                continue
        return res

    @staticmethod
    def _find_mutual_drifts(drifts_before: List[Drift], drifts_after: List[Drift]):
        drifts_before_resources_ids = [drift.resource_id for drift in drifts_before]
        return [drift for drift in drifts_after if drift.resource_id in drifts_before_resources_ids]

    @classmethod
    def _filter_fields(cls, tf_dict: dict, cm_dict: dict):
        cls._filter_pseudo_fields(tf_dict, cm_dict)
        cls._filter_non_exists_empty_fields(cm_dict, tf_dict)
        cls._filter_non_exists_empty_fields(tf_dict, cm_dict)
        cls._filter_empty_fields(cm_dict, tf_dict)

    @staticmethod
    def _filter_pseudo_fields(tf_dict: dict, cm_dict: dict):
        for (key, value) in tf_dict.items():
            if isinstance(value, list) and [item for item in value if isinstance(item, str) and 'pseudo' in item]:
                tf_dict[key] = cm_dict[key]
            if isinstance(value, str) and 'pseudo' in value:
                tf_dict[key] = cm_dict[key]

    @staticmethod
    def _filter_non_exists_empty_fields(src_dict: dict, dst_dict: dict):
        non_exists_fields = set(dst_dict.keys()) - set(src_dict.keys())
        for non_exists_field in non_exists_fields:
            value = dst_dict[non_exists_field]
            if not isinstance(value, bool) and not value:
                del dst_dict[non_exists_field]

    @staticmethod
    def _filter_empty_fields(src_dict: dict, dst_dict: dict):
        common_fields = set(dst_dict.keys()).intersection(src_dict.keys())
        for common_field in common_fields:
            dst_value = dst_dict[common_field]
            src_value = src_dict[common_field]
            if not isinstance(dst_value, bool) and not isinstance(src_value, bool) and not dst_value and not src_value:
                del dst_dict[common_field]
                del src_dict[common_field]

    @classmethod
    def _calculate_iac_coverage(cls, cm_context: BaseEnvironmentContext, tf_context_after: BaseEnvironmentContext):
        cm_count = cls._count_number_of_resources(cm_context)
        iac_count = cls._count_number_of_resources(tf_context_after)
        iac_coverage = min(100, int(iac_count / cm_count * 100)) if cm_count > 0 else 100
        logging.info(f'iac_coverage calculation : cm count = {cm_count}, iac_count = {iac_count}, iac_coverage = {iac_coverage}%')
        return iac_coverage

    @classmethod
    def _count_number_of_resources(cls, context: BaseEnvironmentContext):
        count = 0
        excluded_attrs = ['managed_resources_summary', 'checkov_results']
        for attr in dir(context):
            if callable(getattr(context, attr)) or attr.startswith('_') or attr in excluded_attrs:
                continue
            values = getattr(context, attr)
            if isinstance(values, (list, set, dict, AliasesDict)):
                count += len(values)
        return count
