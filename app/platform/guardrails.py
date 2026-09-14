import re
class GuardrailEngine:
    SECRET_PATTERNS=[re.compile(r"\b(?:otp|one[- ]time password)\b.*\b\d{4,8}\b",re.I),re.compile(r"\bpin\b.*\b\d{4,6}\b",re.I)]
    def inspect_input(self,text):
        for p in self.SECRET_PATTERNS:
            if p.search(text): return False,"Do not send passwords, PINs or one-time codes to the assistant."
        return (False,"Message exceeds the maximum allowed length.") if len(text)>4000 else (True,None)
    def sanitize_output(self,text): return text.strip()
