from typing import List, Optional

from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class LoadBalancerListener(AwsResource):
    """
        Attributes:
            listener_arn: The ARN of this listener.
            listener_port: The port this listener listens on.
            listener_protocol: The protocol the listener listens on.
            load_balancer_arn: The ARN of the load balancer the listener
                is attached to.
            default_action_type: The default action type of this listener.
            redirect_action_protocol: The redirect protocol, if the redirect
                action is configured (None otherwise).
            redirect_action_port: The redirect port, if the redirect
                action is configured (None otherwise).

    """
    def __init__(self,
                 listener_arn: str,
                 listener_port: int,
                 listener_protocol: str,
                 load_balancer_arn: str,
                 account: str,
                 region: str,
                 default_action_type: str,
                 redirect_action_protocol: Optional[str],
                 redirect_action_port: Optional[str]):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER_LISTENER)
        self.listener_arn: str = listener_arn
        self.listener_port: int = listener_port
        self.listener_protocol: str = listener_protocol
        self.load_balancer_arn: str = load_balancer_arn
        self.default_action_type: str = default_action_type
        self.redirect_action_protocol: Optional[str] = redirect_action_protocol
        self.redirect_action_port: Optional[str] = redirect_action_port
        if default_action_type.lower() == 'redirect' and redirect_action_port in ('#{port}', None):
            self.redirect_action_port = listener_port

    def get_keys(self) -> List[str]:
        return [self.listener_arn]

    def get_arn(self) -> str:
        return self.listener_arn

    def get_extra_data(self) -> str:
        port = 'port: {}'.format(self.listener_port)
        protocol = 'protocol: {}'.format(self.listener_protocol)
        load_balancer_arn = 'load balancer arn: {}'.format(self.load_balancer_arn)
        return ', '.join([port, protocol, load_balancer_arn])

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ec2/v2/home?region={1}#LoadBalancers:type=application'\
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return False
