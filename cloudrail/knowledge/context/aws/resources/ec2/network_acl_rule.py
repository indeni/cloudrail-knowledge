from enum import Enum
from typing import List

from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.utils import normalize_port_range
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RuleAction(Enum):
    ALLOW = 'allow'
    DENY = 'deny'

    def __str__(self):
        return str(self.name)


class RuleType(Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'

    def __str__(self):
        return str(self.name)


class NetworkAclRule(AwsResource):
    """
        Attributes:
            network_acl_id: The ID of the NACL this rule belongs to.
            cidr_block: The CIDR block the rule applies to.
            from_port: The bottom of the port range applicable to the rule.
            to_port: The top of the port range applicable to the rule.
            rule_action: The action the rule takes (allow / deny).
            rule_number: The number of the rule in the NACL table.
            rule_type: The type of the rule - inbound or outbound.
            ip_protocol_type: The IP protocol the rule applies to.
    """

    def __init__(self,
                 region: str,
                 account: str,
                 network_acl_id: str,
                 cidr_block: str,
                 from_port: int,
                 to_port: int,
                 rule_action: RuleAction,
                 rule_number: int,
                 rule_type: RuleType,
                 ip_protocol_type: IpProtocol = IpProtocol('ALL')
                 ):
        super().__init__(account, region, AwsServiceName.AWS_NETWORK_ACL_RULE)
        self.network_acl_id = network_acl_id
        self.cidr_block = cidr_block
        normalized_from_port, normalized_to_port = normalize_port_range(from_port, to_port)
        self.from_port = normalized_from_port
        self.to_port = normalized_to_port
        self.rule_action = rule_action
        self.rule_number = rule_number
        self.rule_type = rule_type
        self.ip_protocol_type: IpProtocol = ip_protocol_type

    def __str__(self) -> str:
        return "NACL rule: cidr_block={}, from_port={}, to_port={}, rule_action={}, rule_number={}, rule_type={}" \
            .format(self.cidr_block, self.from_port, self.to_port, self.rule_action, self.rule_number, self.rule_type)

    def get_keys(self) -> List[str]:
        return [self.network_acl_id, self.rule_number, self.rule_type.value]

    def get_extra_data(self) -> str:
        return str(self)

    def get_arn(self) -> str:
        pass

    def get_type(self, is_plural: bool = False) -> str:
        if is_plural:
            return 'Network ACL rule'
        else:
            return "Network ACL rules"

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#NetworkAclDetails:networkAclId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.network_acl_id)

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'cidr_block': self.cidr_block,
                'from_port': self.from_port,
                'to_port': self.to_port,
                'rule_action': self.rule_action,
                'rule_number': self.rule_number,
                'rule_type': self.rule_type,
                'ip_protocol_type': self.ip_protocol_type.__repr__()}
