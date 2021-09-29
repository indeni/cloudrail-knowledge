from typing import Dict
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerListenerBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER_LISTENER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LoadBalancerListener:
        properties: dict = cfn_res_attr['Properties']
        defaults_actions: list = properties.get('DefaultActions', [])
        default_action_type = None
        redirect_action_protocol = None
        redirect_action_port = None
        if defaults_actions:
            first_default_action = defaults_actions[0]
            default_action_type = first_default_action['Type']
            if default_action_type.lower() == 'redirect':
                redirect_action_protocol = self.get_property(first_default_action.get('RedirectConfig', {}), 'Protocol')
                redirect_action_port = self.get_property(first_default_action.get('RedirectConfig', {}), 'Port')

        return LoadBalancerListener(listener_port=self.get_property(properties, 'Port'),
                                    listener_protocol=self.get_property(properties, 'Protocol'),
                                    listener_arn=self.get_resource_id(cfn_res_attr),
                                    load_balancer_arn=self.get_property(properties, 'LoadBalancerArn'),
                                    account=cfn_res_attr['account_id'],
                                    region=cfn_res_attr['region'],
                                    default_action_type=default_action_type,
                                    redirect_action_protocol=redirect_action_protocol,
                                    redirect_action_port=redirect_action_port)
