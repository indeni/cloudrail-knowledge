from typing import Dict

from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder

class CloudformationCodebuildReportGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CODEBUILD_REPORTGROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CodeBuildReportGroup:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        export_config_settings = properties['ExportConfig']
        export_config_type = export_config_settings['ExportConfigType']
        export_config_s3_destination_bucket = None
        export_config_s3_destination_encryption_key = None
        export_config_s3_destination_encryption_disabled = True
        if export_config_type == 'S3':
            export_config_s3_destination_bucket = export_config_settings['S3Destination']['Bucket']
            export_config_s3_destination_encryption_key =\
                self.get_encryption_key_arn(export_config_settings['S3Destination'].get('EncryptionKey'), account, region, CodeBuildReportGroup)
            export_config_s3_destination_encryption_disabled = export_config_settings['S3Destination'].get('EncryptionDisabled')
        return CodeBuildReportGroup(account=account,
                                    region=region,
                                    name=self.get_property(properties, 'Name'),
                                    export_config_type=properties['ExportConfig']['ExportConfigType'],
                                    export_config_s3_destination_bucket=export_config_s3_destination_bucket,
                                    export_config_s3_destination_encryption_key=export_config_s3_destination_encryption_key,
                                    export_config_s3_destination_encryption_disabled=export_config_s3_destination_encryption_disabled,
                                    arn=self.get_resource_id(cfn_res_attr))
