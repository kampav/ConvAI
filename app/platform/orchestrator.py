from uuid import uuid4
from datetime import datetime,timezone
from app.models.schemas import ChatResponse,ConfirmRequest,PendingAction,ToolRequest
class ConversationOrchestrator:
 def __init__(self,context,router,registry,policy,tools,identity,step_up,guardrails,composer,audit): self.context=context;self.router=router;self.registry=registry;self.policy=policy;self.tools=tools;self.identity=identity;self.step_up=step_up;self.guardrails=guardrails;self.composer=composer;self.audit=audit;self.pending={}
 async def chat(self,request):
  trace_id=str(uuid4()); ok,reason=self.guardrails.inspect_input(request.message)
  if not ok:return ChatResponse(conversation_id=request.conversation_id or "rejected",thread_id="none",journey_id="guardrails",message=reason or "Request rejected.",trace_id=trace_id)
  principal=self.identity.authenticate(request.customer_id); cid=self.context.ensure_conversation(request.conversation_id,principal.customer_id); self.context.append_event(cid,"user",request.message)
  intent=self.router.classify(request.message); journey=self.registry.get(intent.journey_id); tid=self.context.create_thread(cid,intent.journey_id)
  if not journey:
   text="I can help with account, payments, cards and lending requests in this reference app."; self.context.append_event(cid,"assistant",text); return ChatResponse(conversation_id=cid,thread_id=tid,journey_id="servicing",message=text,trace_id=trace_id)
  ctx=self.context.get_context(cid,principal.customer_id,intent.journey_id); jr=await journey.handle(request.message,{"global_context":ctx.global_context,"journey_context":ctx.journey_context,"intent_entities":intent.entities}); risk=self._risk(jr.risk_level); decision=self.policy.decide(risk,jr.action)
  self.audit.record("journey.routed",trace_id,{"conversation_id":cid,"customer_id":principal.customer_id,"journey_id":intent.journey_id,"intent":intent.model_dump(),"policy":decision.__dict__})
  if not jr.action:
   text=await self.composer.compose(request.message,jr.text,f"Journey: {intent.journey_id}."); self.context.append_event(cid,"assistant",text,journey_id=intent.journey_id); return ChatResponse(conversation_id=cid,thread_id=tid,journey_id=intent.journey_id,message=text,trace_id=trace_id)
  if decision.requires_confirmation:
   confirmation_id=str(uuid4()); pending=PendingAction(confirmation_id=confirmation_id,conversation_id=cid,customer_id=principal.customer_id,journey_id=intent.journey_id,action=intent.name,tool_name=jr.tool_name or "",arguments=jr.arguments or {},summary=jr.text,created_at=datetime.now(timezone.utc).isoformat()); self.pending[confirmation_id]=pending; self.audit.record("action.pending_confirmation",trace_id,pending.model_dump()); text=f"{jr.text}\n\nPlease confirm this action in the UI. No transaction has been executed yet."; self.context.append_event(cid,"assistant",text,journey_id=intent.journey_id); return ChatResponse(conversation_id=cid,thread_id=tid,journey_id=intent.journey_id,message=text,action_required=True,confirmation_id=confirmation_id,trace_id=trace_id,metadata={"risk_level":risk.value,"requires_step_up":decision.requires_step_up})
  if jr.tool_name:
   result=self.tools.invoke(ToolRequest(tool_name=jr.tool_name,arguments=jr.arguments or {},customer_id=principal.customer_id,conversation_id=cid,idempotency_key=trace_id)); authoritative=result.model_dump_json() if result.success else (result.error or "Tool execution failed."); text=await self.composer.compose(request.message,authoritative,f"Journey: {intent.journey_id}."); self.audit.record("tool.executed",trace_id,{"conversation_id":cid,"journey_id":intent.journey_id,"tool_name":jr.tool_name,"result":result.model_dump()}); self.context.append_event(cid,"assistant",text,journey_id=intent.journey_id); return ChatResponse(conversation_id=cid,thread_id=tid,journey_id=intent.journey_id,message=text,trace_id=trace_id)
  return ChatResponse(conversation_id=cid,thread_id=tid,journey_id=intent.journey_id,message=jr.text,trace_id=trace_id)
 async def confirm(self,request):
  trace_id=str(uuid4()); p=self.pending.get(request.confirmation_id)
  if not p:return ChatResponse(conversation_id=request.conversation_id,thread_id="none",journey_id="unknown",message="Confirmation has expired or is invalid.",trace_id=trace_id)
  if p.conversation_id!=request.conversation_id or p.customer_id!=request.customer_id:return ChatResponse(conversation_id=request.conversation_id,thread_id="none",journey_id=p.journey_id,message="Confirmation does not match the active customer or conversation.",trace_id=trace_id)
  self.identity.authenticate(request.customer_id); decision=self.policy.decide(self._risk("financial"),True)
  if decision.requires_step_up:
   ch=self.step_up.challenge(request.customer_id,p.summary)
   if not self.step_up.verify(request.customer_id,ch):return ChatResponse(conversation_id=request.conversation_id,thread_id="none",journey_id=p.journey_id,message="Step-up authentication failed.",trace_id=trace_id)
  result=self.tools.invoke(ToolRequest(tool_name=p.tool_name,arguments=p.arguments,customer_id=request.customer_id,conversation_id=request.conversation_id,idempotency_key=p.confirmation_id)); self.pending.pop(request.confirmation_id,None); self.audit.record("tool.executed",trace_id,{"conversation_id":request.conversation_id,"journey_id":p.journey_id,"tool_name":p.tool_name,"result":result.model_dump()})
  message=(f"Transfer completed: £{result.data['amount']:,.2f} moved from {result.data['source']} to {result.data['destination']}. Transaction ID: {result.transaction_id}." if result.success else f"The action was not completed: {result.error}"); self.context.append_event(request.conversation_id,"assistant",message,journey_id=p.journey_id); return ChatResponse(conversation_id=request.conversation_id,thread_id=self.context.create_thread(request.conversation_id,p.journey_id),journey_id=p.journey_id,message=message,trace_id=trace_id,metadata={"transaction_id":result.transaction_id})
 @staticmethod
 def _risk(value):
  from app.models.schemas import RiskLevel
  return RiskLevel(value)
