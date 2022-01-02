from typing import Dict

from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationRdsClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.RDS_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> RdsCluster:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        cluster_id = self.get_property(properties, 'DBClusterIdentifier', self.get_resource_id(cfn_res_attr))
        arn = build_arn('rds', region, account, 'cluster', None, cluster_id)
        return RdsCluster(account=account,
                          region=region,
                          cluster_id=cluster_id,
                          arn=arn,
                          )
        
                    #   raw_data['DBClusterIdentifier'],
                    #   raw_data['DBClusterArn'],
                    #   raw_data['Port'],
                    #   raw_data['DBSubnetGroup'],
                    #   [x['VpcSecurityGroupId'] for x in raw_data['VpcSecurityGroups'] if x['Status'] == 'active'],
                    #   get_dict_value(raw_data, 'StorageEncrypted', False),
                    #   raw_data['BackupRetentionPeriod'],
                    #   raw_data['Engine'],
                    #   raw_data['EngineVersion'],
                    #   raw_data['IAMDatabaseAuthenticationEnabled'],
                    #   raw_data.get('EnabledCloudwatchLogsExports')
