# Product Requirements Document (PRD)
**Exercise Checking System**

**Author:** Yair Levi
**Version:** 1.0
**Last Updated:** 2025-11-25

---

## 1. Executive Summary

This document outlines the requirements for a Python-based automated exercise checking system that retrieves student submissions from Gmail, analyzes code quality, generates personalized feedback, and sends draft responses. The system uses a multi-agent architecture where each agent performs a specific task in the workflow.

---

## 2. Project Overview

### 2.1 Purpose
Automate the process of retrieving, analyzing, grading, and providing feedback for student exercise submissions received via Gmail.

### 2.2 Scope
- Gmail integration for retrieving exercise submissions
- GitHub URL extraction and code analysis
- Automated grading based on code quality metrics
- Personalized feedback generation in various character styles
- Gmail draft creation for feedback delivery
- Menu-driven interface for individual or pipeline execution

### 2.3 Target Platform
- **Environment:** WSL (Windows Subsystem for Linux)
- **Language:** Python 3.x
- **Execution:** Virtual environment

---

## 3. Technical Architecture

### 3.1 Project Structure
```
check_exercise/
├── __init__.py
├── main.py
├── requirements.txt
├── log/                    # Log files directory
├── files/                  # CSV input/output files
├── temp/                   # Temporary storage for cloned code
├── .claude/
│   └── agents/
│       ├── gmail-retrieve.md
│       ├── mail-code-analyzer.md
│       ├── greeting-style-generator.md
│       └── gmail-draft-sender.md
├── skills/
│   ├── gmail/
│   │   ├── skill.md
│   │   └── email_retrieve.py
│   ├── url/
│   │   └── skill.md
│   ├── style/
│   │   └── skill.md
│   └── send_draft/
│       └── skill.md
└── credentials.json        # Gmail API credentials (excluded from package)
```

### 3.2 Code Organization
- **Package Structure:** Python package with `__init__.py`
- **File Size Limit:** Each Python file should not exceed 150-200 lines
- **Path Handling:** Use relative paths throughout
- **Concurrency:** Implement multiprocessing where applicable

### 3.3 Logging Requirements

#### 3.3.1 Log Configuration
- **Log Level:** INFO and above
- **Log Format:** Ring buffer implementation
- **Buffer Size:** 20 files
- **File Size:** Maximum 16MB per file
- **Behavior:** When the 20th file is full, overwrite the first file
- **Location:** `./log/` subdirectory

#### 3.3.2 Agent-Specific Logging
- Each agent maintains its own log file
- Logs include agent operations, errors, and status updates

---

## 4. Agent Specifications

### 4.1 Agent Common Requirements

Each agent must have:
1. **Input:** CSV file
2. **Output:** CSV file
3. **Configuration:** JSON settings file (log level, etc.)
4. **Logging:** Individual log file
5. **Skill:** Associated skill file for Claude CLI

---

### 4.2 Agent 1: gmail_retrieve

#### 4.2.1 Purpose
Retrieve exercise submission emails from Gmail using specified filters.

#### 4.2.2 Skill
- **Location:** `./skills/gmail/skill.md`
- **Implementation:** `./skills/gmail/email_retrieve.py`
- **API:** Gmail API
- **Credentials:** `credentials.json` (not exposed)

#### 4.2.3 Filter Criteria
- **Subject Filter:** Emails starting with "self checking of exercise #"
- **Folder:** "exercises"

#### 4.2.4 Output
- **Location:** `./files/`
- **Format:** CSV file with columns:
  - `id` (unique identifier, starting from 1)
  - `subject` (email subject)
  - `date` (email date)
  - `URL` (GitHub URL extracted from email)
  - `status` ("done" when all fields are filled)

#### 4.2.5 Agent Definition
- **Location:** `.claude/agents/gmail-retrieve.md`

---

### 4.3 Agent 2: mail-code-analyzer

#### 4.3.1 Purpose
Retrieve code from GitHub URLs, analyze code quality, and calculate grades.

#### 4.3.2 Skill
- **Location:** `./skills/url/skill.md`
- **Concurrency:** Use multiprocessing to process 4 URLs simultaneously

