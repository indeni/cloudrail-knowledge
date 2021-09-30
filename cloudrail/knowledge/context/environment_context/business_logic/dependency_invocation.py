import logging
import time

from queue import Queue
from typing import Tuple, List, Callable, Dict, Union, Optional
from cloudrail.knowledge.exceptions import ContextEnrichmentException, ResourceDependencyNotFoundException
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.utils.log_utils import log_cloudrail_error


class FunctionData:
    def __init__(self, function: Callable, args: Tuple = (), dependencies: Optional[List[Callable]] = None):
        self.function = function
        self.args = args
        self.dependencies = dependencies or []


class IterFunctionData(FunctionData):
    def __init__(self,
                 function: Callable,
                 iter_args: Union[list, dict, AliasesDict],
                 args: Tuple = (),
                 dependencies: Optional[List[Callable]] = None):
        super().__init__(function, args, dependencies)
        self.iter_args = iter_args


class CircularDependencyException(Exception):
    pass


class DependencyInvocation:
    def __init__(self, *function_pools: List[FunctionData], context: Optional[BaseEnvironmentContext] = None):
        for function_pool in function_pools:
            self._assert_no_circular_dependency(function_pool)
            function_pool.sort(key=lambda x: len(x.dependencies))

        self.function_pools: Tuple[List[FunctionData]] = function_pools
        self.context: BaseEnvironmentContext = context

    def _execute_function(self, function_data: FunctionData):
        start_time = time.time()
        description = function_data.function.__name__.replace('_', ' ')
        logging.info('starting {}'.format(description))
        if isinstance(function_data, IterFunctionData):
            entities = function_data.iter_args
            new_invalidated_entities = []

            for entity in [entity for entity in entities if not entity.invalidation]:
                try:
                    function_data.function(entity, *function_data.args)
                except ResourceDependencyNotFoundException:
                    new_invalidated_entities.append(entity)
                except Exception as ex:
                    entity.add_invalidation('An error occcured. Check logs for more information.')
                    new_invalidated_entities.append(entity)
                    self._report_error(ContextEnrichmentException(description, entity).with_traceback(ex.__traceback__))

            if self.context:
                for invalid_entity in new_invalidated_entities:
                    entities.remove(invalid_entity)
                    self.context.invalidated_resources.add(invalid_entity)
        else:
            try:
                function_data.function(*function_data.args)
            except Exception as ex:
                self._report_error(ContextEnrichmentException(description).with_traceback(ex.__traceback__))
        logging.info(f'finished {description} in {(time.time() - start_time)}s')

    def run(self) -> None:
        for function_pool in self.function_pools:
            queue: Queue = Queue()
            for function in function_pool:
                queue.put(function)
            self._run(queue)

    def _run(self, queue: Queue):
        functions_called = []
        while not queue.empty():
            function_data = queue.get()
            if all((dependency in functions_called) for dependency in function_data.dependencies):
                self._execute_function(function_data)
                functions_called.append(function_data.function)
            else:
                queue.put(function_data)

    def _assert_no_circular_dependency(self, function_pool: List[FunctionData]) -> None:
        function_pool_dict = {function_data.function: function_data.dependencies for function_data in function_pool}
        for function_data in function_pool:
            self._check_dependency(function_data.function, function_data.function, function_pool_dict, [])

    def _check_dependency(self, current: Callable, origin: Callable, function_pool_dict: Dict[Callable, List[Callable]], breadcrumbs: List[Callable]):
        dependencies = function_pool_dict[current]
        for dependency in dependencies:
            if origin is dependency:
                raise CircularDependencyException(
                    f"Circular dependency detected. Breadcrumbs: {' -> '.join([func.__name__ for func in breadcrumbs + [origin]])}")

            self._check_dependency(dependency, origin, function_pool_dict, breadcrumbs + [current])

    @staticmethod
    def _report_error(ex: ContextEnrichmentException):
        log_cloudrail_error(ex.message, type(ex).__name__)
        logging.exception(ex.message, exc_info=ex)
