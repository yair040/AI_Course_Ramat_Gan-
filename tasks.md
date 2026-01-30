# Tasks Breakdown
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**Project:** Gmail API AI Agent  
**Date:** January 29, 2026

---

## Task Categories

- [x] Documentation
- [ ] Setup & Infrastructure
- [ ] Authentication & Configuration
- [ ] Gmail Integration
- [ ] AI Parsing
- [ ] Calendar Integration
- [ ] Main Application
- [ ] Testing
- [ ] Deployment

---

## DOCUMENTATION ✓

### DOC-001: Create PRD.md ✓
**Status:** Complete  
**Priority:** Critical  
**Estimated Time:** 2 hours  
**Dependencies:** None

**Description:** Comprehensive Product Requirements Document

---

### DOC-002: Create planning.md ✓
**Status:** Complete  
**Priority:** Critical  
**Estimated Time:** 1.5 hours  
**Dependencies:** DOC-001

**Description:** Development strategy and technical planning

---

### DOC-003: Create tasks.md ✓
**Status:** Complete  
**Priority:** Critical  
**Estimated Time:** 1 hour  
**Dependencies:** DOC-001, DOC-002

**Description:** This file - detailed task breakdown

---

### DOC-004: Create Claude.md ✓
**Status:** Complete  
**Priority:** High  
**Estimated Time:** 30 minutes  
**Dependencies:** DOC-001

**Description:** Claude AI integration notes and best practices

---

## SETUP & INFRASTRUCTURE

### INF-001: Create Project Structure
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 30 minutes  
**Dependencies:** None

**Steps:**
1. Create `gmail_api/` directory
2. Create subdirectories:
   - `credentials/`
   - `log/`
3. Create empty Python files:
   - `__init__.py`
   - `main.py`
   - `tasks.py`
   - `config.py`
   - `gmail_scanner.py`
   - `calendar_manager.py`
   - `email_parser.py`
   - `auth_manager.py`
   - `logger_setup.py`

**Verification:**
```bash
tree gmail_api/
```

---

### INF-002: Create requirements.txt
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 15 minutes  
**Dependencies:** None

**Content:**
```
google-auth>=2.25.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.110.0
anthropic>=0.18.0
pyyaml>=6.0.1
python-dateutil>=2.8.2
pytz>=2023.3
```

**Verification:**
```bash
pip install -r requirements.txt --dry-run
```

---

### INF-003: Setup Virtual Environment
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 15 minutes  
**Dependencies:** INF-002

**Steps:**
1. Navigate to `../../` from project root
2. Create venv: `python3 -m venv venv`
3. Activate: `source ../../venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`

**Verification:**
```bash
which python  # Should show venv path
pip list | grep google-api-python-client
```

---

### INF-004: Create .gitignore
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 10 minutes  
**Dependencies:** None

**Content:**
```
# Virtual Environment
../../venv/

# Credentials
credentials/
../../Anthropic_API_Key/

# Logs
log/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Package
*.egg-info/
dist/
build/
```

---

## AUTHENTICATION & CONFIGURATION

### AUTH-001: Implement logger_setup.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 1 hour  
**Dependencies:** INF-001

**Requirements:**
- Ring buffer: 20 files, 16MB each
- Log location: `./log/`
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(message)s`
- Min level: INFO

**Key Functions:**
- `setup_logger()` -> logging.Logger
- Creates log directory if not exists
- Configures RotatingFileHandler

**File Size Target:** < 70 lines

**Test Cases:**
1. Log directory creation
2. File rotation after 16MB
3. Circular overwrite at 20 files

---

### AUTH-002: Implement config.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 1.5 hours  
**Dependencies:** AUTH-001

**Requirements:**
- Load `config.yaml`
- Validate configuration
- Provide defaults
- Type checking

**Key Functions:**
- `load_config(path: str = './config.yaml')` -> dict
- `validate_config(config: dict)` -> bool
- `get_search_query(config: dict)` -> str

**File Size Target:** < 100 lines

**Test Cases:**
1. Valid config loading
2. Invalid config detection
3. Missing file handling
4. Search query generation

---

### AUTH-003: Create config.yaml Template
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 20 minutes  
**Dependencies:** AUTH-002

**Content:**
```yaml
# Gmail Search Criteria (configure ONE)
search_criteria:
  subject_keyword: ""           # e.g., "meeting"
  sender_email: ""              # e.g., "boss@company.com"
  label: ""                     # e.g., "important"
  unread_only: false            # true or false

