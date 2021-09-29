from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_rest_api_gw, build_api_gateway_method_settings, build_rest_api_gw_policy, build_rest_api_gw_mapping, \
    build_rest_api_gw_domain, build_api_gateway_method, build_api_gateway_integration, build_api_gateway_stage


class ApiGatewayMethodSettingsBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-stages/*'

    def get_section_name(self) -> str:
        return 'item'

    def do_build(self, attributes: dict):
        return build_api_gateway_method_settings(attributes)


class RestApiGwBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-rest-apis.json'

    def get_section_name(self) -> str:
        return 'items'

    def do_build(self, attributes: dict):
        return build_rest_api_gw(attributes)


class RestApiGwPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-rest-apis.json'

    def get_section_name(self) -> str:
        return 'items'

    def do_build(self, attributes: dict):
        return build_rest_api_gw_policy(attributes)


class RestApiGwMappingBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-base-path-mappings/*'

    def get_section_name(self) -> str:
        return 'items'

    def do_build(self, attributes: dict):
        return build_rest_api_gw_mapping(attributes)


class RestApiGwDomainBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-domain-names.json'

    def get_section_name(self) -> str:
        return 'items'

    def do_build(self, attributes: dict):
        return build_rest_api_gw_domain(attributes)


class ApiGatewayMethodBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-method/*'

    def get_section_name(self) -> str:
        return None

    def do_build(self, attributes: dict):
        return build_api_gateway_method(attributes)


class ApiGatewayIntegrationBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-method/*'

    def get_section_name(self) -> str:
        return None

    def do_build(self, attributes: dict):
        request_http_method = attributes['Value']['httpMethod']
        attributes['request_http_method'] = request_http_method
        return build_api_gateway_integration(attributes)


class ApiGatewayStageBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigateway-get-stages/*'

    def get_section_name(self) -> str:
        return 'item'

    def do_build(self, attributes: dict):
        return build_api_gateway_stage(attributes)
