from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_ec2_instance
from cloudrail.knowledge.utils.tags_utils import get_aws_tags


class Ec2Builder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-instances.json'

    def get_section_name(self) -> str:
        return 'Reservations'

    def do_build(self, attributes: dict):
        results = []
        for instance in attributes['Instances']:
            instance['Account'] = attributes['Account']
            instance['Region'] = attributes['Region']
            instance['salt'] = attributes['salt']
            ec2 = build_ec2_instance(instance)
            if ec2:
                ec2.tags = get_aws_tags(instance) or get_aws_tags(instance.get('Value') or {})
                results.append(ec2)
        return results
