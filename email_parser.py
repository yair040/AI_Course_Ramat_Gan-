"""
Email Parser Module
AI-powered extraction of meeting details from email content.

Author: Yair Levi
"""

import json
import re
from datetime import datetime, timedelta
from anthropic import Anthropic
import logger_setup

logger = logger_setup.get_logger()

SYSTEM_PROMPT = """You are a specialized email parser that extracts meeting details.

Extract the following information:
- Meeting date (YYYY-MM-DD format)
- Start time (HH:MM format, 24-hour)
- End time (HH:MM format, 24-hour)
- Meeting subject/title
- Location (physical or virtual)
- Additional details/description

Rules:
1. Return only valid JSON
2. Use null for missing information
3. Convert all times to 24-hour format
4. Use ISO date format (YYYY-MM-DD)
5. If no end time, estimate 1 hour duration
6. Extract all relevant context for description
"""


def initialize_claude_client(api_key):
    """Initialize Anthropic client."""
    logger.debug("Initializing Anthropic client")
    return Anthropic(api_key=api_key)


def parse_email_for_meeting(client, email_body):
    """Parse email to extract meeting details using Claude."""
    from datetime import datetime
    import calendar
    
    current_date = datetime.now()
    current_date_str = current_date.strftime('%Y-%m-%d')
    current_day = calendar.day_name[current_date.weekday()]
    
    prompt = f"""Analyze this email and extract meeting details:

EMAIL CONTENT:
{email_body[:2000]}

Return JSON with: {{"date": "YYYY-MM-DD or null", "start_time": "HH:MM or null", "end_time": "HH:MM or null", "subject": "string or null", "location": "string or null", "details": "string or null"}}

CONTEXT: Current date: {current_date_str} ({current_day}). Convert DD/MM/YYYY to YYYY-MM-DD. Use 24-hour time. "Friday 30/1/2026" → "2026-01-30". "10:00 AM" → "10:00".

Return ONLY the JSON object."""
    
    logger.info("Sending email to Claude for parsing")
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        logger.debug(f"Claude response: {response_text}")
        
        meeting_data = extract_meeting_data(response_text)
        validate_meeting_data(meeting_data)
        
        return meeting_data
        
    except Exception as e:
        logger.error(f"Parsing failed: {e}")
        raise


def extract_meeting_data(response_text):
    """Extract JSON from Claude response."""
    json_text = re.sub(r'```json\s*|\s*```', '', response_text)
    
    try:
        data = json.loads(json_text)
        
        required_fields = ['date', 'start_time', 'end_time', 
                          'subject', 'location', 'details']
        for field in required_fields:
            if field not in data:
                data[field] = None
        
        return data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Claude: {e}")


def validate_meeting_data(data):
    """Validate extracted meeting data."""
    if not data.get('date'):
        raise ValueError("Missing meeting date")
    
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {data['date']}")
    
    if data.get('start_time'):
        try:
            datetime.strptime(data['start_time'], '%H:%M')
        except ValueError:
            raise ValueError(f"Invalid start time: {data['start_time']}")
    
    if not data.get('subject'):
        raise ValueError("Missing meeting subject")
    
    logger.info(f"Validated meeting: {data['subject']} on {data['date']}")
