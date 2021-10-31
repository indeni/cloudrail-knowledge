from typing import Dict

from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster_parameter_group import DocDbClusterParameterGroup, DocDbClusterParameter
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationDocDbClusterParameterGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DOCDB_CLUSTER_PARAMETER_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DocDbClusterParameterGroup:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        group_name = self.get_property(properties, 'Name', self.get_resource_id(cfn_res_attr))
        parameters = []
        for key, value in self.get_property(properties, 'Parameters').items():
            parameters.append(DocDbClusterParameter(key, value))
        return DocDbClusterParameterGroup(account=account, region=region, group_name=group_name, parameters=parameters)
