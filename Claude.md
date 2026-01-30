# Claude AI Integration Notes
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**Project:** Gmail API AI Agent  
**Date:** January 29, 2026

---

## Overview

This document contains notes, best practices, and implementation details for integrating Anthropic's Claude AI into the Gmail Event Scanner application.

---

## 1. Claude API Configuration

### 1.1 API Key Management

**Location Strategy:**
The API key is stored in `../../Anthropic_API_Key/` relative to the project root with three possible filenames (priority order):

1. `api_key.dat` (primary)
2. `key.txt` (fallback 1)
3. `key.txt.pub` (fallback 2)

**Loading Logic:**
```python
import os

def load_anthropic_api_key():
    """Load Anthropic API key from multiple possible locations."""
    base_path = os.path.join(os.path.dirname(__file__), 
                             '..', '..', 'Anthropic_API_Key')
    
    key_files = ['api_key.dat', 'key.txt', 'key.txt.pub']
    
    for key_file in key_files:
        key_path = os.path.join(base_path, key_file)
        if os.path.exists(key_path):
            with open(key_path, 'r') as f:
                api_key = f.read().strip()
                if api_key:
                    return api_key
    
    raise FileNotFoundError("No valid Anthropic API key found")
```

### 1.2 Model Selection

**Recommended Model:** `claude-sonnet-4-5-20250929`

**Rationale:**
- High accuracy for structured data extraction
- Good balance of speed and capability
- Cost-effective for repetitive parsing tasks
- Excellent JSON output formatting

**Alternative Models:**
- `claude-opus-4-5-20251101` - For complex/ambiguous emails (higher cost)
- `claude-haiku-4-5-20251001` - For simple, well-formatted emails (lower cost)

---

## 2. Prompt Engineering for Email Parsing

### 2.1 System Prompt Strategy

**Goal:** Extract structured meeting information reliably.

**System Prompt Template:**
```python
SYSTEM_PROMPT = """You are a specialized email parser that extracts meeting details from emails.

Your task is to analyze email content and extract the following information:
- Meeting date (YYYY-MM-DD format)
- Start time (HH:MM format, 24-hour)
- End time (HH:MM format, 24-hour)
- Meeting subject/title
- Location (physical or virtual)
- Additional details/description

IMPORTANT RULES:
1. Always return valid JSON
2. Use null for missing information
3. Convert all times to 24-hour format
4. Use ISO date format (YYYY-MM-DD)
5. If no end time is given, estimate reasonable duration (usually 1 hour)
6. Extract all relevant context for the description field
"""
```

### 2.2 User Prompt Construction

**Best Practices:**
1. Provide clear context
2. Show expected output format
3. Include examples for edge cases
4. Be explicit about null handling

**Prompt Template:**
```python
def build_parsing_prompt(email_body):
    """Construct prompt for Claude to parse email."""
    prompt = f"""
Analyze this email and extract meeting details:

EMAIL CONTENT:
{email_body}

Return a JSON object with this exact structure:
{{
  "date": "YYYY-MM-DD or null",
  "start_time": "HH:MM or null",
  "end_time": "HH:MM or null",
  "subject": "string or null",
  "location": "string or null",
  "details": "string or null"
}}

EXAMPLES:
- "tomorrow at 3pm" → Use actual date for tomorrow, "15:00" for time
- "3pm-4pm" → start_time: "15:00", end_time: "16:00"
- "Zoom link: https://..." → Include in location field
- No end time given → Estimate 1 hour duration

Return ONLY the JSON object, no additional text.
"""
    return prompt
```

### 2.3 Handling Ambiguous Dates

**Strategy:** Use current date as reference point.

**Common Patterns:**
- "tomorrow" → Calculate from current date
- "next Monday" → Find next occurrence
- "the 15th" → Assume current month unless passed
- "3/15" → Assume current year if not specified

**Implementation Consideration:**
Pass current date in prompt:
```python
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')
prompt += f"\n\nCURRENT DATE (for reference): {current_date}"
```

---

## 3. API Integration Implementation

### 3.1 Client Initialization

```python
from anthropic import Anthropic

def initialize_claude_client(api_key):
    """Initialize Anthropic client with API key."""
    return Anthropic(api_key=api_key)
```

### 3.2 Making API Calls

**Basic Call Structure:**
```python
def parse_email_with_claude(client, email_body):
    """Parse email content using Claude API."""
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        temperature=0,  # Deterministic for structured output
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_parsing_prompt(email_body)
            }
        ]
    )
    
    return message.content[0].text
```

### 3.3 Response Parsing

