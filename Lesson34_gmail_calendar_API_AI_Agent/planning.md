# Planning Document
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**Project:** Gmail API AI Agent  
**Date:** January 29, 2026

---

## 1. Development Phases

### Phase 1: Foundation (Days 1-2)
**Goal:** Set up project structure and basic infrastructure

#### Tasks:
1. Create project directory structure
2. Set up virtual environment at `../../venv/`
3. Create `requirements.txt`
4. Initialize logging system with ring buffer
5. Create configuration loader (`config.py`)
6. Implement authentication manager (`auth_manager.py`)

**Deliverables:**
- Working project skeleton
- Functional logging system
- Configuration file template
- Authentication with Gmail/Calendar APIs

---

### Phase 2: Core Functionality (Days 3-5)
**Goal:** Implement main business logic

#### Tasks:
1. Implement Gmail scanner (`gmail_scanner.py`)
   - Search functionality
   - Email retrieval
   - Mark as read functionality
2. Implement calendar manager (`calendar_manager.py`)
   - Event creation
   - Duplicate detection
3. Implement email parser (`email_parser.py`)
   - Anthropic API integration
   - Meeting detail extraction
   - Structured output handling

**Deliverables:**
- Working Gmail search
- AI-powered email parsing
- Calendar event creation

---

### Phase 3: Integration (Days 6-7)
**Goal:** Connect all components

#### Tasks:
1. Create task orchestration (`tasks.py`)
   - One-time mode implementation
   - Polling mode implementation
   - Date filtering logic
2. Create main entry point (`main.py`)
   - User interaction
   - Mode selection
   - Error handling
3. Implement multiprocessing where applicable

**Deliverables:**
- End-to-end workflow
- Both execution modes working
- User-friendly interface

---

### Phase 4: Testing & Refinement (Days 8-9)
**Goal:** Ensure reliability and compliance

#### Tasks:
1. Code review for 150-line compliance
2. Test all error scenarios
3. Verify log rotation
4. Performance optimization
5. Documentation review

**Deliverables:**
- Tested, working application
- All files under 150 lines
- Comprehensive logging

---

### Phase 5: Deployment (Day 10)
**Goal:** Prepare for production use

#### Tasks:
1. Create setup instructions
2. Test on WSL environment
3. Create sample configuration
4. Final documentation

**Deliverables:**
- Production-ready application
- User guide
- Example configurations

---

## 2. Technical Architecture

### 2.1 Module Dependency Graph

```
main.py
  ├─> config.py
  ├─> logger_setup.py
  ├─> auth_manager.py
  └─> tasks.py
        ├─> gmail_scanner.py
        │     └─> auth_manager.py
        ├─> email_parser.py
        │     └─> auth_manager.py (Anthropic)
        └─> calendar_manager.py
              └─> auth_manager.py
```

### 2.2 Data Flow

```
1. User Input (mode selection)
   ↓
2. Configuration Loading (config.yaml)
   ↓
3. Authentication (Gmail, Calendar, Anthropic)
   ↓
4. Gmail Search (search criteria)
   ↓
5. Email Retrieval (matching emails)
   ↓
6. AI Parsing (Anthropic API)
   ↓
7. Event Creation (Calendar API)
   ↓
8. Email Marking (read status)
   ↓
9. Logging & Status Update
   ↓
10. [Polling] Sleep → Repeat from step 4
```

---

## 3. Implementation Strategy

### 3.1 File Size Management

**Strategy to stay under 150 lines:**

1. **Separation of Concerns**
   - Each file handles ONE responsibility
   - Use helper functions in separate modules if needed

2. **Minimal Comments**
   - Docstrings for functions only
   - Self-documenting code

3. **Efficient Imports**
   - Group related imports
   - Use concise import statements

4. **Compact Logic**
   - List comprehensions
   - Ternary operators
   - Function composition

