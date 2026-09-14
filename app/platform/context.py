from datetime import datetime,timezone
from uuid import uuid4
from app.models.schemas import Context
class ContextBroker:
    def __init__(self): self.conversations={}; self.threads={}
    def ensure_conversation(self,conversation_id,customer_id):
        cid=conversation_id or str(uuid4()); self.conversations.setdefault(cid,[]); return cid
    def append_event(self,conversation_id,role,content,**metadata):
        self.conversations.setdefault(conversation_id,[]).append({"role":role,"content":content,"timestamp":datetime.now(timezone.utc).isoformat(),**metadata})
    def create_thread(self,conversation_id,journey_id):
        for tid,t in self.threads.items():
            if t["conversation_id"]==conversation_id and t["journey_id"]==journey_id: return tid
        tid=str(uuid4()); self.threads[tid]={"thread_id":tid,"conversation_id":conversation_id,"journey_id":journey_id,"state":{}}; return tid
    def get_context(self,conversation_id,customer_id,journey_id):
        history=self.conversations.get(conversation_id,[]); threads=[t for t in self.threads.values() if t["conversation_id"]==conversation_id]
        state=next((t["state"] for t in threads if t["journey_id"]==journey_id),{})
        return Context(customer_id=customer_id,global_context={"recent_messages":history[-8:],"customer_id":customer_id},journey_context=state,active_threads=threads)
