from dataclasses import dataclass


@dataclass
class LoadBalancingConfiguration:
    """
        Details about the load balancing connection to an ECS Service.
    """
    def __init__(self, elb_name: str, target_group_arn: str, container_name: str, container_port: int) -> None:
        self.elb_name: str = elb_name
        self.target_group_arn = target_group_arn
        self.container_name: str = container_name
        self.container_port: int = container_port

    def __str__(self) -> str:
        return "elb_name={}, target_group_arn={}, container_name={}, container_port={}, "\
            .format(self.elb_name, self.target_group_arn, self.container_name, self.container_port)
