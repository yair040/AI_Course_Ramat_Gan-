"""
Tasks Module - Orchestrates email scanning, parsing, and calendar event creation.
Author: Yair Levi
"""

import time
from datetime import datetime, timedelta
import gmail_scanner
import email_parser
import calendar_manager
import config as config_module
import logger_setup

logger = logger_setup.get_logger()

def process_single_email(email_data, claude_client, calendar_service, 
                         gmail_service, config, mark_read=False):
    """Process single email: parse and create calendar event."""
    try:
        logger.info(f"Processing email: {email_data['subject']}")
        meeting_data = email_parser.parse_email_for_meeting(
            claude_client, email_data['body']
        )
        timezone = config['calendar']['timezone']
        event = calendar_manager.create_event(
            calendar_service, meeting_data, timezone
        )
        if event and mark_read:
            gmail_scanner.mark_as_read(gmail_service, email_data['id'])
        return True
    except Exception as e:
        logger.error(f"Failed to process email {email_data['id']}: {e}")
        return False

def run_one_time_mode(config, gmail_service, claude_client, calendar_service):
    """Run in one-time mode: scan once and exit."""
    logger.info("Starting one-time mode")
    query = get_search_query_from_config(config)
    since_date = get_yesterday_date()
    messages = gmail_scanner.search_emails(gmail_service, query, since_date)
    
    if not messages:
        logger.info("No matching emails found")
        print("\nNo emails found matching the search criteria.")
        return
    
    max_emails = config['system'].get('max_emails_per_scan', 50)
    messages = messages[:max_emails]
    logger.info(f"Processing {len(messages)} emails")
    
    for msg in messages:
        email_data = gmail_scanner.get_email_content(gmail_service, msg['id'])
        process_single_email(
            email_data, claude_client, calendar_service, 
            gmail_service, config, mark_read=False
        )
    logger.info("One-time mode completed")
    print(f"\nProcessed {len(messages)} emails. Check your calendar!")

def run_polling_mode(config, gmail_service, claude_client, calendar_service):
    """Run in polling mode: continuous scanning with intervals."""
    interval = config['polling']['scan_interval_seconds']
    logger.info(f"Starting polling mode (interval: {interval}s)")
    print(f"\nPolling mode active. Scanning every {interval} seconds.")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            scan_and_process(config, gmail_service, claude_client, 
                           calendar_service, mark_read=True)
            logger.info(f"Sleeping for {interval} seconds")
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Polling mode stopped by user")
        print("\n\nPolling stopped. Goodbye!")

def scan_and_process(config, gmail_service, claude_client, 
                     calendar_service, mark_read=True):
    """Perform single scan and process emails."""
    query = get_search_query_from_config(config)
    since_date = get_yesterday_date()
    messages = gmail_scanner.search_emails(gmail_service, query, since_date)
    
    if not messages:
        logger.debug("No new emails found")
        return
    
    max_emails = config['system'].get('max_emails_per_scan', 50)
    messages = messages[:max_emails]
    
    for msg in messages:
        email_data = gmail_scanner.get_email_content(gmail_service, msg['id'])
        process_single_email(
            email_data, claude_client, calendar_service,
            gmail_service, config, mark_read=mark_read
        )

def get_search_query_from_config(config):
    """Get search query from config."""
    return config_module.get_search_query(config)

def get_yesterday_date():
    """Get yesterday's date."""
    return datetime.now() - timedelta(days=1)
