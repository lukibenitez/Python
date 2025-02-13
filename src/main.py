# src/main.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from task import Task
from calendar_sync import CalendarSync
from storage import TaskStorage

class TaskOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Tareas")
        self.root.geometry("1000x700")
        
        # Configurar estilo
        self.setup_styles()
        
        # Inicializar servicios
        self.calendar_sync = CalendarSync()
        self.storage = TaskStorage()
        self.tasks = self.storage.load_tasks()
        
        self._create_widgets()
        
    def setup_styles(self):
        # Configurar estilos personalizados
        style = ttk.Style()
        style.configure("Action.TButton", padding=10, font=('Helvetica', 11))
        style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))
        style.configure("Search.TEntry", padding=5)
        
        # Estilos para la tabla
        style.configure("Treeview", rowheight=30, font=('Helvetica', 10))
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'))
        
    def _create_widgets(self):
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Frame superior para búsqueda y filtros
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Búsqueda
        ttk.Label(top_frame, text="Buscar:", style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_tasks)
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, style="Search.TEntry", width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Filtro de prioridad
        ttk.Label(top_frame, text="Prioridad:", style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.priority_filter = ttk.Combobox(top_frame, values=["Todas", "Alta", "Media", "Baja"], width=15)
        self.priority_filter.set("Todas")
        self.priority_filter.pack(side=tk.LEFT, padx=(0, 20))
        self.priority_filter.bind('<<ComboboxSelected>>', self.filter_tasks)
        
        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Button(button_frame, text="✚ Nueva Tarea", 
                  command=self.show_add_task_window, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✎ Editar Tarea", 
                  command=self.edit_selected_task, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✓ Completar Tarea", 
                  command=self.complete_task, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✗ Eliminar Tarea", 
                  command=self.delete_task, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)
        
        # Lista de tareas con scrollbar
        self.create_task_tree(main_frame)
        
        # Estadísticas
        self.create_stats_frame(main_frame)
        
    def create_task_tree(self, parent):
        # Frame para la tabla con scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        parent.rowconfigure(2, weight=1)
        
        # Crear Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                columns=("Título", "Descripción", "Fecha", "Prioridad", "Estado"),
                                show="headings",
                                selectmode="browse")
        
        # Configurar columnas
        self.tree.heading("Título", text="Título")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Fecha", text="Fecha Límite")
        self.tree.heading("Prioridad", text="Prioridad")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("Título", width=200)
        self.tree.column("Descripción", width=300)
        self.tree.column("Fecha", width=150)
        self.tree.column("Prioridad", width=100)
        self.tree.column("Estado", width=100)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        y_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        x_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Colorear filas según prioridad
        self.tree.tag_configure('alta', background='#ffeded')
        self.tree.tag_configure('media', background='#fff9ed')
        self.tree.tag_configure('baja', background='#edffed')
        
    def create_stats_frame(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_labels = {
            'total': ttk.Label(stats_frame, text="Total: 0"),
            'pendientes': ttk.Label(stats_frame, text="Pendientes: 0"),
            'completadas': ttk.Label(stats_frame, text="Completadas: 0")
        }
        
        for i, label in enumerate(self.stats_labels.values()):
            label.grid(row=0, column=i, padx=20)
            
    def filter_tasks(self, *args):
        search_text = self.search_var.get().lower()
        priority_filter = self.priority_filter.get().lower()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Aplicar filtros
        for task in self.tasks:
            if search_text and search_text not in task.title.lower():
                continue
            if priority_filter != "todas" and priority_filter != task.priority:
                continue
                
            self.insert_task_in_tree(task)
            
        self.update_stats()
        
    def insert_task_in_tree(self, task):
        status = "Completada" if task.completed else "Pendiente"
        values = (task.title, task.description, task.due_date.strftime("%Y-%m-%d"),
                 task.priority.capitalize(), status)
        
        self.tree.insert("", tk.END, values=values, tags=(task.priority,))
        
    def update_stats(self):
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        pending = total - completed
        
        self.stats_labels['total'].config(text=f"Total: {total}")
        self.stats_labels['pendientes'].config(text=f"Pendientes: {pending}")
        self.stats_labels['completadas'].config(text=f"Completadas: {completed}")
        
    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione una tarea para eliminar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta tarea?"):
            task_values = self.tree.item(selected_item)['values']
            task_index = next(i for i, task in enumerate(self.tasks) 
                            if task.title == task_values[0])
            
            # Eliminar tarea
            del self.tasks[task_index]
            self.storage.save_tasks(self.tasks)
            self.filter_tasks()
            messagebox.showinfo("Éxito", "Tarea eliminada correctamente")

    def show_add_task_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Nueva Tarea")
        add_window.geometry("500x400")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Frame principal
        frame = ttk.Frame(add_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos
        ttk.Label(frame, text="Título:", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(frame, width=40)
        title_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Descripción:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(frame, width=40)
        desc_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Fecha (YYYY-MM-DD):", style="Header.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(frame, width=40)
        date_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Prioridad:", style="Header.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        priority_var = tk.StringVar(value="media")
        priority_combo = ttk.Combobox(frame, textvariable=priority_var, 
                                    values=["alta", "media", "baja"])
        priority_combo.grid(row=3, column=1, pady=5)
        
        def save_task():
            try:
                due_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
                task = Task(
                    title=title_entry.get(),
                    description=desc_entry.get(),
                    due_date=due_date,
                    priority=priority_var.get()
                )
                self.tasks.append(task)
                self.calendar_sync.create_calendar_event(task)
                self.storage.save_tasks(self.tasks)
                self.filter_tasks()
                add_window.destroy()
                messagebox.showinfo("Éxito", "Tarea agregada correctamente")
            except ValueError as e:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD")
        
        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Guardar", 
                  command=save_task, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", 
                  command=add_window.destroy, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskOrganizerGUI(root)
    root.mainloop()