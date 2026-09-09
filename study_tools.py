# =============================================================
# STUDY ASSISTANT TOOLS
# =============================================================


def create_quiz(topic, number_of_questions=5, difficulty="medium"):
    """
    Create a structured quiz request for the LLM.
    """

    topic = topic.strip()

    if not topic:
        return "Please provide a study topic."

    if number_of_questions < 1:
        return "The number of questions must be at least 1."

    if number_of_questions > 20:
        return "The maximum number of questions is 20."

    difficulty = difficulty.lower().strip()

    if difficulty not in {"easy", "medium", "hard"}:
        return "Difficulty must be easy, medium, or hard."

    return (
        f"Create a {difficulty} difficulty quiz about '{topic}' "
        f"with {number_of_questions} questions. "
        "Ask one question at a time and wait for the user's answer."
    )


def explain_topic(topic, level="intermediate"):
    """
    Create a structured study explanation request.
    """

    topic = topic.strip()

    if not topic:
        return "Please provide a topic to explain."

    level = level.lower().strip()

    allowed_levels = {
        "beginner",
        "intermediate",
        "advanced"
    }

    if level not in allowed_levels:
        return (
            "Level must be beginner, intermediate, or advanced."
        )

    return (
        f"Explain '{topic}' at an {level} level. "
        "Use clear explanations and a simple example where useful."
    )


def generate_study_questions(topic, number_of_questions=5):
    """
    Generate a structured request for practice questions.
    """

    topic = topic.strip()

    if not topic:
        return "Please provide a study topic."

    if number_of_questions < 1:
        return "The number of questions must be at least 1."

    if number_of_questions > 20:
        return "The maximum number of questions is 20."

    return (
        f"Generate {number_of_questions} practice questions "
        f"about '{topic}'. Include a mixture of conceptual "
        "and application-based questions."
    )


def evaluate_answer(question, answer):
    """
    Create a structured request for evaluating a student's answer.
    """

    question = question.strip()
    answer = answer.strip()

    if not question:
        return "Please provide the question."

    if not answer:
        return "Please provide the student's answer."

    return (
        "Evaluate the student's answer to the following question.\n\n"
        f"Question: {question}\n"
        f"Student answer: {answer}\n\n"
        "Explain whether the answer is correct, partially correct, "
        "or incorrect. Give a concise explanation and mention what "
        "could be improved."
    )