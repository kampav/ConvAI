from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
class RiskLevel(str, Enum):
    PUBLIC="public"; PERSONAL="personal"; LOW="low"; FINANCIAL="financial"
class ChatRequest(BaseModel):
    conversation_id:str|None=None; customer_id:str="demo-user"; message:str=Field(min_length=1,max_length=4000); channel:str="web"
class ConfirmRequest(BaseModel):
    conversation_id:str; customer_id:str="demo-user"; confirmation_id:str
class ChatResponse(BaseModel):
    conversation_id:str; thread_id:str; journey_id:str; message:str; action_required:bool=False; confirmation_id:str|None=None; trace_id:str; metadata:dict[str,Any]={}
class Intent(BaseModel):
    name:str; journey_id:str; confidence:float; entities:dict[str,Any]={}
class Capability(BaseModel):
    name:str; description:str; risk_level:RiskLevel; requires_confirmation:bool=False
class JourneyDescriptor(BaseModel):
    journey_id:str; version:str; owner:str; description:str; capabilities:list[Capability]
class Context(BaseModel):
    customer_id:str; global_context:dict[str,Any]={}; journey_context:dict[str,Any]={}; active_threads:list[dict[str,Any]]=[]
class ToolRequest(BaseModel):
    tool_name:str; arguments:dict[str,Any]; customer_id:str; conversation_id:str; idempotency_key:str
class ToolResult(BaseModel):
    success:bool; tool_name:str; data:dict[str,Any]={}; error:str|None=None; transaction_id:str|None=None
class PendingAction(BaseModel):
    confirmation_id:str; conversation_id:str; customer_id:str; journey_id:str; action:str; tool_name:str; arguments:dict[str,Any]; summary:str; created_at:str
