from typing import Dict

from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata


def get_before_raw_resources_by_type(raw_data, resources_metadata: Dict[str, IacResourceMetadata]):
    resources = {}
    for resource in raw_data:
        if resource['mode'] != 'managed':
            continue

        resource_type = resource['type']
        if resource_type not in resources:
            resources[resource_type] = []
        address = resource['address'].replace('"', '')
        before_att = resource['change']['before']
        if not before_att:
            continue
        before_att['tf_address'] = address
        metadata = resources_metadata.get(address.split('[')[0])
        attributes = before_att
        actions = resource['change']['actions']
        if len(actions) == 1:
            if actions[0] == IacActionType.CREATE.value:
                attributes['tf_action'] = IacActionType.DELETE
            if actions[0] in (IacActionType.NO_OP.value, IacActionType.UPDATE.value,
                              IacActionType.READ.value, IacActionType.DELETE):
                attributes['tf_action'] = IacActionType.NO_OP
        if len(actions) == 2:
            attributes['tf_action'] = IacActionType.NO_OP
        attributes['cloudrail_resource_metadata'] = metadata
        attributes['is_new'] = False
        resources[resource_type].append(attributes)

    return resources


def get_after_raw_resources_by_type(raw_data,
                                    resources_metadata: Dict[str, IacResourceMetadata],
                                    keep_deleted_entities=True):
    resources = {}
    for resource in raw_data:
        if resource['mode'] != 'managed':
            continue

        resource_type = resource['type']
        if resource_type not in resources:
            resources[resource_type] = []
        address = resource['address'].replace('"', '')
        before_att = resource['change']['before']
        after_att = resource['change']['after']
        if before_att:
            before_att['tf_address'] = address
        if after_att is not None:
            if after_unknown := resource['change'].get('after_unknown'):
                for key in after_unknown:
                    full_address = '{}.{}'.format(address, key)
                    after_att[key] = after_att.get(key, full_address)
                    assign_inner_addresses(full_address, after_att[key], after_unknown[key])
            after_att['tf_address'] = address

        metadata = resources_metadata.get(address.split('[')[0])
        if len(resource['change']['actions']) == 1 \
                and resource['change']['actions'][0] != IacActionType.UPDATE.value:
            attributes = after_att or before_att
            attributes['tf_action'] = resource['change']['actions'][0]
            attributes['cloudrail_resource_metadata'] = metadata
            attributes['is_new'] = attributes['tf_action'] == IacActionType.CREATE
            resources[resource_type].append(attributes)

        if len(resource['change']['actions']) == 2 \
                or resource['change']['actions'][0] == IacActionType.UPDATE.value:
            if keep_deleted_entities:
                before_att['tf_action'] = IacActionType.DELETE.value
                before_att['cloudrail_resource_metadata'] = metadata
                before_att['is_new'] = False
                resources[resource_type].append(before_att)
            after_att['tf_action'] = IacActionType.CREATE.value
            after_att['cloudrail_resource_metadata'] = metadata
            after_att['is_new'] = len(resource['change']['actions']) == 2
            resources[resource_type].append(after_att)

    return resources


def assign_inner_addresses(full_address: str, after_attribute, unknowns_map):
    if not (isinstance(after_attribute, list) and len(after_attribute) == 1 and \
            isinstance(unknowns_map, list) and len(unknowns_map) == 1):
        return
    after_item = after_attribute[0]
    unknown_item = unknowns_map[0]
    if not isinstance(unknown_item, dict):
        return
    for key, value in unknown_item.items():
        new_path = f'{full_address}.{key}'
        if isinstance(value, list) and len(value) == 1:
            val_item = value[0]
            if isinstance(val_item, dict):
                assign_inner_addresses(new_path, after_item[key], value)

        if value is True:
            after_item[key] = new_path

    after_item['tf_address'] = full_address


def get_raw_resources_by_type(raw_data,
                              resources_metadata: Dict[str, IacResourceMetadata],
                              use_after_data=True,
                              keep_deleted_entities=True):
    if use_after_data:
        return get_after_raw_resources_by_type(raw_data, resources_metadata, keep_deleted_entities)
    else:
        return get_before_raw_resources_by_type(raw_data, resources_metadata)
