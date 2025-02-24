import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from task_manager import TaskManager
from notification_manager import NotificationManager
from automation_handler import AutomationHandler

class TaskAnythingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Task Anything")
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager(self.task_manager)
        self.automation_handler = AutomationHandler()
        self.create_btn = None
        self.setup_gui()
    
    def setup_gui(self):
        # Add task counter at top
        counter_frame = ttk.Frame(self.root)
        counter_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=5, pady=2)
        
        self.task_counter = ttk.Label(counter_frame, text="")
        self.task_counter.pack(side=tk.RIGHT)
        self.update_task_counter()

        # Labels (shift everything down one row)
        ttk.Label(self.root, text="Task Type:").grid(row=1, column=0, sticky='w', padx=2)
        ttk.Label(self.root, text="Priority:").grid(row=1, column=1, sticky='w', padx=2)
        ttk.Label(self.root, text="Due Date:").grid(row=1, column=2, sticky='w', padx=2)
        ttk.Label(self.root, text="Description:").grid(row=2, column=0, sticky='w', padx=2)

        # Task type selection
        task_types = ["Script Automation", "Email", "Meeting", "PR Review"]
        self.task_type = ttk.Combobox(self.root, values=task_types)
        self.task_type.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        # Priority selection
        priorities = ["H", "M", "L"]
        self.priority = ttk.Combobox(self.root, values=priorities)
        self.priority.grid(row=1, column=1, padx=5, pady=5, sticky='e')
        
        # Due date with calendar
        self.due_date = DateEntry(self.root, width=12, mindate=date.today(), date_pattern='yyyy-mm-dd')
        self.due_date.set_date(date.today())
        self.due_date.grid(row=1, column=2, padx=5, pady=5, sticky='e')
        
        # Task description
        self.description = tk.Text(self.root, height=5)
        self.description.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
        # Button frame for multiple buttons
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Create task button - store reference
        self.create_btn = ttk.Button(button_frame, text="Create Task", command=self.create_task)
        self.create_btn.pack(side=tk.LEFT, padx=5)
        
        # View Tasks button
        view_btn = ttk.Button(button_frame, text="View Tasks", command=self.show_task_view)
        view_btn.pack(side=tk.LEFT, padx=5)
        
        # New task button
        new_btn = ttk.Button(button_frame, text="New Task", command=self.clear_form)
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind task type changes
        self.task_type.bind('<<ComboboxSelected>>', self.on_task_type_change)
    
    def update_task_counter(self):
        """Update the task counter display"""
        counts = self.task_manager.get_task_counts()
        self.task_counter.config(
            text=f"Tasks: {counts['pending']} pending, {counts['completed']} completed"
        )
        # Update every 30 seconds
        self.root.after(30000, self.update_task_counter)

    def clear_form(self):
        self.task_type.set('')
        self.priority.set('')
        self.due_date.set_date(date.today())
        self.description.delete('1.0', tk.END)

    def create_task(self):
        self.create_btn.configure(state='disabled')
        
        try:
            due_date = self.due_date.get_date()
            if due_date < date.today():
                messagebox.showerror("Invalid Date", "Due date cannot be in the past")
                return
            
            task_data = {
                "type": self.task_type.get(),
                "priority": self.priority.get(),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "description": self.description.get("1.0", tk.END).strip()
            }
            
            # First create the task
            self.task_manager.add_task(task_data)
            self.update_task_counter()  # Update counter after adding task
            
            # Only handle automation if task creation was successful
            try:
                print(f"Triggering automation for task type: {task_data['type']}")
                self.automation_handler.handle_task(task_data)
            except Exception as auto_error:
                print(f"Automation error: {str(auto_error)}")
                messagebox.showwarning("Automation Warning", 
                    f"Task created but automation failed: {str(auto_error)}")
            else:
                messagebox.showinfo("Success", "Task created and automated successfully!")
            self.clear_form()
        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create task: {str(e)}")
        finally:
            self.create_btn.configure(state='normal')
    
    def on_task_type_change(self, event=None):
        """Update description template when task type changes"""
        task_type = self.task_type.get()
        if (task_type):
            self.description.delete('1.0', tk.END)
            if task_type == "Email":
                self.description.insert('1.0', "Message content:")
            elif task_type == "Meeting":
                self.description.insert('1.0', "Attendees: [list]\nAgenda:\n1. \n2. ")
    
    def show_task_view(self):
        """Show the task view window"""
        from task_view import TaskViewWindow
        TaskViewWindow(self.root, self.task_manager)
    
    def run(self):
        self.notification_manager.start_reminder_thread()
        self.root.mainloop()

if __name__ == "__main__":
    app = TaskAnythingApp()
    app.run()
