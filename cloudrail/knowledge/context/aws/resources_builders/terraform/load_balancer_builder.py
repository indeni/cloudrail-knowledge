from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper \
    import build_load_balancer, build_load_balancer_target_group, \
    build_load_balancer_target_group_association, build_load_balancer_target
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class LoadBalancerBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_load_balancer(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER


class LoadBalancerTargetGroupBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_load_balancer_target_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP


class LoadBalancerTargetGroupAssociationBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_load_balancer_target_group_association(attributes) \
            if any(action['target_group_arn'] for action in attributes['default_action']) else None

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER_LISTENER


class LoadBalancerTargetBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_load_balancer_target(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP_ATTACHMENT
