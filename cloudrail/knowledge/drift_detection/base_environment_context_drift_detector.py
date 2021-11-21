import dataclasses
import logging
from abc import abstractmethod
from typing import List, Optional, Union

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import LambdaAlias
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.drift_detection.drift_detection_result import (Drift, DriftDetectionResult)
from cloudrail.knowledge.utils.utils import hash_list
from deepdiff import DeepDiff



class BaseEnvironmentContextDriftDetector:

    @classmethod
    @abstractmethod
    def supported_drift_resource(cls, mergeable: Mergeable):
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
            new_as_mergaeble = mergeable(new)
            if new_as_mergaeble.iac_state and new_as_mergaeble.is_standalone():
                if isinstance(new_as_mergaeble, LambdaAlias):
                    continue
                old = next((old for old in iterable(olds) if hash_list(mergeable(old).get_keys()) == hash_list(mergeable(new).get_keys())), None)
                if old:
                    if drift := cls._compare_entity(mergeable(new), mergeable(old)):
                        drifts[drift.resource_id] = drift
                # If the resource is missing from the cloud provider (=old), we will report it,
                # unless this is a resource which we do not build from the first place, due to API limitations.
                elif not old and cls.supported_drift_resource(new):
                    drifts[mergeable(new).iac_state.address] = Drift(new_as_mergaeble.get_type(),
                                                                     new_as_mergaeble.iac_state.address,
                                                                     new_as_mergaeble.to_drift_detection_object(),
                                                                     {},
                                                                     new_as_mergaeble.iac_state.resource_metadata and dataclasses.asdict(
                                                                         new_as_mergaeble.iac_state.resource_metadata),
                                                                     f'resource {new_as_mergaeble.iac_state.address} is missing from your cloud account, or we could not collect any data about it',
                                                                     '',
                                                                     new_as_mergaeble.iac_state.iac_resource_url)
                    logging.warning(f'missing entity in live env {new_as_mergaeble.iac_state.address}')
        return list(drifts.values())

    @classmethod
    def find_drifts(cls,
                    provider: CloudProvider,
                    iac_type: IacType,
                    account_data: str,
                    iac_file_before: str,
                    iac_file_after: str,
                    salt: str,
                    account_id: str,
                    workspace_id: str,
                    iac_url_template: str = None,
                    tenant_id: str = None,
                    region: str = None,
                    cfn_template_params: dict = None,
                    stack_name: str = None
                    ) -> DriftDetectionResult:
        cfn_template_params = cfn_template_params or {}
        environment_context_builder = EnvironmentContextBuilderFactory.get(provider, iac_type)
        scanner_context = environment_context_builder.build(account_data,
                                                            None,
                                                            ignore_exceptions=True,
                                                            run_enrichment_requiring_aws=False,
                                                            salt=salt,
                                                            account_id=account_id,
                                                            tenant_id=tenant_id,
                                                            region=region)
        iac_context_before = environment_context_builder.build(account_data_dir_path=account_data,
                                                               iac_file_path=iac_file_before,
                                                               account_id=account_id,
                                                               ignore_exceptions=True,
                                                               run_enrichment_requiring_aws=False,
                                                               use_after_data=False,
                                                               iac_url_template=iac_url_template,
                                                               salt=salt,
                                                               default_resources_only=True,
                                                               tenant_id=tenant_id,
                                                               region=region,
                                                               cfn_template_params=cfn_template_params,
                                                               stack_name=stack_name)
        iac_context_after = environment_context_builder.build(account_data_dir_path=account_data,
                                                              iac_file_path=iac_file_after,
                                                              account_id=account_id,
                                                              ignore_exceptions=True,
                                                              default_resources_only=True,
                                                              run_enrichment_requiring_aws=False,
                                                              use_after_data=True,
                                                              keep_deleted_entities=False,
                                                              iac_url_template=iac_url_template,
                                                              salt=salt,
                                                              tenant_id=tenant_id,
                                                              region=region,
                                                              cfn_template_params=cfn_template_params,
                                                              stack_name=stack_name)
        drifts_before = cls._compare_environments(scanner_context, iac_context_before)
        drifts_after = cls._compare_environments(scanner_context, iac_context_after)
        drifts = cls._find_mutual_drifts(drifts_before, drifts_after)
        environment_context_builder.destroy()
        return DriftDetectionResult(drifts, cls._calculate_iac_coverage(scanner_context, iac_context_after), workspace_id)

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
        tf_dict = tf_entity.to_drift_detection_object()
        cm_dict = cm_entity.to_drift_detection_object()
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
