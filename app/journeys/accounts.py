from app.journeys.base import BaseJourney, JourneyResult
from app.models.schemas import Capability, JourneyDescriptor, RiskLevel
class AccountsJourney(BaseJourney):
    descriptor = JourneyDescriptor(journey_id="accounts", version="1.0.0", owner="domain.accounts", description="Account information and servicing.", capabilities=[Capability(name="balance", description="View account balances.", risk_level=RiskLevel.PERSONAL)])
    async def handle(self, message: str, context: dict) -> JourneyResult:
        return JourneyResult(text="I will retrieve your account balances.", action=True, tool_name="accounts.get_balances", risk_level="personal")
