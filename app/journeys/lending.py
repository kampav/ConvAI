from app.journeys.base import BaseJourney, JourneyResult
from app.models.schemas import Capability, JourneyDescriptor, RiskLevel
class LendingJourney(BaseJourney):
    descriptor = JourneyDescriptor(journey_id="lending", version="1.0.0", owner="domain.lending", description="Lending and borrowing information.", capabilities=[Capability(name="options", description="Explain illustrative lending options.", risk_level=RiskLevel.PERSONAL)])
    async def handle(self, message: str, context: dict) -> JourneyResult:
        return JourneyResult(text="For this reference implementation, illustrative lending options are: personal loan, home mortgage, and overdraft. No credit decision is made here.", action=False, risk_level="personal")
