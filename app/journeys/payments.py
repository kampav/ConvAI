from app.journeys.base import BaseJourney, JourneyResult
from app.models.schemas import Capability, JourneyDescriptor, RiskLevel
class PaymentsJourney(BaseJourney):
    descriptor = JourneyDescriptor(journey_id="payments", version="1.0.0", owner="domain.payments", description="Payments and account-to-account transfers.", capabilities=[Capability(name="transfer", description="Transfer money between owned demo accounts.", risk_level=RiskLevel.FINANCIAL, requires_confirmation=True)])
    async def handle(self, message: str, context: dict) -> JourneyResult:
        amount = context.get("intent_entities", {}).get("amount")
        if amount is None:
            return JourneyResult(text="What amount would you like to transfer?", action=False, risk_level="financial")
        return JourneyResult(text=f"I can prepare a transfer of £{amount:,.2f} from your Current Account to your Savings Account.", action=True, tool_name="payments.transfer", arguments={"source":"current","destination":"savings","amount":amount}, risk_level="financial")
