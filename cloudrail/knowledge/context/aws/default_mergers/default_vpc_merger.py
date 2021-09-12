from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.default_mergers.base_default_resource_merger import BaseDefaultResourceMerger


class DefaultVpcMerger(BaseDefaultResourceMerger):

    def _merge_condition(self, existing_entity: Vpc, new_entity: Vpc, *args) -> bool:
        return existing_entity.region == new_entity.region and existing_entity.account == new_entity.account

    @property
    def resource_type(self) -> str:
        return 'Vpc'
