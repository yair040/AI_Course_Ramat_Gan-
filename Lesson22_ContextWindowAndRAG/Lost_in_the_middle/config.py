"""
Configuration Module

Central configuration for the Lost in the Middle experiment.
All paths are relative to the project root.

Author: Yair Levi
"""

from pathlib import Path

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Base directory (project root)
BASE_DIR = Path(__file__).parent

# Subdirectories (relative paths only)
FILES_DIR = BASE_DIR / "files"
LOG_DIR = BASE_DIR / "log"
RESULTS_DIR = BASE_DIR / "results"

# Credential files
API_KEY_FILE = BASE_DIR / "api_key.dat"
TOKEN_FILE = BASE_DIR / "token.pickle"

# ============================================================================
# EXPERIMENT PARAMETERS
# ============================================================================

# Document configuration
DOCUMENT_COUNT = 6
WORD_COUNT_PER_DOCUMENT = 75000
WORDS_PER_PARAGRAPH = 150

# Test configuration
TEST_ITERATIONS = 5
TEST_SENTENCE = "The 6 day war lasted 7 days"
TEST_QUESTION = "How many days did the 6 day war last?"

# Position types
POSITION_TYPES = ["start", "middle", "end"]
DOCUMENTS_PER_POSITION = 2

# Position-specific settings
START_POSITION_RANGE = (1, 5)  # Insert between sentences 1-5
END_POSITION_RANGE = (1, 5)    # Insert within last 5 sentences

# ============================================================================
# API CONFIGURATION
# ============================================================================

# Anthropic API settings
API_MODEL = "claude-3-5-haiku-20241022"  # Claude 3.5 Haiku (latest available)
MAX_TOKENS = 1024
API_TIMEOUT = 60  # seconds

# Rate limiting
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # Base delay for exponential backoff (seconds)

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Ring buffer configuration (20 files × 16MB = 320MB total)
LOG_FILE_NAME = "app.log"
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB per file
LOG_BACKUP_COUNT = 19  # 20 files total (1 current + 19 backups)
LOG_LEVEL = "INFO"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================================================
# ANSWER VALIDATION
# ============================================================================

# Similarity threshold for answer validation
SIMILARITY_THRESHOLD = 0.6

# Keywords to check in responses
EXPECTED_KEYWORDS = ["7", "day"]

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Chart settings
CHART_TITLE = "Lost in the Middle: Information Retrieval Accuracy by Position"
CHART_XLABEL = "Sentence Position"
CHART_YLABEL = "Success Rate (%)"
CHART_COLORS = ["#2ecc71", "#e74c3c", "#3498db"]  # Green, Red, Blue
CHART_DPI = 300
CHART_FIGSIZE = (10, 6)

# Output file names
RESULTS_GRAPH_FILE = "results_graph.png"
STATISTICS_FILE = "statistics.txt"

# ============================================================================
# FILE NAMING
# ============================================================================

# Base document naming pattern
BASE_DOC_PATTERN = "doc_{}.txt"

# Modified document naming patterns
MODIFIED_DOC_PATTERN = "{}_doc_{}.txt"  # {position}_doc_{number}.txt

# ============================================================================
# MULTIPROCESSING
# ============================================================================

# Multiprocessing settings
USE_MULTIPROCESSING = False  # Set to False to avoid API rate limits
MAX_WORKERS = 6  # Maximum parallel workers

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_directories():
    """Create all required directories if they don't exist."""
    FILES_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)


def get_base_document_path(doc_number: int) -> Path:
    """Get path for base document."""
    return FILES_DIR / BASE_DOC_PATTERN.format(doc_number)


def get_modified_document_path(position: str, doc_number: int) -> Path:
    """Get path for modified document with position prefix."""
    return FILES_DIR / MODIFIED_DOC_PATTERN.format(position, doc_number)


def get_document_position_type(filename: str) -> str:
    """Extract position type from filename.

    Args:
        filename: Document filename

    Returns:
        Position type: 'start', 'middle', or 'end'

    Raises:
        ValueError: If position cannot be determined
    """
    filename = Path(filename).name

    for position in POSITION_TYPES:
        if filename.startswith(f"{position}_"):
            return position

    raise ValueError(f"Cannot determine position type from filename: {filename}")


def get_log_file_path() -> Path:
    """Get path to main log file."""
    return LOG_DIR / LOG_FILE_NAME


def get_results_graph_path() -> Path:
    """Get path to results graph file."""
    return RESULTS_DIR / RESULTS_GRAPH_FILE


def get_statistics_path() -> Path:
    """Get path to statistics file."""
    return RESULTS_DIR / STATISTICS_FILE
