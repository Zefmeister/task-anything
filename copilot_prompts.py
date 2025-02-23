def get_email_prompt(task_data):
    """Generate prompt for email suggestions"""
    desc = task_data.get('description', '').strip()
    return f"""Generate a professional email based on this input:
{desc}

Requirements:
- Keep the original To: and Subject: lines if present
- Use clear and professional business tone
- Expand the content to be more detailed and professional
- Add proper greeting and closing
- Add clear action items if applicable

Format as complete email with all components."""