**Example Split:**
```python
# Instead of one 200-line gmail_scanner.py:
gmail_scanner.py (120 lines)
  - Main search logic
  - Email retrieval

gmail_filters.py (80 lines)  # If needed
  - Date filtering
  - Criteria matching
```

### 3.2 Multiprocessing Strategy

**Where to Apply:**

1. **Parallel Email Processing**
   ```python
   from multiprocessing import Pool
   
   with Pool(processes=4) as pool:
       results = pool.map(process_email, email_list)
   ```

2. **Async API Calls**
   - Use `concurrent.futures` for I/O-bound operations
   - Parallel Anthropic API calls for multiple emails

**Where NOT to Apply:**
- Single email processing (overhead > benefit)
- Configuration loading
- Logging operations

### 3.3 Error Handling Strategy

**Hierarchical Error Handling:**

```
Level 1: Function-level (try/except specific errors)
Level 2: Task-level (handle task failures)
Level 3: Main-level (graceful shutdown)
```

**Retry Logic:**
- API calls: 3 retries with exponential backoff
- Network errors: 5 retries with 2^n second delays
- Authentication: Fail fast, no retries

---

## 4. Logging Strategy

### 4.1 Ring Buffer Implementation

**Using `RotatingFileHandler`:**
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    filename='log/app.log',
    maxBytes=16*1024*1024,  # 16 MB
    backupCount=19  # Total 20 files
)
```

### 4.2 Log Levels Usage

| Level    | Usage                                      |
|----------|--------------------------------------------|
| DEBUG    | API request/response details               |
| INFO     | Email found, event created, mode changes   |
| WARNING  | Parsing issues, missing fields             |
| ERROR    | API failures, authentication issues        |
| CRITICAL | Unrecoverable errors, system shutdown      |

### 4.3 Log Message Examples

```python
logger.info("Starting Gmail scan (polling mode, interval: 300s)")
logger.info(f"Found {count} matching emails")
logger.warning(f"Failed to parse email {email_id}: missing date field")
logger.error(f"Gmail API error: {error_msg}")
logger.critical("Authentication failed, exiting")
```

---

## 5. Configuration Management

### 5.1 YAML Structure

```yaml
# Validation: Exactly ONE criteria must be non-empty
search_criteria:
  subject_keyword: ""
  sender_email: ""
  label: ""
  unread_only: false

polling:
  scan_interval_seconds: 300

calendar:
  timezone: "UTC"
  
# Internal use only
system:
  log_level: "INFO"
  max_emails_per_scan: 50
```

### 5.2 Configuration Validation

**Requirements:**
1. At least one search criterion set
2. Scan interval > 0
3. Valid timezone string
4. All required fields present

**Implementation:**
```python
def validate_config(config):
    criteria = config['search_criteria']
    active = sum([
        bool(criteria['subject_keyword']),
        bool(criteria['sender_email']),
        bool(criteria['label']),
        criteria['unread_only']
    ])
    if active == 0:
        raise ValueError("At least one search criterion required")
```

---

## 6. API Integration Details

### 6.1 Gmail API

**Scopes Required:**
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]
```

**Search Query Building:**
```python
# Example queries:
"subject:meeting is:unread after:2026/01/28"
"from:sender@example.com after:2026/01/28"
"label:important is:unread after:2026/01/28"
```

### 6.2 Calendar API

**Scopes Required:**
```python
SCOPES = [
    'https://www.googleapis.com/auth/calendar'
]
```

**Event Structure:**
```python
event = {
    'summary': 'Team Meeting',
    'location': 'Conference Room A',
    'description': 'Quarterly review',
    'start': {
        'dateTime': '2026-02-01T10:00:00',
        'timeZone': 'UTC',
    },
    'end': {
        'dateTime': '2026-02-01T11:00:00',
        'timeZone': 'UTC',
    },
}
```

### 6.3 Anthropic API

**Model:** Claude Sonnet 4.5

