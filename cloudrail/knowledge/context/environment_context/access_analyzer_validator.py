import functools
import logging
from concurrent.futures.thread import ThreadPoolExecutor

import backoff
import boto3

from cloudrail.knowledge.context.aws.resources.iam.policy import Policy, PolicyType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class AccessAnalyzerValidator:
    @staticmethod
    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def get_boto_client():
        return boto3.client('accessanalyzer')

    def __init__(self, context: AwsEnvironmentContext, client=None):
        self.context = context
        self.client = client or self.get_boto_client()
        self.max_workers = 20

    def validate_policies(self):
        try:
            policies = self.context.get_iac_managed_policies()
            logging.info(f'validating {len(policies)} policies using AccessAnalyzerValidator')
            tasks = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                for policy in policies:
                    tasks.append(executor.submit(self._run_validate, policy))

            for execution in tasks:
                execution.result()
        except Exception:
            logging.exception('Error while validating policies using AccessAnalyzerValidator')
        finally:
            self._run_validation.cache_clear()

    @functools.lru_cache(maxsize=None)
    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def _run_validation(self, policy_doc: str, policy_type: PolicyType) -> dict:
        return self.client.validate_policy(
            policyDocument=policy_doc,
            policyType=policy_type
        )

    def _run_validate(self, policy: Policy):
        if not policy.raw_document:
            return
        for statement in policy.statements:
            for resource in statement.resources:
                if not resource.lower().startswith('arn') and not resource.lower().startswith('*'):
                    return
        response = self._run_validation(policy.raw_document, policy.policy_type)
        status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status_code != 200:
            raise Exception(f'Got status code {status_code} while validating policy {policy.raw_document}')
        policy.access_analyzer_findings = response.get('findings', [])
