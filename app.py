
import re

from crew import (
    create_learning_crew,
    create_evaluation_crew,
    create_reteach_crew,
    create_retry_quiz_crew,
    create_retry_evaluation_crew
)

from memory import (
    get_student_memory,
    update_student_memory,
    format_student_memory
)


def print_header(title):
    print("\n")
    print("=" * 70)
    print(f"{title:^70}")
    print("=" * 70)


def get_score(evaluation_text):
    """Extract score such as 3/5 from evaluator output."""

    patterns = [
        r"(?:Total\s+Score|Total\s+score|Score)"
        r".*?(\d+)\s*/\s*5",

        r"(\d+)\s*/\s*5"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            evaluation_text,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            return int(match.group(1))

    return None


def extract_weak_topics(evaluation_text):
    """Extract weak topics from evaluator feedback."""

    patterns = [
        r"Topics?\s+(?:Needing|that need)\s+Practice\s*:?(.*)",
        r"Topics?\s+to\s+Review\s*:?(.*)",
        r"Weak\s+Topics?\s*:?(.*)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            evaluation_text,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            result = match.group(1).strip()

            if result:
                return result

    return evaluation_text


def run_learning_session(student_name, student_request):

    # ---------------------------------------------------------
    # Show existing memory
    # ---------------------------------------------------------

    print_header("LEO - STUDENT MEMORY")

    print(
        format_student_memory(student_name)
    )

    # ---------------------------------------------------------
    # Phase 1: Coordinator → Explainer → Quiz Master
    # ---------------------------------------------------------

    print_header("PHASE 1: LEARNING")

    print("\nCoordinator is planning your lesson...")

    learning_crew = create_learning_crew(
        student_request=student_request,
        student_name=student_name
    )

    learning_result = learning_crew.kickoff()

    learning_text = str(learning_result)

    # ---------------------------------------------------------
    # Hide answer key from student
    # ---------------------------------------------------------

    answer_key_marker = "ANSWER KEY"

    if answer_key_marker in learning_text:

        student_quiz = learning_text.split(
            answer_key_marker,
            1
        )[0].strip()

    else:

        student_quiz = learning_text

    # ---------------------------------------------------------
    # Display quiz
    # ---------------------------------------------------------

    print_header("QUIZ MASTER - YOUR QUIZ")

    print(student_quiz)

    # ---------------------------------------------------------
    # Student answers
    # ---------------------------------------------------------

    print_header("YOUR ANSWERS")

    print("Enter answers for questions 1-5.")
    print("Example: A B C D A")

    student_answers = input(
        "\nYour answers: "
    ).strip()

    if not student_answers:

        print(
            "\nNo answers entered."
        )

        student_answers = "No answers provided"

    # ---------------------------------------------------------
    # Phase 2: Evaluator
    # ---------------------------------------------------------

    print_header("PHASE 2: EVALUATION")

    print(
        "\nEvaluator is checking your answers..."
    )

    evaluation_crew = create_evaluation_crew(
        quiz_result=learning_result,
        student_answers=student_answers
    )

    evaluation_result = evaluation_crew.kickoff()

    evaluation_text = str(evaluation_result)

    print_header("LEO FEEDBACK")

    print(evaluation_text)

    # ---------------------------------------------------------
    # Get score
    # ---------------------------------------------------------

    score = get_score(evaluation_text)

    # ---------------------------------------------------------
    # Save session memory
    # ---------------------------------------------------------

    if score is not None:

        score_text = f"{score}/5"

    else:

        score_text = "Unknown"

    update_student_memory(
        student_name=student_name,
        topic=student_request,
        score=score_text
    )

    # ---------------------------------------------------------
    # Feedback loop
    # ---------------------------------------------------------

    if score is not None and score < 3:

        print_header(
            "FEEDBACK LOOP ACTIVATED"
        )

        print(
            "\nYour score is below 60%."
        )

        print(
            "Leo will re-teach the topics "
            "that need practice."
        )

        # -----------------------------------------------------
        # Identify weak topics
        # -----------------------------------------------------

        weak_topics = extract_weak_topics(
            evaluation_text
        )

        # -----------------------------------------------------
        # Re-teaching
        # -----------------------------------------------------

        print_header(
            "EXPLAINER: RE-TEACHING WEAK TOPICS"
        )

        reteach_crew = create_reteach_crew(
            weak_topics=weak_topics,
            previous_lesson=learning_text
        )

        reteach_result = reteach_crew.kickoff()

        print("\n")
        print(reteach_result)

        # -----------------------------------------------------
        # Retry quiz
        # -----------------------------------------------------

        print_header(
            "QUIZ MASTER: RETRY QUIZ"
        )

        retry_quiz_crew = create_retry_quiz_crew(
            reteach_result=str(
                reteach_result
            )
        )

        retry_quiz_result = (
            retry_quiz_crew.kickoff()
        )

        retry_quiz_text = str(
            retry_quiz_result
        )

        if answer_key_marker in retry_quiz_text:

            retry_student_quiz = (
                retry_quiz_text.split(
                    answer_key_marker,
                    1
                )[0].strip()
            )

        else:

            retry_student_quiz = retry_quiz_text

        print("\n")
        print(retry_student_quiz)

        # -----------------------------------------------------
        # Retry answers
        # -----------------------------------------------------

        print_header(
            "RETRY YOUR ANSWERS"
        )

        print(
            "Enter your 3 answers."
        )

        print(
            "Example: A B C"
        )

        retry_answers = input(
            "\nYour answers: "
        ).strip()

        if not retry_answers:

            retry_answers = "No answers provided"

        # -----------------------------------------------------
        # Retry evaluation
        # -----------------------------------------------------

        print_header(
            "EVALUATOR: CHECKING RETRY"
        )

        retry_evaluation_crew = (
            create_retry_evaluation_crew(
                retry_quiz=str(
                    retry_quiz_result
                ),
                student_answers=retry_answers
            )
        )

        retry_evaluation = (
            retry_evaluation_crew.kickoff()
        )

        print_header(
            "LEO RETRY FEEDBACK"
        )

        print(retry_evaluation)

    else:

        print_header(
            "LEO: GREAT JOB!"
        )

        print(
            "\nYou demonstrated sufficient "
            "understanding of the topic."
        )

        print(
            "Keep practicing!"
        )

    # ---------------------------------------------------------
    # Show updated memory
    # ---------------------------------------------------------

    print_header(
        "UPDATED STUDENT MEMORY"
    )

    print(
        format_student_memory(student_name)
    )


def main():

    print("\n")
    print("=" * 70)
    print(
        "LEO - MULTI-AGENT AI TUTOR".center(70)
    )
    print("=" * 70)

    print(
        "\nYour personal AI tutor powered by CrewAI."
    )

    print(
        "Agents: Coordinator | Explainer | Quiz Master | Evaluator"
    )

    # ---------------------------------------------------------
    # Student name
    # ---------------------------------------------------------

    student_name = input(
        "\nEnter your name: "
    ).strip()

    if not student_name:

        student_name = "Student"

    # ---------------------------------------------------------
    # Student request
    # ---------------------------------------------------------

    student_request = input(
        "What would you like to learn? "
    ).strip()

    if not student_request:

        student_request = "Python variables"

    # ---------------------------------------------------------
    # Run session
    # ---------------------------------------------------------

    run_learning_session(
        student_name=student_name,
        student_request=student_request
    )

    # ---------------------------------------------------------
    # Complete
    # ---------------------------------------------------------

    print_header(
        "LEO SESSION COMPLETE"
    )

    print(
        "\nThank you for learning with Leo!"
    )


if __name__ == "__main__":
    main()