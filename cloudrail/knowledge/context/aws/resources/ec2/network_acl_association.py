from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class NetworkAclAssociation(AwsResource):
    """
        Attributes:
            network_acl_id: The ID of the NACL.
            subnet_id: The ID of the Subnet the NACL associate with.
            network_acl_association_id: The ID of the nacl and subnet association resource.
    """

    def __init__(self,
                 network_acl_id: str,
                 subnet_id: str,
                 network_acl_association_id: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_NETWORK_ACL)
        self.network_acl_id: str = network_acl_id
        self.subnet_id: str = subnet_id
        self.network_acl_association_id: str = network_acl_association_id
        self.with_aliases(network_acl_id)

    def get_keys(self) -> List[str]:
        return [self.subnet_id, self.network_acl_id]

    def get_id(self) -> str:
        return self.network_acl_association_id

    def get_arn(self) -> str:
        pass

    def get_extra_data(self) -> str:
        vpc_id = 'vpc_id: {}'.format(self.subnet_id) if self.subnet_id else ''
        network_acl_id = 'network_acl_id: {}'.format(self.network_acl_id) if self.network_acl_id else ''
        network_acl_association_id = 'network_acl_association_id: {}'.format(self.network_acl_association_id) \
            if self.network_acl_association_id else ''
        return ', '.join([vpc_id, network_acl_id, network_acl_association_id])

    def get_type(self, is_plural: bool = False) -> str:
        if is_plural:
            return 'Network ACL Association'
        else:
            return "Network ACL's Association"

    @property
    def is_tagable(self) -> bool:
        return False

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'network_acl_id': self.network_acl_id,
                'subnet_id': self.subnet_id}
