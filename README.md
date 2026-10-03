
# Leo — Multi-Agent AI Tutor

Leo is a multi-agent AI tutoring system built with **CrewAI** and **Groq**. It uses multiple specialized AI agents to teach a student, generate a quiz, evaluate the student's answers, and provide additional teaching when the student needs more practice.

The project uses the `openai/gpt-oss-20b` model through the Groq API.

---

## Project Objective

The goal of Leo is to demonstrate how multiple AI agents can collaborate to create an interactive tutoring workflow.

Instead of using a single AI agent for every task, Leo divides the tutoring process among specialized agents:

1. **Coordinator** — understands the student's request and creates a learning plan.
2. **Explainer** — teaches the requested topic.
3. **Quiz Master** — creates a multiple-choice quiz based on the lesson.
4. **Evaluator** — evaluates the student's answers and provides feedback.

Leo also includes a feedback loop. If the student's score is below the required threshold, the Explainer re-teaches the weak topics, the Quiz Master creates a retry quiz, and the Evaluator checks the retry answers.

---

## Features

* Multi-agent architecture using CrewAI
* Four specialized AI agents
* Sequential agent orchestration
* Groq API integration
* `openai/gpt-oss-20b` model
* Interactive command-line interface
* Student memory using a local JSON file
* Automatic quiz generation
* Automatic answer evaluation
* Score calculation
* Weak-topic identification
* Re-teaching feedback loop
* Retry quiz
* Retry evaluation
* Environment variable based API key management
* GitHub-safe configuration

---

## System Architecture

```text
                    ┌───────────────────┐
                    │      Student      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Student Memory   │
                    │  JSON Storage     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Coordinator    │
                    │  Learning Plan    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Explainer     │
                    │   Teach Topic     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Quiz Master    │
                    │   Create Quiz     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │      Student      │
                    │   Answers Quiz    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Evaluator     │
                    │ Check Answers     │
                    └─────────┬─────────┘
                              │
                       ┌──────┴──────┐
                       │             │
                    Score >= 3     Score < 3
                       │             │
                       ▼             ▼
                    Complete     Re-teach
                                     │
                                     ▼
                                Retry Quiz
                                     │
                                     ▼
                                  Evaluator
                                     │
                                     ▼
                                  Complete
```

---

## Agent Roles

### 1. Coordinator

**Role:** Learning coordinator

The Coordinator receives the student's request and creates a concise learning plan.

Responsibilities:

* Understand the student's topic
* Identify the learning goal
* Decide what the Explainer should teach
* Decide what the Quiz Master should test
* Decide what the Evaluator should check

The Coordinator does not directly teach the topic.

---

### 2. Explainer

**Role:** Teacher

The Explainer receives the Coordinator's plan and teaches the requested topic.

Responsibilities:

* Explain concepts using simple language
* Teach at the student's level
* Provide examples
* Focus on the requested topic
* Re-teach weak areas when the feedback loop is activated

---

### 3. Quiz Master

**Role:** Assessment designer

The Quiz Master receives the lesson from the Explainer.

Responsibilities:

* Create five multiple-choice questions
* Provide four options for each question
* Base questions on the lesson
* Maintain a separate answer key
* Create a shorter retry quiz during the feedback loop

The student's displayed quiz hides the answer key.

---

### 4. Evaluator

**Role:** Assessment evaluator

The Evaluator receives:

* The complete quiz
* The answer key
* The student's answers

Responsibilities:

* Check each answer
* Calculate the score
* Explain mistakes
* Identify weak topics
* Give learning feedback

When the student's score is below the threshold, the feedback loop is activated.

---

## Orchestration

Leo uses **CrewAI sequential orchestration**.

The first phase follows:

```text
Coordinator
     ↓
Explainer
     ↓
Quiz Master
```

The student then answers the quiz.

The second phase is:

```text
Student Answers
       ↓
Evaluator
```

If the student needs additional practice:

```text
Evaluator
    ↓
Weak Topics
    ↓
Explainer
    ↓
Retry Quiz Master
    ↓
Student
    ↓
Retry Evaluator
```

This allows the agents to pass the output of one stage into the next stage.

---

## Feedback Loop

Leo includes a feedback loop as an additional feature.

If the student's score is below 3 out of 5:

1. The Evaluator identifies weak topics.
2. The Explainer re-teaches those topics.
3. The Quiz Master creates a three-question retry quiz.
4. The student answers the retry quiz.
5. The Evaluator evaluates the retry answers.

This creates an adaptive tutoring cycle rather than ending after the first quiz.

---

## Memory

Leo stores simple student learning information locally in:

```text
student_memory.json
```

The memory records:

* Student name
* Topics studied
* Previous scores
* Number of sessions

Example:

```json
{
    "Student": {
        "topics": [
            "Python Variables"
        ],
        "scores": [
            {
                "topic": "Python Variables",
                "score": "3/5"
            }
        ],
        "sessions": 1
    }
}
```

