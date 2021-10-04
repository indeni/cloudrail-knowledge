from typing import List

from cloudrail.knowledge.context.aws.resources.aws_resource_with_based_policy import AwsResourceWithBasedPolicy
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault_policy import GlacierVaultPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlacierVault(AwsResourceWithBasedPolicy):
    """
        Attributes:
            vault_name: The name of the vualt.
            arn: The ARN of the vault.
    """
    def __init__(self,
                 vault_name: str,
                 arn: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_GLACIER_VAULT)
        self.vault_name: str = vault_name
        self.arn: str = arn

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.vault_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'S3 Glacier Vault'
        else:
            return 'S3 Glacier Vaults'

    def get_cloud_resource_url(self) -> str:
        return '{0}glacier/home?region={1}#/vaults'\
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
