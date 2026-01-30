"""
Gmail Scanner Module
Handles Gmail API operations for searching and retrieving emails.

Author: Yair Levi
"""

import base64
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import logger_setup

logger = logger_setup.get_logger()


def build_gmail_service(credentials):
    """Build Gmail API service."""
    logger.debug("Building Gmail service")
    return build('gmail', 'v1', credentials=credentials)


def search_emails(service, query, since_date):
    """
    Search for emails matching criteria since given date.
    
    Args:
        service: Gmail API service
        query: Search query string
        since_date: Only emails after this date
    
    Returns:
        List of email message objects
    """
    date_str = since_date.strftime('%Y/%m/%d')
    full_query = f"{query} after:{date_str}"
    
    logger.info(f"Searching emails with query: {full_query}")
    
    try:
        results = service.users().messages().list(
            userId='me',
            q=full_query
        ).execute()
        
        messages = results.get('messages', [])
        logger.info(f"Found {len(messages)} matching emails")
        return messages
        
    except Exception as e:
        logger.error(f"Gmail search failed: {e}")
        raise


def get_email_content(service, email_id):
    """
    Retrieve full email content.
    
    Args:
        service: Gmail API service
        email_id: Email message ID
    
    Returns:
        Dictionary with email metadata and body
    """
    logger.debug(f"Retrieving email {email_id}")
    
    try:
        message = service.users().messages().get(
            userId='me',
            id=email_id,
            format='full'
        ).execute()
        
        headers = message['payload'].get('headers', [])
        subject = next(
            (h['value'] for h in headers if h['name'] == 'Subject'),
            'No Subject'
        )
        
        body = extract_email_body(message['payload'])
        
        return {
            'id': email_id,
            'subject': subject,
            'body': body
        }
        
    except Exception as e:
        logger.error(f"Failed to retrieve email {email_id}: {e}")
        raise


def extract_email_body(payload):
    """Extract and clean email body from payload."""
    body = ''
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body = decode_body(part['body'].get('data', ''))
                break
            elif part['mimeType'] == 'text/html':
                html = decode_body(part['body'].get('data', ''))
                body = clean_html(html)
    elif 'body' in payload:
        body = decode_body(payload['body'].get('data', ''))
    
    return body


def decode_body(data):
    """Decode base64 email body."""
    if not data:
        return ''
    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')


def clean_html(html_text):
    """Remove HTML tags from email body."""
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


def mark_as_read(service, email_id):
    """Mark email as read."""
    logger.debug(f"Marking email {email_id} as read")
    
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return True
        
    except Exception as e:
        logger.warning(f"Failed to mark email {email_id} as read: {e}")
        return False


def get_yesterday_date():
    """Get date for yesterday (for filtering)."""
    return datetime.now() - timedelta(days=1)
