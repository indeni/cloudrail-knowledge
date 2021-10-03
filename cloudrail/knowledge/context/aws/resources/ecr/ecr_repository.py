from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ecr.ecr_repository_policy import EcrRepositoryPolicy
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class EcrRepository(AwsResource):
    """
        Attributes:
            repo_name: The name of the ECR repository.
            arn: The ARN of the repository.
            policy: The resource policy of the ECR.
            encryption_type: The type of encryption used by the ECR repository.
            kms_key_id: The KMS key ID used to encrypt the ECR repository, if the encryption type is KMS.
            kms_data: The actual KmsKey object referenced by the KMS ID.
            image_tag_mutability: Image tag mutability setting for the ECR repository.
            is_image_scan_on_push: An indication whether images are scanned after being pushed to the ECR repository.
    """
    def __init__(self,
                 repo_name: str,
                 arn: str,
                 region: str,
                 account: str,
                 image_tag_mutability: str,
                 is_image_scan_on_push: bool,
                 encryption_type: str,
                 kms_key_id: Optional[str]):
        super().__init__(account, region, AwsServiceName.AWS_ECR_REPOSITORY)
        self.repo_name: str = repo_name
        self.arn: str = arn
        self.policy: EcrRepositoryPolicy = None
        self.encryption_type: str = encryption_type
        self.kms_key_id: str = kms_key_id
        self.kms_data: Optional[KmsKey] = None
        self.image_tag_mutability: str = image_tag_mutability
        self.is_image_scan_on_push: bool = is_image_scan_on_push

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.repo_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECR repository'
        else:
            return 'ECR repositories'

    def get_cloud_resource_url(self) -> str:
        return '{0}ecr/repositories/private/{1}/{2}?region={3}'\
            .format(self.AWS_CONSOLE_URL, self.account, self.repo_name, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
