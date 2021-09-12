from dataclasses import dataclass

from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup


@dataclass
class IndirectPublicConnectionData:
    security_group: SecurityGroup
    target_eni: NetworkInterface
