
# Leo — Multi-Agent AI Tutor Architecture

## 1. High-Level Architecture

Leo uses a sequential multi-agent architecture implemented with CrewAI.

```text
                         ┌──────────────┐
                         │    Student   │
                         └──────┬───────┘
                                │
                                ▼
                    ┌────────────────────┐
                    │  Student Memory    │
                    │ student_memory.json│
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │    Coordinator     │
                    │                    │
                    │ Understand request │
                    │ Create plan        │
                    └──────────┬─────────┘
                               │
                               │ Context
                               ▼
                    ┌────────────────────┐
                    │     Explainer      │
                    │                    │
                    │ Teach topic        │
                    │ Give examples      │
                    └──────────┬─────────┘
                               │
                               │ Lesson
                               ▼
                    ┌────────────────────┐
                    │    Quiz Master     │
                    │                    │
                    │ Generate quiz      │
                    │ Generate key       │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │      Student       │
                    │                    │
                    │ Answer quiz        │
                    └──────────┬─────────┘
                               │
                               │ Answers
                               ▼
                    ┌────────────────────┐
                    │     Evaluator      │
                    │                    │
                    │ Check answers      │
                    │ Calculate score    │
                    │ Find weak topics   │
                    └──────────┬─────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                 Score ≥ 3             Score < 3
                    │                     │
                    ▼                     ▼
                 Complete             Explainer
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

## 2. Agent Communication

The agents are not independent.

The output of one stage becomes context for the next stage.

### Coordinator → Explainer

The Coordinator creates a learning plan.

```text
Coordinator
      ↓
Learning Plan
      ↓
Explainer
```

### Explainer → Quiz Master

The Quiz Master receives the lesson.

```text
Explainer
      ↓
Lesson
      ↓
Quiz Master
```

The quiz is therefore based on the lesson generated during the current session.

### Quiz Master → Student

The application extracts the student-visible quiz and hides the answer key.

```text
Quiz Master
      ↓
Student Quiz
      ↓
Student
```

### Student → Evaluator

The student's answers are passed to the Evaluator together with the complete quiz.

```text
Student Answers
      ↓
Evaluator
```

---

## 3. Feedback Loop

The Evaluator determines whether additional practice is required.

```text
                  Evaluator
                      │
                 Calculate score
                      │
             ┌────────┴────────┐
             │                 │
          >= 3/5             < 3/5
             │                 │
             ▼                 ▼
          Complete          Weak Topics
                                │
                                ▼
                            Explainer
                                │
                                ▼
                           Re-teaching
                                │
                                ▼
                           Quiz Master
                                │
                                ▼
                           Retry Quiz
                                │
                                ▼
                            Evaluator
```

This provides an adaptive learning cycle.

---

## 4. LLM Layer

Leo uses:

```text
Groq API
   │
   ▼
openai/gpt-oss-20b
   │
   ▼
CrewAI LLM
   │
   ▼
Agents
```

The API key is loaded from the `.env` file.

---

## 5. Memory Layer

Student memory is stored locally.

```text
app.py
   │
   ▼
memory.py
   │
   ▼
student_memory.json
```

The memory contains:

* Student name
* Topics studied
* Previous scores
* Session count

The JSON file is excluded from source control.

---

## 6. Application Layer

The main entry point is:

```text
app.py
```

The application is responsible for:

* Collecting student information
* Displaying the workflow
* Starting CrewAI workflows
* Collecting quiz answers
* Triggering evaluation
* Triggering the feedback loop
* Updating student memory

---

## 7. File Architecture

```text
app.py
 │
 ├── crew.py
 │     │
 │     ├── agents.py
 │     │
 │     └── tasks.py
 │
 ├── memory.py
 │
 └── config.py
       │
       └── Groq / CrewAI LLM

models.py
 │
 └── Pydantic models
```

---

## 8. Orchestration Pattern

Leo uses:

```text
Process.sequential
```

The primary learning crew executes:

```text
Coordinator Task
        ↓
Explainer Task
        ↓
Quiz Task
```

The evaluation workflow is executed after the student provides answers.

The feedback workflow is conditionally executed when the score is below the threshold.

---

## 9. Design Principle

The main design principle is **specialization**.

Instead of asking one AI agent to perform every tutoring task, Leo assigns different responsibilities to specialized agents.

This makes the workflow easier to understand, demonstrate, and extend.
