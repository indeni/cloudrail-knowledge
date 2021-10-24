from typing import List
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_association import NetworkAclAssociation
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.utils.string_utils import generate_random_string


class NetworkAclAssociationBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        acl_assoc_list: List[NetworkAclAssociation] = []
        network_acl_id = attributes['id']
        for subnet_id in attributes['subnet_ids']:
            network_acl_assoc_id = 'pseudo-naclassoc-' + generate_random_string()
            acl_assoc_list.append(NetworkAclAssociation(network_acl_id, subnet_id, network_acl_assoc_id,
                                                        attributes['region'], attributes['account_id']))
        return acl_assoc_list

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_NETWORK_ACL
