"""
Configuration file for Context Window Size Impact Testing

This module contains all configuration constants used throughout the application.
No logic should be implemented here - only configuration values.

Author: Yair Levi
"""

# ============================================================================
# API Configuration
# ============================================================================

# Path to the file containing the Anthropic API key
API_KEY_FILE = "api_key.dat"

# Claude model to use (Haiku 3.5 for cost efficiency)
MODEL_NAME = "claude-3-5-haiku-20241022"

# Maximum tokens for API response
MAX_TOKENS_RESPONSE = 4096

# API retry configuration
API_MAX_RETRIES = 3
API_RETRY_DELAY = 2  # Base seconds for exponential backoff
RATE_LIMIT_WAIT = 70  # Seconds to wait when hitting rate limit

# Delay between processing documents to avoid rate limits
INTER_DOCUMENT_DELAY = 10  # Seconds to wait between documents

# ============================================================================
# Document Configuration
# ============================================================================

# Target word counts for generated documents
WORD_COUNTS = [2000, 5000, 10000, 20000, 30000, 40000, 50000]

# The sentence to insert in the middle of each document
TARGET_SENTENCE = "The first prime minister of Israel was Ben Gurion"

# Directory where documents will be stored
FILES_DIR = "./files"

# Document naming convention
DOC_NAME_PREFIX = "doc_"
DOC_EXTENSION = ".txt"

# ============================================================================
# Query Configuration
# ============================================================================

# The query to ask Claude about the documents
QUERY_TEXT = "Who was the first Prime Minister of Israel?"

# The expected answer for accuracy validation
EXPECTED_ANSWER = "Ben Gurion was the first Prime Minister of Israel"

# Similarity threshold for determining accuracy (0-1 scale)
SIMILARITY_THRESHOLD = 0.85

# ============================================================================
# Logging Configuration
# ============================================================================

# Directory where log files will be stored
LOG_DIR = "./log"

# Name of the main log file
LOG_FILENAME = "app.log"

# Maximum size of each log file (16MB)
LOG_FILE_SIZE = 16 * 1024 * 1024

# Number of log files in the ring buffer
LOG_FILE_COUNT = 20

# Logging level (INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"

# Log message format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# Visualization Configuration
# ============================================================================

# Output filename for the results graph
OUTPUT_GRAPH = "results_graph.png"

# Graph title
GRAPH_TITLE = "Context Window Size Impact on Query Performance"

# Graph DPI (resolution)
GRAPH_DPI = 300

# Graph figure size (width, height in inches)
GRAPH_FIGSIZE = (12, 8)

# ============================================================================
# Text Generation Configuration
# ============================================================================

# Base Lorem Ipsum text for document generation
LOREM_IPSUM_BASE = """Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur
sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est
laborum Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque
laudantium totam rem aperiam eaque ipsa quae ab illo inventore veritatis et quasi architecto
beatae vitae dicta sunt explicabo Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut
odit aut fugit sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt
Neque porro quisquam est qui dolorem ipsum quia dolor sit amet consectetur adipisci velit sed
quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat
voluptatem"""

# Random seed for reproducibility
RANDOM_SEED = 42

# ============================================================================
# Multiprocessing Configuration
# ============================================================================

# Maximum number of parallel processes for document generation
MAX_PROCESSES = 7
