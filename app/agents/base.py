from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseAgent(ABC, Generic[InputT, OutputT]):
    """Provider-neutral boundary for deterministic or future ADK agents."""

    provider = "local"

    @abstractmethod
    def run(self, value: InputT) -> OutputT: ...
