from cloudrail.knowledge.context.aws.default_mergers.base_default_resource_merger import BaseDefaultResourceMerger
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl


class DefaultNaclMerger(BaseDefaultResourceMerger):

    def _merge_condition(self, existing_entity: NetworkAcl, new_entity: NetworkAcl, *args) -> bool:
        return existing_entity.network_acl_id in new_entity.aliases

    @property
    def resource_type(self) -> str:
        return 'NetworkACL'

    def _assign_data(self, existing_entity: NetworkAcl, new_entity: NetworkAcl) -> None:
        super()._assign_data(existing_entity, new_entity)
        for subnet_id in new_entity.subnet_ids:
            if subnet_id not in existing_entity.subnet_ids:
                existing_entity.subnet_ids.append(subnet_id)
