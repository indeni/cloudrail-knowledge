from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class DmsReplicationInstanceSubnetGroup(AwsResource):
    """
        Attributes:
            rep_subnet_group_id: The ID of this subnet group.
            subnet_ids: The IDs of the subnets contained in this group.
            vpc_id: The ID of the VPC the subnets are in.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 rep_subnet_group_id: str,
                 subnet_ids: List,
                 vpc_id: Optional[str]):
        super().__init__(account, region, AwsServiceName.AWS_DMS_REPLICATION_SUBNET_GROUP)
        self.rep_subnet_group_id: str = rep_subnet_group_id
        self.subnet_ids: List = subnet_ids
        self.vpc_id: Optional[str] = vpc_id

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.rep_subnet_group_id]

    def get_id(self) -> str:
        return self.rep_subnet_group_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Dms Subnet Group'
        else:
            return 'Dms Subnet Groups'

    def get_arn(self) -> Optional[str]:
        if self.account:
            return f"arn:aws:dms:{self.region}:{self.account}:subgrp:{self.rep_subnet_group_id}"
        else:
            return None

    def get_cloud_resource_url(self) -> str:
        return '{0}dms/v2/home?region={1}#subnetGroupDetail/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.rep_subnet_group_id)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'subnet_ids': self.subnet_ids}
