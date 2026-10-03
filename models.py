
from pydantic import BaseModel, Field
from typing import List


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class Quiz(BaseModel):
    topic: str
    questions: List[QuizQuestion] = Field(min_length=5, max_length=5)