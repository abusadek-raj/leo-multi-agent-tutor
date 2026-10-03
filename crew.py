
from crewai import Crew, Process

from agents import (
    create_coordinator,
    create_explainer,
    create_quiz_master,
    create_evaluator
)

from tasks import (
    create_coordinator_task,
    create_explainer_task,
    create_quiz_task,
    create_evaluator_task,
    create_reteach_task,
    create_retry_quiz_task,
    create_retry_evaluator_task
)


# ============================================================
# PHASE 1
# Coordinator → Explainer → Quiz Master
# ============================================================

def create_learning_crew(student_request, student_name):

    coordinator = create_coordinator()
    explainer = create_explainer()
    quiz_master = create_quiz_master()

    coordinator_task = create_coordinator_task(
        coordinator,
        student_request,
        student_name
    )

    explainer_task = create_explainer_task(
        explainer,
        coordinator_task
    )

    quiz_task = create_quiz_task(
        quiz_master,
        explainer_task
    )

    crew = Crew(
        agents=[
            coordinator,
            explainer,
            quiz_master
        ],
        tasks=[
            coordinator_task,
            explainer_task,
            quiz_task
        ],
        process=Process.sequential,
        verbose=True
    )

    return crew


# ============================================================
# PHASE 2
# Evaluator
# ============================================================

def create_evaluation_crew(
    quiz_result,
    student_answers
):

    evaluator = create_evaluator()

    evaluator_task = create_evaluator_task(
        evaluator,
        quiz_result,
        student_answers
    )

    crew = Crew(
        agents=[evaluator],
        tasks=[evaluator_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


# ============================================================
# PHASE 3
# RE-TEACHING
# ============================================================

def create_reteach_crew(
    weak_topics,
    previous_lesson
):

    explainer = create_explainer()

    reteach_task = create_reteach_task(
        explainer,
        weak_topics,
        previous_lesson
    )

    crew = Crew(
        agents=[explainer],
        tasks=[reteach_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


# ============================================================
# PHASE 4
# RETRY QUIZ
# ============================================================

def create_retry_quiz_crew(reteach_result):

    quiz_master = create_quiz_master()

    retry_task = create_retry_quiz_task(
        quiz_master,
        reteach_result
    )

    crew = Crew(
        agents=[quiz_master],
        tasks=[retry_task],
        process=Process.sequential,
        verbose=False
    )

    return crew


# ============================================================
# PHASE 5
# RETRY EVALUATION
# ============================================================

def create_retry_evaluation_crew(
    retry_quiz,
    student_answers
):

    evaluator = create_evaluator()

    retry_task = create_retry_evaluator_task(
        evaluator,
        retry_quiz,
        student_answers
    )

    crew = Crew(
        agents=[evaluator],
        tasks=[retry_task],
        process=Process.sequential,
        verbose=True
    )

    return crew