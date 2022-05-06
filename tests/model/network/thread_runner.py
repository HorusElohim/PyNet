import abc
from threading import Thread
from typing import Any, List


class Worker(Thread):
    pass


class WorkerRunner:
    @staticmethod
    def run(workers: List[Worker]):
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
