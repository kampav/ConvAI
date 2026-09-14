from pathlib import Path
class LocalKnowledgeBase:
 def __init__(self,root="./data/knowledge"): self.root=Path(root)
 def search(self,query,limit=3):
  if not self.root.exists():return []
  terms=set(query.lower().split()); scored=[]
  for p in self.root.glob("*.md"):
   text=p.read_text(encoding="utf-8"); score=sum(1 for term in terms if term in text.lower())
   if score:scored.append((score,text[:3000]))
  scored.sort(reverse=True,key=lambda x:x[0]); return [text for _,text in scored[:limit]]
