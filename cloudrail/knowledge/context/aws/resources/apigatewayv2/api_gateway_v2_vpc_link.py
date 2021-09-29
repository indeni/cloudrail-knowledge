from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGatewayVpcLink(AwsResource):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        vpc_link_id: The ID of the VPC link.
        name: The name of the VPC link.
        arn: The ARN of the VPC link.
        security_group_ids: List of security groups ID's used by the VPC link.
        subnet_ids: List of subnet ID's used by the VPC link.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 vpc_link_id: str,
                 name: str,
                 arn: Optional[str],
                 security_group_ids: list,
                 subnet_ids: list):
        super().__init__(account, region, AwsServiceName.AWS_APIGATEWAYV_2_VPC_LINK)
        self.vpc_link_id: str = vpc_link_id
        self.name: str = name
        self.security_group_ids: list = security_group_ids
        self.subnet_ids: list = subnet_ids
        self.arn: Optional[str] = arn if arn else self._create_arn()
        self.with_aliases(vpc_link_id)

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.vpc_link_id]

    def get_id(self) -> str:
        return self.vpc_link_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API Gateway VPC link'
        else:
            return 'API Gateway VPC links'

    def _create_arn(self) -> Optional[str]:
        if self.vpc_link_id:
            return f'arn:aws:apigateway:{self.region}::/vpclinks/{self.vpc_link_id}'
        else:
            return None

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/main/vpc-links/list?region={1}&vpcLink={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.vpc_link_id)

    @property
    def is_tagable(self) -> bool:
        return True
