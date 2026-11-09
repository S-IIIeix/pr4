# task_app.py (минимальный пример для варианта 1)
import argparse
import json
import sys

class TaskError(Exception):
    pass

class TaskManager:
    def __init__(self, path):
        self.path = path
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self, title, priority="normal"):
        if not title or not title.strip():
            raise TaskError("Название задачи не может быть пустым")
        task = {"id": len(self.tasks) + 1, "title": title.strip(), "priority": priority}
        self.tasks.append(task)
        self._save()
        return task

    def list_tasks(self):
        return self.tasks

def main():
    parser = argparse.ArgumentParser(description="Менеджер задач")
    parser.add_argument("--data", default="tasks.json", help="Путь к файлу данных")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Добавить задачу")
    add.add_argument("title")
    add.add_argument("--priority", default="normal")

    sub.add_parser("list", help="Список задач")

    args = parser.parse_args()
    manager = TaskManager(args.data)

    if args.command == "add":
        task = manager.add_task(args.title, args.priority)
        print(f"Добавлена задача: {task['title']}")
    elif args.command == "list":
        for t in manager.list_tasks():
            print(t)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()