from typing import Dict

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources.cloudfront.origin_access_identity import OriginAccessIdentity


class CloudformationCloudfrontOriginAccessIdentityBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDFRONT_ORIGIN_ACCESS_IDENTITY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> OriginAccessIdentity:
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        oai_id = self.get_resource_id(cfn_res_attr)
        cloudfront_access_identity_path = f'origin-access-identity/cloudfront/{oai_id}'
        iam_arn = f'arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai_id}'
        return OriginAccessIdentity(account=account, region=region, oai_id=oai_id,
                                    cloudfront_access_identity_path=cloudfront_access_identity_path,
                                    iam_arn=iam_arn, s3_canonical_user_id=None)
