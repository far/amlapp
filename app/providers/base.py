from abc import ABC, abstractmethod


class AMLProvider(ABC):
    @abstractmethod
    async def get_aml_data(self, post_data: dict) -> dict:
        pass
