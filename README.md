# Task Anything

A comprehensive task management system with automation capabilities for developers.

## Features

- Task creation and management with priority levels
- Automated task handling for:
  - Script automation with VSCode and GitHub Copilot
  - Email drafting with AI enhancement
  - Meeting agenda generation
  - PR review assistance
- Daily task reminders at 9 AM
- Priority-based task organization (High/Medium/Low)
- Due date tracking
- Task completion tracking
- Task filtering and sorting

## Prerequisites

- Python 3.7+
- VSCode with GitHub Copilot extension
- Git
- GitHub account and personal access token (for PR reviews)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-anything.git
cd task-anything
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\activate   # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Linux/Mac
export GITHUB_TOKEN=your_github_token_here

# Windows (PowerShell)
$env:GITHUB_TOKEN="your_github_token_here"

# Windows (Command Prompt)
set GITHUB_TOKEN=your_github_token_here
```

## Usage

### Starting the Application

```bash
python main.py
```

### Creating Tasks

1. Select task type:
   - **Script Automation**: For code generation tasks
   - **Email**: For drafting emails with AI assistance
   - **Meeting**: For creating meeting agendas
   - **PR Review**: For code review assistance

2. Set priority (H/M/L)
3. Set due date using calendar
4. Enter task description:
   - For emails: Include message content
   - For meetings: List attendees and agenda items
5. Click "Create Task"

### Task Management

- View all tasks using the task view
- Filter tasks by status (Pending/Completed)
- Sort tasks by any column
- Mark tasks as complete
- Track task completion statistics

### Task Types

#### Email Tasks
```
Message content: Your email content here
```
- AI will help enhance the email content
- Professional formatting applied automatically

#### Meeting Tasks
```
Attendees: [list of names]
Agenda:
1. First item
2. Second item
```
- Agenda items automatically formatted
- Meeting summaries generated

## Configuration

### tasks.json Format
```json
{
    "type": "Email/Meeting/Script/PR",
    "priority": "H/M/L",
    "due_date": "YYYY-MM-DD",
    "description": "task_description",
    "status": "pending/completed",
    "created_at": "timestamp",
    "completed_at": "timestamp"  // Only for completed tasks
}
```

### Notification Settings
- Daily reminders at 9 AM
- Task creation confirmations
- Automation status updates

## Development

### Project Structure
```
task-anything/
├── main.py              # Main application entry
├── task_manager.py      # Task management logic
├── automation_handler.py # Task automation
├── notification_manager.py # Notifications
├── task_view.py        # Task viewing UI
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

### Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details