**Handling JSON Response:**
```python
import json
import re

def extract_meeting_data(claude_response):
    """Extract and validate meeting data from Claude response."""
    try:
        # Remove markdown code blocks if present
        json_text = re.sub(r'```json\s*|\s*```', '', claude_response)
        
        # Parse JSON
        meeting_data = json.loads(json_text)
        
        # Validate required fields
        required_fields = ['date', 'start_time', 'end_time', 
                          'subject', 'location', 'details']
        for field in required_fields:
            if field not in meeting_data:
                meeting_data[field] = None
        
        return meeting_data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Claude: {e}")
```

---

## 4. Error Handling & Retry Logic

### 4.1 Common Error Types

**1. Rate Limiting (429)**
```python
from anthropic import RateLimitError
import time

def call_with_retry(client, email_body, max_retries=3):
    """Call Claude API with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return parse_email_with_claude(client, email_body)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise
```

**2. API Errors (500+)**
```python
from anthropic import APIError

try:
    response = parse_email_with_claude(client, email_body)
except APIError as e:
    logger.error(f"Anthropic API error: {e}")
    # Fallback to manual parsing or skip email
```

**3. Authentication Errors (401)**
```python
from anthropic import AuthenticationError

try:
    client = initialize_claude_client(api_key)
except AuthenticationError:
    logger.critical("Invalid Anthropic API key")
    sys.exit(1)
```

### 4.2 Validation of Extracted Data

```python
from datetime import datetime

def validate_meeting_data(data):
    """Validate extracted meeting data."""
    errors = []
    
    # Check date format
    if data['date']:
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            errors.append(f"Invalid date format: {data['date']}")
    else:
        errors.append("Missing date")
    
    # Check time format
    for time_field in ['start_time', 'end_time']:
        if data[time_field]:
            try:
                datetime.strptime(data[time_field], '%H:%M')
            except ValueError:
                errors.append(f"Invalid time format: {data[time_field]}")
    
    # Check required fields
    if not data['subject']:
        errors.append("Missing subject")
    
    return len(errors) == 0, errors
```

---

## 5. Performance Optimization

### 5.1 Caching Strategy

**For Identical Emails:**
```python
import hashlib
import json

cache = {}

def get_email_hash(email_body):
    """Generate hash of email content."""
    return hashlib.sha256(email_body.encode()).hexdigest()

def parse_with_cache(client, email_body):
    """Parse email with caching."""
    email_hash = get_email_hash(email_body)
    
    if email_hash in cache:
        return cache[email_hash]
    
    result = parse_email_with_claude(client, email_body)
    cache[email_hash] = result
    return result
```

### 5.2 Batch Processing

**For Multiple Emails:**
```python
from concurrent.futures import ThreadPoolExecutor

def parse_multiple_emails(client, email_list, max_workers=3):
    """Parse multiple emails concurrently."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(parse_email_with_claude, client, email['body']): email
            for email in email_list
        }
        
        results = []
        for future in futures:
            try:
                parsed = future.result()
                results.append({
                    'email': futures[future],
                    'meeting_data': extract_meeting_data(parsed)
                })
            except Exception as e:
                logger.error(f"Failed to parse email: {e}")
        
        return results
```

### 5.3 Token Optimization

**Reduce Token Usage:**
1. Strip unnecessary email headers
2. Remove quoted replies
3. Clean HTML formatting
4. Limit description length

```python
from bs4 import BeautifulSoup

def clean_email_body(html_body, max_chars=2000):
    """Clean and truncate email body."""
    # Remove HTML tags
    soup = BeautifulSoup(html_body, 'html.parser')
    text = soup.get_text()
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate if too long
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    
    return text
```

---

## 6. Testing Strategies

### 6.1 Test Email Corpus

**Create diverse test cases:**

1. **Simple Plain Text:**
```
Subject: Team Meeting

Hi team,

Let's meet tomorrow at 2pm in Conference Room A for the quarterly review.

Thanks,
Manager
```

2. **HTML Formatted:**
```html
<div>
  <h2>Invitation: Project Kickoff</h2>
  <p><strong>When:</strong> January 30, 2026 at 10:00 AM - 11:30 AM</p>
  <p><strong>Where:</strong> Zoom (link below)</p>
  <p><strong>Description:</strong> Initial project planning session</p>
</div>
```

3. **Ambiguous Time:**
```
Hey, can we chat about the proposal tomorrow afternoon? 
Maybe around 3 or 4?
```

4. **Multiple Events:**
```
Meeting Schedule:
1. Monday 9am - Status update (Room B)
2. Wednesday 2pm - Client call (Zoom)
3. Friday 4pm - Happy hour (Rooftop)
```

5. **Missing Information:**
```
Subject: Quick sync

Let's catch up sometime next week. I'll send a calendar invite.
```

