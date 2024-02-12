from abc import ABC, abstractmethod
from typing import AsyncGenerator


class DataReader(ABC):
    @abstractmethod
    async def read_data(self) -> AsyncGenerator[dict, None]:
        """
        Abstract method to be implemented by subclasses for reading data.
        This method is an async generator.
        """
        pass
