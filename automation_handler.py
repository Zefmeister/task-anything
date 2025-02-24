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
        print(f"Starting script automation: {task_data}")
        description = task_data['description']
        
        try:
            temp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'script_task.txt'))
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(f"""// Task: Generate script code
// Description: {description}
// Instructions: Use Copilot to generate the code below
// ----------------------------------------

""")
            
            subprocess.run(['code', '--new-window', '--wait', temp_file], check=True)
            return "Script task completed"
        except Exception as e:
            raise Exception(f"Script automation failed: {str(e)}")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
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
        print(f"Starting meeting task automation: {task_data}")
        description = task_data['description']
        
        try:
            # Create temp directory if it doesn't exist
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Parse attendees and agenda
            lines = description.split('\n')
            attendees = next((line for line in lines if line.startswith('Attendees:')), '')
            agenda_items = [line.strip() for line in lines if line.strip().startswith(('1.', '2.', '3.'))]
            
            meeting_notes = f"""Meeting Details:
{attendees}

Agenda:
{chr(10).join(agenda_items)}

Action Items:
1. [To be filled during meeting]
2. [To be filled during meeting]

Notes:
[Space for meeting notes]
"""
            
            temp_file = os.path.join(temp_dir, 'meeting_notes.txt')
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(temp_file), exist_ok=True)
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(meeting_notes)
            
            # Try multiple ways to launch VSCode
            try:
                # Try direct command first
                subprocess.run(['code', '--new-window', '--wait', temp_file], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback to full path on Windows
                if os.name == 'nt':
                    vscode_path = os.path.join(os.environ.get('LOCALAPPDATA', ''),
                                             'Programs', 'Microsoft VS Code', 'Code.exe')
                    if os.path.exists(vscode_path):
                        subprocess.run([vscode_path, '--new-window', '--wait', temp_file], check=True)
                    else:
                        raise Exception("VSCode not found. Please ensure it's installed.")
                else:
                    raise
            
            print("Meeting notes template created")
            return "Meeting task completed"
        except Exception as e:
            raise Exception(f"Meeting automation failed: {str(e)}")
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
    
    def handle_pr_task(self, task_data):
        if not GITHUB_AVAILABLE or not self.gh_client:
            raise Exception("GitHub integration not available")
        
        print(f"Starting PR review automation: {task_data}")
        description = task_data['description']
        
        try:
            # Parse PR URL or number from description
            pr_info = description.split('\n')[0]  # First line should contain PR info
            repo_name = None
            pr_number = None
            
            # Try to parse GitHub URL or repo/PR format
            if 'github.com' in pr_info:
                parts = pr_info.split('/')
                repo_name = f"{parts[-4]}/{parts[-3]}"
                pr_number = int(parts[-1])
            else:
                # Expect format: repo_name#PR_number
                repo_pr = pr_info.split('#')
                if len(repo_pr) == 2:
                    repo_name = repo_pr[0]
                    pr_number = int(repo_pr[1])
            
            if not repo_name or not pr_number:
                raise ValueError("Could not parse repository and PR number")
            
            # Get PR details from GitHub
            repo = self.gh_client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            # Create PR review template
            review_template = f"""PR Review: {pr.title}
URL: {pr.html_url}
Author: {pr.user.login}
Changed Files: {pr.changed_files}

Description:
{pr.body}

Review Notes:
- [ ] Code review completed
- [ ] Tests reviewed
- [ ] Documentation checked

Comments:
[Add review comments here]
"""
            
            temp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pr_review.txt'))
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(review_template)
            
            subprocess.run(['code', '--new-window', '--wait', temp_file], check=True)
            print("PR review template created")
            return "PR review task completed"
        except Exception as e:
            raise Exception(f"PR review automation failed: {str(e)}")
