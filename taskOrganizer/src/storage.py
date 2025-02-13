# src/storage.py
import json
import os
from task import Task

class TaskStorage:
    def __init__(self, filename='data/tasks.json'):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Asegura que el archivo de tareas existe"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def save_tasks(self, tasks):
        """Guarda la lista de tareas en el archivo JSON"""
        tasks_data = [task.to_dict() for task in tasks]
        with open(self.filename, 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def load_tasks(self):
        """Carga las tareas desde el archivo JSON"""
        with open(self.filename, 'r') as f:
            tasks_data = json.load(f)
        return [Task.from_dict(task_data) for task_data in tasks_data]