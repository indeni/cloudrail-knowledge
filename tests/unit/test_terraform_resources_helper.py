import copy
import unittest

from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.environment_context.terraform_resources_helper import get_before_raw_resources_by_type, \
    get_after_raw_resources_by_type


class TestTerraformResourceHelper(unittest.TestCase):
    vpc = {'address': 'aws_default_vpc.default',
           'mode': 'managed',
           'type': 'aws_default_vpc',
           'name': 'default',
           'provider_name': 'registry.terraform.io/hashicorp/aws',
           'change': {'actions': ['no-op'],
                      'before': {'arn': 'arn:aws:ec2:us-east-1:111111111111:vpc/vpc-bd9b60c0',
                                 'cidr_block': '172.31.0.0/16',
                                 'default_network_acl_id': 'acl-4756743a',
                                 'default_route_table_id': 'rtb-e24c0a9c',
                                 'default_security_group_id': 'sg-37970008',
                                 'dhcp_options_id': 'dopt-3045214a',
                                 'id': 'vpc-bd9b60c0',
                                 'owner_id': '111111111111',
                                 'tags': {'Name': 'default-vpc'},
                                 'tags_all': {'Name': 'default-vpc'}},
                      'after': {'arn': 'arn:aws:ec2:us-east-1:111111111111:vpc/vpc-bd9b60c0',
                                'cidr_block': '172.31.0.0/16',
                                'default_network_acl_id': 'acl-4756743a',
                                'default_route_table_id': 'rtb-e24c0a9c',
                                'default_security_group_id': 'sg-37970008',
                                'id': 'vpc-bd9b60c0',
                                'owner_id': '111111111111',
                                'tags': {'Name': 'default-vpc'},
                                'tags_all': {'Name': 'default-vpc'}},
                      'after_unknown': {},
                      'before_sensitive': {'tags': {}, 'tags_all': {}},
                      'after_sensitive': {'tags': {}, 'tags_all': {}}}}

    cloudfront = {
            "address": "module.all.module.cf.aws_cloudfront_distribution.main",
            "type": "aws_cloudfront_distribution",
            "name": "main",
            "mode": "managed",
            "provider_name": "registry.terraform.io/hashicorp/aws",
            "change": {
                "before": None,
                "after": {
                    "default_cache_behavior": [
                        {
                            "allowed_methods": [
                                "DELETE",
                                "GET",
                                "HEAD",
                                "OPTIONS",
                                "PATCH",
                                "POST",
                                "PUT"
                            ],
                            "cache_policy_id": None,
                            "cached_methods": [
                                "GET",
                                "HEAD"
                            ],
                            "compress": None,
                            "default_ttl": 3600,
                            "field_level_encryption_id": None,
                            "forwarded_values": [
                                {
                                    "cookies": [
                                        {
                                            "forward": "none",
                                            "whitelisted_names": None
                                        }
                                    ],
                                    "headers": None,
                                    "query_string": False,
                                    "query_string_cache_keys": None
                                }
                            ],
                            "function_association": [],
                            "lambda_function_association": [
                                {
                                    "event_type": "origin-response",
                                    "include_body": False,
                                    "lambda_arn": "module.all.module.cf.aws_lambda_function.lambda_edge_headers.qualified_arn"
                                }
                            ],
                            "max_ttl": 86400,
                            "min_ttl": 0,
                            "origin_request_policy_id": None,
                            "realtime_log_config_arn": None,
                            "smooth_streaming": None,
                            "trusted_key_groups": None,
                            "trusted_signers": None,
                            "viewer_protocol_policy": "redirect-to-https"
                        }
                    ],
                },
                "after_unknown": {
                    "default_cache_behavior": [
                        {
                            "allowed_methods": [
                                False,
                                False,
                                False,
                                False,
                                False,
                                False,
                                False
                            ],
                            "cached_methods": [
                                False,
                                False
                            ],
                            "forwarded_values": [
                                {
                                    "cookies": [
                                        {
                                            "forward": True
                                        }
                                    ]
                                }
                            ],
                            "function_association": [],
                            "lambda_function_association": [
                                {}
                            ],
                            "target_origin_id": True
                        }
                    ],
                },
                "actions": [
                    "create"
                ]
            }
        }

    def test_get_before_when_no_op(self):
        raw_data = copy.deepcopy(self.vpc)

        result = get_before_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], False)
        self.assertEqual(vpc_result['tf_action'], IacActionType.NO_OP)
        for key in raw_data['change']['before'].keys():
            self.assertEqual(raw_data['change']['before'][key], vpc_result[key])

    def test_get_before_when_create(self):
        raw_data = copy.deepcopy(self.vpc)
        raw_data['change']['actions'] = [IacActionType.CREATE.value]

        result = get_before_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], False)
        self.assertEqual(vpc_result['tf_action'], IacActionType.DELETE)
        for key in raw_data['change']['before'].keys():
            self.assertEqual(raw_data['change']['before'][key], vpc_result[key])

    def test_get_before_when_update(self):
        raw_data = copy.deepcopy(self.vpc)
        raw_data['change']['actions'] = [IacActionType.UPDATE.value]

        result = get_before_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], False)
        self.assertEqual(vpc_result['tf_action'], IacActionType.NO_OP)
        for key in raw_data['change']['before'].keys():
            self.assertEqual(raw_data['change']['before'][key], vpc_result[key])

    def test_get_before_when_create_delete(self):
        raw_data = copy.deepcopy(self.vpc)
        raw_data['change']['actions'] = [IacActionType.CREATE.value, IacActionType.DELETE.value]

        result = get_before_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], False)
        self.assertEqual(vpc_result['tf_action'], IacActionType.NO_OP)
        for key in raw_data['change']['before'].keys():
            self.assertEqual(raw_data['change']['before'][key], vpc_result[key])

    def test_get_after_when_no_op(self):
        raw_data = copy.deepcopy(self.vpc)

        result = get_after_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], False)
        self.assertEqual(vpc_result['tf_action'], IacActionType.NO_OP)
        for key in raw_data['change']['after'].keys():
            self.assertEqual(raw_data['change']['after'][key], vpc_result[key])

    def test_get_after_when_create(self):
        raw_data = copy.deepcopy(self.vpc)
        raw_data['change']['actions'] = [IacActionType.CREATE.value]

        result = get_after_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], True)
        self.assertEqual(vpc_result['tf_action'], IacActionType.CREATE)
        for key in raw_data['change']['after'].keys():
            self.assertEqual(raw_data['change']['after'][key], vpc_result[key])

    def test_get_after_when_update(self):
        raw_data = copy.deepcopy(self.vpc)
        raw_data['change']['actions'] = [IacActionType.UPDATE.value]

        result = get_after_raw_resources_by_type([raw_data], {})
        vpc_result_before = next(res for res in result['aws_default_vpc'] if res['tf_action'] == IacActionType.DELETE)
        vpc_result_after = next(res for res in result['aws_default_vpc'] if res['tf_action'] == IacActionType.CREATE)

        self.assertIsNotNone(vpc_result_before)
        self.assertIsNotNone(vpc_result_after)
        self.assertEqual(vpc_result_before['is_new'], False)
        self.assertEqual(vpc_result_after['is_new'], False)
        for key in raw_data['change']['after'].keys():
            self.assertEqual(raw_data['change']['after'][key], vpc_result_after[key])

    def test_get_after_when_create_delete(self):
        raw_data = copy.deepcopy(self.vpc)
        raw_data['change']['actions'] = [IacActionType.CREATE.value, IacActionType.DELETE.value]

        result = get_after_raw_resources_by_type([raw_data], {})
        vpc_result = result['aws_default_vpc'][0]

        self.assertEqual(vpc_result['is_new'], False)
        self.assertEqual(vpc_result['tf_action'], IacActionType.DELETE)
        for key in [key for key in raw_data['change']['after'].keys() if key not in ['tf_action', 'is_new']]:
            self.assertEqual(raw_data['change']['after'][key], vpc_result[key])

    def test_inner_unknowns(self):
        raw_data = copy.deepcopy(self.cloudfront)
        raw_data['change']['actions'] = [IacActionType.CREATE.value]

        result = get_after_raw_resources_by_type([raw_data], {})
        cloudfrontt = result['aws_cloudfront_distribution'][0]

        self.assertEqual(cloudfrontt['default_cache_behavior'][0]['forwarded_values'][0]['cookies'][0]['forward'],
                         'module.all.module.cf.aws_cloudfront_distribution.main.default_cache_behavior.forwarded_values.cookies.forward')
        self.assertEqual(cloudfrontt['default_cache_behavior'][0]['target_origin_id'],
                         'module.all.module.cf.aws_cloudfront_distribution.main.default_cache_behavior.target_origin_id')
