from typing import Dict

from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationDocumentDbClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DOCDB_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DocumentDbCluster:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        cluster_identifier = self.get_property(properties, 'DBClusterIdentifier', self.get_resource_id(cfn_res_attr))
        storage_encrypted = self.get_property(properties, 'StorageEncrypted', False)
        parameter_group_name = self.get_property(properties, 'DBClusterParameterGroupName')
        kms_key_id = None
        if storage_encrypted:
            kms_key_id = self.get_encryption_key_arn(self.get_property(properties, 'KmsKeyId'), account, region, DocumentDbCluster)
        enabled_cloudwatch_logs_exports = self.get_property(properties, 'EnableCloudwatchLogsExports')
        cluster_arn = build_arn('rds', region, account, 'cluster', None, cluster_identifier)
        return DocumentDbCluster(account=account, region=region, cluster_identifier=cluster_identifier, storage_encrypted=storage_encrypted,
                                 parameter_group_name=parameter_group_name, kms_key_id=kms_key_id, cluster_arn=cluster_arn,
                                 enabled_cloudwatch_logs_exports=enabled_cloudwatch_logs_exports)
