from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.default_mergers.base_default_resource_merger import BaseDefaultResourceMerger


class DefaultSecurityGroupMerger(BaseDefaultResourceMerger):

    def _merge_condition(self, existing_entity: SecurityGroup, new_entity: SecurityGroup, *args: AliasesDict[Vpc]) -> bool:
        vpcs = args[0]
        existing_entity_vpc = vpcs.get(existing_entity.vpc_id)
        return existing_entity_vpc and new_entity.vpc_id in existing_entity_vpc.aliases

    @property
    def resource_type(self) -> str:
        return 'Security-Group'
