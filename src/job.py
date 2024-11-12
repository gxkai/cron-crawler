from abc import ABC, abstractmethod
from typing import Any


class AbstractJob(ABC):
    name = "Abstract Job"
    _report = ""
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def success(self, payload: Any):
        raise NotImplementedError

    @abstractmethod
    def fail(self, payload: Any):
        raise NotImplementedError

    def report(self, payload: str):
        AbstractJob._report += f"\n{'='*50}\n"
        AbstractJob._report += payload