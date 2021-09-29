from cloudrail.knowledge.context.aws.resources.ec2.availability_zone import AvailabilityZone
from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder


class Ec2AvailabilityZonesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-availability-zones.json'

    def get_section_name(self) -> str:
        return 'AvailabilityZones'

    def do_build(self, attributes: dict) -> AvailabilityZone:
        return AvailabilityZone(account=attributes['Account'], region=attributes['Region'],
                                zone_id=attributes['ZoneId'], zone_name=attributes['ZoneName'])
