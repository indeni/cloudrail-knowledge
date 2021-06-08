import uuid
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import List

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class ParameterType(str, Enum):
    FIREWALL_EC2 = 'firewall_ec2'
    S3_BUCKET = 's3_bucket'


class ParameterFilterType(str, Enum):
    ID = 'id'
    NAME = 'name'
    IMAGE = 'image'
    IP = 'ip'
    SUBNET = 'subnet'


class BaseParameter:
    def __init__(self, parameter_type: ParameterType, filter_type: str, value: str, parameter_id: str = None,
                 created_at: datetime = datetime.utcnow()):
        self.parameter_type = parameter_type
        self.filter_type = filter_type
        self.value = value
        self.parameter_id = parameter_id or str(uuid.uuid4())
        self.created_at = created_at

    @abstractmethod
    def execute(self, env_context: AwsEnvironmentContext) -> List[any]:
        pass

    @abstractmethod
    def get_parameter_friendly_name(self) -> str:
        pass