#### 4.3.3 Process
1. Read URLs from gmail_retrieve output CSV
2. Clone GitHub repositories
3. Copy only Python files to temp folder
4. Analyze code files

#### 4.3.4 Grading Algorithm
1. Calculate sum of lines in code files < 150 lines (Result A)
2. Calculate sum of lines in all code files (Result B)
3. Grade = (A / B) × 100

#### 4.3.5 Output
- **Location:** `./files/`
- **Format:** CSV file with columns:
  - `id` (matching id from gmail_retrieve)
  - `grade` (calculated grade)
  - `status` ("done" when all fields are filled)

#### 4.3.6 Agent Definition
- **Location:** `.claude/agents/mail-code-analyzer.md`
- **Implementation:** `./skills/` (specific file to be determined)

---

### 4.4 Agent 3: greeting-style-generator

#### 4.4.1 Purpose
Generate personalized greeting messages based on grade categories.

#### 4.4.2 Skill
- **Location:** `./skills/style/skill.md`

#### 4.4.3 Process
1. Read the latest grades file
2. Divide grades into 4 categories (highest to lowest)
3. Generate random greetings in character-specific styles

#### 4.4.4 Character Styles by Grade Category
- **Highest Grade:** Donald Trump style
- **Second Highest:** Benny Hill style
- **Third Highest:** Kramer (Seinfeld) style
- **Lowest Grade:** Chandler (Friends) style

#### 4.4.5 Output
- **Location:** `./files/`
- **Filename Pattern:** Contains "personalized_greetings"
- **Format:** CSV with:
  - `id` (matching id from previous agents)
  - `greeting` (generated personalized greeting)

#### 4.4.6 Requirements
- Greetings must be randomized (not constant sentences)
- Each greeting reflects the character's distinctive style

#### 4.4.7 Agent Definition
- **Location:** `.claude/agents/greeting-style-generator.md`

---

### 4.5 Agent 4: gmail-draft-sender

#### 4.5.1 Purpose
Create Gmail draft emails with feedback for each student submission.

#### 4.5.2 Skill
- **Location:** `./check_exercise/skills/send_draft/skill.md`
- **API:** Gmail API
- **Credentials:** `credentials.json` (not exposed)

#### 4.5.3 Input Sources
All CSV files located in `./check_exercise/files/`:
1. File containing "personalized_greetings" → greeting and id
2. File containing "code_analysis_report" → grade by id
3. File containing "gmail_extract" → URL by id

#### 4.5.4 Email Format
- **Recipient:** yair040@gmail.com
- **Subject:** "self testing"
- **Body Structure:**
  ```
  Regarding the [GitHub URL as clickable link]

  Your score is [grade]
  [Personalized greeting]
  ```

#### 4.5.5 Skill Parameters
- Email address
- Subject
- URL
- Text to send
- Name

#### 4.5.6 Output
- Creates draft in Gmail account (not sent)

#### 4.5.7 Agent Definition
- **Location:** `.claude/agents/gmail-draft-sender.md`

---

## 5. Main Program Requirements

### 5.1 Menu Interface

The main program must present a menu with the following options:

```
1. Run Agent 1: gmail_retrieve
2. Run Agent 2: mail-code-analyzer
3. Run Agent 3: greeting-style-generator
4. Run Agent 4: gmail-draft-sender
5. Run Pipeline: Execute all agents in sequence
6. Reset: Clean up files and temp directories
```

### 5.2 Menu Option Details

#### 5.2.1 Options 1-4: Individual Agent Execution
- Execute the specified agent independently
- Log all operations
- Display status and results

#### 5.2.2 Option 5: Pipeline Execution
Sequential execution with status checking:
1. Run `gmail_retrieve`
2. Wait for status = "done" in output CSV
3. Run `mail-code-analyzer`
4. Wait for status = "done" in output CSV
5. Run `greeting-style-generator`
6. Wait for status = "done" in output CSV
7. Run `gmail-draft-sender`

#### 5.2.3 Option 6: Reset
1. Delete all contents in `./check_exercise/files/` folder
2. Delete all contents in `./check_exercise/temp/` folder

### 5.3 Logging
- Main program must use logging (INFO level and above)
- Follow ring buffer configuration (20 files × 16MB)

---

