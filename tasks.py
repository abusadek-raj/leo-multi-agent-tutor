
from crewai import Task


# ============================================================
# COORDINATOR
# ============================================================

def create_coordinator_task(agent, student_request, student_name):

    return Task(
        description=f"""
Student: {student_name}

Student request:
{student_request}

Create a concise tutoring plan.

Include:
1. Topic
2. Learning goal
3. What the Explainer should teach
4. What the Quiz Master should test
5. What the Evaluator should check

Do not teach the topic.

Keep the plan under 100 words.
""",
        expected_output="A concise tutoring plan under 100 words.",
        agent=agent
    )


# ============================================================
# EXPLAINER
# ============================================================

def create_explainer_task(agent, coordinator_task):

    return Task(
        description="""
Use the Coordinator's plan below.

{coordinator_task}

Teach the topic to a beginner.

Requirements:
- Use simple language
- Explain key concepts
- Give 2 examples
- Avoid unnecessary information
- Maximum 300 words
""",
        expected_output="A beginner-friendly lesson under 300 words.",
        agent=agent,
        context=[coordinator_task]
    )


# ============================================================
# QUIZ MASTER
# ============================================================

def create_quiz_task(agent, explainer_task):

    return Task(
        description="""
Create a 5-question multiple-choice quiz based ONLY
on the lesson below.

LESSON:
{explainer_task}

Create exactly two sections.

SECTION 1 — STUDENT QUIZ
- Exactly 5 questions
- Exactly 4 options per question
- Label options A, B, C, D
- Do not reveal answers in this section

SECTION 2 — ANSWER KEY
- Correct option for questions 1-5
- Short explanation for each answer

Make sure every answer key entry exactly matches
one of the four options in its question.
""",
        expected_output="""
STUDENT QUIZ

1. Question
A) Option
B) Option
C) Option
D) Option

...

ANSWER KEY

1. Correct answer: X
Explanation: ...

Continue through question 5.
""",
        agent=agent,
        context=[explainer_task]
    )


# ============================================================
# EVALUATOR
# ============================================================

def create_evaluator_task(
    agent,
    quiz_result,
    student_answers
):

    return Task(
        description=f"""
Evaluate the student's answers using the complete quiz below.

QUIZ:
{quiz_result}

STUDENT ANSWERS:
{student_answers}

Use the ANSWER KEY in the quiz to determine correctness.

For each question:
- State Correct or Incorrect
- Give a short explanation
- Identify the concept to review if incorrect

Then provide:
- Total score out of 5
- Overall feedback
- Topics needing practice

Keep the evaluation concise.
""",
        expected_output="""
A concise evaluation containing:
- Question-by-question feedback
- Total score out of 5
- Overall feedback
- Topics needing practice
""",
        agent=agent
    )


# ============================================================
# RE-TEACHER
# ============================================================

def create_reteach_task(
    agent,
    weak_topics,
    previous_lesson
):

    return Task(
        description=f"""
The student struggled with these topics:

{weak_topics}

Previous lesson:

{previous_lesson}

Re-teach ONLY the weak topics.

Requirements:
- Use very simple language
- Explain the misunderstood concepts
- Give practical examples
- Correct common mistakes
- Maximum 250 words
- Do not create a quiz
""",
        expected_output="""
A short remedial lesson focused only on the student's weak topics.
""",
        agent=agent
    )


# ============================================================
# RETRY QUIZ
# ============================================================

def create_retry_quiz_task(
    agent,
    reteach_result
):

    return Task(
        description=f"""
Create a short 3-question multiple-choice quiz based ONLY
on the remedial lesson below.

REMEDIAL LESSON:
{reteach_result}

Requirements:
- Exactly 3 questions
- Exactly 4 options per question
- Label options A, B, C, D
- Do not reveal answers in the student section

Then create an ANSWER KEY containing:
- Correct answer for each question
- Short explanation

The questions must focus on the weak topics.
""",
        expected_output="""
STUDENT QUIZ

1. Question
A) ...
B) ...
C) ...
D) ...

2. Question
A) ...
B) ...
C) ...
D) ...

3. Question
A) ...
B) ...
C) ...
D) ...

ANSWER KEY

1. Correct answer: X
Explanation: ...

2. Correct answer: X
Explanation: ...

3. Correct answer: X
Explanation: ...
""",
        agent=agent
    )


# ============================================================
# RETRY EVALUATOR
# ============================================================

def create_retry_evaluator_task(
    agent,
    retry_quiz,
    student_answers
):

    return Task(
        description=f"""
Evaluate the student's retry answers.

RETRY QUIZ:
{retry_quiz}

STUDENT ANSWERS:
{student_answers}

Use the ANSWER KEY to determine correctness.

Provide:
- Question-by-question result
- Score out of 3
- Short feedback
- Whether the student still needs practice
""",
        expected_output="""
A concise retry evaluation with score, feedback,
and remaining weak areas.
""",
        agent=agent
    )