from typing import List, Dict, Set

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.connection import PrivateConnectionDetail
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class Ec2S3ShareRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'ec2_s3_share_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        public_ec2_to_private_s3_bucket_connections = \
            self._public_ec2_doesnt_have_access_to_private_buckets_rule(env_context)
        issues: List = []
        for public_ec2, private_buckets in public_ec2_to_private_s3_bucket_connections.items():
            for bucket in private_buckets:
                issues.append(Issue('{} Public {} has access to the following private {}: {}'
                                    .format(public_ec2.get_friendly_name(),
                                            public_ec2.get_type(),
                                            bucket.get_type(),
                                            bucket.get_friendly_name()),
                                    bucket,
                                    public_ec2))
        return issues

    @classmethod
    def _public_ec2_doesnt_have_access_to_private_buckets_rule(cls, env_context: AwsEnvironmentContext) -> \
            Dict[Ec2Instance, Set[S3Bucket]]:
        public_ec2s_with_private_bucket_access = {}
        ec2_list: List[Ec2Instance] = env_context.ec2s
        public_ec2s = [x for x in ec2_list if x.network_resource.is_inbound_public]
        private_ec2s = [x for x in ec2_list if not x.network_resource.is_inbound_public]
        privately_accessible_buckets = {
            connection.target_instance for private_ec2 in private_ec2s for connection in
            private_ec2.network_resource.outbound_connections if
            isinstance(connection, PrivateConnectionDetail) and isinstance(connection.target_instance, S3Bucket)}

        for public_ec2 in public_ec2s:
            publicly_accessible_buckets = \
                {x.target_instance for x in public_ec2.network_resource.outbound_connections if
                 isinstance(x, PrivateConnectionDetail) and isinstance(x.target_instance, S3Bucket)}
            misplaced_buckets = publicly_accessible_buckets.intersection(privately_accessible_buckets)
            if misplaced_buckets:
                public_ec2s_with_private_bucket_access[public_ec2] = misplaced_buckets

        return public_ec2s_with_private_bucket_access

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets)
