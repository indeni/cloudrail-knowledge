from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudWatchEventTarget(AwsResource):
    """
        Attributes:
            name: The name of the CloudWatch Event Target.
            rule_name: The name of the rule used with the target.
            target_id: The ID of this traget.
            role_arn: The ARN of the role used to send the events, may be None.
            cluster_arn: If an ECS cluster is targeted, this is the ARN of the ECS cluster.
            ecs_target_list: If an ECS cluster is targeted, lists the ECS targets.
    """

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'rule_name': self.rule_name,
                'role_arn': self.role_arn,
                'cluster_arn': self.cluster_arn}

    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 rule_name: str,
                 target_id: str,
                 role_arn: str,
                 cluster_arn: str,
                 ecs_target_list: List[EcsTarget]) -> None:
        super().__init__(account, region, AwsServiceName.AWS_CLOUD_WATCH_EVENT_TARGET)
        self.name: str = name
        self.rule_name: str = rule_name
        self.target_id: str = target_id
        self.role_arn: str = role_arn
        self.cluster_arn: str = cluster_arn
        self._ecs_target_list: List[EcsTarget] = ecs_target_list

    @property
    def ecs_target_list(self):
        return [target for target in self._ecs_target_list if not target.is_invalidated]

    def get_keys(self) -> List[str]:
        return [self.rule_name, self.cluster_arn]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudWatch Event Target'
        else:
            return "CloudWatch Event Targets"

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}cloudwatch/home?{1}#rules:name={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.rule_name)

    @property
    def is_tagable(self) -> bool:
        return False

    def exclude_from_invalidation(self):
        # EcsTarget can be configurerd to use entities that no longer exist, which will make them invalid, but we dont want to
        # invalidate the cluster because of it
        return [self._ecs_target_list]