# Polling Configuration
polling:
  scan_interval_seconds: 300    # Default: 5 minutes

# Calendar Configuration
calendar:
  timezone: "UTC"               # Your timezone

# System Configuration (advanced)
system:
  log_level: "INFO"             # DEBUG, INFO, WARNING, ERROR
  max_emails_per_scan: 50       # Limit per scan
  api_retry_attempts: 3         # Retry count for API calls
```

---

### AUTH-004: Implement auth_manager.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 2 hours  
**Dependencies:** AUTH-001, AUTH-002

**Requirements:**
- Load Gmail/Calendar credentials from `./credentials/`
- Load Anthropic API key from `../../Anthropic_API_Key/`
- Handle token refresh
- Validate credentials

**Key Functions:**
- `get_google_credentials()` -> Credentials
- `get_anthropic_api_key()` -> str
- `refresh_token_if_needed(creds: Credentials)` -> Credentials

**File Size Target:** < 120 lines

**Test Cases:**
1. Load existing token.pickle
2. Handle expired token
3. Load API key from primary file
4. Fallback to alternate API key files

---

## GMAIL INTEGRATION

### GMAIL-001: Implement gmail_scanner.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 3 hours  
**Dependencies:** AUTH-004

**Requirements:**
- Build Gmail service
- Execute search queries
- Retrieve email content
- Mark emails as read
- Filter by date (from yesterday)

**Key Functions:**
- `build_service(credentials)` -> Resource
- `search_emails(service, query: str, since_date: datetime)` -> List[dict]
- `get_email_content(service, email_id: str)` -> dict
- `mark_as_read(service, email_id: str)` -> bool

**File Size Target:** < 140 lines

**Test Cases:**
1. Search with subject keyword
2. Search by sender
3. Search by label
4. Filter unread only
5. Date filtering
6. Mark as read

---

### GMAIL-002: Implement Email Body Extraction
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 1 hour  
**Dependencies:** GMAIL-001

**Requirements:**
- Handle both plain text and HTML
- Decode base64 content
- Clean HTML tags if needed
- Handle multipart messages

**Integration:** Part of `gmail_scanner.py` or helper module

**File Size Target:** < 50 lines (if separate module)

**Test Cases:**
1. Plain text email
2. HTML email
3. Multipart email
4. Empty body handling

---

## AI PARSING

### AI-001: Implement email_parser.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 2.5 hours  
**Dependencies:** AUTH-004

**Requirements:**
- Initialize Anthropic client
- Send email content for parsing
- Extract structured meeting data
- Validate extracted fields
- Handle parsing errors

**Key Functions:**
- `initialize_client(api_key: str)` -> Anthropic
- `parse_email_for_meeting(client, email_body: str)` -> dict
- `validate_meeting_data(data: dict)` -> bool
- `extract_datetime(date_str: str, time_str: str)` -> datetime

**File Size Target:** < 130 lines

**Expected Output Format:**
```json
{
  "date": "2026-02-01",
  "start_time": "10:00",
  "end_time": "11:00",
  "subject": "Team Meeting",
  "location": "Conference Room A",
  "details": "Quarterly review meeting"
}
```

**Test Cases:**
1. Parse complete meeting info
2. Handle missing location
3. Handle ambiguous dates
4. Parse 12/24 hour formats
5. Handle parsing failures gracefully

---

### AI-002: Create Parsing Prompt Template
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 45 minutes  
**Dependencies:** None

**Requirements:**
- Clear instructions for Claude
- JSON output specification
- Handle various email formats
- Timezone considerations

**Integration:** String constant in `email_parser.py`

**Test:** Validate with sample emails

---

## CALENDAR INTEGRATION

### CAL-001: Implement calendar_manager.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 2.5 hours  
**Dependencies:** AUTH-004, AI-001

**Requirements:**
- Build Calendar service
- Create calendar events
- Check for duplicate events
- Handle timezone conversion

**Key Functions:**
- `build_service(credentials)` -> Resource
- `create_event(service, meeting_data: dict)` -> dict
- `check_duplicate_event(service, meeting_data: dict)` -> bool
- `format_event_for_api(meeting_data: dict)` -> dict

**File Size Target:** < 130 lines

**Test Cases:**
1. Create new event
2. Detect duplicate event
3. Handle timezone conversion
4. Handle missing optional fields

---

### CAL-002: Implement Duplicate Detection Logic
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 1 hour  
**Dependencies:** CAL-001

**Requirements:**
- Search for events in time window
- Compare event details
- Handle fuzzy matching

**Integration:** Part of `calendar_manager.py`

**Matching Criteria:**
- Same date and start time (exact)
- Similar subject (fuzzy, 80% match)
- Within ±15 minutes

---

## MAIN APPLICATION

### MAIN-001: Implement tasks.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 3 hours  
**Dependencies:** GMAIL-001, AI-001, CAL-001

**Requirements:**
- Orchestrate all components
- Implement one-time mode
- Implement polling mode
- Handle date filtering
- Implement multiprocessing (if applicable)

**Key Functions:**
- `process_single_email(email_data: dict)` -> bool
- `run_one_time_mode(config: dict)` -> None
- `run_polling_mode(config: dict)` -> None
- `get_yesterday_date()` -> datetime

**File Size Target:** < 145 lines

**Test Cases:**
1. One-time mode: emails found
2. One-time mode: no emails
3. Polling mode: continuous operation
4. Polling mode: graceful shutdown
5. Date filtering accuracy

---

### MAIN-002: Implement main.py
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 1.5 hours  
**Dependencies:** MAIN-001, AUTH-001, AUTH-002, AUTH-004

**Requirements:**
- Entry point for application
- Initialize logging
- Load configuration
- Authenticate services
- Prompt user for mode selection
- Handle top-level errors
- Graceful shutdown

**Key Functions:**
- `main()` -> None
- `prompt_user_mode()` -> str
- `initialize_app()` -> dict
- `cleanup()` -> None

**File Size Target:** < 100 lines

**Test Cases:**
1. Valid mode selection (1)
2. Valid mode selection (2)
3. Invalid mode selection
4. Configuration error handling
5. Authentication error handling
6. Keyboard interrupt (Ctrl+C)

---

### MAIN-003: Implement __init__.py
**Status:** Pending  
**Priority:** Medium  
**Estimated Time:** 30 minutes  
**Dependencies:** All modules

**Requirements:**
- Package initialization
- Version information
- Public API exposure

**Content:**
```python
"""Gmail Event Scanner & Calendar Integration Package"""

