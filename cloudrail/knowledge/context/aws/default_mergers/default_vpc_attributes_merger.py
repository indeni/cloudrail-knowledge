from cloudrail.knowledge.context.aws.resources.ec2.vpc import VpcAttribute

from cloudrail.knowledge.context.aws.default_mergers.base_default_resource_merger import BaseDefaultResourceMerger


class DefaultVpcAttributesMerger(BaseDefaultResourceMerger):

    def _merge_condition(self, existing_entity: VpcAttribute, new_entity: VpcAttribute, *args) -> bool:
        return existing_entity.region == new_entity.region and existing_entity.account == new_entity.account and existing_entity.attribute_name == new_entity.attribute_name

    @property
    def resource_type(self) -> str:
        return 'Vpc Attribute'

    def _assign_data(self, existing_entity: VpcAttribute, new_entity: VpcAttribute) -> None:
        if new_entity.enable is not None:
            existing_entity.enable = new_entity.enable
