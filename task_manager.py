import json
from datetime import datetime
import hashlib

__all__ = ['TaskManager']

class TaskManager:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f)
    
    def generate_task_id(self, task_data):
        # Create unique ID from timestamp and task data
        timestamp = datetime.now().isoformat()
        task_str = f"{timestamp}-{task_data['type']}-{task_data['description']}"
        return hashlib.md5(task_str.encode()).hexdigest()
    
    def is_duplicate(self, task_data, time_window=60):
        """Check if similar task was created in the last time_window seconds"""
        now = datetime.now()
        task_type = task_data.get('type', '').strip()
        task_desc = task_data.get('description', '').strip()
        
        if not task_type or not task_desc:
            return False
            
        for task in self.tasks:
            if (task['type'].strip() == task_type and 
                task['description'].strip() == task_desc):
                try:
                    task_time = datetime.fromisoformat(task['created_at'])
                    time_diff = (now - task_time).total_seconds()
                    if time_diff < time_window:
                        return True
                except (ValueError, KeyError):
                    continue
        return False
    
    def add_task(self, task_data):
        # Validate required fields
        if not task_data.get('type') or not task_data.get('description'):
            raise ValueError("Task type and description are required")
            
        if self.is_duplicate(task_data):
            raise ValueError("Similar task was recently created. Please wait before creating again.")
        
        task_data['id'] = self.generate_task_id(task_data)
        task_data['created_at'] = datetime.now().isoformat()
        task_data['status'] = 'pending'
        self.tasks.append(task_data)
        self.save_tasks()
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if task['status'] == 'pending']
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id and task['status'] == 'pending':
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def get_task_counts(self):
        """Get counts of pending and completed tasks"""
        pending = len([t for t in self.tasks if t['status'] == 'pending'])
        completed = len([t for t in self.tasks if t['status'] == 'completed'])
        return {'pending': pending, 'completed': completed}
