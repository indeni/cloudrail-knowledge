from abc import abstractmethod
from typing import Optional, Type

from cloudrail.knowledge.context.aws.aws_relations_assigner import AwsRelationsAssigner
from cloudrail.knowledge.context.aws.parallel.assign_inbound_permissions_connections_task import AssignInboundPermissionsConnectionsTask
from cloudrail.knowledge.context.aws.parallel.assign_roles_to_bucket_task import AssignRolesToBucketTask
from cloudrail.knowledge.context.aws.resources_assigner_util import ResourcesAssignerUtil
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.environment_context.environment_context_defaults_merger import EnvironmentContextDefaultsMerger
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment
from cloudrail.knowledge.context.environment_context.environment_context_merger import EnvironmentContextMerger
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder
from cloudrail.knowledge.utils.policy_evaluator import PolicyEvaluator


class BaseEnvironmentContextBuilder:

    @classmethod
    def build(cls,
              account_data_dir_path: str,
              iac_file_path: str,
              account_id: Optional[str] = None,
              salt: Optional[str] = None,
              **extra_args) -> BaseEnvironmentContext:
        if not account_data_dir_path and not iac_file_path:
            raise Exception('build should get at least one of account_data_dir_path and iac_file_path')
        account_id = account_id or cls.get_default_account_id()
        scanner_context = cls.get_scanner_builder_type().build(account_data_dir_path, account_id, salt, **extra_args)

        if extra_args and 'default_resources_only' in extra_args:
            cloned_extra_args = extra_args.copy()
            cloned_extra_args.pop('default_resources_only', None)
            full_scanner_context = cls.get_scanner_builder_type().build(account_data_dir_path, account_id, salt, **cloned_extra_args)
        else:
            full_scanner_context = scanner_context

        iac_context = cls.get_iac_builder_type().build(iac_file_path, account_id, full_scanner_context, salt, **extra_args)
        defaults_merger = cls.get_defaults_merger_type()
        if defaults_merger and account_data_dir_path:
            defaults_merger.merge_defaults(scanner_context, iac_context)
        merged_context = EnvironmentContextMerger.merge(scanner_context, iac_context)
        cls.get_context_enrichment_type().enrich(merged_context, **extra_args)
        return merged_context

    @classmethod
    @abstractmethod
    def get_default_account_id(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_scanner_builder_type(cls) -> Type[ScannerContextBuilder]:
        pass

    @classmethod
    @abstractmethod
    def get_iac_builder_type(cls) -> Type[IacContextBuilder]:
        pass

    @classmethod
    @abstractmethod
    def get_defaults_merger_type(cls) -> Optional[Type[EnvironmentContextDefaultsMerger]]:
        pass

    @classmethod
    @abstractmethod
    def get_context_enrichment_type(cls) -> Type[EnvironmentContextEnrichment]:
        pass

    @classmethod
    def destroy(cls):
        AssignInboundPermissionsConnectionsTask.clear_cache()
        PolicyEvaluator.equals_resources.cache_clear()
        ResourcesAssignerUtil.clear_cache()
        AwsRelationsAssigner.clear_cache()
        AssignRolesToBucketTask.clear_cache()
