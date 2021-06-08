from datetime import datetime
from typing import List

from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import BaseParameter, ParameterFilterType, ParameterType
from cloudrail.knowledge.rules.rule_parameters.ec2_instance_filter import ec2_instance_filter_type_to_class


class FirewallEc2Parameter(BaseParameter):
    def __init__(self, filter_type: ParameterFilterType, value: str, parameter_id: str = None, created_at: datetime = datetime.utcnow()):
        BaseParameter.__init__(self, ParameterType.FIREWALL_EC2, filter_type, value, parameter_id, created_at)

    def execute(self, env_context: AwsEnvironmentContext) -> List[Ec2Instance]:
        filter_class = ec2_instance_filter_type_to_class(self.filter_type)
        filter_obj = filter_class(*(self.value.split('=')))
        return list(x for x in env_context.ec2s if filter_obj.passed(x))

    def get_parameter_friendly_name(self) -> str:
        return 'EC2s that act as the system firewall'
