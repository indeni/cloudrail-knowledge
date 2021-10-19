from typing import List, Optional, Union

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.utils.utils import str_to_bool


class NetworkConfiguration:
    def __init__(self, assign_public_ip: Union[bool, str], security_groups_ids: List[str], subnet_list_ids: List[str]) -> None:
        self.assign_public_ip: Optional[bool] = str_to_bool(assign_public_ip) if isinstance(assign_public_ip, str) else assign_public_ip
        self.security_groups_ids: List[str] = security_groups_ids or []
        self.subnet_list_ids: List[str] = subnet_list_ids
        self.subnets: List[Subnet] = []
        self.security_groups: List[SecurityGroup] = []

    def to_dict(self):
        return {'assign_public_ip': self.assign_public_ip,
                'security_groups_ids': self.security_groups_ids,
                'subnet_list_ids': self.subnet_list_ids}
