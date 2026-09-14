class MockStepUpAuth:
    def challenge(self,customer_id,action_summary): return f"STEP-UP:{customer_id}:{abs(hash(action_summary))%100000}"
    def verify(self,customer_id,challenge): return challenge.startswith(f"STEP-UP:{customer_id}:")
