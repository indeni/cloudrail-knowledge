from typing import List
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_association import NetworkAclAssociation
from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder


class NetworkAclAssociationBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-network-acls.json'

    def get_section_name(self) -> str:
        return 'NetworkAcls'

    def do_build(self, attributes: dict):
        acl_assoc_list: List[NetworkAclAssociation] = []
        for assoc in attributes['Associations']:
            network_acl_assoc_id = assoc['NetworkAclAssociationId']
            network_acl_id = assoc['NetworkAclId']
            subnet_id = assoc['SubnetId']
            acl_assoc_list.append(NetworkAclAssociation(network_acl_id, subnet_id, network_acl_assoc_id, attributes['Region'], attributes['Account']))
        return acl_assoc_list
