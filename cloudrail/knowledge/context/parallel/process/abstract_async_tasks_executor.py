import logging
import math
import multiprocessing
import time
from abc import abstractmethod
from typing import List

from cloudrail.knowledge.context.parallel.process.async_queue_executor import AsyncQueueExecutor


class AbstractAsyncTasksExecutor:

    def __init__(self, function, workers_count: int = multiprocessing.cpu_count(),
                 batch_size: int = 0) -> None:
        self._function = function
        self.args: List = []
        self.extra_args: List = []
        self.args_batch_list: List[List] = []
        self.workers_count: int = workers_count
        self._batch_size: int = batch_size

    @abstractmethod
    def init_args(self) -> None:
        pass

    @abstractmethod
    def handle_results(self, results: list) -> None:
        pass

    def execute(self) -> None:
        start_time: float = time.time()
        self.init_args()
        self._split_args_to_batch()
        if self.args_batch_list:
            logging.info('executing parallel action with {} workers'.format(self.workers_count))
            results: list
            async_exec: AsyncQueueExecutor = AsyncQueueExecutor(function=self._function,
                                                                args=self.args_batch_list,
                                                                extra_args=self.extra_args)
            async_exec.execute()
            results = async_exec.get_results()
            self.handle_results(results)
            logging.info(f'task \'{self.__class__.__name__}\'  executed in {(time.time() - start_time)}s')

    def _split_args_to_batch(self) -> None:
        args_size: int = len(self.args)
        if self._batch_size == 0:
            self._batch_size = math.ceil(args_size / self.workers_count) if args_size > self.workers_count else args_size
        start_batch: int = 0
        end_batch: int = self._batch_size
        remaining_items: int = args_size

        while remaining_items > 0:
            self.args_batch_list.append(self.args[start_batch:end_batch])
            remaining_items = args_size - (start_batch + self._batch_size)
            start_batch += self._batch_size
            end_batch += self._batch_size if remaining_items > self._batch_size else args_size - start_batch
        self.args.clear()
