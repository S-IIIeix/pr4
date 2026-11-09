import unittest
import os
import json
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import task_app

class TestTaskApp(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.orig_tasks_file = task_app.TASKS_FILE
        task_app.TASKS_FILE = os.path.join(self.temp_dir, "tasks.json")
        task_app.save_tasks([])

    def tearDown(self):
        task_app.TASKS_FILE = self.orig_tasks_file
        if os.path.exists(task_app.TASKS_FILE):
            os.remove(task_app.TASKS_FILE)
        os.rmdir(self.temp_dir)

    def test_add_task(self):
        task_app.add_task("Тестовая задача", "high")
        tasks = task_app.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Тестовая задача")
        self.assertEqual(tasks[0]["priority"], "high")
        self.assertFalse(tasks[0]["completed"])

    def test_complete_task(self):
        task_app.add_task("Задача 1")
        task_app.complete_task(1)
        tasks = task_app.load_tasks()
        self.assertTrue(tasks[0]["completed"])

    def test_filter_tasks(self):
        task_app.add_task("Активная")
        task_app.add_task("Выполненная")
        task_app.complete_task(2)
        tasks = task_app.load_tasks()
        active = [t for t in tasks if not t["completed"]]
        completed = [t for t in tasks if t["completed"]]
        self.assertEqual(len(active), 1)
        self.assertEqual(len(completed), 1)

    def test_sort_by_priority(self):
        task_app.add_task("Низкий", "low")
        task_app.add_task("Высокий", "high")
        task_app.add_task("Обычный", "normal")
        tasks = task_app.load_tasks()
        tasks.sort(key=lambda t: task_app.PRIORITY_ORDER.get(t.get("priority", task_app.DEFAULT_PRIORITY), 1))
        self.assertEqual(tasks[0]["priority"], "high")
        self.assertEqual(tasks[1]["priority"], "normal")
        self.assertEqual(tasks[2]["priority"], "low")

if __name__ == "__main__":
    unittest.main()