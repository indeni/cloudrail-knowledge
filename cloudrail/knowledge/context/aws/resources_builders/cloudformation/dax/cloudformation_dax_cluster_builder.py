from typing import Dict

from cloudrail.knowledge.context.aws.resources.dax.dax_cluster import DaxCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationDaxClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DAX_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DaxCluster:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        cluster_name = self.get_property(properties, "ClusterName", self.create_random_pseudo_identifier())
        cluster_arn = build_arn(service='dax', region=region, account_id=account, path='cache/', resource_name=cluster_name, resource_type="")
        server_side_encryption = properties.get("SSESpecification", {}).get("SSEEnabled", False)
        return DaxCluster(cluster_name=cluster_name,
                          server_side_encryption=server_side_encryption,
                          cluster_arn=cluster_arn,
                          region=region,
                          account=account)
