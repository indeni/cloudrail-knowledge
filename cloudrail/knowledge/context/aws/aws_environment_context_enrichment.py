import logging

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from cloudrail.knowledge.context.aws.aws_connection_builder import AwsConnectionBuilder
from cloudrail.knowledge.context.aws.aws_relations_assigner import AwsRelationsAssigner
from cloudrail.knowledge.context.aws.aws_resource_enrichment import AwsResourceEnrichment
from cloudrail.knowledge.context.environment_context.access_analyzer_validator import AccessAnalyzerValidator
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.environment_context.ec2_instance_types_enrichment import Ec2sInstanceTypesEnrichment
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment


class AwsEnvironmentContextEnrichment(EnvironmentContextEnrichment):

    @staticmethod
    def enrich(environment_context: AwsEnvironmentContext,
               **extra_args) -> AwsEnvironmentContext:
        ignore_exceptions: bool = bool(extra_args.get('ignore_exceptions')) if 'ignore_exceptions' in extra_args else False
        run_enrichment_requiring_aws: bool = bool(extra_args.get('run_enrichment_requiring_aws')) \
            if 'run_enrichment_requiring_aws' in extra_args else True
        try:
            AwsRelationsAssigner(environment_context).run()
            environment_context.clear_cache()
            # This flag is used to skip redundant logic when running drift detection
            if run_enrichment_requiring_aws:
                ResourceInvalidator(environment_context).remove_invalid_resources()
                AwsConnectionBuilder(environment_context).run()
                AwsResourceEnrichment(environment_context).run()
                AccessAnalyzerValidator(environment_context).validate_policies()
                Ec2sInstanceTypesEnrichment(environment_context).run()
            return environment_context
        except Exception as ex:
            if ignore_exceptions:
                logging.warning(f'got exception but running with ignore_exceptions=True. exception was: {ex}')
                return environment_context
            else:
                raise ex
