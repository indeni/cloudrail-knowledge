from abc import abstractmethod
from typing import List, Dict, Optional
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixLists, PrefixList
from cloudrail.knowledge.context.aws.resources.ec2.route import Route, RouteTargetType
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpoint
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.utils.utils import is_subset
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_rule import AbstractVpcEndpointRule


class AbstractVpcEndpointGatewayRule(AbstractVpcEndpointRule):

    S3_SERVICES_EXCLUDE_LIST: List[str] = ["aws_apigatewayv2_vpc_link", "aws_batch_compute_environment", "aws_cloudwatch_event_target",
                                           "aws_dax_cluster", "aws_db_proxy", "aws_dms_replication_instance", "aws_docdb_cluster",
                                           "aws_ecs_task_definition", "aws_efs_mount_target", "aws_eks_cluster", "aws_elasticsearch_domain",
                                           "aws_fsx_windows_file_system", "aws_mq_broker", "aws_neptune_cluster", "aws_sagemaker_notebook_instance",
                                           "aws_workspaces_directory"]

    DYNAMODB_SERVICES_INCLUDE_LIST: List[str] = ["aws_appsync_datasource", "aws_autoscalingplans_scaling_plan", "aws_dms_replication_instance",
                                                 "aws_glue_crawler", "aws_iot_topic_rule", "aws_lambda_function", "aws_api_gateway_rest_api",
                                                 "aws_instance", "aws_ecs_service", "aws_eks_cluster", "aws_elastic_beanstalk_environment",
                                                 "aws_emr_cluster", "aws_redshift_cluster"]

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @staticmethod
    def _is_valid_vpc_endpoint_route(route: Route, service_pl: PrefixList, vpc_endpoints_list: List[VpcEndpoint]) -> bool:
        return any(route.target_type == RouteTargetType.GATEWAY_ID and
                   route.target == vpce.vpce_id and
                   any(route.destination == service_pl.pl_id or
                       is_subset(route.destination, cidr)
                       for cidr in service_pl.cidr_list) for vpce in vpc_endpoints_list)

    @staticmethod
    def _get_most_specific_service_pl_route(rtb: RouteTable, prefix_list: PrefixList) -> Optional[Route]:
        most_specific_route: Optional[Route] = rtb.get_prefix_list_route_by_id(prefix_list.pl_id)
        if not most_specific_route:
            for cidr in prefix_list.cidr_list:
                route: Route = rtb.get_most_specific_route(cidr)
                if route and (most_specific_route is None or
                              is_subset(route.destination, most_specific_route.destination)):
                    most_specific_route = route
                    if is_subset(most_specific_route.destination, cidr):
                        break
        return most_specific_route

    @staticmethod
    def _create_prefix_list_by_region_map(env_context: AwsEnvironmentContext) -> Dict[str, PrefixLists]:
        return {pl.region: pl for pl in env_context.prefix_lists}
