from typing import List, Dict

from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EfsVolume
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ecs_task_definition_encrypt_in_transit_with_EFS'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for task_def in env_context.ecs_task_definitions:
            if task_def.is_new_resource() and task_def.is_volume_efs:
                effected_volumes = self._non_encrypted_volumes(task_def.efs_volume_data)
                if effected_volumes:
                    issues.append(
                        Issue(
                            f'The {task_def.get_type()} `{task_def.family}` is not set to use encryption in transit with '
                            f"EFS volumes: `{', '.join([volume.volume_name for volume in effected_volumes])}`", task_def, task_def))
        return issues

    @staticmethod
    def _non_encrypted_volumes(volumes_data: List[EfsVolume]) -> List[EfsVolume]:
        volumes_list = []
        for volume in volumes_data:
            if not volume.encrypt_efs_in_transit:
                volumes_list.append(volume)
        return volumes_list

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ecs_task_definitions)
