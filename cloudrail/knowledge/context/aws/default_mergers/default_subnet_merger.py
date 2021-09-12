from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.default_mergers.base_default_resource_merger import BaseDefaultResourceMerger


class DefaultSubnetMerger(BaseDefaultResourceMerger):

    def _merge_condition(self, existing_entity: Subnet, new_entity: Subnet, *args) -> bool:
        return existing_entity.availability_zone == new_entity.availability_zone and existing_entity.account == new_entity.account

    @property
    def resource_type(self) -> str:
        return 'Subnet'

    def _assign_data(self, existing_entity: Subnet, new_entity: Subnet) -> None:
        super()._assign_data(existing_entity, new_entity)
        if new_entity.map_public_ip_on_launch is not None:
            existing_entity.map_public_ip_on_launch = new_entity.map_public_ip_on_launch
