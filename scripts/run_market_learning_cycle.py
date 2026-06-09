"""Market Learning Cycle - Extract lessons and generate knowledge from accuracy results."""

from datetime import datetime, timezone


def run_cycle() -> dict:
    from services.forecast_accuracy_engine import list_all_accuracies
    from services.market_lesson_engine import extract_lesson
    from services.market_knowledge_engine import generate_knowledge, store_knowledge
    from services.market_skill_improvement_engine import create_skill_proposal

    accuracies = list_all_accuracies()
    lessons_created = 0
    knowledge_created = 0
    proposals_created = 0

    for acc in accuracies:
        forecast_id = acc.get("forecast_id")
        accuracy_id = acc.get("accuracy_id")
        if forecast_id and accuracy_id:
            lesson = extract_lesson(accuracy_id, forecast_id)
            if lesson:
                lessons_created += 1
                knowledge = generate_knowledge(lesson.get("lesson_id", ""))
                if knowledge:
                    store_knowledge(knowledge)
                    knowledge_created += 1
                proposal = create_skill_proposal(lesson.get("lesson_id", ""))
                if proposal:
                    proposals_created += 1

    return {
        "cycle": "market_learning",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lessons_created": lessons_created,
        "knowledge_created": knowledge_created,
        "proposals_created": proposals_created,
        "status": "completed",
    }


if __name__ == "__main__":
    result = run_cycle()
    print(f"Market Learning Cycle: {result['lessons_created']} lessons, {result['knowledge_created']} knowledge, {result['proposals_created']} proposals")