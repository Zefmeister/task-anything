import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Export TaskViewWindow class explicitly
__all__ = ['TaskViewWindow']

class TaskViewWindow:
    """Task view window for displaying and managing tasks"""
    def __init__(self, parent, task_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Task View")
        self.task_manager = task_manager
        self.setup_gui()
        
    def setup_gui(self):
        # Add filter frame
        filter_frame = ttk.Frame(self.window)
        filter_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'Pending', 'Completed'])
        self.status_filter.set('All')
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_tasks())
        
        # Create treeview
        columns = ('Type', 'Priority', 'Due Date', 'Description', 'Status', 'Created')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings')
        
        # Set column headings and widths
        widths = {'Type': 100, 'Priority': 60, 'Due Date': 100, 
                 'Description': 300, 'Status': 80, 'Created': 150}
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=widths.get(col, 100))
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack widgets
        self.tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        y_scrollbar.grid(row=1, column=1, sticky='ns')
        x_scrollbar.grid(row=2, column=0, sticky='ew')
        
        # Buttons frame
        btn_frame = ttk.Frame(self.window)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        complete_btn = ttk.Button(btn_frame, text="Mark Complete", command=self.complete_task)
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(btn_frame, text="↻ Refresh", command=self.load_tasks)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        # Set window size
        self.window.geometry('800x600')
        
        # Load tasks
        self.load_tasks()
        
    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        status_filter = self.status_filter.get()
        for task in self.task_manager.tasks:
            if status_filter != 'All' and task['status'].capitalize() != status_filter:
                continue
                
            created_at = datetime.fromisoformat(task['created_at']).strftime('%Y-%m-%d %H:%M')
            values = (
                task['type'],
                task['priority'],
                task['due_date'],
                task['description'][:50] + '...' if len(task['description']) > 50 else task['description'],
                task['status'].capitalize(),
                created_at
            )
            
            tags = ('completed',) if task['status'] == 'completed' else ()
            self.tree.insert('', tk.END, values=values, tags=(task['id'],) + tags)
        
        # Configure tag colors
        self.tree.tag_configure('completed', foreground='gray')
    
    def sort_by(self, col):
        """Sort treeview when column header is clicked"""
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        items.sort()
        
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to complete")
            return
            
        task_id = self.tree.item(selected[0], 'tags')[0]
        self.task_manager.complete_task(task_id)
        self.load_tasks()  # Refresh view
