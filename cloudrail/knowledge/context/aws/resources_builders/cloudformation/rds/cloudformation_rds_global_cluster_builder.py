from typing import Dict

from cloudrail.knowledge.context.aws.resources.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationRdsGlobalClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.RDS_GLOBAL_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> RdsGlobalCluster:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        rds_global_cluster = RdsGlobalCluster(account=account,
                                              region=region,
                                              cluster_id=self.get_property(properties, 'GlobalClusterIdentifier', self.get_resource_id(cfn_res_attr)),
                                              encrypted_at_rest=self.get_property(properties, 'StorageEncrypted', False))
        rds_global_cluster.with_raw_data(self.get_property(properties, 'SourceDBClusterIdentifier'))
        return rds_global_cluster
