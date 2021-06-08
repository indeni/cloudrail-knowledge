from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.ec2.vpc_endpoint import VpcEndpointInterface
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.service_name import AwsServiceType
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_rule import AbstractVpcEndpointRule


class AbstractVpcEndpointInterfaceAvailabilityZoneRule(AbstractVpcEndpointRule):

    MIN_AZ: int = 2

    @abstractmethod
    def get_id(self) -> str:
        pass

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        vpc_list, region_to_service_map, vpc_to_eni_map = self._init_maps(env_context)
        issues_list: List[Issue] = []
        for vpc in vpc_list:
            vpce_eni_to_az_map: Dict[str, List[NetworkInterface]] = {}
            vpc_instance_exist: bool = False
            for eni in vpc_to_eni_map.get(vpc, []):
                if not isinstance(eni.owner, VpcEndpointInterface) and \
                        self._is_service_eni_match(eni):
                    vpc_instance_exist = True
                    if eni.is_outbound_public() and (vpc.enable_dns_support or vpc.enable_dns_hostnames):
                        vpc_endpoint_eni_list: List[NetworkInterface] = self._get_all_active_vpc_endpoint_eni_list(eni)
                        for vpce_eni in vpc_endpoint_eni_list:
                            if vpce_eni.availability_zone not in vpce_eni_to_az_map:
                                vpce_eni_to_az_map[vpce_eni.availability_zone] = []
                            vpce_eni_to_az_map[vpce_eni.availability_zone].append(vpce_eni)
                        if len(vpce_eni_to_az_map) >= self.MIN_AZ:
                            break
            if vpc_instance_exist and len(vpce_eni_to_az_map) < self.MIN_AZ:
                subnets_ids = []
                availability_zones = set()

                for subnets in vpc.subnets_by_az_map.values():
                    for subnet in subnets:
                        subnets_ids.append(subnet.subnet_id)
                        availability_zones.add(subnet.availability_zone)

                for service in region_to_service_map[vpc.region]:
                    issues_list.append(Issue(f"The service {self.aws_service_type.name} is in use in region `{vpc.region}`. "
                                             f"which contains a VPC `{vpc.vpc_id}`. "
                                             f"and the following subnets `{str(subnets_ids)}`. in availability zones `{str(availability_zones)}`. "
                                             f"can reach the Internet but do not have at least {self.MIN_AZ} VPC endpoints"
                                             f" from different availability zones",
                                             service, vpc))
        return issues_list


class SqsVpcEndpointInterfaceAvailabilityZoneRule(AbstractVpcEndpointInterfaceAvailabilityZoneRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.SQS, (443, ), [], False)

    def get_id(self) -> str:
        return 'vpc_endpoint_sqs_subnet_exposure'
