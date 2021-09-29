import json


class TerraformOutputFormatException(Exception):
    pass


class TerraformOutputValidator:

    @staticmethod
    def validate(data: str):
        terraform_output = json.loads(data)
        if terraform_output.get('resource_changes') is None:
            raise TerraformOutputFormatException('terraform output missing mandatory field: resource_changes')
        if terraform_output.get('configuration') is None:
            raise TerraformOutputFormatException('terraform output missing mandatory field: configuration')
        if terraform_output.get('configuration').get('root_module') is None:
            raise TerraformOutputFormatException('terraform output missing mandatory field: root_module')
