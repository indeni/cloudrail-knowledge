from typing import Dict, List
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import NetworkMode
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition, ContainerDefinition, EfsVolume, PortMappings
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.ip_protocol import IpProtocol


class CloudformationEcsTaskDefinitionBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.TASK_DEFINITION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> EcsTaskDefinition:
        properties: dict = cfn_res_attr['Properties']

        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        network_mode: NetworkMode = NetworkMode(properties.get('NetworkMode', 'none'))
        container_definitions: List[ContainerDefinition] = []
        efs_volume_data = []
        for volume in properties.get('Volumes', []):
            if conf := volume.get('EFSVolumeConfiguration', {}):
                efs_volume_data.append(EfsVolume(volume.get('Name'),
                                                 conf.get('FilesystemId'),
                                                 bool(conf.get('TransitEncryption') == 'ENABLED')))
        for container in properties.get('ContainerDefinitions', []):
            port_mappings: List[PortMappings] = []
            for port_map in container.get('PortMappings', []):
                host_port: int = port_map.get('HostPort', -1)
                container_port: int = port_map.get('ContainerPort', -1)
                if network_mode == NetworkMode.AWS_VPC:
                    host_port = container_port
                port_mappings.append(PortMappings(container_port=container_port,
                                                  host_port=host_port,
                                                  protocol=IpProtocol(port_map.get('Protocol', ''))))
            container_definitions.append(ContainerDefinition(container_name=container.get('Name'),
                                                             image=container.get('Image'),
                                                             port_mappings=port_mappings))
        return EcsTaskDefinition(task_arn=self.get_resource_id(cfn_res_attr),
                                 family=properties.get('Family'),
                                 revision=cfn_res_attr['physical_id'].split(':')[-1] if 'physical_id' in cfn_res_attr else None,
                                 account=account,
                                 region=region,
                                 task_role_arn=properties.get('TaskRoleArn', None),
                                 execution_role_arn=self.get_property(properties, 'ExecutionRoleArn'),
                                 network_mode=network_mode,
                                 container_definitions=container_definitions,
                                 efs_volume_data=efs_volume_data)
