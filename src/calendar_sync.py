# src/calendar_sync.py
from icalendar import Calendar, Event
import subprocess
from datetime import datetime, timedelta
import os

class CalendarSync:
    def __init__(self):
        self.temp_dir = 'data/calendar'
        os.makedirs(self.temp_dir, exist_ok=True)

    def create_calendar_event(self, task):
        """Crea un evento de calendario para una tarea"""
        cal = Calendar()
        event = Event()
        
        event.add('summary', task.title)
        event.add('description', task.description)
        event.add('dtstart', task.due_date)
        event.add('dtend', task.due_date + timedelta(hours=1))
        
        # Agregar alarma para recordatorio (1 hora antes)
        from icalendar import Alarm
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', f'Recordatorio: {task.title}')
        alarm.add('trigger', timedelta(hours=-1))
        event.add_component(alarm)
        
        cal.add_component(event)
        
        # Guardar el archivo .ics
        file_path = f'{self.temp_dir}/{task.id}.ics'
        with open(file_path, 'wb') as f:
            f.write(cal.to_ical())
        
        # Abrir con la aplicación de Calendario
        subprocess.run(['open', file_path])
        
        return file_path

    def update_calendar_event(self, task):
        """Actualiza un evento existente"""
        # Primero elimina el evento anterior si existe
        self.delete_calendar_event(task)
        # Crea un nuevo evento
        return self.create_calendar_event(task)

    def delete_calendar_event(self, task):
        """Elimina un evento del calendario"""
        if task.calendar_event_id:
            file_path = f'{self.temp_dir}/{task.id}.ics'
            if os.path.exists(file_path):
                os.remove(file_path)