import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

__all__ = ['NotificationManager']

class NotificationManager:
    def __init__(self):
        self.reminder_thread = None
    
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
        # TODO: Get pending tasks from TaskManager
        messagebox.showinfo("Daily Reminder", "You have pending tasks!")
