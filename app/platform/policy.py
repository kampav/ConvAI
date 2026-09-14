from dataclasses import dataclass
from app.models.schemas import RiskLevel
@dataclass
class PolicyDecision: allowed:bool; requires_confirmation:bool; requires_step_up:bool; reason:str
class PolicyEngine:
 def decide(self,risk_level,action):
  if not action:return PolicyDecision(True,False,False,"Read/information request.")
  if risk_level==RiskLevel.FINANCIAL:return PolicyDecision(True,True,True,"Financial action requires explicit confirmation and step-up authentication.")
  if risk_level==RiskLevel.LOW:return PolicyDecision(True,True,False,"Low-risk action requires explicit confirmation.")
  return PolicyDecision(True,False,False,"Permitted non-transactional request.")
