import os
import core
from dragoneye import AwsScanner, AwsCloudScanSettings, AzureScanner, AzureCloudScanSettings, AwsSessionFactory, AzureAuthorizer, \
    GcpCloudScanSettings, GcpScanner, GcpCredentialsFactory

from cloudrail.knowledge.context.cloud_provider import CloudProvider

core_path = os.path.dirname(os.path.abspath(core.__file__))
scan_commands_dir_path = os.path.join(core_path, 'scan_commands')

cloud_provider = CloudProvider.AZURE

if cloud_provider == CloudProvider.AMAZON_WEB_SERVICES:
    aws_settings = AwsCloudScanSettings(
        commands_path=os.path.join(scan_commands_dir_path, 'aws.yaml'),
        account_name='dev', regions_filter=['us-east-1'], default_region='us-east-1'
    )
    session = AwsSessionFactory.get_session(region='us-east-1')
    AwsScanner(session, aws_settings).scan()
elif cloud_provider == CloudProvider.AZURE:
    azure_settings = AzureCloudScanSettings(
        commands_path=os.path.join(scan_commands_dir_path, 'azure.yaml'),
        subscription_id='...',
        account_name='dev'
    )
    token = AzureAuthorizer.get_authorization_token(
        subscription_id=azure_settings.subscription_id,
        tenant_id='...',
        client_id='...',
        client_secret='...'
    )
    AzureScanner(token, azure_settings).scan()
elif cloud_provider == CloudProvider.GCP:
    gcp_settings = GcpCloudScanSettings(
        commands_path=os.path.join(scan_commands_dir_path, 'gcp.yaml'),
        account_name='dev',
        project_id='project id'
    )
    # If you have GCP user: Download SDK (https://cloud.google.com/sdk/docs/install) and log in via gcloud auth application-default login
    credentials = GcpCredentialsFactory.get_default_credentials()
    # If you want to login via credentials file
    # credentials = GcpCredentialsFactory.from_service_account_file('path-to-your-credentials-file')
    # If you want to login via credentials dictionary (the above's file content)
    # credentials = GcpCredentialsFactory.from_service_account_info({})
    GcpScanner(credentials, gcp_settings).scan()
