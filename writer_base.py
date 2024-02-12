from abc import ABC, abstractmethod


class DataWriter(ABC):
    @abstractmethod
    async def write_data(self, data: str):
        """
        Abstract method to be implemented by subclasses for writing data.
        """
        pass
