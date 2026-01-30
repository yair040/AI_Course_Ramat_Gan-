"""
Configuration Management Module
Loads and validates configuration from YAML file.

Author: Yair Levi
"""

import os
import yaml
import logger_setup

logger = logger_setup.get_logger()


def load_config(config_path=None):
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file (default: ./config.yaml)
    
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    
    logger.info(f"Loading configuration from {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        validate_config(config)
        logger.info("Configuration loaded successfully")
        return config
        
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML format: {e}")
        raise


def validate_config(config):
    """
    Validate configuration structure and values.
    
    Args:
        config: Configuration dictionary
    
    Raises:
        ValueError: If configuration is invalid
    """
    required_sections = ['search_criteria', 'polling', 'calendar']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required section: {section}")
    
    criteria = config['search_criteria']
    active_criteria = sum([
        bool(criteria.get('subject_keyword')),
        bool(criteria.get('sender_email')),
        bool(criteria.get('label')),
        criteria.get('unread_only', False)
    ])
    
    if active_criteria == 0:
        raise ValueError("At least one search criterion must be configured")
    
    if config['polling']['scan_interval_seconds'] <= 0:
        raise ValueError("Scan interval must be positive")
    
    logger.debug("Configuration validation passed")


def get_search_query(config):
    """
    Build Gmail search query from configuration.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Gmail search query string
    """
    criteria = config['search_criteria']
    query_parts = []
    
    if criteria.get('subject_keyword'):
        query_parts.append(f"subject:{criteria['subject_keyword']}")
    
    if criteria.get('sender_email'):
        query_parts.append(f"from:{criteria['sender_email']}")
    
    if criteria.get('label'):
        query_parts.append(f"label:{criteria['label']}")
    
    if criteria.get('unread_only'):
        query_parts.append("is:unread")
    
    query = ' '.join(query_parts)
    logger.debug(f"Generated search query: {query}")
    return query
