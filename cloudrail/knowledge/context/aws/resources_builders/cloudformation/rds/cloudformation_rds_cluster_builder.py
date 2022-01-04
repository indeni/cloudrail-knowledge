from typing import Dict

from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn
from cloudrail.knowledge.utils.port_utils import get_rds_cluster_port_cfn


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
        port = get_rds_cluster_port_cfn(engine_mode, engine)
        return RdsCluster(account=account,
                          region=region,
                          cluster_id=cluster_id,
                          arn=arn,
                          port=self.get_property(properties, 'Port', port),
                          db_subnet_group_name=self.get_property(properties, 'DBSubnetGroupName', 'default'),
                          security_group_ids=self.get_property(properties, 'VpcSecurityGroupIds', []),
                          encrypted_at_rest=self.get_property(properties, 'StorageEncrypted', False),
                          backup_retention_period=self.get_property(properties, 'BackupRetentionPeriod', 1),
                          engine_type=engine,
                          engine_version=self.get_property(properties, 'EngineVersion'),
                          iam_database_authentication_enabled=self.get_property(properties, 'EnableIAMDatabaseAuthentication', False),
                          cloudwatch_logs_exports=self.get_property(properties, 'EnableCloudwatchLogsExports'))
