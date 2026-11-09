import argparse
import json
import os
import sys




DEFAULT_PRIORITY = "normal"
PRIORITIES = ["low", "normal", "high"]
PRIORITY_ORDER = {"high": 0, "normal": 1, "low": 2}
TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(description, priority=DEFAULT_PRIORITY):
    if priority not in PRIORITIES:
        raise ValueError(f"Недопустимый приоритет: {priority}")
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "completed": False,
        "priority": priority
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Задача добавлена: {task}")

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Задача {task_id} отмечена как выполненная")
            return
    print(f"Задача с id={task_id} не найдена")

def filter_tasks(status):
    tasks = load_tasks()
    if status == "completed":
        filtered = [t for t in tasks if t["completed"]]
    elif status == "active":
        filtered = [t for t in tasks if not t["completed"]]
    else:
        filtered = tasks
    for task in filtered:
        print(task)

def list_tasks(sort_by_priority=False):
    tasks = load_tasks()
    if sort_by_priority:
        tasks.sort(key=lambda t: PRIORITY_ORDER.get(t.get("priority", DEFAULT_PRIORITY), 1))
    for task in tasks:
        print(task)

def main():
    parser = argparse.ArgumentParser(description="Учёт задач")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Добавить задачу")
    add_parser.add_argument("description", help="Описание задачи")
    add_parser.add_argument("--priority", choices=PRIORITIES, default=DEFAULT_PRIORITY, help="Приоритет задачи")

    complete_parser = subparsers.add_parser("complete", help="Отметить задачу выполненной")
    complete_parser.add_argument("id", type=int, help="ID задачи")

    list_parser = subparsers.add_parser("list", help="Показать все задачи")
    list_parser.add_argument("--sort", action="store_true", help="Сортировать по приоритету")

    filter_parser = subparsers.add_parser("filter", help="Фильтр по статусу")
    filter_parser.add_argument("status", choices=["all", "active", "completed"], help="Статус задач")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description, args.priority)
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "list":
        list_tasks(args.sort)
    elif args.command == "filter":
        filter_tasks(args.status)

if __name__ == "__main__":
    main()


"Comment"