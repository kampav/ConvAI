import json
class ResponseComposer:
 def __init__(self,model_gateway): self.model_gateway=model_gateway
 async def compose(self,user_message,authoritative_result,context=""):
  if self.model_gateway.provider_name=="local-mock":return self._local_format(authoritative_result)
  system="You are the response layer of an enterprise banking conversational platform. The supplied result is authoritative. Explain it clearly. Never change amounts, statuses, transaction IDs or decisions."
  return await self.model_gateway.generate(system,user_message,f"AUTHORITATIVE RESULT:\n{authoritative_result}\n{context}")
 @staticmethod
 def _local_format(authoritative_result):
  try:
   data=json.loads(authoritative_result)
   if data.get("tool_name")=="accounts.get_balances":
    a=data["data"]["accounts"]; return f"Current Account: £{a['current']['balance']:,.2f}\nSavings Account: £{a['savings']['balance']:,.2f}"
   if data.get("tool_name")=="cards.list":
    return "Your cards:\n"+"\n".join(f"• {c['name']} ending {c['last4']} — {c['status']}" for c in data["data"]["cards"])
   return authoritative_result
  except (ValueError,KeyError,TypeError):return authoritative_result
