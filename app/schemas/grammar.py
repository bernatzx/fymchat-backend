from pydantic import BaseModel


class GrammarCheckRequest(BaseModel):
    sentence: str


class GrammarCheckResponse(BaseModel):
    corrected_answer: str
    explanation: str