__version__ = "1.0.0"
__author__ = "Yair Levi"

from .main import main
from .tasks import run_one_time_mode, run_polling_mode

__all__ = ['main', 'run_one_time_mode', 'run_polling_mode']
```

**File Size Target:** < 20 lines

---

### MAIN-004: Implement Signal Handling
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 45 minutes  
**Dependencies:** MAIN-002

**Requirements:**
- Handle SIGINT (Ctrl+C)
- Handle SIGTERM
- Graceful shutdown in polling mode
- Cleanup resources

**Integration:** Part of `main.py`

**Test:** Interrupt during polling mode

---

## TESTING

### TEST-001: Create Test Email Samples
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 1 hour  
**Dependencies:** None

**Requirements:**
Create 5 sample email bodies:
1. Plain text with clear meeting details
2. HTML formatted meeting invite
3. Ambiguous time format
4. Missing location
5. Multi-paragraph with embedded details

**Location:** `test_data/sample_emails/`

---

### TEST-002: Unit Test - config.py
**Status:** Pending  
**Priority:** Medium  
**Estimated Time:** 1 hour  
**Dependencies:** AUTH-002

**Test Cases:**
- Load valid configuration
- Reject invalid configuration
- Handle missing file
- Validate search criteria
- Generate correct search queries

---

### TEST-003: Unit Test - gmail_scanner.py
**Status:** Pending  
**Priority:** Medium  
**Estimated Time:** 1.5 hours  
**Dependencies:** GMAIL-001

**Test Cases:**
- Build search query correctly
- Parse email list response
- Extract email body (plain text)
- Extract email body (HTML)
- Date filtering logic

---

### TEST-004: Unit Test - email_parser.py
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 2 hours  
**Dependencies:** AI-001, TEST-001

**Test Cases:**
- Parse sample email 1
- Parse sample email 2
- Parse sample email 3
- Parse sample email 4
- Parse sample email 5
- Handle parsing failure
- Validate extracted data

---

### TEST-005: Unit Test - calendar_manager.py
**Status:** Pending  
**Priority:** Medium  
**Estimated Time:** 1.5 hours  
**Dependencies:** CAL-001

**Test Cases:**
- Format event correctly
- Detect duplicate (positive)
- Detect duplicate (negative)
- Handle timezone conversion

---

### TEST-006: Integration Test - Full Workflow
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 2 hours  
**Dependencies:** All modules

**Test Scenario:**
1. Create test email in Gmail
2. Run one-time mode
3. Verify event created in calendar
4. Verify email marked as read
5. Run again (should not duplicate)

---

### TEST-007: Integration Test - Polling Mode
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 1 hour  
**Dependencies:** MAIN-001, MAIN-002

**Test Scenario:**
1. Start in polling mode
2. Create test email
3. Wait for scan interval
4. Verify event creation
5. Send SIGINT
6. Verify graceful shutdown

---

### TEST-008: Test Log Rotation
**Status:** Pending  
**Priority:** Medium  
**Estimated Time:** 30 minutes  
**Dependencies:** AUTH-001

**Test Scenario:**
1. Generate large volume of logs
2. Verify files rotate at 16MB
3. Verify max 20 files maintained
4. Verify oldest overwritten

---

## DEPLOYMENT

### DEP-001: Create Setup Instructions
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 1 hour  
**Dependencies:** All modules complete

**Create README.md with:**
1. Prerequisites
2. Installation steps
3. Configuration guide
4. Usage examples
5. Troubleshooting

---

### DEP-002: Create Run Script
**Status:** Pending  
**Priority:** Medium  
**Estimated Time:** 30 minutes  
**Dependencies:** All modules complete

**Create `run.sh`:**
```bash
#!/bin/bash
cd "$(dirname "$0")"
source ../../venv/bin/activate
python -m gmail_api.main
```

**Make executable:** `chmod +x run.sh`

---

### DEP-003: Verify File Size Compliance
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 1 hour  
**Dependencies:** All Python files complete

**Check each file:**
```bash
wc -l *.py
```

**Ensure all files ≤ 150 lines**

---

### DEP-004: Final Testing on WSL
**Status:** Pending  
**Priority:** Critical  
**Estimated Time:** 2 hours  
**Dependencies:** All modules complete

**Test Checklist:**
- [ ] Virtual environment activation
- [ ] Credentials loaded correctly
- [ ] Configuration file read
- [ ] One-time mode works
- [ ] Polling mode works
- [ ] Logs generated correctly
- [ ] Ctrl+C handling
- [ ] Permissions correct

---

### DEP-005: Create Sample Configuration
**Status:** Pending  
**Priority:** High  
**Estimated Time:** 20 minutes  
**Dependencies:** AUTH-003

**Create `config.example.yaml`:**
- Documented example
- All options explained
- Safe defaults

**User copies to `config.yaml` and edits**

---

## TIMELINE SUMMARY

### Week 1: Core Development
**Days 1-2:** Infrastructure + Authentication (INF, AUTH tasks)  
**Days 3-4:** Gmail + AI Integration (GMAIL, AI tasks)  
**Days 5-6:** Calendar + Main App (CAL, MAIN tasks)  
**Day 7:** Buffer day

### Week 2: Testing + Deployment
**Days 8-9:** Testing (TEST tasks)  
**Day 10:** Deployment + Documentation (DEP tasks)

---

## PROGRESS TRACKING

### Completed Tasks: 4/64
- [x] DOC-001: PRD.md
- [x] DOC-002: planning.md
- [x] DOC-003: tasks.md
- [x] DOC-004: Claude.md

### In Progress: 0
### Blocked: 0
### Not Started: 60

---

## NOTES

### Line Count Strategy
Monitor continuously during development. If approaching 150:
1. Extract helper functions to separate module
2. Remove unnecessary comments
3. Simplify complex expressions
4. Use more compact patterns

### Testing Priority
1. Critical path: Email search → Parse → Create event
2. Error handling: API failures, auth issues
3. Edge cases: Missing fields, duplicate events
4. Performance: Multiprocessing, API rate limits

### Multiprocessing Candidates
- Parallel processing of multiple emails
- Concurrent API calls to Anthropic
- Background polling in separate process

**Avoid multiprocessing for:**
- Single email processing
- Configuration/logging setup
- UI interactions

---

**Last Updated:** January 29, 2026  
**Next Review:** After completing INF tasks
