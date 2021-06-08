from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.aws.prefix_lists import PrefixLists, PrefixList
from cloudrail.knowledge.context.aws.ec2.route import Route
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.service_name import AwsServiceType
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_gateway_rule import AbstractVpcEndpointGatewayRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType



class AbstractVpcEndpointRouteTableExposureRule(AbstractVpcEndpointGatewayRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        vpc_list, _, vpc_to_eni_map = self._init_maps(env_context)
        region_to_prefix_lists_map: Dict[str, PrefixLists] = self._create_prefix_list_by_region_map(env_context)
        issues_list: List[Issue] = []

        for vpc in vpc_list:
            for eni in vpc_to_eni_map.get(vpc, []):
                if self._is_service_eni_match(eni):
                    for subnet in vpc.subnets:
                        prefix_list: PrefixLists = region_to_prefix_lists_map[vpc.region]
                        aws_service_pl: PrefixList = prefix_list.get_prefix_lists_by_service(self.aws_service_type.value)
                        most_specific_service_pl_route: Route = self._get_most_specific_service_pl_route(subnet.route_table, aws_service_pl)
                        if vpc.endpoints and \
                                not (most_specific_service_pl_route and
                                     self._is_valid_vpc_endpoint_route(most_specific_service_pl_route, aws_service_pl, subnet.vpc.endpoints)):
                            issues_list.append(Issue(f"~The {vpc.get_type()}~. `{vpc.get_friendly_name()}` "
                                                     f"has a {aws_service_pl.service_name.upper()} Endpoint gateway "
                                                     f"but `{subnet.get_friendly_name()}` uses `{subnet.route_table.get_friendly_name()}`"
                                                     f", which does not have a route to the Endpoint gateway.", subnet.vpc, subnet.route_table))
                break

        return issues_list

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.vpc_endpoints)


class S3VpcEndpointRouteTableExposureRule(AbstractVpcEndpointRouteTableExposureRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.S3, (443, 80), self.S3_SERVICES_EXCLUDE_LIST, False)

    def get_id(self) -> str:
        return "endpoint_s3_route_table_exposure"


class DynamoDbVpcEndpointRouteTableExposureRule(AbstractVpcEndpointRouteTableExposureRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.DYNAMODB, (443,), self.DYNAMODB_SERVICES_INCLUDE_LIST, True)

    def get_id(self) -> str:
        return "endpoint_dynamodb_route_table_exposure"
