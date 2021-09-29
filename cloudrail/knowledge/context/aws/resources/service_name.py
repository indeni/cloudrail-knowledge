from enum import Enum
from typing import Optional


class AwsServiceName(Enum):
    NONE = 'none'
    AWS_VPC = 'aws_vpc'
    AWS_INTERNET_GATEWAY = 'aws_internet_gateway'
    AWS_EGRESS_ONLY_INTERNET_GATEWAY = 'aws_egress_only_internet_gateway'
    AWS_VPC_ENDPOINT = 'aws_vpc_endpoint'
    AWS_NETWORK_ACL = 'aws_network_acl'
    AWS_DEFAULT_NETWORK_ACL = 'aws_default_network_acl'
    AWS_NETWORK_ACL_RULE = 'aws_network_acl_rule'
    AWS_SUBNET = 'aws_subnet'
    AWS_DEFAULT_SUBNET = 'aws_default_subnet'
    AWS_EC2_INSTANCE = 'aws_instance'
    AWS_LOAD_BALANCER = 'aws_lb'
    AWS_LOAD_BALANCER_TARGET_GROUP = 'aws_lb_target_group'
    AWS_LOAD_BALANCER_LISTENER = 'aws_lb_listener'
    AWS_LOAD_BALANCER_TARGET_GROUP_ATTACHMENT = 'aws_lb_target_group_attachment'
    AWS_LAUNCH_CONFIGURATION = 'aws_launch_configuration'
    AWS_AUTO_SCALING_GROUP = 'aws_autoscaling_group'
    AWS_SECURITY_GROUP = 'aws_security_group'
    AWS_DEFAULT_SECURITY_GROUP = 'aws_default_security_group'
    AWS_SECURITY_GROUP_RULE = 'aws_security_group_rule'
    AWS_S3_BUCKET = 'aws_s3_bucket'
    AWS_S3_BUCKET_OBJECT = 'aws_s3_bucket_object'
    AWS_S3_ACCESS_POINT = 'aws_s3_access_point'
    AWS_S3_BUCKET_POLICY = 'aws_s3_bucket_policy'
    AWS_S3_BUCKET_PUBLIC_ACCESS_BLOCK = 'aws_s3_bucket_public_access_block'
    AWS_S3_ACCOUNT_PUBLIC_ACCESS_BLOCK = 'aws_s3_account_public_access_block'
    AWS_VPC_PEERING_CONNECTION = 'aws_vpc_peering_connection'
    AWS_TRANSIT_GATEWAY = 'aws_ec2_transit_gateway'
    AWS_TRANSIT_GATEWAY_ROUTE = 'aws_ec2_transit_gateway_route'
    AWS_TRANSIT_GATEWAY_ATTACHMENT = 'aws_ec2_transit_gateway_vpc_attachment'
    AWS_TRANSIT_GATEWAY_ROUTE_TABLE = 'aws_ec2_transit_gateway_route_table'
    AWS_TRANSIT_GATEWAY_ROUTE_TABLE_ASSOCIATION = 'aws_ec2_transit_gateway_route_table_association'
    AWS_TRANSIT_GATEWAY_ROUTE_TABLE_PROPAGATION = 'aws_ec2_transit_gateway_route_table_propagation'
    AWS_ROUTE_TABLE = 'aws_route_table'
    AWS_MAIN_ROUTE_TABLE_ASSOCIATION = 'aws_main_route_table_association'
    AWS_DEFAULT_ROUTE_TABLE = 'aws_default_route_table'
    AWS_ROUTE = 'aws_route'
    AWS_ROUTE_TABLE_ASSOCIATION = 'aws_route_table_association'
    AWS_IAM_ROLE = 'aws_iam_role'
    AWS_IAM_POLICY = 'aws_iam_policy'
    AWS_IAM_ROLE_POLICY = 'aws_iam_role_policy'
    AWS_IAM_ROLE_POLICY_ATTACHMENT = 'aws_iam_role_policy_attachment'
    AWS_IAM_INSTANCE_PROFILE = 'aws_iam_instance_profile'
    AWS_NETWORK_INTERFACE = 'aws_network_interface'
    AWS_ECS_CLUSTER = 'aws_ecs_cluster'
    AWS_ECS_SERVICE = 'aws_ecs_service'
    AWS_ECS_TASK_DEFINITION = 'aws_ecs_task_definition'
    AWS_CLOUD_WATCH_EVENT_RULE = 'aws_cloudwatch_event_rule'
    AWS_CLOUD_WATCH_EVENT_TARGET = 'aws_cloudwatch_event_target'
    AWS_IAM_GROUP = 'aws_iam_group'
    AWS_IAM_GROUP_POLICY = 'aws_iam_group_policy'
    AWS_IAM_GROUP_POLICY_ATTACHMENT = 'aws_iam_group_policy_attachment'
    AWS_IAM_GROUP_MEMBERSHIP = 'aws_iam_group_membership'
    AWS_IAM_USER = 'aws_iam_user'
    AWS_IAM_USER_POLICY = 'aws_iam_user_policy'
    AWS_IAM_USER_POLICY_ATTACHMENT = 'aws_iam_user_policy_attachment'
    AWS_IAM_USER_GROUP_MEMBERSHIP = 'aws_iam_user_group_membership'
    AWS_REDSHIFT_CLUSTER = 'aws_redshift_cluster'
    AWS_REDSHIFT_SUBNET_GROUP = 'aws_redshift_subnet_group'
    AWS_DB_INSTANCE = 'aws_db_instance'
    AWS_DB_SUBNET_GROUP = 'aws_db_subnet_group'
    AWS_RDS_CLUSTER = 'aws_rds_cluster'
    AWS_RDS_GLOBAL_CLUSTER = 'aws_rds_global_cluster'
    AWS_RDS_CLUSTER_INSTANCE = 'aws_rds_cluster_instance'
    AWS_DEFAULT_VPC = 'aws_default_vpc'
    AWS_ELASTIC_SEARCH_DOMAIN = 'aws_elasticsearch_domain'
    AWS_EKS_CLUSTER = 'aws_eks_cluster'
    AWS_CLOUDFRONT_DISTRIBUTION_LIST = 'aws_cloudfront_distribution'
    AWS_CLOUDFRONT_ORIGIN_ACCESS_IDENTITY = 'aws_cloudfront_origin_access_identity'
    AWS_ELASTIC_IP = 'aws_eip'
    AWS_LAUNCH_TEMPLATE = 'aws_launch_template'
    AWS_ATHENA_WORKGROUP = 'aws_athena_workgroup'
    AWS_DYNAMODB_TABLE = 'aws_dynamodb_table'
    AWS_REST_API_GW = 'aws_api_gateway_rest_api'
    AWS_REST_API_GW_METHOD_SETTINGS = 'aws_api_gateway_method_settings'
    AWS_IAM_USER_LOGIN_PROFILE = 'aws_iam_user_login_profile'
    AWS_NAT_GATEWAY = 'aws_nat_gateway'
    AWS_AMI = 'aws_ami'
    AWS_AMI_COPY = 'aws_ami_copy'
    AWS_AMI_FROM_INSTANCE = 'aws_ami_from_instance'
    AWS_DAX_CLUSTER = 'aws_dax_cluster'
    AWS_DOCDB_CLUSTER = 'aws_docdb_cluster'
    AWS_DOCDB_CLUSTER_PARAMETER_GROUP = 'aws_docdb_cluster_parameter_group'
    AWS_CODEBUILD_PROJECT = 'aws_codebuild_project'
    AWS_CODEBUILD_REPORT_GROUP = 'aws_codebuild_report_group'
    AWS_CLOUDTRAIL = 'aws_cloudtrail'
    AWS_CLOUDWATCH_LOG_GROUP = 'aws_cloudwatch_log_group'
    AWS_KMS_KEY = 'aws_kms_key'
    AWS_VPC_ENDPOINT_ROUTE_TABLE_ASSOCIATION = 'aws_vpc_endpoint_route_table_association'
    AWS_SQS_QUEUE = 'aws_sqs_queue'
    AWS_ELASTICACHE_REPLICATION_GROUP = 'aws_elasticache_replication_group'
    AWS_ELASTICACHE_CLUSTER = 'aws_elasticache_cluster'
    AWS_ELASTICACHE_SUBNET_GROUP = 'aws_elasticache_subnet_group'
    AWS_SNS_TOPIC = 'aws_sns_topic'
    AWS_SQS_QUEUE_POLICY = 'aws_sqs_queue_policy'
    AWS_NEPTUNE_CLUSTER = 'aws_neptune_cluster'
    AWS_ECR_REPOSITORY = 'aws_ecr_repository'
    AWS_ECR_REPOSITORY_POLICY = 'aws_ecr_repository_policy'
    AWS_CLOUDWATCH_LOG_DESTINATION = 'aws_cloudwatch_log_destination'
    AWS_CLOUDWATCH_LOG_DESTINATION_POLICY = 'aws_cloudwatch_log_destination_policy'
    AWS_API_GATEWAY_REST_API_POLICY = 'aws_api_gateway_rest_api_policy'
    AWS_ELASTICSEARCH_DOMAIN_POLICY = 'aws_elasticsearch_domain_policy'
    AWS_LAMBDA_FUNCTION = 'aws_lambda_function'
    AWS_LAMBDA_PERMISSION = 'aws_lambda_permission'
    AWS_LAMBDA_ALIAS = 'aws_lambda_alias'
    AWS_GLACIER_VAULT = 'aws_glacier_vault'
    AWS_EFS_FILE_SYSTEM = 'aws_efs_file_system'
    AWS_EFS_FILE_SYSTEM_POLICY = 'aws_efs_file_system_policy'
    AWS_EFS_MOUNT_TARGET = 'aws_efs_mount_target'
    AWS_GLUE_RESOURCE_POLICY = 'aws_glue_resource_policy'
    AWS_SECRETSMANAGER_SECRET = 'aws_secretsmanager_secret'
    AWS_SECRETSMANAGER_SECRET_POLICY = 'aws_secretsmanager_secret_policy'
    AWS_API_GATEWAY_BASE_PATH_MAPPING = 'aws_api_gateway_base_path_mapping'
    AWS_API_GATEWAY_DOMAIN_NAME = 'aws_api_gateway_domain_name'
    AWS_API_GATEWAY_INTEGRATION = 'aws_api_gateway_integration'
    AWS_API_GATEWAY_METHOD = 'aws_api_gateway_method'
    AWS_KINESIS_STREAM = 'aws_kinesis_stream'
    AWS_GLUE_CRAWLER = 'aws_glue_crawler'
    AWS_GLUE_CATALOG_TABLE = 'aws_glue_catalog_table'
    AWS_GLUE_CONNECTION = 'aws_glue_connection'
    AWS_XRAY_ENCRYPTION_CONFIG = 'aws_xray_encryption_config'
    AWS_KINESIS_FIREHOSE_DELIVERY_STREAM = 'aws_kinesis_firehose_delivery_stream'
    AWS_IAM_ACCOUNT_PASSWORD_POLICY = 'aws_iam_account_password_policy'
    AWS_WORKSPACES_WORKSPACE = 'aws_workspaces_workspace'
    AWS_WORKSPACES_DIRECTORY = 'aws_workspaces_directory'
    AWS_KMS_ALIAS = 'aws_kms_alias'
    AWS_NEPTUNE_CLUSTER_INSTANCE = 'aws_neptune_cluster_instance'
    AWS_IAM_POLICY_ATTACHMENT = 'aws_iam_policy_attachment'
    AWS_SSM_PARAMETER = 'aws_ssm_parameter'
    AWS_DMS_REPLICATION_INSTANCE = 'aws_dms_replication_instance'
    AWS_DMS_REPLICATION_SUBNET_GROUP = 'aws_dms_replication_subnet_group'
    AWS_SAGEMAKER_ENDPOINT_CONFIGURATION = 'aws_sagemaker_endpoint_configuration'
    AWS_SAGEMAKER_NOTEBOOK_INSTANCE = 'aws_sagemaker_notebook_instance'
    AWS_DIRECTORY_SERVICE_DIRECTORY = 'aws_directory_service_directory'
    AWS_BATCH_COMPUTE_ENVIRONMENT = 'aws_batch_compute_environment'
    AWS_MQ_BROKER = 'aws_mq_broker'
    AWS_APIGATEWAYV_2_API = 'aws_apigatewayv2_api'
    AWS_APIGATEWAYV_2_INTEGRATION = 'aws_apigatewayv2_integration'
    AWS_APIGATEWAYV_2_VPC_LINK = 'aws_apigatewayv2_vpc_link'
    AWS_EMR_CLUSTER = 'aws_emr_cluster'
    AWS_GLOBALACCELERATOR_ACCELERATOR = 'aws_globalaccelerator_accelerator'
    AWS_GLOBALACCELERATOR_ENDPOINT_GROUP = 'aws_globalaccelerator_endpoint_group'
    AWS_GLOBALACCELERATOR_LISTENER = 'aws_globalaccelerator_listener'
    AWS_CLOUDHSM_V_2_CLUSTER = 'aws_cloudhsm_v2_cluster'
    AWS_CLOUDHSM_V_2_HSM = 'aws_cloudhsm_v2_hsm'
    AWS_S_3_OUTPOSTS_ENDPOINT = 'aws_s3outposts_endpoint'
    AWS_WORKLINK_FLEET = 'aws_worklink_fleet'
    AWS_CONFIG_CONFIGURATION_AGGREGATOR = 'aws_config_configuration_aggregator'
    AWS_API_GATEWAY_STAGE = 'aws_api_gateway_stage'
    AWS_ATHENA_DATABASE = 'aws_athena_database'
    AWS_FSX_WINDOWS_FILE_SYSTEM = 'aws_fsx_windows_file_system'


AWS_SERVICES_DOMAIN: str = ".amazonaws.com"


class AwsServiceAttributes:

    def __init__(self, aws_service_type: str, region: str = None) -> None:
        self._aws_service_type: str = aws_service_type
        self._qualified_service_name: str = f"{aws_service_type}.amazonaws.com"
        self._domain_name: str = f"com.amazonaws.{aws_service_type}" if region is None else f"com.amazonaws.{region}.{aws_service_type}"

    def get_service_type(self) -> Optional[str]:
        return self._aws_service_type

    def get_qualified_service_name(self) -> Optional[str]:
        return self._qualified_service_name

    def get_domain_name(self) -> Optional[str]:
        return self._domain_name

    @staticmethod
    def parse_service_name(qualified_service_name: str) -> str:
        return qualified_service_name.split('.', 3)[-1]


class AwsServiceType(Enum):
    EC2 = "ec2"
    S3 = "s3"
    CLOUDFRONT = "cloudfront"
    APIGATEWAY = "apigateway"
    DYNAMODB = "dynamodb"
    LAMBDA = "lambda"
    ECS = "ecs"
    SQS = "sqs"
    CLOUDFORMATION = "cloudformation"
