from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamPasswordPolicy(AwsResource):
    """
        Attributes:
            min_pass_length: The minimum length required for passwords.
            require_low_case_characters: True if lower cases characters are required
                according to the policy.
            require_upper_case_characters: True if upper cases characters are required
                according to the policy.
            require_numbers: True if number characters are required
                according to the policy.
            require_symbols: True if symbol characters are required
                according to the policy.
            allow_users_to_change_pass: True if users can change their password.
            max_pass_age: The maximum age of a password before it needs to be
                replaced.
            password_reuse_prevention: Number of passwords kept in history that cannot
                be repeated.
    """

    def __init__(self,
                 min_pass_length: int,
                 require_low_case_characters: bool,
                 require_numbers: bool,
                 require_upper_case_characters: bool,
                 require_symbols: bool,
                 allow_users_to_change_pass: bool,
                 max_pass_age: int,
                 password_reuse_prevention: int,
                 account: str):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_ACCOUNT_PASSWORD_POLICY)
        self.min_pass_length: int = min_pass_length
        self.require_low_case_characters: bool = require_low_case_characters
        self.require_numbers: bool = require_numbers
        self.require_upper_case_characters: bool = require_upper_case_characters
        self.require_symbols: bool = require_symbols
        self.allow_users_to_change_pass: bool = allow_users_to_change_pass
        self.max_pass_age: int = max_pass_age
        self.password_reuse_prevention: int = password_reuse_prevention

    def get_keys(self) -> List[str]:
        return [self.account]

    def get_name(self) -> str:
        if self.account:
            return f'IAM account password policy for account {self.account}'
        else:
            return 'IAM account password policy'

    def get_type(self, is_plural: bool = False) -> str:
        return 'IAM Password Policy'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/account_settings$editPasswordPolicy?step=passwordPolicy' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1')

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'min_pass_length': self.min_pass_length,
                'require_low_case_characters': self.require_low_case_characters,
                'require_numbers': self.require_numbers,
                'require_upper_case_characters': self.require_upper_case_characters,
                'require_symbols': self.require_symbols,
                'allow_users_to_change_pass': self.allow_users_to_change_pass,
                'max_pass_age': self.max_pass_age,
                'password_reuse_prevention': self.password_reuse_prevention}
