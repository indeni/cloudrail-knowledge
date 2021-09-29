from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixLists, PrefixList
from cloudrail.knowledge.context.aws.resources.ec2.route import Route
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceType
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_gateway_rule import AbstractVpcEndpointGatewayRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType



class AbstractVpcEndpointGatewayIsNotUsedRule(AbstractVpcEndpointGatewayRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        vpc_list, region_to_service_map, vpc_to_eni_map = self._init_maps(env_context)
        issues_list: List[Issue] = []
        region_to_prefix_lists_map: Dict[str, PrefixLists] = self._create_prefix_list_by_region_map(env_context)
        for vpc in vpc_list:
            for eni in vpc_to_eni_map.get(vpc, []):
                if self._is_service_eni_match(eni):
                    prefix_list: PrefixLists = region_to_prefix_lists_map[vpc.region]
                    aws_service_pl: PrefixList = prefix_list.get_prefix_lists_by_service(self.aws_service_type.value)
                    if self._add_new_issue_from_outbound(eni, region_to_service_map, issues_list, aws_service_pl):
                        break

        return issues_list

    def _add_new_issue_from_outbound(self, eni: NetworkInterface, region_to_service_map: Dict[str, List[Mergeable]],
                                     issues_list: List[Issue], service_pl: PrefixList) -> bool:
        if self._is_public_connection_exist(eni):
            most_specific_service_pl_route: Route = self._get_most_specific_service_pl_route(eni.subnet.route_table, service_pl)
            if not self._is_valid_vpc_endpoint_route(most_specific_service_pl_route, service_pl, eni.vpc.endpoints):
                for service in region_to_service_map[eni.vpc.region]:
                    issues_list.append(Issue(f"~The {eni.vpc.get_type()}~. `{eni.vpc.get_friendly_name()}` in region `{eni.vpc.region}`"
                                             f" is in use but not leveraging {self.aws_service_type.name} Endpoint Gateway", service, eni.vpc))
                return True
        return False


class S3VpcEndpointGatewayNotUsedRule(AbstractVpcEndpointGatewayIsNotUsedRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.S3, (443, 80), self.S3_SERVICES_EXCLUDE_LIST, False)

    def get_id(self) -> str:
        return "vpc_endpoint_s3_exposure"


class DynamoDbVpcEndpointGatewayNotUsedRule(AbstractVpcEndpointGatewayIsNotUsedRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.DYNAMODB, (443,), self.DYNAMODB_SERVICES_INCLUDE_LIST, True)

    def get_id(self) -> str:
        return "vpc_endpoint_dynamodb_exposure"
