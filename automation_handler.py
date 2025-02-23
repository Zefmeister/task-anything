import subprocess
import os
from tkinter import messagebox
try:
    from copilot_prompts import get_email_prompt
except ImportError:
    # Fallback if module not found
    def get_email_prompt(task_data):
        return task_data.get('description', '')

GITHUB_AVAILABLE = False
try:
    from github import Github
    GITHUB_AVAILABLE = True
except ImportError:
    print("Warning: PyGithub not installed. PR review features will be disabled.")

class AutomationHandler:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.gh_client = None
        
        if GITHUB_AVAILABLE and self.github_token:
            try:
                self.gh_client = Github(self.github_token)
            except Exception as e:
                print(f"Failed to initialize GitHub client: {e}")
    
    def handle_task(self, task_data):
        task_type = task_data['type']
        handlers = {
            "Script Automation": self.handle_script_task,
            "Email": self.handle_email_task,
            "Meeting": self.handle_meeting_task,
            "PR Review": self.handle_pr_task
        }
        handler = handlers.get(task_type)
        if handler:
            handler(task_data)
    
    def handle_script_task(self, task_data):
        description = task_data['description']
        # Open VSCode with the task description
        subprocess.run(['code', '--new-window', '--wait'])
        # TODO: Implement Copilot interaction
    
    def handle_email_task(self, task_data):
        print(f"Starting email task automation: {task_data}")
        description = task_data['description']
        
        try:
            # Use absolute path for temp file
            temp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'email_draft.txt'))
            os.makedirs(os.path.dirname(temp_file), exist_ok=True)
            
            # Create prompt for VSCode
            email_text = f"""// Task: Write a professional email
// Input: {description}
// Instructions: Write your response below this line
// ----------------------------------------

"""
            # Write to file and ensure it exists
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(email_text)
            
            print(f"Created temp file at: {temp_file}")
            
            # Try multiple ways to launch VSCode
            try:
                # Try direct command first
                result = subprocess.run(['code', '--new-window', '--wait', temp_file], 
                                     check=True, capture_output=True, text=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback to full path on Windows
                if os.name == 'nt':
                    vscode_path = os.path.join(os.environ.get('LOCALAPPDATA', ''),
                                             'Programs', 'Microsoft VS Code', 'Code.exe')
                    if os.path.exists(vscode_path):
                        result = subprocess.run([vscode_path, '--new-window', '--wait', temp_file],
                                             check=True, capture_output=True, text=True)
                    else:
                        raise Exception("VSCode not found. Please ensure it's installed.")
            
            # Read result
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    generated_email = f.read()
                    # Remove comments and instructions
                    final_email = generated_email.split('----------------------------------------\n')[-1].strip()
                print("Email content generated successfully")
                return final_email
            else:
                raise Exception("Email file not found after VSCode closed")
            
        except Exception as e:
            print(f"Email task failed: {str(e)}")
            raise Exception(f"Failed to generate email: {str(e)}")
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
    
    def handle_meeting_task(self, task_data):
        # TODO: Implement meeting agenda generation with Copilot
        pass
    
    def handle_pr_task(self, task_data):
        if not GITHUB_AVAILABLE:
            print("PR review feature is not available - PyGithub not installed")
            return
        if not self.gh_client:
            print("PR review feature is not available - No GitHub token provided")
            return
        # TODO: Implement PR review with Copilot
        pass
