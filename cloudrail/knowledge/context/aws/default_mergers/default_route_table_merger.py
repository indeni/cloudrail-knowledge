from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.default_mergers.base_default_resource_merger import BaseDefaultResourceMerger


class DefaultRouteTableMerger(BaseDefaultResourceMerger):

    def _merge_condition(self, existing_entity: RouteTable, new_entity: RouteTable, *args) -> bool:
        return existing_entity.route_table_id in new_entity.aliases or new_entity.vpc_id == existing_entity.vpc_id

    @property
    def resource_type(self) -> str:
        return 'Route-Table'
