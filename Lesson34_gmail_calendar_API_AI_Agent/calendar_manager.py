"""
Calendar Manager Module
Handles Google Calendar API operations for event creation.

Author: Yair Levi
"""

from datetime import datetime
from googleapiclient.discovery import build
import logger_setup

logger = logger_setup.get_logger()


def build_calendar_service(credentials):
    """Build Calendar API service."""
    logger.debug("Building Calendar service")
    return build('calendar', 'v3', credentials=credentials)


def create_event(service, meeting_data, timezone='UTC'):
    """
    Create calendar event from meeting data.
    
    Args:
        service: Calendar API service
        meeting_data: Dictionary with meeting details
        timezone: Timezone string
    
    Returns:
        Created event object
    """
    event_body = format_event_for_api(meeting_data, timezone)
    
    if check_duplicate_event(service, event_body):
        logger.warning(f"Event already exists: {meeting_data['subject']}")
        return None
    
    logger.info(f"Creating calendar event: {meeting_data['subject']}")
    
    try:
        event = service.events().insert(
            calendarId='primary',
            body=event_body
        ).execute()
        
        logger.info(f"Event created successfully: {event.get('htmlLink')}")
        return event
        
    except Exception as e:
        logger.error(f"Failed to create event: {e}")
        raise


def format_event_for_api(meeting_data, timezone):
    """
    Format meeting data for Calendar API.
    
    Args:
        meeting_data: Dictionary with meeting details
        timezone: Timezone string
    
    Returns:
        Event dictionary for API
    """
    start_datetime = f"{meeting_data['date']}T{meeting_data['start_time']}:00"
    
    end_time = meeting_data.get('end_time')
    if not end_time:
        start_dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S')
        from datetime import timedelta
        end_dt = start_dt + timedelta(hours=1)
        end_datetime = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
    else:
        end_datetime = f"{meeting_data['date']}T{end_time}:00"
    
    event = {
        'summary': meeting_data['subject'],
        'start': {
            'dateTime': start_datetime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': timezone,
        },
    }
    
    if meeting_data.get('location'):
        event['location'] = meeting_data['location']
    
    if meeting_data.get('details'):
        event['description'] = meeting_data['details']
    
    return event


def check_duplicate_event(service, event_body):
    """Check if similar event already exists."""
    from datetime import datetime
    import pytz
    
    start_time = event_body['start']['dateTime']
    end_time = event_body['end']['dateTime']
    timezone_str = event_body['start'].get('timeZone', 'UTC')
    
    try:
        tz = pytz.timezone(timezone_str)
        start_dt = tz.localize(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S'))
        end_dt = tz.localize(datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S'))
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        for event in events_result.get('items', []):
            if event.get('summary') == event_body['summary']:
                logger.info(f"Duplicate event found: {event_body['summary']}")
                return True
        return False
    except Exception as e:
        logger.warning(f"Duplicate check failed: {e}")
        return False
