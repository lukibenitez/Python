# src/task.py
from datetime import datetime
import json
from uuid import uuid4

class Task:
    def __init__(self, title, description, due_date, priority='medium'):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority.lower()
        self.completed = False
        self.created_at = datetime.now()
        self.calendar_event_id = None  # Para sincronización con calendario

    def to_dict(self):
        """Convierte la tarea a un diccionario para almacenamiento"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat(),
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'calendar_event_id': self.calendar_event_id
        }

    @classmethod
    def from_dict(cls, data):
        """Crea una tarea desde un diccionario"""
        task = cls(
            title=data['title'],
            description=data['description'],
            due_date=datetime.fromisoformat(data['due_date']),
            priority=data['priority']
        )
        task.id = data['id']
        task.completed = data['completed']
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.calendar_event_id = data.get('calendar_event_id')
        return task

    def mark_as_completed(self):
        """Marca la tarea como completada"""
        self.completed = True

    def update(self, title=None, description=None, due_date=None, priority=None):
        """Actualiza los campos de la tarea"""
        if title:
            self.title = title
        if description:
            self.description = description
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority.lower()