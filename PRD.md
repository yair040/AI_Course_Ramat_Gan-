# Product Requirements Document (PRD)
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**Version:** 1.0  
**Date:** January 29, 2026  
**Platform:** WSL (Windows Subsystem for Linux)  
**Python Version:** 3.8+

---

## 1. Executive Summary

This application automates the process of scanning Gmail for meeting invitations and automatically adding them to Google Calendar. The system uses AI-powered parsing (via Anthropic's Claude API) to extract meeting details from email content and integrates with both Gmail and Google Calendar APIs.

---

## 2. Project Overview

### 2.1 Purpose
Automate the workflow of:
1. Monitoring Gmail for meeting-related emails
2. Extracting meeting details using AI
3. Creating corresponding calendar events

### 2.2 Target Users
- Professionals managing multiple meeting invitations
- Users who receive meeting details via email
- Anyone wanting to automate email-to-calendar workflows

---

## 3. Technical Architecture

### 3.1 Project Structure
```
gmail_api/
├── __init__.py
├── main.py                 # Entry point
├── tasks.py               # Task orchestration
├── config.py              # Configuration management
├── gmail_scanner.py       # Gmail API integration
├── calendar_manager.py    # Calendar API integration
├── email_parser.py        # AI-powered email parsing
├── auth_manager.py        # Authentication handling
├── logger_setup.py        # Logging configuration
├── config.yaml            # User configuration file
├── requirements.txt       # Dependencies
├── PRD.md                # This document
├── planning.md           # Development planning
├── tasks.md              # Task breakdown
├── Claude.md             # Claude AI integration notes
├── credentials/          # API credentials
│   ├── credentials.json
│   └── token.pickle
└── log/                  # Log files directory
    └── (ring buffer logs)
```

### 3.2 Virtual Environment Location
- Path: `../../venv/` (relative to project root)
- Must be activated before running

### 3.3 External Dependencies Location
- Anthropic API Key: `../../Anthropic_API_Key/`
  - Files: `api_key.dat`, `key.txt`, `key.txt.pub`

---

## 4. Functional Requirements

### 4.1 Authentication & Credentials

#### FR-1.1: Gmail API Authentication
- **Description:** Use existing credentials from `./credentials/`
- **Files:** 
  - `credentials.json` - OAuth 2.0 credentials
  - `token.pickle` - Stored authentication token
- **Scope:** Gmail read/modify, Calendar write

#### FR-1.2: Anthropic API Authentication
- **Description:** Load API key from relative path
- **Location:** `../../Anthropic_API_Key/`
- **Priority Files:** `api_key.dat` → `key.txt` → `key.txt.pub`

### 4.2 Configuration System

#### FR-2.1: Search Criteria Configuration
- **File:** `config.yaml`
- **Parameters:**
  1. **Subject keyword** (string)
  2. **Sender email** (string)
  3. **Label** (string)
  4. **Unread status** (boolean)
- **Requirement:** User must edit before first run

#### FR-2.2: Polling Configuration
- **Parameter:** `scan_interval_seconds` (integer)
- **Description:** Time between scans in polling mode
- **Default:** 300 seconds (5 minutes)

### 4.3 Execution Modes

#### FR-3.1: One-Time Mode
- **Trigger:** User selection at startup
- **Behavior:**
  1. Search for emails matching criteria
  2. If found: Process and exit with success
  3. If not found: Exit with appropriate message
  4. No loop, single execution

#### FR-3.2: Polling Mode
- **Trigger:** User selection at startup
- **Behavior:**
  1. Continuous loop with configured interval
  2. Search for emails matching criteria
  3. Mark processed emails as "read"
  4. Only scan emails from previous day onward
  5. Log each iteration
  6. Graceful shutdown on SIGINT (Ctrl+C)

### 4.4 Email Processing

#### FR-4.1: Gmail Search
- **Criteria Support:**
  - Subject contains keyword
  - From specific sender
  - Has specific label
  - Unread status
- **Date Filter:** Only emails from yesterday onwards
- **Deduplication:** Mark as read to avoid reprocessing

#### FR-4.2: AI-Powered Parsing
- **Service:** Anthropic Claude API
- **Extract:**
  1. **Date** (YYYY-MM-DD)
  2. **Start Time** (HH:MM)
  3. **End Time** (HH:MM)
  4. **Subject/Title** (string)
  5. **Location** (string, optional)
  6. **Description/Details** (string)
- **Input:** Email body (HTML or plain text)
- **Output:** Structured JSON

### 4.5 Calendar Integration

#### FR-5.1: Event Creation
- **API:** Google Calendar API
- **Required Fields:**
  - Summary (from subject)
  - Start datetime
  - End datetime
  - Description
  - Location (if available)
- **Calendar:** Primary calendar
- **Duplicate Prevention:** Check existing events before creating

---

## 5. Non-Functional Requirements

### 5.1 Code Quality

#### NFR-1.1: File Size Limit
- **Constraint:** Maximum 150 lines per Python file
- **Purpose:** Maintainability and readability

#### NFR-1.2: Path Handling
- **Requirement:** Use relative paths exclusively
- **Rationale:** Portability across environments

#### NFR-1.3: Package Structure
- **Requirement:** Proper Python package with `__init__.py`
- **Import Style:** Relative imports within package

### 5.2 Performance

#### NFR-2.1: Multiprocessing
- **Requirement:** Use multiprocessing where applicable
- **Candidates:**
  - Parallel email parsing (if multiple emails)
  - Async API calls

#### NFR-2.2: Resource Management
- **Requirement:** Proper cleanup of resources
- **Includes:** API connections, file handles, processes

### 5.3 Logging

#### NFR-3.1: Log Level
- **Minimum Level:** INFO
- **Levels Used:** DEBUG, INFO, WARNING, ERROR, CRITICAL

#### NFR-3.2: Log Rotation (Ring Buffer)
- **File Count:** 20 files
- **File Size:** 16 MB each
- **Behavior:** Circular overwrite when full
- **Location:** `./log/` subdirectory
- **Naming:** `app.log`, `app.log.1`, `app.log.2`, ..., `app.log.19`

#### NFR-3.3: Log Format
```
%(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(message)s
```

### 5.4 Error Handling

#### NFR-4.1: Graceful Degradation
- **API Failures:** Log and retry with exponential backoff
- **Parse Failures:** Log error, skip email, continue
- **Auth Failures:** Exit with clear error message

#### NFR-4.2: User Feedback
- **Console Output:** Progress indicators and status
- **Error Messages:** Clear, actionable messages

---

## 6. Dependencies

### 6.1 Python Packages
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`
- `anthropic`
- `pyyaml`
- `python-dateutil`
- `pytz`

### 6.2 External Services
- Google Gmail API (v1)
- Google Calendar API (v3)
- Anthropic Claude API (Messages API)

---

## 7. User Interaction Flow

### 7.1 Startup Sequence
```
1. Load configuration from config.yaml
2. Initialize logging system
3. Authenticate with Gmail API (using credentials/)
4. Authenticate with Calendar API (same credentials)
5. Load Anthropic API key from ../../Anthropic_API_Key/
6. Prompt user: "Run mode? [1] One-time [2] Polling"
7. Execute selected mode
```

### 7.2 Processing Flow (Both Modes)
```
1. Search Gmail with configured criteria
2. Filter emails from yesterday onwards
3. For each matching email:
   a. Extract email body
   b. Send to Anthropic API for parsing
   c. Validate extracted meeting details
   d. Check if event already exists in calendar
   e. Create calendar event
   f. Mark email as read (polling mode only)
4. Log results
5. [Polling mode only] Sleep for configured interval, repeat
```

---

## 8. Configuration Example

### 8.1 config.yaml
```yaml
# Gmail Search Criteria (configure ONE of these)
search_criteria:
  subject_keyword: "meeting"      # Search in subject
  sender_email: ""                # Search by sender
  label: ""                       # Search by label
  unread_only: true               # Only unread emails

# Polling Configuration
polling:
  scan_interval_seconds: 300      # 5 minutes

# Calendar Configuration
calendar:
  timezone: "UTC"                 # Default timezone
```

---

## 9. Security Considerations

### 9.1 Credential Storage
- **Gmail/Calendar:** OAuth tokens stored securely in `token.pickle`
- **Anthropic:** API key read from file, never logged
- **Git:** Add credentials/ and API key path to .gitignore

### 9.2 API Rate Limits
- **Gmail API:** Respect quota limits (250 quota units/second/user)
- **Calendar API:** Batch requests when possible
- **Anthropic API:** Implement retry logic with exponential backoff

---

## 10. Testing Strategy

### 10.1 Unit Tests
- Email parsing logic
- Configuration loading
- Date/time handling

### 10.2 Integration Tests
- Gmail API connectivity
- Calendar API connectivity
- Anthropic API connectivity

### 10.3 End-to-End Tests
- Full workflow with test emails
- Polling mode with mock data

---

## 11. Success Criteria

1. ✅ Successfully authenticate with all required APIs
2. ✅ Find emails matching configured criteria
3. ✅ Extract meeting details with >90% accuracy
4. ✅ Create calendar events without duplicates
5. ✅ Run continuously in polling mode without crashes
6. ✅ Proper log rotation with 20-file ring buffer
7. ✅ All files under 150 lines
8. ✅ Clean shutdown on interrupt

---

## 12. Future Enhancements

- Support for recurring meetings
- Email notification on event creation
- Web UI for configuration
- Multiple calendar support
- Meeting conflict detection
- Natural language time parsing improvements

---

## 13. Glossary

- **Ring Buffer:** Circular log file system that overwrites oldest when full
- **OAuth 2.0:** Authentication protocol for Google APIs
- **API Key:** Secret token for Anthropic API access
- **WSL:** Windows Subsystem for Linux
- **venv:** Python virtual environment

---

## 14. Appendix

### A. File Size Compliance
All Python files must adhere to 150-line limit:
- Use helper functions
- Split complex logic into modules
- Leverage imports effectively

### B. Relative Path Examples
```python
# Correct
"../../venv/bin/activate"
"./credentials/token.pickle"
"../../Anthropic_API_Key/api_key.dat"

# Incorrect
"/home/user/gmail_api/credentials/token.pickle"
"C:\\Users\\yair0\\AI_continue\\..."
```

---

**Document Status:** Final  
**Review Status:** Pending Implementation  
**Next Steps:** See planning.md and tasks.md
