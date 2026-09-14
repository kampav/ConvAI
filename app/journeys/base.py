from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from app.models.schemas import JourneyDescriptor
@dataclass
class JourneyResult:
    text: str
    action: bool = False
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None
    risk_level: str = "personal"
class BaseJourney(ABC):
    descriptor: JourneyDescriptor
    @abstractmethod
    async def handle(self, message: str, context: dict[str, Any]) -> JourneyResult:
        raise NotImplementedError
