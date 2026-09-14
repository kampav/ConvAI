from typing import Protocol
class ModelProvider(Protocol):
    async def generate(self,system:str,user:str,context:str="")->str: ...
class LocalModelProvider:
    async def generate(self,system,user,context=""): return "I can help with that. The platform has processed your request using the configured journey and policy controls."
class GeminiModelProvider:
    def __init__(self,api_key,model):
        from google import genai
        self.client=genai.Client(api_key=api_key); self.model=model
    async def generate(self,system,user,context=""):
        prompt=f"SYSTEM INSTRUCTIONS:\n{system}\n\nCONTEXT:\n{context}\n\nUSER:\n{user}\n\nAnswer concisely. Do not invent account balances, transactions, authorizations or policy decisions."
        response=self.client.models.generate_content(model=self.model,contents=prompt)
        return response.text or "I could not generate a response."
class ModelGateway:
    def __init__(self,api_key,model): self.provider=GeminiModelProvider(api_key,model) if api_key else LocalModelProvider(); self.provider_name="gemini" if api_key else "local-mock"; self.model_name=model if api_key else "deterministic-local"
    async def generate(self,system,user,context=""): return await self.provider.generate(system,user,context)
