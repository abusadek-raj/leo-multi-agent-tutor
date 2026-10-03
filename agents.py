
from crewai import Agent
from config import llm


def create_coordinator():
    return Agent(
        role="Coordinator",
        goal="Understand the student's request and coordinate the tutoring process.",
        backstory=(
            "You are Leo's Coordinator. You understand what the student wants "
            "to learn and organize the other tutor agents."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        cache=False
    )


def create_explainer():
    return Agent(
        role="Explainer",
        goal="Explain the requested topic clearly at the student's level.",
        backstory=(
            "You are an expert teacher who explains difficult concepts "
            "using simple language, examples, and step-by-step explanations."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        cache=False
    )


def create_quiz_master():
    return Agent(
        role="Quiz Master",
        goal="Create useful practice questions based on the lesson.",
        backstory=(
            "You are a quiz designer. You create questions that test "
            "whether the student understands the lesson."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        cache=False
    )


def create_evaluator():
    return Agent(
        role="Evaluator",
        goal="Evaluate the student's answers and provide constructive feedback.",
        backstory=(
            "You are an educational evaluator. You identify correct and incorrect "
            "answers, explain mistakes, and suggest what the student should review."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        cache=False
    )