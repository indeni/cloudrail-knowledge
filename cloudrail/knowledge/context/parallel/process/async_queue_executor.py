import logging
import multiprocessing
import time
from multiprocessing import Process, connection
from typing import Tuple, List, Dict

from cloudrail.knowledge.utils.log_utils import log_cloudrail_error


class AsyncQueueExecutor:

    def __init__(self,
                 function,
                 args: List,
                 extra_args: List = None) -> None:
        self._function = function
        self._args: List[Tuple] = args
        self._extra_args: List = extra_args or []
        self._results: list = []

    def execute(self) -> None:
        start_time: float = time.time()
        logging.info('about to execute task')
        self._multi_processes()
        logging.info(f'total executions of function \'{self._function.__name__}\'  completed in {(time.time() - start_time)}s')

    def get_results(self) -> list:
        return list(self._results)

    def _multi_processes(self) -> None:
        if len(self._args) == 1:
            self._run_in_main_process(self._args)
        else:
            self._run_in_multi_process(self._args)

    def _run_in_main_process(self, batch_args):
        for args in batch_args:
            try:
                res: list = self._function(args, *self._extra_args)
                self._results.extend(res)
            except Exception:
                logging.exception(f'fail running {self._function.__name__}')

    def _run_in_multi_process(self, batch_args_list):
        conn_to_process_map: Dict[Tuple[connection.Connection, connection.Connection], Process] = {}
        process_to_task_map: Dict[Process, str] = {}
        for args in batch_args_list:
            reader_conn, writer_conn = multiprocessing.Pipe(duplex=False)
            task: _AsyncTask = _AsyncTask(self._function, writer_conn, args, self._extra_args)
            proc: Process = Process(target=task.do_task)
            conn_to_process_map[(reader_conn, writer_conn)] = proc
            process_to_task_map[proc] = task.get_function_name()
            proc.start()
        self._wait_processes_until_timeout(conn_to_process_map, self._results, process_to_task_map)

        for conn_tuple in conn_to_process_map:
            reader_conn, writer_conn = conn_tuple
            try:
                writer_conn.close()
                self._results.extend(self._read_conn(reader_conn))
            finally:
                if not reader_conn.closed:
                    logging.info(f'about to close connection={str(reader_conn)}')
                    reader_conn.close()

    @staticmethod
    def _read_conn(conn: connection.Connection) -> list:
        try:
            if not conn.closed and conn.poll():
                return conn.recv()
        except (EOFError, OSError):
            logging.warning('failed reading bytes from connection={}'.format(str(conn)))
        finally:
            if not conn.closed:
                conn.close()
        return []

    def _wait_processes_until_timeout(self, conn_to_process_map, result, process_to_task_name_map):
        timeout: int = 60
        end_time: float = time.time() + timeout

        while any(process.is_alive() for process in conn_to_process_map.values()) and time.time() < end_time:
            for (reader_conn, _), process in conn_to_process_map.items():
                try:
                    if process.is_alive() and reader_conn.poll():
                        result.extend(reader_conn.recv())
                except Exception:
                    logging.exception('failed receive data')

        if time.time() >= end_time:
            logging.warning(f'got timeout for command {self._function.__name__}')
            for process in conn_to_process_map.values():
                if process.is_alive():
                    log_cloudrail_error(f'task="{process_to_task_name_map[process]}" not completed in {timeout}s', 'AsyncExecution')
                    process.kill()


class _AsyncTask:

    def __init__(self, function, child_conn: connection.Connection, args: List, extra_args: List) -> None:
        self._function = function
        self.child_conn: connection.Connection = child_conn
        self.args: List = args
        self.extra_args = extra_args

    def do_task(self) -> None:
        try:
            res: list = self._function(self.args, *self.extra_args)
            index = 0
            while index < len(res):
                self.child_conn.send(res[index:index + 100])
                index = index + 100
        except Exception:
            logging.exception(f'error running task for {self._function}')
        finally:
            self.child_conn.close()

    def get_function_name(self):
        return self._function.__name__
