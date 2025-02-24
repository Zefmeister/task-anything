import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

__all__ = ['NotificationManager']

class NotificationManager:
    def __init__(self, task_manager=None):
        self.reminder_thread = None
        self.task_manager = task_manager
    
    def start_reminder_thread(self):
        self.reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def reminder_loop(self):
        while True:
            now = datetime.now()
            # Check for pending tasks at 9 AM daily
            if now.hour == 9 and now.minute == 0:
                self.show_daily_reminder()
            time.sleep(60)  # Check every minute
    
    def show_daily_reminder(self):
        if not self.task_manager:
            return
            
        pending_tasks = self.task_manager.get_pending_tasks()
        if not pending_tasks:
            return
            
        task_summary = "\n".join([
            f"- {task['type']}: {task['description'][:50]}..."
            for task in pending_tasks[:5]
        ])
        
        if len(pending_tasks) > 5:
            task_summary += f"\n...and {len(pending_tasks) - 5} more"
        
        messagebox.showinfo(
            "Daily Reminder", 
            f"You have {len(pending_tasks)} pending tasks:\n\n{task_summary}"
        )
