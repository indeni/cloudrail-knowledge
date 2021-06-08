from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessElasticSearchRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'public_access_elasticsearch_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:

        issues: List[Issue] = [Issue(
            f"~Internet~. {es.get_type()}: `{es.get_friendly_name()}` is publicly accessible. "
            f"{es.get_type()} is currently not deployed within a VPC. ~ElasticSearch~", es, es)
                               for es in env_context.elastic_search_domains if es.is_public]
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.elastic_search_domains)
