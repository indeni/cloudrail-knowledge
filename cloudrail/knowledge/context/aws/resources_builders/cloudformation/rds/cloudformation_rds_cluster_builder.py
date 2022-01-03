from typing import Dict

from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn
from cloudrail.knowledge.utils.port_utils import get_rds_port_cfn


class CloudformationRdsClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.RDS_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> RdsCluster:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        cluster_id = self.get_property(properties, 'DBClusterIdentifier', self.get_resource_id(cfn_res_attr))
        arn = build_arn('rds', region, account, 'cluster', None, cluster_id)
        engine_mode = self.get_property(properties, 'EngineMode', 'provisioned')
        engine = self.get_property(properties, 'Engine')
        port = get_rds_port_cfn(engine_mode, engine)
        default_engine_version = _get_default_engine_version(engine)
        return RdsCluster(account=account,
                          region=region,
                          cluster_id=cluster_id,
                          arn=arn,
                          port=port,
                          db_subnet_group_name=self.get_property(properties, 'DBSubnetGroupName', 'default'),
                          security_group_ids=self.get_property(properties, 'VpcSecurityGroupIds'),
                          encrypted_at_rest=self.get_property(properties, 'StorageEncrypted', False),
                          backup_retention_period=self.get_property(properties, 'BackupRetentionPeriod', 1),
                          engine_type=engine,
                          engine_version=self.get_property(properties, 'EngineVersion', default_engine_version))

def _get_default_engine_version(engine: str):
    if engine == 'mysql_aurora':
        return '5.7.mysql_aurora.2.07.2'
    if engine == 'aurora':
        return '5.6.mysql_aurora.1.22.5'
    if engine == 'aurora-postgresql':
        return '12.7'
    return None

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
