from abc import abstractmethod
from typing import Optional, Type

from cloudrail.knowledge.utils.utils import is_subset
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterFilterType


class Ec2InstanceFilter:
    def __init__(self, filter_type: ParameterFilterType):
        self.filter_type = filter_type

    @abstractmethod
    def passed(self, ec2: Ec2Instance) -> bool:
        return False


class Ec2InstanceFilterById(Ec2InstanceFilter):
    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        Ec2InstanceFilter.__init__(self, ParameterFilterType.ID)

    def passed(self, ec2: Ec2Instance) -> bool:
        return self.instance_id == ec2.instance_id


class Ec2InstanceFilterByName(Ec2InstanceFilter):
    def __init__(self, instance_name: str):
        self.instance_name = instance_name
        Ec2InstanceFilter.__init__(self, ParameterFilterType.NAME)

    def passed(self, ec2: Ec2Instance) -> bool:
        return self.instance_name == ec2.name


class Ec2InstanceFilterByImage(Ec2InstanceFilter):
    def __init__(self, image_id: str):
        self.image_id = image_id
        Ec2InstanceFilter.__init__(self, ParameterFilterType.IMAGE)

    def passed(self, ec2: Ec2Instance) -> bool:
        return self.image_id == ec2.image_id


class Ec2InstanceFilterByIp(Ec2InstanceFilter):
    def __init__(self, ip: str):
        self.ip = ip
        Ec2InstanceFilter.__init__(self, ParameterFilterType.IP)

    def passed(self, ec2: Ec2Instance) -> bool:
        return self.ip in ec2.network_resource.private_ip_addresses or \
               self.ip in ec2.network_resource.public_ip_addresses


class Ec2InstanceFilterBySubnet(Ec2InstanceFilter):
    def __init__(self, instance_subnet: str):
        self.instance_subnet = instance_subnet
        Ec2InstanceFilter.__init__(self, ParameterFilterType.SUBNET)

    def passed(self, ec2: Ec2Instance) -> bool:
        return any(ip for ip in ec2.network_resource.private_ip_addresses
                   if is_subset(ip, self.instance_subnet))


def ec2_instance_filter_type_to_class(filter_type: ParameterFilterType) -> Optional[Type[Ec2InstanceFilter]]:
    if filter_type == ParameterFilterType.ID:
        return Ec2InstanceFilterById
    if filter_type == ParameterFilterType.NAME:
        return Ec2InstanceFilterByName
    if filter_type == ParameterFilterType.IMAGE:
        return Ec2InstanceFilterByImage
    if filter_type == ParameterFilterType.IP:
        return Ec2InstanceFilterByIp
    if filter_type == ParameterFilterType.SUBNET:
        return Ec2InstanceFilterBySubnet

    return None
