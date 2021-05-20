from typing import List
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class Account(AwsResource):
    """
        Attributes:
            account: The ID of the account.
            account_name: The name of the account, as registered within Cloudrail.
            supports_ec2_classic_mode: True if this is an account created before 2013-12-04.

        Represents the AWS account we're doing the analysis against. There will always be 1, or 0 (if running without
        a cloud account).
    """

    # account class is mergeable in order to add it to Issue as exposed attributes
    def __init__(self, account: str, account_name: str, supports_ec2_classic_mode: bool):
        super().__init__(account=account, region=AwsResource.GLOBAL_REGION, tf_resource_type=AwsServiceName.NONE)
        self.account: str = account
        self.account_name: str = account_name
        self.supports_ec2_classic_mode: bool = supports_ec2_classic_mode

    def get_keys(self) -> List[str]:
        return [self.account]

    def get_id(self) -> str:
        return self.account

    def get_name(self) -> str:
        return self.account_name

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region=us-east-1#/account_settings'\
            .format(self.AWS_CONSOLE_URL)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
