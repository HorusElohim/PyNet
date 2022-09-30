from .core import Card, Status, StatusEnum
from .worker import Worker, WorkerData

SUCCESS_STR = "🟢"
FAILED_STR = "🔴"


def status_str(x: bool):
    return SUCCESS_STR if x else FAILED_STR
