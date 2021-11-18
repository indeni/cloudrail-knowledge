import copy
import logging
from typing import List, Union
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.utils.utils import hash_list
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.utils.utils import is_first_octet_in_range, PUBLIC_IP_MAX_FIRST_OCTET, PUBLIC_IP_MIN_FIRST_OCTET
from cloudrail.knowledge.utils.log_utils import log_cloudrail_error


class EnvironmentContextMerger:

    @staticmethod
    def _merge_components(attr: str, olds: Union[List[Mergeable], AliasesDict[Mergeable], dict],
                          news: Union[List[Mergeable], AliasesDict[Mergeable], dict]):
        logging.info('merging the attribute: {}'.format(attr))
        if isinstance(olds, list):
            identity_func = lambda x: x
            add_func = list.append
            remove_func = list.remove
            iterable = identity_func
            mergeable = identity_func
        elif isinstance(olds, dict):
            add_func = lambda x, y: x.update({y[0]: y[1]})
            remove_func = lambda items, item: items.pop(item[0])
            iterable = dict.items
            mergeable = lambda tpl: tpl[1]
        elif isinstance(olds, AliasesDict):
            add_func = AliasesDict.update
            remove_func = lambda items, item: items.pop(list(item.aliases)[0])
            iterable = AliasesDict.values
            mergeable = lambda x: x
        else:
            raise NotImplementedError(f"Merging components of type {type(olds).__name__} is not supported")

        if new := next((x for x in iterable(news)), None):
            if mergeable(new).get_keys() is None:
                logging.warning(f'An entity of type {type(new).__name__} did not implement "get_keys" method and therefore all new entities '
                                f'will overwrite old entities')

        entities_to_add = []

        for new in iterable(news):
            state = mergeable(new).iac_state
            if state:
                if state.action == IacActionType.CREATE:
                    old = next((old for old in iterable(olds) if hash_list(mergeable(old).get_keys()) == hash_list(mergeable(new).get_keys())), None)
                    if old:
                        logging.warning('remove unneeded old components the att: {}:{}'.format(attr, mergeable(new).get_keys()))
                        remove_func(olds, old)
                    logging.info('adding new components the att: {}:{}'.format(attr, mergeable(new).get_keys()))
                    entities_to_add.append(new)
                elif state.action == IacActionType.DELETE:
                    old = next((old for old in iterable(olds) if hash_list(mergeable(old).get_keys()) == hash_list(mergeable(new).get_keys())), None)
                    if old:
                        remove_func(olds, old)
                        logging.info('removing components the att: {}:{}'.format(attr, mergeable(new).get_keys()))
                    else:
                        logging.warning('failed removing components the att: {}:{}'.format(attr, mergeable(new).get_keys()))
                elif state.action == IacActionType.NO_OP or state.action == IacActionType.READ:
                    old = next((old for old in iterable(olds) if hash_list(mergeable(old).get_keys()) == hash_list(mergeable(new).get_keys())), None)
                    if old:
                        remove_func(olds, old)
                    else:
                        logging.warning('failed finding components the att: {}:{}'.format(attr, mergeable(new).get_keys()))
                    entities_to_add.append(new)
                elif state.action == IacActionType.UPDATE:
                    old = next((old for old in iterable(olds) if hash_list(mergeable(old).get_keys()) == hash_list(mergeable(new).get_keys())), None)
                    if old:
                        EnvironmentContextMerger._update_object_properties(new, old)
                        remove_func(olds, old)
                    entities_to_add.append(new)

        for entity in entities_to_add:
            add_func(olds, entity)

    @staticmethod
    def merge(cm_ctx: BaseEnvironmentContext, tf_ctx: BaseEnvironmentContext):
        old_ctx = copy.deepcopy(cm_ctx)
        new_ctx = tf_ctx
        for attr in dir(cm_ctx):
            try:
                if not callable(getattr(cm_ctx, attr)) and not attr.startswith('_'):
                    logging.info(f'starting merging entity {attr}')
                    old_values = getattr(old_ctx, attr)
                    new_values = getattr(new_ctx, attr)
                    values = old_values or new_values
                    if not values:
                        continue
                    if isinstance(values, list):
                        values_class = values[0].__class__
                        if issubclass(values_class, Mergeable):
                            EnvironmentContextMerger._merge_components(attr, old_values, new_values)
                    if isinstance(values, dict):
                        values_class = list(values.values())[0].__class__
                        if issubclass(values_class, Mergeable):
                            EnvironmentContextMerger._merge_components(attr, old_values, new_values)
                        else:
                            old_values.update({k: v for k, v in new_values.items() if v})
                    if isinstance(values, AliasesDict):
                        EnvironmentContextMerger._merge_components(attr, old_values, new_values)
            except Exception as ex:
                message = f'failed merging entity {attr}'
                log_cloudrail_error(message, type(ex).__name__)
                logging.exception(message)
        old_ctx.unknown_blocks = new_ctx.unknown_blocks
        old_ctx.managed_resources_summary = new_ctx.managed_resources_summary
        return old_ctx

    @staticmethod
    def _update_object_properties(src_obj, target_obj):
        for attr in dir(src_obj):
            if '__' not in attr:
                src_val = getattr(src_obj, attr)
                if src_val is None or (isinstance(src_val, str) and 'cfn-pseudo' in src_val) \
                    or is_first_octet_in_range(src_val, (PUBLIC_IP_MIN_FIRST_OCTET, PUBLIC_IP_MAX_FIRST_OCTET)) \
                        or src_val == ['cfn-pseudo']:
                    target_val = getattr(target_obj, attr)
                    setattr(src_obj, attr, target_val)
