from typing import Dict

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType

from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationDmsReplicationInstanceBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DMS_REPLICATION_INSTANCE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DmsReplicationInstance:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        name = self.get_property(properties, 'ReplicationInstanceIdentifier', self.get_resource_id(cfn_res_attr))
        arn = build_arn(service='dms', region=region, account_id=account, resource_type='replication-instance/', path='replication-instance-', resource_name=self.create_random_pseudo_identifier())
        publicly_accessible = self.get_property(properties, 'PubliclyAccessible', True)
        rep_instance_subnet_group_id = self.get_property(properties, 'ReplicationSubnetGroupIdentifier', 'default')
        security_group_ids = self.get_property(properties, 'VpcSecurityGroupIds', [])
        return DmsReplicationInstance(account=account,
                                      region=region,
                                      name=name,
                                      arn=arn,
                                      publicly_accessible=publicly_accessible,
                                      rep_instance_subnet_group_id=rep_instance_subnet_group_id,
                                      security_group_ids=security_group_ids)
