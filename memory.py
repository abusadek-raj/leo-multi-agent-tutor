
import json
import os


MEMORY_FILE = "student_memory.json"


def load_memory():
    """Load student memory from JSON file."""

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    """Save student memory to JSON file."""

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_student_memory(student_name):
    """Get memory for a specific student."""

    memory = load_memory()

    if student_name not in memory:
        memory[student_name] = {
            "topics": [],
            "scores": [],
            "sessions": 0
        }

        save_memory(memory)

    return memory[student_name]


def update_student_memory(
    student_name,
    topic,
    score=None
):
    """Update the student's learning history."""

    memory = load_memory()

    if student_name not in memory:
        memory[student_name] = {
            "topics": [],
            "scores": [],
            "sessions": 0
        }

    student = memory[student_name]

    # Save topic if it is new
    if topic and topic not in student["topics"]:
        student["topics"].append(topic)

    # Save score
    if score is not None:
        student["scores"].append({
            "topic": topic,
            "score": score
        })

    student["sessions"] += 1

    save_memory(memory)


def format_student_memory(student_name):
    """Create a readable memory summary for Leo."""

    student = get_student_memory(student_name)

    topics = student.get("topics", [])
    scores = student.get("scores", [])
    sessions = student.get("sessions", 0)

    lines = []

    lines.append(f"Student: {student_name}")
    lines.append(f"Previous sessions: {sessions}")

    if topics:
        lines.append(
            "Topics studied: " + ", ".join(topics)
        )
    else:
        lines.append("Topics studied: None")

    if scores:
        lines.append("Previous scores:")

        for item in scores[-5:]:
            lines.append(
                f"- {item['topic']}: {item['score']}"
            )
    else:
        lines.append("Previous scores: None")

    return "\n".join(lines)