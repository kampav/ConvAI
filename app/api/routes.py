from fastapi import APIRouter, Request
from app.models.schemas import ChatRequest, ConfirmRequest
router = APIRouter(prefix="/api/v1")
@router.post("/chat")
async def chat(request: ChatRequest, app_request: Request):
    return await app_request.app.state.orchestrator.chat(request)
@router.post("/chat/confirm")
async def confirm(request: ConfirmRequest, app_request: Request):
    return await app_request.app.state.orchestrator.confirm(request)
@router.get("/journeys")
def journeys(app_request: Request):
    return app_request.app.state.registry.list()
@router.get("/context/{customer_id}")
def context(customer_id: str, app_request: Request):
    ctx = app_request.app.state.context
    return {"customer_id": customer_id, "conversations": {cid: events for cid, events in ctx.conversations.items()}}
@router.get("/audit/{conversation_id}")
def audit(conversation_id: str, app_request: Request):
    return app_request.app.state.audit.find_by_conversation(conversation_id)
