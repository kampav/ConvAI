from dataclasses import dataclass
@dataclass
class Principal:
    customer_id:str; authenticated:bool; scopes:set[str]
class MockIdentityProvider:
    def authenticate(self,customer_id):
        if not customer_id: raise ValueError("customer_id is required")
        return Principal(customer_id,True,{"accounts:read","payments:write","cards:read","lending:read"})
    def authorize(self,principal,scope): return principal.authenticated and scope in principal.scopes
