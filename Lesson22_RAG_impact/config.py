"""Configuration constants for Context Window vs RAG comparison."""

import os

# ============================================================================
# Paths
# ============================================================================
DOCS_DIR = "./docs"
LOG_DIR = "./log"
RESULTS_DIR = "./results"
API_KEY_FILE = "./api_key.dat"
VECTOR_DB_DIR = "./vector_db"

# ============================================================================
# API Settings
# ============================================================================
MODEL_NAME = "claude-3-5-haiku-20241022"  # Haiku 3.5 for cost optimization
MAX_TOKENS = 1024                          # Maximum tokens for response
API_TIMEOUT = 120                          # API timeout in seconds
MAX_RETRIES = 3                            # Number of retry attempts
RETRY_DELAY = 40                           # Seconds between queries (rate limiting)

# ============================================================================
# RAG Settings
# ============================================================================
CHUNK_SIZE = 500                           # Words per chunk
CHUNK_OVERLAP = 50                         # Word overlap between chunks
TOP_K_CHUNKS = 3                           # Number of chunks to retrieve
EMBEDDING_MODEL = "all-MiniLM-L6-v2"      # Fast and efficient embedding model

# ============================================================================
# Test Settings
# ============================================================================
ITERATIONS = 3                             # Number of test iterations per method
QUERY = "What are the side effects of taking calcium carbonate?"

# ============================================================================
# Logging Settings
# ============================================================================
LOG_LEVEL = "INFO"                         # Minimum log level
LOG_MAX_BYTES = 16 * 1024 * 1024          # 16MB per log file
LOG_BACKUP_COUNT = 19                      # 19 backups + 1 active = 20 total files
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# Visualization Settings
# ============================================================================
DPI = 300                                  # Resolution for saved graphs
FIGURE_SIZE = (10, 6)                      # Figure size in inches (width, height)
OUTPUT_DIR = "."                           # Directory for output files

# ============================================================================
# Cost Settings (USD per million tokens)
# ============================================================================
COST_PER_MILLION_INPUT = 0.80             # Input token cost (Haiku 3.5)
COST_PER_MILLION_OUTPUT = 4.00            # Output token cost (Haiku 3.5)

# ============================================================================
# Helper Functions
# ============================================================================

def ensure_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
