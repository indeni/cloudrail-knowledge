from typing import Dict
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationEksClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.EKS_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> EksCluster:
        properties: dict = cfn_res_attr['Properties']
        vpc_config = properties['ResourcesVpcConfig']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        cluster_name = self.get_property(properties, 'Name', self.get_resource_id(cfn_res_attr))
        eks_arn = build_arn('eks', region, account, 'cluster', None, cluster_name)
        return EksCluster(name=cluster_name,
                          arn=eks_arn,
                          role_arn=self.get_property(properties, 'RoleArn'),
                          endpoint=None,
                          security_group_ids=self.get_property(vpc_config, 'SecurityGroupIds', []),
                          cluster_security_group_id=None,
                          subnet_ids=self.get_property(vpc_config, 'SubnetIds'),
                          endpoint_public_access=self.get_property(vpc_config, 'EndpointPublicAccess', True),
                          endpoint_private_access=self.get_property(vpc_config, 'EndpointPrivateAccess', False),
                          public_access_cidrs=self.get_property(vpc_config, 'PublicAccessCidrs', ['0.0.0.0/0']),
                          account=account,
                          region=region)
