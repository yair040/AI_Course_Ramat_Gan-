"""
Main Entry Point
Gmail Event Scanner & Calendar Integration

Author: Yair Levi
"""

import sys
import os

# Add current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
import auth_manager
import logger_setup
import gmail_scanner
import email_parser
import calendar_manager
import tasks


def main():
    """Main application entry point."""
    try:
        app_config, gmail_service, claude_client, calendar_service = initialize_app()
        
        mode = prompt_user_mode()
        
        if mode == '1':
            tasks.run_one_time_mode(
                app_config, gmail_service, claude_client, calendar_service
            )
        elif mode == '2':
            tasks.run_polling_mode(
                app_config, gmail_service, claude_client, calendar_service
            )
        else:
            print("Invalid selection. Exiting.")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        logger = logger_setup.get_logger()
        logger.critical(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        print("Check the logs for details.")
        sys.exit(1)


def initialize_app():
    """
    Initialize application components.
    
    Returns:
        Tuple of (config, gmail_service, claude_client, calendar_service)
    """
    print("=" * 60)
    print("Gmail Event Scanner & Calendar Integration")
    print("Author: Yair Levi")
    print("=" * 60)
    print()
    
    print("Initializing...")
    
    app_config = config.load_config()
    log_level = app_config.get('system', {}).get('log_level', 'INFO')
    logger = logger_setup.setup_logger(log_level=log_level)
    
    logger.info("Application starting")
    
    print("Authenticating with Google APIs...")
    google_creds = auth_manager.get_google_credentials()
    
    print("Connecting to Gmail...")
    gmail_service = gmail_scanner.build_gmail_service(google_creds)
    
    print("Connecting to Calendar...")
    calendar_service = calendar_manager.build_calendar_service(google_creds)
    
    print("Loading Anthropic API key...")
    api_key = auth_manager.get_anthropic_api_key()
    claude_client = email_parser.initialize_claude_client(api_key)
    
    print("Initialization complete!\n")
    
    return app_config, gmail_service, claude_client, calendar_service


def prompt_user_mode():
    """
    Prompt user to select execution mode.
    
    Returns:
        User's mode selection ('1' or '2')
    """
    print("Select execution mode:")
    print("  [1] One-time mode  - Scan once and exit")
    print("  [2] Polling mode   - Continuous scanning")
    print()
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == '__main__':
    main()
