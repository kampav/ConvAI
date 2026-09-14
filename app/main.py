from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.journeys.accounts import AccountsJourney
from app.journeys.cards import CardsJourney
from app.journeys.lending import LendingJourney
from app.journeys.payments import PaymentsJourney
from app.platform.audit import AuditStore
from app.platform.context import ContextBroker
from app.platform.guardrails import GuardrailEngine
from app.platform.journey_registry import JourneyRegistry
from app.platform.model_gateway import ModelGateway
from app.platform.orchestrator import ConversationOrchestrator
from app.platform.policy import PolicyEngine
from app.platform.response import ResponseComposer
from app.platform.router import IntentRouter
from app.security.auth import MockIdentityProvider
from app.security.step_up import MockStepUpAuth
from app.tools.dummy_bank import DummyBankService
from app.tools.gateway import ToolGateway
configure_logging(settings.log_level)
app=FastAPI(title="Enterprise Conversational AI Reference Platform",version="0.1.0")
context=ContextBroker(); registry=JourneyRegistry()
for j in (AccountsJourney(),PaymentsJourney(),CardsJourney(),LendingJourney()): registry.register(j)
identity=MockIdentityProvider(); step_up=MockStepUpAuth(); bank=DummyBankService(); tools=ToolGateway(bank,identity)
model_gateway=ModelGateway(settings.gemini_api_key,settings.gemini_model); composer=ResponseComposer(model_gateway); audit=AuditStore()
orchestrator=ConversationOrchestrator(context=context,router=IntentRouter(),registry=registry,policy=PolicyEngine(),tools=tools,identity=identity,step_up=step_up,guardrails=GuardrailEngine(),composer=composer,audit=audit)
app.state.context=context; app.state.registry=registry; app.state.audit=audit; app.state.orchestrator=orchestrator
@app.get("/health")
def health(): return {"status":"ok","service":"enterprise-conversational-ai","model_provider":model_gateway.provider_name,"model":model_gateway.model_name}
@app.get("/")
def index(): return FileResponse(Path(__file__).parent.parent/"frontend"/"index.html")
@app.get("/app.js")
def javascript(): return FileResponse(Path(__file__).parent.parent/"frontend"/"app.js",media_type="application/javascript")
@app.get("/styles.css")
def css(): return FileResponse(Path(__file__).parent.parent/"frontend"/"styles.css",media_type="text/css")
app.include_router(api_router)
