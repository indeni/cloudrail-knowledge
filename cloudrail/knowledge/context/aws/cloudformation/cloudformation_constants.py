from enum import Enum


class CloudformationResourceType(str, Enum):
    VPC = 'AWS::EC2::VPC'
    VPC_ENDPOINT = 'AWS::EC2::VPCEndpoint'
    INTERNET_GATEWAY = 'AWS::EC2::InternetGateway'
    VPC_GATEWAY_ATTACHMENT = 'AWS::EC2::VPCGatewayAttachment'
    EC2_INSTANCE = 'AWS::EC2::Instance'
    SUBNET = 'AWS::EC2::Subnet'
    SECURITY_GROUP = 'AWS::EC2::SecurityGroup'
    NAT_GW = 'AWS::EC2::NatGateway'
    SECURITY_GROUP_EGRESS = 'AWS::EC2::SecurityGroupEgress'
    SECURITY_GROUP_INGRESS = 'AWS::EC2::SecurityGroupIngress'
    ROUTE_TABLE = 'AWS::EC2::RouteTable'
    ROUTE = 'AWS::EC2::Route'
    SUBNET_ROUTE_TABLE_ASSOCIATION = 'AWS::EC2::SubnetRouteTableAssociation'
    S3_BUCKET = 'AWS::S3::Bucket'
    S3_BUCKET_POLICY = 'AWS::S3::BucketPolicy'
    DAX_CLUSTER = 'AWS::DAX::Cluster'
    IAM_ROLE = 'AWS::IAM::Role'
    ATHENA_WORKGROUP = 'AWS::Athena::WorkGroup'
    KMS_KEY = 'AWS::KMS::Key'
    KMS_KEY_ALIAS = 'AWS::KMS::Alias'
    CLOUDTRAIL = 'AWS::CloudTrail::Trail'
    CODEBUILD_REPORTGROUP = 'AWS::CodeBuild::ReportGroup'
    ELASTIC_LOAD_BALANCER = 'AWS::ElasticLoadBalancingV2::LoadBalancer'
    ELASTIC_LOAD_BALANCER_LISTENER = 'AWS::ElasticLoadBalancingV2::Listener'
    API_GATEWAY_V2 = 'AWS::ApiGatewayV2::Api'
    API_GATEWAY_V2_VPC_LINK = 'AWS::ApiGatewayV2::VpcLink'
    API_GATEWAY_V2_INTEGRATION = 'AWS::ApiGatewayV2::Integration'
    BATCH_COMPUTE_ENVIRONMENT = 'AWS::Batch::ComputeEnvironment'
    ELASTIC_LOAD_BALANCER_TARGET_GROUP = 'AWS::ElasticLoadBalancingV2::TargetGroup'
    ELASTIC_IP = 'AWS::EC2::EIP'
    DYNAMODB_TABLE = 'AWS::DynamoDB::Table'
    CONFIG_SERVICE_AGGREGATOR = 'AWS::Config::ConfigurationAggregator'
    AUTO_SCALING_GROUP = 'AWS::AutoScaling::AutoScalingGroup'
    DMS_REPLICATION_SUBNET_GROUP = 'AWS::DMS::ReplicationSubnetGroup'
    DMS_REPLICATION_INSTANCE = 'AWS::DMS::ReplicationInstance'
    LAUNCH_TEMPLATE = 'AWS::EC2::LaunchTemplate'
    LAUNCH_CONFIGURATION = 'AWS::AutoScaling::LaunchConfiguration'
    CLOUDFRONT_DISTRIBUTION_LIST = 'AWS::CloudFront::Distribution'
    CLOUDFRONT_ORIGIN_ACCESS_IDENTITY = 'AWS::CloudFront::CloudFrontOriginAccessIdentity'
    CLOUDWATCH_LOGS_DESTINATION = 'AWS::Logs::Destination'
    LAMBDA_FUNCTION = 'AWS::Lambda::Function'
    NETWORK_ACL = 'AWS::EC2::NetworkAcl'
    SUBNET_NETWORK_ACL_ASSOCIATION = 'AWS::EC2::SubnetNetworkAclAssociation'
    NETWORK_ACL_ENTRY = 'AWS::EC2::NetworkAclEntry'
    IAM_INSTANCE_PROFILE = 'AWS::IAM::InstanceProfile'
    TRANSIT_GATEWAY_ATTACHMENT = 'AWS::EC2::TransitGatewayAttachment'
    TRANSIT_GATEWAY = 'AWS::EC2::TransitGateway'
    TRANSIT_GATEWAY_ROUTE_TABLE = 'AWS::EC2::TransitGatewayRouteTable'
    TRANSIT_GATEWAY_ROUTE_TABLE_ASSOCIATION = 'AWS::EC2::TransitGatewayRouteTableAssociation'
    TRANSIT_GATEWAY_ROUTE = 'AWS::EC2::TransitGatewayRoute'
    CODEBUILD_PROJECT = 'AWS::CodeBuild::Project'
    DOCDB_CLUSTER = 'AWS::DocDB::DBCluster'
    DOCDB_CLUSTER_PARAMETER_GROUP = 'AWS::DocDB::DBClusterParameterGroup'
    KINESIS_STREAM = 'AWS::Kinesis::Stream'
    RDS_CLUSTER = 'AWS::RDS::DBCluster'