## 6. Dependencies

### 6.1 Requirements File
- **File:** `requirements.txt`
- Must include all necessary packages:
  - Gmail API client libraries
  - GitHub API client (if needed)
  - Multiprocessing support
  - Logging utilities
  - CSV handling
  - JSON parsing

---

## 7. Data Flow

```
┌─────────────────────┐
│  Gmail (exercises)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐         ┌────────────────────┐
│  gmail_retrieve     │────────>│ gmail_extract.csv  │
└─────────────────────┘         │ (id, subject,      │
                                │  date, URL,        │
                                │  status)           │
                                └─────────┬──────────┘
                                          │
                                          ▼
                         ┌────────────────────────────┐
                         │  mail-code-analyzer        │
                         │  (clones repos,            │
                         │   analyzes code)           │
                         └─────────────┬──────────────┘
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │ code_analysis_report.csv    │
                         │ (id, grade, status)         │
                         └─────────────┬───────────────┘
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │ greeting-style-generator    │
                         │ (categorizes grades,        │
                         │  generates greetings)       │
                         └─────────────┬───────────────┘
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │ personalized_greetings.csv  │
                         │ (id, greeting)              │
                         └─────────────┬───────────────┘
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │  gmail-draft-sender         │
                         │  (combines data,            │
                         │   creates drafts)           │
                         └─────────────┬───────────────┘
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │  Gmail Drafts               │
                         └─────────────────────────────┘
```

---

## 8. Security Requirements

### 8.1 Credential Management
- `credentials.json` must NOT be exposed
- `token.pickle` must NOT be exposed
- Exclude both files from final package distribution

### 8.2 API Access
- Use Gmail API with proper authentication
- Skills must not expose credentials in logs or outputs

---

## 9. Packaging Requirements

### 9.1 Package Contents
Include all files from `./check_exercise/` folder EXCEPT:
- `credentials.json`
- `token.pickle`

### 9.2 Package Structure
- Create distributable package
- Include all agents, skills, and main program
- Include `requirements.txt`
- Include documentation files

---

## 10. Performance Requirements

### 10.1 Concurrency
- Use multiprocessing for URL retrieval (4 simultaneous connections)
- Optimize for batch processing of multiple submissions

### 10.2 Error Handling
- Graceful handling of API failures
- Retry logic for network operations
- Clear error messages in logs

---

## 11. Success Criteria

### 11.1 Functional Requirements
- ✓ All 4 agents execute independently
- ✓ Pipeline mode executes agents sequentially with proper status checks
- ✓ CSV files generated with correct data
- ✓ Gmail drafts created successfully
- ✓ Reset function clears directories properly

### 11.2 Non-Functional Requirements
- ✓ Ring buffer logging implemented correctly
- ✓ All file size limits respected (150-200 lines per file)
- ✓ Relative paths used throughout
- ✓ Credentials not exposed
- ✓ Code organized as proper Python package

---

## 12. Future Enhancements (Out of Scope)

- Email sending automation (currently creates drafts only)
- Web interface for monitoring
- Database storage for historical data
- Additional character styles for greetings
- Configurable grading algorithms

---

## 13. Assumptions

1. All agents and skills are already implemented and functional
2. Gmail API is properly configured with valid credentials
3. GitHub repositories are publicly accessible
4. Student submissions follow expected format
5. Python files in submissions have `.py` extension

---

## 14. Constraints

1. WSL environment only
2. Python file size limit: 150-200 lines
3. Log file size: 16MB maximum
4. Ring buffer: 20 files
5. Package must not include credentials

---

## 15. Glossary

- **Agent:** An autonomous component that performs a specific task
- **Skill:** A Claude CLI configuration file that defines agent behavior
- **Ring Buffer:** Circular logging system that overwrites oldest files
- **Pipeline:** Sequential execution of all agents with status checking

---

## Appendix A: File Naming Conventions

- **Gmail Extract:** Filename contains "gmail_extract"
- **Code Analysis:** Filename contains "code_analysis_report"
- **Greetings:** Filename contains "personalized_greetings"

---

## Appendix B: Status Values

All CSV files use `status` column with value:
- `"done"` - All fields in the row are successfully filled

---

**End of Document**