The memory file is excluded from GitHub using `.gitignore`.

---

## Technologies Used

* Python 3.12
* CrewAI
* Groq API
* `openai/gpt-oss-20b`
* LiteLLM
* Pydantic
* python-dotenv
* OpenAI Python SDK
* JSON for local student memory

---

## Project Structure

```text
leo-multi-agent-tutor/
│
├── app.py
├── config.py
├── agents.py
├── tasks.py
├── crew.py
├── models.py
├── memory.py
│
├── requirements.txt
├── README.md
├── architecture.md
├── .env.example
├── .gitignore
│
├── .env
└── student_memory.json
```

### File descriptions

| File               | Purpose                                           |
| ------------------ | ------------------------------------------------- |
| `app.py`           | Main application                                  |
| `config.py`        | Groq/CrewAI LLM configuration                     |
| `agents.py`        | Defines the four AI agents                        |
| `tasks.py`         | Defines agent tasks                               |
| `crew.py`          | Builds the CrewAI workflows                       |
| `models.py`        | Pydantic data models                              |
| `memory.py`        | Student memory management                         |
| `requirements.txt` | Python dependencies                               |
| `.env.example`     | Example environment configuration                 |
| `.gitignore`       | Prevents secrets/local files from being committed |
| `README.md`        | Project documentation                             |
| `architecture.md`  | Architecture documentation                        |

---

## Requirements

Python 3.12 is recommended.

A Groq API key is also required.

---

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Enter the project directory:

```bash
cd leo-multi-agent-tutor
```

Install the dependencies:

```bash
py -3.12 -m pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root.

Add:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not commit the `.env` file to GitHub.

The repository contains `.env.example` as a safe template:

```text
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running Leo

Run:

```bash
py -3.12 app.py
```

Leo will ask for:

```text
Enter your name:
```

Then:

```text
What would you like to learn?
```

For example:

```text
Python variables
```

Leo will then execute the multi-agent learning workflow.

---

## Example Workflow

A typical session looks like:

```text
Student
  ↓
Coordinator creates learning plan
  ↓
Explainer teaches Python variables
  ↓
Quiz Master creates quiz
  ↓
Student answers
  ↓
Evaluator checks answers
  ↓
Score generated
```

If the student needs more practice:

```text
Evaluator
  ↓
Identifies weak topics
  ↓
Explainer re-teaches
  ↓
Quiz Master creates retry quiz
  ↓
Student answers again
  ↓
Evaluator provides retry feedback
```

---

## Security

API keys are stored in environment variables.

The following files should never be committed:

```text
.env
student_memory.json
```

They are included in `.gitignore`.

Before publishing the repository, make sure no API key appears in:

* Source code
* README
* Screenshots
* Demo video
* Git history

---

## Limitations

Leo currently uses a command-line interface.

The student memory is stored locally in a JSON file rather than a database.

The quiz is generated by the language model, so the application does not currently use a separate deterministic question bank.

---

## Future Improvements

Possible future improvements include:

* Streamlit or Gradio interface
* Persistent database storage
* More detailed student profiles
* Difficulty adaptation
* Topic mastery tracking
* More quiz types
* Structured quiz output
* Learning progress visualization
* Human-in-the-loop review
* More advanced long-term memory

---

## Assignment Requirements Mapping

| Assignment Requirement  | Implementation                                 |
| ----------------------- | ---------------------------------------------- |
| CrewAI                  | CrewAI framework                               |
| Coordinator             | `create_coordinator()`                         |
| Explainer               | `create_explainer()`                           |
| Quiz Master             | `create_quiz_master()`                         |
| Evaluator               | `create_evaluator()`                           |
| Agent handoff           | Task context passing                           |
| Orchestration           | Sequential CrewAI process                      |
| Memory                  | `memory.py` + JSON                             |
| Prompt templates        | Agent goals, backstories and task descriptions |
| Structured quiz         | Multiple-choice quiz with defined format       |
| Graceful input handling | Default handling for empty input               |
| User interface          | CLI via `app.py`                               |
| Feedback loop           | Re-teaching + retry quiz                       |
| Environment security    | `.env` + `.gitignore`                          |

---

## Demo

The recommended demonstration flow is:

1. Start Leo.
2. Enter the student's name.
3. Enter a learning topic.
4. Show the Coordinator's work.
5. Show the Explainer teaching the topic.
6. Show the Quiz Master generating the quiz.
7. Answer the quiz.
8. Show the Evaluator's feedback.
9. Demonstrate the feedback loop with a low score.
10. Show re-teaching.
11. Show the retry quiz.
12. Show the retry evaluation.
13. Show the updated student memory.

---

## Author

**Leo — Multi-Agent AI Tutor**

Built as an educational multi-agent AI project using CrewAI and Groq.
