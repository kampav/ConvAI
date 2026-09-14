from app.journeys.base import BaseJourney, JourneyResult
from app.models.schemas import Capability, JourneyDescriptor, RiskLevel
class CardsJourney(BaseJourney):
    descriptor = JourneyDescriptor(journey_id="cards", version="1.0.0", owner="domain.cards", description="Card information and servicing.", capabilities=[Capability(name="status", description="View cards and status.", risk_level=RiskLevel.PERSONAL)])
    async def handle(self, message: str, context: dict) -> JourneyResult:
        return JourneyResult(text="I will retrieve your cards.", action=True, tool_name="cards.list", risk_level="personal")
