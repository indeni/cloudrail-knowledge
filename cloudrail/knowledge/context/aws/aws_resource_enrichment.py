from typing import Dict, List

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, Policy
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.utils.policy_utils import is_any_resource_based_action_allowed
from cloudrail.knowledge.utils.s3_public_access_evaluator import S3PublicAccessEvaluator, PublicAccessResults

from cloudrail.knowledge.utils.policy_evaluator import is_action_subset_allowed
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from cloudrail.knowledge.utils.connection_utils import get_allowing_indirect_public_access_on_ports, get_allowing_public_access_portless, \
    get_allowing_public_access_on_ports
from cloudrail.knowledge.utils.role_utils import is_policy_allowing_external_assume


class AwsResourceEnrichment(DependencyInvocation):
    def __init__(self, ctx: AwsEnvironmentContext):

        functions_pool = [
            IterFunctionData(self._assume_role_policy_is_allowing_external_assume, ctx.assume_role_policies),
            IterFunctionData(self._rds_instance_indirect_connection_data, ctx.rds_instances),
            IterFunctionData(self._redshift_indirect_connection_data, ctx.redshift_clusters),
            IterFunctionData(self._elastic_search_indirect_connection_data, ctx.elastic_search_domains),
            IterFunctionData(self._neptune_instance_sg_allowing_public_access, ctx.neptune_cluster_instances),
            IterFunctionData(self._dms_sg_allowing_public_access, ctx.dms_replication_instances),
            IterFunctionData(self._rds_instance_sg_allowing_public_access, ctx.rds_instances),
            IterFunctionData(self._eks_cluster_sg_allowing_public_access, ctx.eks_clusters),
            IterFunctionData(self._redshift_sg_allowing_public_access, ctx.redshift_clusters),
            IterFunctionData(self._s3_bucket_publicly_allowing_resources, ctx.s3_buckets),
            IterFunctionData(self._s3_bucket_exposed_to_agw_methods, ctx.rest_api_gw, (ctx.s3_buckets,)),
        ]
        super().__init__(functions_pool)

    @staticmethod
    def _assume_role_policy_is_allowing_external_assume(policy: AssumeRolePolicy):
        policy.is_allowing_external_assume = is_policy_allowing_external_assume(policy)

    @staticmethod
    def _rds_instance_indirect_connection_data(rds_instance: RdsInstance):
        rds_instance.indirect_public_connection_data = get_allowing_indirect_public_access_on_ports(rds_instance, [rds_instance.port])

    @staticmethod
    def _redshift_indirect_connection_data(redshift: RedshiftCluster):
        redshift.indirect_public_connection_data = get_allowing_indirect_public_access_on_ports(redshift, [redshift.port])

    @staticmethod
    def _elastic_search_indirect_connection_data(elastic_search: ElasticSearchDomain):
        elastic_search.indirect_public_connection_data = get_allowing_indirect_public_access_on_ports(elastic_search, elastic_search.ports)

    @staticmethod
    def _neptune_instance_sg_allowing_public_access(neptune_instance: NeptuneInstance):
        neptune_instance.security_group_allowing_public_access = get_allowing_public_access_on_ports(neptune_instance, [neptune_instance.port])

    @staticmethod
    def _rds_instance_sg_allowing_public_access(rds_instance: RdsInstance):
        rds_instance.security_group_allowing_public_access = get_allowing_public_access_on_ports(rds_instance, [rds_instance.port])

    @staticmethod
    def _dms_sg_allowing_public_access(dms: DmsReplicationInstance):
        dms.security_group_allowing_public_access = get_allowing_public_access_portless(dms)

    @staticmethod
    def _eks_cluster_sg_allowing_public_access(eks_cluster: EksCluster):
        eks_cluster.security_group_allowing_public_access = get_allowing_public_access_on_ports(eks_cluster, [eks_cluster.port])

    @staticmethod
    def _redshift_sg_allowing_public_access(redshift: RedshiftCluster):
        redshift.security_group_allowing_public_access = get_allowing_public_access_on_ports(redshift, [redshift.port])

    @staticmethod
    def _s3_bucket_publicly_allowing_resources(s3_bucket: S3Bucket):
        evaluator: S3PublicAccessEvaluator = S3PublicAccessEvaluator(s3_bucket, True)
        results_map: Dict[AwsResource, PublicAccessResults] = evaluator.evaluate()
        for resource, results in results_map.items():
            if is_any_resource_based_action_allowed(PolicyEvaluation(resource_allowed_actions=results.allowed_actions,
                                                                     resource_denied_actions=results.denied_actions)):
                s3_bucket.publicly_allowing_resources.append(resource)

    @classmethod
    def _s3_bucket_exposed_to_agw_methods(cls, api_gateway: RestApiGw, s3_buckets: AliasesDict[S3Bucket]):
        for agw_method in api_gateway.agw_methods_with_valid_integrations_and_allowed_lambda_access:
            for resource_arn, evaluation_results in agw_method.integration.lambda_func_integration.iam_role.policy_evaluation_result_map.items():
                s3_bucket: S3Bucket = s3_buckets.get(resource_arn)
                if s3_bucket and \
                        cls._allows_access_to_buckets(evaluation_results,
                                                      agw_method.integration.lambda_func_integration.iam_role.permissions_policies):
                    s3_bucket.exposed_to_agw_methods.append(agw_method)

    @staticmethod
    def _allows_access_to_buckets(results: PolicyEvaluation, policies: List[Policy]):
        if is_action_subset_allowed(results, 's3:*'):
            for statement in [statement for policy in policies for statement in policy.statements]:
                if any(resource == '*' for resource in statement.resources) and \
                        any(action.startswith('s3:') or action == '*' for action in statement.actions):
                    return True
        return False
