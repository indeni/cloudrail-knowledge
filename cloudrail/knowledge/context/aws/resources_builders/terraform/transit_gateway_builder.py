from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_transit_gateway, \
    build_transit_gateway_route, build_transit_gateway_route_table, build_transit_gateway_attachments, \
    build_transit_gateway_route_table_association, build_transit_gateway_route_table_propagation
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class TransitGatewayBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_transit_gateway(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_TRANSIT_GATEWAY


class TransitGatewayRouteBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_transit_gateway_route(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE


class TransitGatewayRouteTableBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_transit_gateway_route_table(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE_TABLE


class TransitGatewayAttachmentBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_transit_gateway_attachments(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_TRANSIT_GATEWAY_ATTACHMENT


class TransitGatewayRouteTableAssociationBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_transit_gateway_route_table_association(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE_TABLE_ASSOCIATION


class TransitGatewayRouteTablePropagationBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_transit_gateway_route_table_propagation(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE_TABLE_PROPAGATION
