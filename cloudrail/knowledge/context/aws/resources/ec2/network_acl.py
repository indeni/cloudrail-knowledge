from typing import List

from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class NetworkAcl(AwsResource):
    """
        Attributes:
            network_acl_id: The ID of the NACL.
            vpc_id: The ID of the VPC the NACL belongs to.
            is_default: True if this is the default NACL for the subnets.
            name: The name of the NACL.
            subnet_ids: List of IDs of subnets the NACL bleongs to.
            inbound_rules: The inbound/ingress rules defined in the NACL.
            outbound_rules: The outbound/egress rules defined in the NACL.
    """
    def __init__(self,
                 network_acl_id: str,
                 vpc_id: str,
                 is_default: bool,
                 name: str,
                 subnet_ids: List[str],
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_NETWORK_ACL)
        self.network_acl_id: str = network_acl_id
        self.vpc_id: str = vpc_id
        self.is_default: bool = is_default
        self.name: str = name
        self.subnet_ids: List[str] = subnet_ids
        self.inbound_rules: List[NetworkAclRule] = []
        self.outbound_rules: List[NetworkAclRule] = []
        self.with_aliases(network_acl_id)

    def get_keys(self) -> List[str]:
        return [self.network_acl_id]

    def get_id(self) -> str:
        return self.network_acl_id

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        pass

    def __str__(self) -> str:
        return "network_acl_id={}, vpc_id={}, name={}".format(self.network_acl_id, self.vpc_id, self.name)

    def get_extra_data(self) -> str:
        vpc_id = 'vpc_id: {}'.format(self.vpc_id) if self.vpc_id else ''
        is_default = 'is_default: {}'.format(self.is_default) if self.is_default else ''
        subnets = 'subnets: {}'.format(self.subnet_ids) if self.subnet_ids else ''

        return ', '.join([vpc_id, is_default, subnets])

    def get_type(self, is_plural: bool = False) -> str:
        if is_plural:
            return 'Network ACL'
        else:
            return "Network ACL's"

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#NetworkAclDetails:networkAclId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.network_acl_id)

    @property
    def is_tagable(self) -> bool:
        return True
