import unittest
import tempfile
import os
import sys
import subprocess
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task_app import TaskManager, TaskError


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.manager = TaskManager(self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_task(self):
        task = self.manager.add_task("Купить молоко", priority="normal")
        self.assertEqual(task["title"], "Купить молоко")

    def test_blank_title_is_rejected(self):
        with self.assertRaises(TaskError):
            self.manager.add_task("", priority="normal")

    def test_whitespace_title_is_rejected(self):
        with self.assertRaises(TaskError):
            self.manager.add_task("   ", priority="normal")

    def test_list_tasks(self):
        self.manager.add_task("A", priority="low")
        self.manager.add_task("B", priority="high")
        self.assertEqual(len(self.manager.list_tasks()), 2)

    def test_search_by_title(self):
        self.manager.add_task("Позвонить маме", priority="normal")
        titles = [t["title"] for t in self.manager.list_tasks()]
        self.assertIn("Позвонить маме", titles)

    def test_persistence(self):
        self.manager.add_task("Сохранить", priority="normal")
        manager2 = TaskManager(self.tmp.name)
        self.assertEqual(len(manager2.list_tasks()), 1)

    def test_help_runs(self):
        result = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "..", "task_app.py"), "--help"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)

    def test_id_increment(self):
        t1 = self.manager.add_task("Первая", priority="normal")
        t2 = self.manager.add_task("Вторая", priority="normal")
        self.assertEqual(t2["id"], t1["id"] + 1)

    def test_json_file_created(self):
        self.manager.add_task("Задача", priority="normal")
        with open(self.tmp.name, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)


if __name__ == "__main__":
    unittest.main()