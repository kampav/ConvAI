import asyncio
from app.main import orchestrator
from app.models.schemas import ChatRequest,ConfirmRequest
def test_registry_contains_core_journeys():
 assert all(orchestrator.registry.get(x) for x in ("accounts","payments","cards","lending"))
def test_transfer_requires_confirmation():
 r=asyncio.run(orchestrator.chat(ChatRequest(customer_id="demo-user",message="Move £500 to my savings")));assert r.action_required and r.confirmation_id
def test_transfer_confirmation_executes():
 r=asyncio.run(orchestrator.chat(ChatRequest(customer_id="demo-user",message="Move £100 to my savings")));c=asyncio.run(orchestrator.confirm(ConfirmRequest(conversation_id=r.conversation_id,customer_id="demo-user",confirmation_id=r.confirmation_id)));assert "Transfer completed" in c.message and c.metadata["transaction_id"]
def test_balance_returns_authoritative_dummy_data():
 orchestrator.tools.bank.accounts["demo-user"]["savings"]["balance"]=12000.0;r=asyncio.run(orchestrator.chat(ChatRequest(customer_id="demo-user",message="What is my savings balance?")));assert "£12,000.00" in r.message
def test_same_conversation_can_switch_journeys():
 a=asyncio.run(orchestrator.chat(ChatRequest(customer_id="demo-user",message="What is my balance?")));b=asyncio.run(orchestrator.chat(ChatRequest(customer_id="demo-user",conversation_id=a.conversation_id,message="Show my cards")));assert b.conversation_id==a.conversation_id and b.journey_id=="cards" and "1234" in b.message
