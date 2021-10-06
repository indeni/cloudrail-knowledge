import random
import time
import uuid
from time import sleep
from unittest import TestCase
from cloudrail.knowledge.context.parallel.process.async_queue_executor import AsyncQueueExecutor


class TestAsyncQueueExecutor(TestCase):

    ARGS_SIZE: int = 10

    def setUp(self) -> None:
        self.executor: AsyncQueueExecutor = AsyncQueueExecutor(self._get_uuid_with_delay, [(i, ) for i in range(0, self.ARGS_SIZE)])

    def test_get_results(self):
        start: float = time.time()
        self.executor.execute()
        self.assertGreaterEqual(10, (time.time()-start))
        self.assertEqual(len(self.executor.get_results()), 10)

    def test_empty_results(self):
        # pylint: disable=protected-access
        self.executor._function = self._get_throw_exception_with_delay
        self.executor.execute()
        self.assertEqual(len(self.executor.get_results()), 0)

    def test_one_worker_fails(self):
        # pylint: disable=protected-access
        self.executor._function = self._seven_boom
        self.executor.execute()
        res = self.executor.get_results()
        self.assertTrue(7 not in res)

    @staticmethod
    def _get_uuid_with_delay(num: int) -> list:
        sleep(random.uniform(0.1, 0.5))
        return [str(uuid.uuid4()) + '_' + str(num)]

    @staticmethod
    def _get_throw_exception_with_delay(num: int):
        sleep(random.uniform(0.1, 0.5))
        raise Exception(str(num) + '-Boom!')

    @staticmethod
    def _seven_boom(num: int):
        sleep(random.uniform(0.1, 0.5))
        if num == 7:
            raise Exception(str(num) + '-Boom!')
        return [num]
