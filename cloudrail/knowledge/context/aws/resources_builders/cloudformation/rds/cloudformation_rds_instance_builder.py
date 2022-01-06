from typing import Dict

from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn
from cloudrail.knowledge.utils.port_utils import get_port_by_engine


class CloudformationRdsInstanceBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.RDS_INSTANCE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> RdsInstance:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        instance_name = self.get_property(properties, 'DBInstanceIdentifier', self.get_resource_id(cfn_res_attr))
        arn = build_arn('rds', region, account, 'db', None, instance_name)
        engine: str = self.get_property(properties, 'Engine')
        db_cluster_id = self.get_property(properties, 'DBClusterIdentifier')
        default_backup_retention_period = None if engine.lower().startswith('aurora') else 1
        performance_insights_kms_key = self.get_encryption_key_arn(self.get_property(properties, 'PerformanceInsightsKMSKeyId'),
                                                                   account, region, RdsInstance)
        rds_instance = RdsInstance(account=account,
                                   region=region,
                                   name=instance_name,
                                   arn=arn,
                                   port=self.get_property(properties, 'Port') or get_port_by_engine(engine.lower()),
                                   publicly_accessible=self.get_property(properties, 'PubliclyAccessible'),
                                   db_subnet_group_name=self.get_property(properties, 'DBSubnetGroupName', 'default'),
                                   security_group_ids=self.get_property(properties, 'VPCSecurityGroups') or self.get_property(properties, 'DBSecurityGroups', []),
                                   db_cluster_id=db_cluster_id,
                                   encrypted_at_rest=self.get_property(properties, 'StorageEncrypted', False),
                                   performance_insights_enabled=self.get_property(properties, 'EnablePerformanceInsights', False),
                                   performance_insights_kms_key=performance_insights_kms_key,
                                   engine_type=engine,
                                   engine_version=self.get_property(properties, 'EngineVersion'),
                                   instance_id=None if db_cluster_id else instance_name)
        rds_instance.backup_retention_period = self.get_property(properties, 'BackupRetentionPeriod', default_backup_retention_period)
        rds_instance.iam_database_authentication_enabled = self.get_property(properties, 'EnableIAMDatabaseAuthentication', False)
        rds_instance.cloudwatch_logs_exports = self.get_property(properties, 'EnableCloudwatchLogsExports')
        return rds_instance
