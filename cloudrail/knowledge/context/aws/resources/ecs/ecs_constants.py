from enum import Enum


class ClusterStatus(Enum):
    ACTIVE: str = "ACTIVE"
    PROVISIONING: str = "PROVISIONING"
    DEPROVISIONING: str = "DEPROVISIONING"
    FAILED: str = "FAILED"
    INACTIVE: str = "INACTIVE"


class LaunchType(str, Enum):
    FARGATE: str = "FARGATE"
    EC2: str = "EC2"


class NetworkMode(Enum):
    NONE = "none"
    AWS_VPC = "awsvpc"
    BRIDGE = "bridge"
    HOST = "host"
