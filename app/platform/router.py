import re
from app.models.schemas import Intent
class IntentRouter:
 def classify(self,text):
  t=text.lower()
  if any(x in t for x in ["transfer","move £","move ","send money","pay "]):return Intent(name="payments.transfer",journey_id="payments",confidence=.97,entities={"amount":self._amount(t)} if self._amount(t)!=None else {})
  if any(x in t for x in ["balance","how much","savings","current account"]):return Intent(name="accounts.balance",journey_id="accounts",confidence=.96)
  if any(x in t for x in ["card","cards","cash withdrawal"]):return Intent(name="cards.status",journey_id="cards",confidence=.95)
  if any(x in t for x in ["mortgage","loan","borrow","lending"]):return Intent(name="lending.options",journey_id="lending",confidence=.92)
  return Intent(name="general.help",journey_id="servicing",confidence=.60)
 @staticmethod
 def _amount(text):
  m=re.search(r"£\s?(\d+(?:\.\d{1,2})?)",text); return float(m.group(1)) if m else None