### 6.2 Accuracy Metrics

**Track parsing success:**
```python
def calculate_accuracy(test_results):
    """Calculate parsing accuracy metrics."""
    total = len(test_results)
    successful = sum(1 for r in test_results if r['parsed_correctly'])
    
    field_accuracy = {
        'date': sum(1 for r in test_results if r['date_correct']) / total,
        'time': sum(1 for r in test_results if r['time_correct']) / total,
        'subject': sum(1 for r in test_results if r['subject_correct']) / total,
    }
    
    return {
        'overall': successful / total,
        'by_field': field_accuracy
    }
```

**Target Accuracy:**
- Overall: > 90%
- Date extraction: > 95%
- Time extraction: > 90%
- Subject extraction: > 95%
- Location extraction: > 80%

---

## 7. Cost Management

### 7.1 Cost Estimation

**Claude Sonnet 4.5 Pricing (as of Jan 2026):**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Typical Email:**
- Input: ~500 tokens (email + prompt)
- Output: ~100 tokens (JSON response)
- Cost per email: ~$0.002

**Monthly Estimate:**
- 100 emails/day × 30 days = 3,000 emails/month
- Estimated cost: ~$6/month

### 7.2 Cost Optimization Tips

1. **Reduce prompt verbosity** - Keep prompts concise
2. **Cache results** - Avoid re-parsing identical emails
3. **Filter emails first** - Only parse likely meeting emails
4. **Use Haiku for simple cases** - Switch to cheaper model when appropriate

```python
def select_model_for_email(email_body):
    """Choose appropriate model based on email complexity."""
    # Simple heuristic: check for common meeting keywords
    simple_indicators = ['calendar invite', 'meeting request', 'zoom']
    
    if any(ind in email_body.lower() for ind in simple_indicators):
        return "claude-haiku-4-5-20251001"  # Cheaper
    else:
        return "claude-sonnet-4-5-20250929"  # Default
```

---

## 8. Best Practices Summary

### Do's ✓
- ✓ Use temperature=0 for structured output
- ✓ Validate all extracted data before using
- ✓ Implement retry logic with exponential backoff
- ✓ Cache API responses for identical emails
- ✓ Clean email bodies before sending to API
- ✓ Monitor token usage and costs
- ✓ Test with diverse email formats
- ✓ Handle null/missing values gracefully

### Don'ts ✗
- ✗ Don't send entire email thread (extract relevant part only)
- ✗ Don't skip input validation
- ✗ Don't ignore API errors
- ✗ Don't hard-code API keys in source
- ✗ Don't assume 100% parsing accuracy
- ✗ Don't send sensitive data without necessity
- ✗ Don't exceed rate limits (implement throttling)

---

## 9. Troubleshooting Guide

### Issue: Inconsistent Date Formats

**Problem:** Claude returns dates in various formats.

**Solution:**
```python
from dateutil import parser

def normalize_date(date_str):
    """Normalize various date formats to YYYY-MM-DD."""
    try:
        dt = parser.parse(date_str)
        return dt.strftime('%Y-%m-%d')
    except:
        return None
```

### Issue: Missing End Time

**Problem:** Email doesn't specify meeting duration.

**Solution:**
```python
def add_default_duration(start_time, duration_hours=1):
    """Add default duration if end time missing."""
    from datetime import datetime, timedelta
    
    start = datetime.strptime(start_time, '%H:%M')
    end = start + timedelta(hours=duration_hours)
    return end.strftime('%H:%M')
```

### Issue: Timezone Confusion

**Problem:** Email mentions time without timezone.

**Solution:**
Include user's timezone in prompt:
```python
prompt += f"\n\nAssume timezone: {config['calendar']['timezone']}"
```

---

## 10. Future Enhancements

### 10.1 Advanced Features

1. **Multi-turn Parsing:**
   - Ask clarifying questions if data incomplete
   - Interactive parsing for ambiguous emails

2. **Learning from Corrections:**
   - Store user corrections
   - Fine-tune prompts based on patterns

3. **Context Awareness:**
   - Reference previous meetings
   - Understand recurring patterns

### 10.2 Integration Improvements

1. **Streaming Responses:**
```python
def parse_with_streaming(client, email_body):
    """Use streaming for faster perceived performance."""
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
```

2. **Function Calling:**
   - Use Claude's tool use for structured extraction
   - More reliable than JSON parsing

---

## References

- [Anthropic API Documentation](https://docs.anthropic.com)
- [Claude Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Best Practices for JSON Output](https://docs.anthropic.com/claude/docs/json-output)

---

**Document Status:** Reference Guide  
**Last Updated:** January 29, 2026  
**Maintained By:** Yair Levi
