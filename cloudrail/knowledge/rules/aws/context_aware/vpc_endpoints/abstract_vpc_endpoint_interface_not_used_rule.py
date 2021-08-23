from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.aws.ec2.vpc_endpoint import VpcEndpointInterface
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.service_name import AwsServiceType
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_rule import AbstractVpcEndpointRule


class AbstractVpcEndpointInterfaceNotUsedRule(AbstractVpcEndpointRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        vpc_list, region_to_service_map, vpc_to_eni_map = self._init_maps(env_context)
        issues_list: List[Issue] = []
        for region in region_to_service_map:
            violated_vpc = None
            for vpc in vpc_list:
                if vpc.region != region:
                    continue
                if violated_vpc:
                    break
                for eni in vpc_to_eni_map.get(vpc, []):
                    if not isinstance(eni.owner, VpcEndpointInterface) \
                            and self._is_service_eni_match(eni) \
                            and eni.is_outbound_public() \
                            and not ((vpc.enable_dns_support or vpc.enable_dns_hostnames) and self._is_vpce_interface_connection_exist(eni)):
                        violated_vpc = vpc
                        break
                if violated_vpc:
                    for service in region_to_service_map[region]:
                        issues_list.append(Issue(f"The service {self.aws_service_type.name} is in use in region `{violated_vpc.region}`,"
                                                 f" but VPC `{violated_vpc.get_friendly_name()}`. is not configured to"
                                                 f" use a VPC Endpoint for {self.aws_service_type.name}",
                                                 service, violated_vpc))
        return issues_list


class SqsVpcEndpointExposureRule(AbstractVpcEndpointInterfaceNotUsedRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.SQS, (443,), [], False)

    def get_id(self) -> str:
        return 'vpc_endpoint_sqs_exposure'


class Ec2VpcEndpointExposureRule(AbstractVpcEndpointInterfaceNotUsedRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.EC2, (443,), [], False)

    def get_id(self) -> str:
        return 'vpc_endpoint_ec2_exposure'
