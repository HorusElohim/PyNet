from threading import Thread
from typing import Any, List
from time import sleep


class Worker(Thread):
    pass


class WorkerRunner:
    @staticmethod
    def run(workers: List[Worker]):
        for worker in workers:
            worker.start()
            sleep(0.1)
        for worker in workers:
            worker.join()
