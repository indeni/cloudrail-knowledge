from typing import Dict
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAttributes, LoadBalancerAccessLogs
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerAttributesBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LoadBalancerAttributes:
        if self.get_property(cfn_res_attr['Properties'], 'LoadBalancerAttributes'):
            properties: dict = cfn_res_attr['Properties']
            account = cfn_res_attr['account_id']
            region = cfn_res_attr['region']
            load_balancer_arn = self.get_resource_id(cfn_res_attr)
            attributes_dict = {}
            for attribute in self.get_property(properties, 'LoadBalancerAttributes', []):
                if attribute['Value'] == 'true':
                    attributes_dict.update({attribute['Key']: True})
                elif attribute['Value'] == 'false':
                    attributes_dict.update({attribute['Key']: False})
                else:
                    attributes_dict.update({attribute['Key']: attribute['Value']})
            drop_invalid_header_fields = attributes_dict.get('routing.http.drop_invalid_header_fields.enabled', False)
            access_logs = LoadBalancerAccessLogs(attributes_dict.get('access_logs.s3.bucket', ''),
                                                 attributes_dict.get('access_logs.s3.prefix', ''),
                                                 attributes_dict.get('access_logs.s3.enabled', False))
            return LoadBalancerAttributes(account=account, region=region, load_balancer_arn=load_balancer_arn,
                                      drop_invalid_header_fields=drop_invalid_header_fields, access_logs=access_logs)
        return None
