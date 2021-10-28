from typing import Dict

from cloudrail.knowledge.context.aws.resources.configservice.config_aggregator import ConfigAggregator
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance_subnet_group import DmsReplicationInstanceSubnetGroup
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationDmsReplicationInstanceBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DMS_REPLICATION_SUBNET_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ConfigAggregator:
        properties: dict = cfn_res_attr['Properties']
        replication_subnet_group_id = self.get_property(properties, "ReplicationSubnetGroupIdentifier", self.get_resource_id(cfn_res_attr))
        account_id = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        return DmsReplicationInstanceSubnetGroup(account_id,
                                                 region,
                                                 replication_subnet_group_id,
                                                 self.get_property(properties, "SubnetIds"),
                                                 vpc_id=None).with_aliases(self.get_resource_id(cfn_res_attr),
                                                                           replication_subnet_group_id + account_id + region)
