import logging

class UnsupportedCloudProviderException(Exception):
    def __init__(self, cloud_provider=None):
        if cloud_provider:
            super().__init__(f'Cloud provider {cloud_provider} is not supported')
        else:
            super().__init__()


class UnsupportedIacTypeException(Exception):
    def __init__(self, iac_type=None):
        if iac_type:
            super().__init__(f'Iac type {iac_type} is not supported')
        else:
            super().__init__()

class TerraformApplyExpectedToFail(Exception):
    pass


class ResourceDependencyNotFoundException(Exception):
    pass


class UnsupportedResourceCollectionTypeException(Exception):
    pass


class UnknownResultOfTerraformApply(Exception):
    pass

class ValidationException(Exception):
    pass

class ContextEnrichmentException(Exception):
    def __init__(self, description: str, entity=None):
        self.entity = entity
        self.description = description
        super().__init__()

    @property
    def message(self):
        failed_phase = self.description
        entity_type = ''
        entity_name = ''
        extra_data_text = ''
        if self.entity:
            entity_type = 'component type: {}'.format(self.entity.get_type())
            entity_name = 'component name: {}'.format(self.entity.get_friendly_name())
            try:
                extra_data = self.entity.get_extra_data()
                extra_data_text = 'extra_data: {}'.format(extra_data) if extra_data else ''
            except Exception as ex:
                logging.warning('failed getting extra data {}'.format(ex), exc_info=1)
        entity_info = '\n'.join([entity_type, entity_name, extra_data_text]).strip()
        return 'failed while enriching component data.\nfailed_phase: {}\n{}'.format(failed_phase, entity_info)

    def __str__(self):
        return self.message
