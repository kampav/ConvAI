from app.models.schemas import JourneyDescriptor
class JourneyRegistry:
    def __init__(self): self._journeys={}
    def register(self,journey): self._journeys[journey.descriptor.journey_id]=journey
    def get(self,journey_id): return self._journeys.get(journey_id)
    def list(self): return [j.descriptor for j in self._journeys.values()]
