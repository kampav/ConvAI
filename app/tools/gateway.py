from app.models.schemas import ToolRequest,ToolResult
class ToolGateway:
    def __init__(self,bank,identity): self.bank=bank;self.identity=identity
    def invoke(self,request):
        p=self.identity.authenticate(request.customer_id)
        if request.tool_name=="accounts.get_balances":
            if not self.identity.authorize(p,"accounts:read"):return ToolResult(success=False,tool_name=request.tool_name,error="Not authorized.")
            return ToolResult(success=True,tool_name=request.tool_name,data={"accounts":self.bank.get_balances(request.customer_id)})
        if request.tool_name=="cards.list":
            if not self.identity.authorize(p,"cards:read"):return ToolResult(success=False,tool_name=request.tool_name,error="Not authorized.")
            return ToolResult(success=True,tool_name=request.tool_name,data={"cards":self.bank.get_cards(request.customer_id)})
        if request.tool_name=="payments.transfer":
            if not self.identity.authorize(p,"payments:write"):return ToolResult(success=False,tool_name=request.tool_name,error="Not authorized.")
            try:
                r=self.bank.transfer(request.customer_id,request.arguments["source"],request.arguments["destination"],float(request.arguments["amount"]),request.idempotency_key);return ToolResult(success=True,tool_name=request.tool_name,data=r,transaction_id=r["transaction_id"])
            except (KeyError,ValueError) as e:return ToolResult(success=False,tool_name=request.tool_name,error=str(e))
        return ToolResult(success=False,tool_name=request.tool_name,error=f"Unknown tool: {request.tool_name}")
