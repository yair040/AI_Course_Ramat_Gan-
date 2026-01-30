"""
Authentication Manager Module
Handles Google API and Anthropic API authentication.

Author: Yair Levi
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import logger_setup

logger = logger_setup.get_logger()

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'
]


def get_google_credentials():
    """
    Load or create Google API credentials.
    
    Returns:
        Google OAuth2 credentials
    """
    creds = None
    creds_dir = os.path.join(os.path.dirname(__file__), 'credentials')
    token_path = os.path.join(creds_dir, 'token.pickle')
    credentials_path = os.path.join(creds_dir, 'credentials.json')
    
    if os.path.exists(token_path):
        logger.info("Loading existing credentials from token.pickle")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials")
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Credentials file not found: {credentials_path}"
                )
            
            logger.info("Initiating OAuth2 flow")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        logger.info("Saving credentials to token.pickle")
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    logger.info("Google credentials ready")
    return creds


def get_anthropic_api_key():
    """
    Load Anthropic API key from file.
    
    Returns:
        Anthropic API key string
    """
    base_path = os.path.join(
        os.path.dirname(__file__), 'Anthropic_API_Key'
    )
    
    key_files = ['api_key.dat', 'key.txt', 'key.txt.pub']
    
    for key_file in key_files:
        key_path = os.path.join(base_path, key_file)
        if os.path.exists(key_path):
            logger.info(f"Loading Anthropic API key from {key_file}")
            with open(key_path, 'r') as f:
                api_key = f.read().strip()
                if api_key:
                    return api_key
    
    raise FileNotFoundError(
        f"No valid Anthropic API key found in {base_path}"
    )