**Prompt Strategy:**
```python
prompt = f"""
Extract meeting details from this email:

{email_body}

Return a JSON object with these fields:
- date (YYYY-MM-DD)
- start_time (HH:MM)
- end_time (HH:MM)
- subject (string)
- location (string or null)
- details (string)

If any field cannot be determined, use null.
"""
```

**Response Parsing:**
```python
import json

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

meeting_data = json.loads(response.content[0].text)
```

---

## 7. Testing Plan

### 7.1 Unit Tests

| Module              | Test Cases                                    |
|---------------------|-----------------------------------------------|
| config.py           | Load valid/invalid configs                    |
| gmail_scanner.py    | Build search queries, parse responses         |
| email_parser.py     | Extract details from various email formats    |
| calendar_manager.py | Create events, detect duplicates              |
| auth_manager.py     | Load credentials, refresh tokens              |

### 7.2 Integration Tests

1. **Gmail + Parser:** Search → Parse → Validate
2. **Parser + Calendar:** Parse → Create Event
3. **Full Workflow:** Search → Parse → Create → Mark Read

### 7.3 Test Data

**Sample Emails:**
```
1. Plain text meeting invite
2. HTML formatted invite
3. Ambiguous time formats
4. Missing location
5. Multi-day events
```

---

## 8. Deployment Checklist

- [ ] Virtual environment created at `../../venv/`
- [ ] Dependencies installed from `requirements.txt`
- [ ] Credentials placed in `./credentials/`
- [ ] Anthropic API key at `../../Anthropic_API_Key/`
- [ ] `config.yaml` configured
- [ ] `log/` directory created
- [ ] Permissions verified (WSL file permissions)
- [ ] Test run in one-time mode
- [ ] Test run in polling mode
- [ ] Verify log rotation works
- [ ] Test interrupt handling (Ctrl+C)

---

## 9. Risk Mitigation

### 9.1 Identified Risks

| Risk                          | Impact | Mitigation                                |
|-------------------------------|--------|-------------------------------------------|
| API rate limiting             | High   | Implement exponential backoff             |
| Incorrect parsing             | Medium | Validate all extracted fields             |
| Token expiration              | Medium | Auto-refresh with error handling          |
| Duplicate events              | Low    | Check existing events before creating     |
| File size exceeds 150 lines   | Low    | Continuous monitoring during development  |

### 9.2 Monitoring

**Key Metrics:**
- Emails scanned per hour
- Parsing success rate
- Events created per day
- API error rate
- Log file growth rate

---

## 10. Maintenance Plan

### 10.1 Regular Tasks

**Daily:**
- Monitor log files for errors
- Check API quota usage

**Weekly:**
- Review parsing accuracy
- Update search criteria if needed

**Monthly:**
- Update dependencies
- Review and archive old logs

### 10.2 Upgrade Path

**Version 1.1 (Future):**
- Support for meeting updates/cancellations
- Email response integration
- Attendee management

**Version 2.0 (Future):**
- Web interface
- Multi-user support
- Advanced filtering

---

## 11. Documentation Requirements

### 11.1 Code Documentation

**Docstring Format:**
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description of return value
    """
```

### 11.2 User Documentation

**README.md Contents:**
1. Installation instructions
2. Configuration guide
3. Usage examples
4. Troubleshooting
5. FAQ

---

## 12. Success Metrics

**Definition of Done:**
1. All files ≤ 150 lines
2. All tests passing
3. Both modes working correctly
4. Log rotation functioning
5. Error handling comprehensive
6. Documentation complete

**Performance Targets:**
- Email parsing: < 5 seconds per email
- Calendar event creation: < 2 seconds
- Polling loop overhead: < 1 second
- Memory usage: < 100 MB

---

## Next Steps

1. Review PRD.md and tasks.md
2. Set up development environment
3. Begin Phase 1 implementation
4. Daily progress review against this plan

---

**Document Status:** Living Document  
**Last Updated:** January 29, 2026  
**Next Review:** After Phase 1 completion
