import dataclasses
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeHealthCheckType(Enum):
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    TCP = 'TCP'
    SSL = 'SSL'
    GRPC = 'gRPC'
    HTTP2 = 'HTTP2'


class GcpComputeHealthCheckPortSpecification(Enum):
    USE_FIXED_PORT = 'USE_FIXED_PORT'
    USE_NAMED_PORT = 'USE_NAMED_PORT'
    USE_SERVING_PORT = 'USE_SERVING_PORT'


@dataclass
class GcpComputeHealthCheckAttributes:
    """
        Attributes:
            host: (Optional) The value of the host header in the health-check request (relevant only for HTTP and HTTPS types).
            request_path: (Optional) The request path of the health-check request (relevant only for HTTP and HTTPS types).
            request: (Optional) The application data to send once connection established (relevant only for SSL and TCP types).
            response: (Optional) The bytes to match against the beginning of the response data (not relevant for gRPC).
            port: (Optional) The port number for the health-check request.
            port_name: (Optional) The porn name of the health-check request.
            proxy_header: (Optional) Specifies the type of proxy header to append before sending data to the backend (not relevant for gRPC).
            port_specification: (Optional) Specify which port will be used for the health-check request.
            grpc_service_name: (Optional) The gRPC service name for the health check (only relevant for gRPC)
    """
    host: Optional[str]
    request_path: Optional[str]
    response: Optional[str]
    port: Optional[int]
    port_name: Optional[str]
    proxy_header: Optional[str]
    port_specification: Optional[GcpComputeHealthCheckPortSpecification]
    grpc_service_name: Optional[str]


class GcpComputeHealthCheck(GcpResource):
    """
        Attributes:
            name: A unique name for the health-check resource.
            health_check_type: The health-check type (one of: HTTP, HTTPS, TCP, SSL, gRPC, HTTP2).
            check_interval_sec: (Optional) The frequent, in seconds, to send a health check.
            description: (Optional) Description for the health-check resource.
            healthy_threshold: (Optional) The number of success health-checks to consider instances as healthy after it was set to unhealthy.
            timeout_sec: (Optional) The number of seconds to determine failure due to timeout.
            unhealthy_threshold: (Optional) The number of failures health-checks to consider instances as unhealthy.
            http_health_check: (Optional) Enable HTTP type health check.
            https_health_check: (Optional) Enable HTTPS type health check.
            tcp_health_check: (Optional) Enable TCP type health check.
            ssl_health_check: (Optional) Enable SSL type health check.
            http2_health_check: (Optional) Enable HTTP2 type health check.
            grpc_health_check: (Optional) Enable gRPC type health check.
            logging_enabled: (Optional) An indication if the logs should be exported or not.
            project: (Optional) The project ID in which this health-check resource belongs.
    """

    def __init__(self,
                 name: str,
                 health_check_type: GcpComputeHealthCheckType,
                 http_health_check: Optional[GcpComputeHealthCheckAttributes],
                 https_health_check: Optional[GcpComputeHealthCheckAttributes],
                 tcp_health_check: Optional[GcpComputeHealthCheckAttributes],
                 ssl_health_check: Optional[GcpComputeHealthCheckAttributes],
                 http2_health_check: Optional[GcpComputeHealthCheckAttributes],
                 grpc_health_check: Optional[GcpComputeHealthCheckAttributes],
                 logging_enabled: bool,
                 project: Optional[str],
                 check_interval_sec: int = 5,
                 healthy_threshold: int = 2,
                 timeout_sec: int = 5,
                 unhealthy_threshold: int = 2):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_HEALTH_CHECK)
        self.name: str = name
        self.health_check_type: GcpComputeHealthCheckType = health_check_type
        self.check_interval_sec: int = check_interval_sec
        self.healthy_threshold: int = healthy_threshold
        self.timeout_sec: int = timeout_sec
        self.unhealthy_threshold: int = unhealthy_threshold
        self.http_health_check: Optional[GcpComputeHealthCheckAttributes] = http_health_check
        self.https_health_check: Optional[GcpComputeHealthCheckAttributes] = https_health_check
        self.tcp_health_check: Optional[GcpComputeHealthCheckAttributes] = tcp_health_check
        self.ssl_health_check: Optional[GcpComputeHealthCheckAttributes] = ssl_health_check
        self.http2_health_check: Optional[GcpComputeHealthCheckAttributes] = http2_health_check
        self.grpc_health_check: Optional[GcpComputeHealthCheckAttributes] = grpc_health_check
        self.logging_enabled: bool = logging_enabled
        self.project: Optional[str] = project

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_labeled(self) -> bool:
        return False

    @property
    def is_tagable(self) -> bool:
        return False

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Health Check'
        else:
            return 'Compute Health Checks'

    def to_drift_detection_object(self) -> dict:
        return {'health_check_type': self.health_check_type.value,
                'check_interval_sec': self.check_interval_sec,
                'healthy_threshold': self.healthy_threshold,
                'timeout_sec': self.timeout_sec,
                'unhealthy_threshold': self.unhealthy_threshold,
                'http_health_check': dataclasses.asdict(self.http_health_check),
                'https_health_check': dataclasses.asdict(self.https_health_check),
                'tcp_health_check': dataclasses.asdict(self.tcp_health_check),
                'ssl_health_check': dataclasses.asdict(self.ssl_health_check),
                'http2_health_check': dataclasses.asdict(self.http2_health_check),
                'grpc_health_check': dataclasses.asdict(self.grpc_health_check),
                'logging_enabled': self.logging_enabled}
