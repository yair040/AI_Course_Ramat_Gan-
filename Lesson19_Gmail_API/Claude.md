# Claude AI Integration Documentation

**Author:** Yair Levi
**Project:** Exercise Checking System
**Version:** 1.0
**Date:** 2025-11-25

---

## Overview

This document describes how Claude AI (via Claude CLI) is integrated into the Exercise Checking System for automated exercise grading and feedback generation.

---

## Claude CLI Agents

The system uses Claude CLI agents for intelligent processing tasks that require natural language understanding and generation.

### Agent Architecture

Each Claude agent is defined in `.claude/agents/` directory with a `.md` file that contains:
- Agent purpose and description
- Input/output specifications
- Processing instructions
- Error handling guidelines

---

## Agent Definitions

### 1. gmail-retrieve Agent

**Location:** `.claude/agents/gmail-retrieve.md`

**Purpose:**
- Retrieve exercise submission emails from Gmail
- Extract GitHub URLs from email content
- Parse email metadata (subject, date, sender)

**Claude Skills Used:**
- Natural language processing for email parsing
- Pattern matching for URL extraction
- Data structuring for CSV output

**Skill File:** `./skills/gmail/skill.md`

**Python Implementation:** `./skills/gmail/email_retrieve.py`

**Key Capabilities:**
- Filter emails by subject pattern: "self checking of exercise #"
- Search within "exercises" folder
- Extract GitHub repository URLs
- Handle various email formats
- Error recovery for malformed emails

**Output:**
- CSV file with pattern: `gmail_extract_*.csv`
- Columns: id, subject, date, URL, status

---

### 2. mail-code-analyzer Agent

**Location:** `.claude/agents/mail-code-analyzer.md`

**Purpose:**
- Clone GitHub repositories from URLs
- Analyze Python code quality
- Calculate grades based on code metrics

**Claude Skills Used:**
- Code analysis and understanding
- Quality assessment
- Metric calculation

**Skill File:** `./skills/url/skill.md`

**Python Implementation:** `./skills/url/analyze_code.py`

**Key Capabilities:**
- Parallel processing (4 URLs simultaneously)
- Repository cloning and file extraction
- Python file identification
- Line counting and analysis
- Grade calculation based on file size metrics

**Grading Algorithm:**
```
grade = (sum_of_lines_in_files_under_150 / total_lines) × 100
```

**Output:**
- CSV file with pattern: `code_analysis_report_*.csv`
- Columns: id, grade, status

---

### 3. greeting-style-generator Agent

**Location:** `.claude/agents/greeting-style-generator.md`

**Purpose:**
- Generate personalized feedback greetings
- Match greeting style to grade level
- Create engaging, character-appropriate messages

**Claude Skills Used:**
- Natural language generation
- Character voice emulation
- Creative writing
- Tone adaptation

**Skill File:** `./skills/style/skill.md`

**Key Capabilities:**
- Grade categorization (4 levels)
- Character style emulation:
  - **Highest Grade:** Donald Trump style
    - Confident, superlative language
    - "Tremendous", "The best", "Fantastic"
    - Enthusiastic and promotional

  - **Second Highest:** Benny Hill style
    - Playful and cheeky
    - Light-hearted humor
    - Encouraging with wit

  - **Third Highest:** Kramer (Seinfeld) style
    - Energetic and quirky
    - Unconventional observations
    - Enthusiastic with odd metaphors

  - **Lowest Grade:** Chandler (Friends) style
    - Sarcastic but supportive
    - Self-deprecating humor
    - Encouraging despite jokes

**Important Features:**
- **Randomization:** Each greeting is unique, not template-based
- **Context-aware:** References coding and exercises
- **Motivational:** Even low grades get encouraging messages

**Output:**
- CSV file with pattern: `personalized_greetings_*.csv`
- Columns: id, greeting

**Example Outputs:**

```
Trump Style (Highest):
"Incredible work! This is absolutely tremendous code - probably the best
I've seen all week. You're going to be a fantastic developer, believe me!"

Benny Hill Style (Second):
"Well done, you clever thing! Your code is almost as neat as my tie -
and that's saying something! Keep up the cheeky good work!"

Kramer Style (Third):
"Hey buddy! Your code is like a pizza - even when it's not perfect,
it's still pretty good! Keep that energy going!"

Chandler Style (Lowest):
"Could this BE any more of a learning opportunity? But seriously,
we all start somewhere. I once wrote code that made my computer cry."
```

---

### 4. gmail-draft-sender Agent

**Location:** `.claude/agents/gmail-draft-sender.md`

**Purpose:**
- Combine data from all previous agents
- Create personalized draft emails
- Format feedback professionally

**Claude Skills Used:**
- Data aggregation from multiple sources
- Email composition
- Professional formatting
- Context integration

**Skill File:** `./skills/send_draft/skill.md`

**Python Implementation:** `./skills/send_draft/send_draft.py`

**Key Capabilities:**
- Read multiple CSV files
- Match data by ID across files
- Compose professional emails
- Create Gmail drafts (not send)
- Handle missing data gracefully

**Email Format:**
```
To: yair040@gmail.com
Subject: self testing

Regarding the [GitHub URL]

Your score is [grade]
[Personalized greeting in character style]
```

**Output:**
- Gmail drafts created in user's account
- Log file documenting all operations

---

## Using Claude Agents

### Command Line Execution

```bash
# From project root directory
cd check_exercise

# Run individual agent
claude agent run gmail-retrieve

# Run with specific skill
claude agent run mail-code-analyzer --skill ./skills/url/skill.md
```

### Programmatic Execution

The `agent_runner.py` module handles agent execution:

```python
from agent_runner import AgentRunner

# Create runner
runner = AgentRunner("greeting-style-generator")

# Execute agent
success = runner.run()

# Wait for completion
if success:
    completed = runner.check_status(timeout=300)
```

---

## Skills vs Agents

### Skills
- Reusable capabilities defined in `./skills/`
- Can be used by multiple agents
- Define specific tasks (email retrieval, code analysis, etc.)
- Include both `.md` documentation and Python implementation

### Agents
- Orchestrate one or more skills
- Defined in `.claude/agents/`
- Add business logic and workflow
- Handle data transformation and output

---

## Data Flow with Claude

```
1. Gmail API
   ↓
2. gmail-retrieve agent (Claude)
   ↓ Parses emails, extracts URLs
   ↓
3. gmail_extract.csv
   ↓
4. mail-code-analyzer agent (Claude)
   ↓ Clones repos, analyzes code
   ↓
5. code_analysis_report.csv
   ↓
6. greeting-style-generator agent (Claude)
   ↓ Categorizes grades, generates greetings
   ↓
7. personalized_greetings.csv
   ↓
8. gmail-draft-sender agent (Claude)
   ↓ Combines data, creates drafts
   ↓
9. Gmail Drafts
```

---

## Configuration

### Agent Configuration (config.json)

Each agent can be configured with:
- `enabled`: Enable/disable agent
- `log_level`: Logging verbosity
- `timeout_seconds`: Execution timeout
- `output_pattern`: Expected output file pattern
- Agent-specific parameters

Example:
```json
{
  "agents": {
    "greeting-style-generator": {
      "enabled": true,
      "log_level": "INFO",
      "timeout_seconds": 300,
      "output_pattern": "personalized_greetings",
      "grade_categories": 4,
      "styles": {
        "highest": "Trump",
        "second": "Benny Hill",
        "third": "Kramer",
        "lowest": "Chandler"
      }
    }
  }
}
```

---

## Logging

All Claude agent interactions are logged:

**Log Files:**
- `./log/agent_gmail_retrieve.log`
- `./log/agent_mail-code-analyzer.log`
- `./log/agent_greeting-style-generator.log`
- `./log/agent_gmail-draft-sender.log`

**Log Information:**
- Agent start/completion times
- Input/output file paths
- Processing steps
- Errors and warnings
- Performance metrics

---

## Error Handling

### Common Issues

**1. Agent Not Found**
```
Error: Unknown agent: agent-name
Solution: Check agent name matches definition in .claude/agents/
```

**2. Skill File Missing**
```
Error: Skill file not found: ./skills/*/skill.md
Solution: Ensure all skill files are present
```

**3. Timeout**
```
Warning: Agent execution timed out
Solution: Increase timeout_seconds in config.json
```

**4. Invalid Output**
```
Error: Output CSV missing required columns
Solution: Check agent skill definition and implementation
```

### Recovery Strategies

1. **Automatic Retry:** Agents can be re-run safely
2. **Manual Intervention:** Review logs and fix issues
3. **Pipeline Resume:** Can resume from any agent in sequence
4. **Data Validation:** Each agent validates its input

---

## Best Practices

### 1. Skill Development
- Keep skills focused and single-purpose
- Document input/output clearly
- Include error handling
- Provide usage examples

### 2. Agent Design
- Make agents stateless where possible
- Use CSV for data persistence
- Include status tracking
- Log all operations

### 3. Testing
- Test agents individually before pipeline
- Verify CSV output format
- Check status field updates
- Validate error handling

### 4. Maintenance
- Keep skill.md files updated
- Document any API changes
- Update examples regularly
- Review logs periodically

---

## Advanced Usage

### Custom Greeting Styles

To add new character styles:

1. Edit `config.json`:
```json
"styles": {
  "highest": "NewCharacter",
  ...
}
```

2. Update `greeting-style-generator` agent definition

3. Add character examples to skill file

### Parallel Agent Execution

For independent agents (not in pipeline):

```python
import multiprocessing
from agent_runner import run_agent

# Run multiple agents in parallel
with multiprocessing.Pool(2) as pool:
    results = pool.map(run_agent,
                      ['agent1', 'agent2'])
```

### Custom Grade Categories

Modify categories in `config.json`:

```json
"greeting-style-generator": {
  "grade_categories": 5,  // Change from 4 to 5
  "styles": {
    "highest": "Style1",
    "second": "Style2",
    "third": "Style3",
    "fourth": "Style4",
    "lowest": "Style5"
  }
}
```

---

## API Reference

### AgentRunner Class

```python
class AgentRunner:
    def __init__(self, agent_name: str)
    def run(self) -> bool
    def check_status(self, timeout: int, poll_interval: int) -> bool
```

### Helper Functions

```python
def run_agent(agent_name: str, wait_for_completion: bool) -> bool
def get_agent_logger(agent_name: str) -> Logger
```

---

## Troubleshooting

### Agent Won't Start

1. Check agent definition exists
2. Verify skill file is present
3. Review agent logs
4. Test skill independently

### Incorrect Output

1. Validate input CSV format
2. Check agent configuration
3. Review skill implementation
4. Test with sample data

### Performance Issues

1. Increase timeout values
2. Check network connectivity
3. Monitor system resources
4. Review parallel processing settings

---

## Security Considerations

### Credentials
- `credentials.json` is never exposed to Claude
- API tokens are handled securely
- No credentials in logs
- No credentials in CSV files

### Data Privacy
- Student emails processed locally
- No data sent to external services (except Gmail API)
- Temporary files cleaned after processing
- Logs can be sanitized if needed

---

## Future Enhancements

### Potential Improvements

1. **More Character Styles:** Add additional feedback personalities
2. **Grade Weighting:** More sophisticated grading algorithms
3. **Sentiment Analysis:** Analyze student questions in emails
4. **Automated Sending:** Option to send emails directly (not just drafts)
5. **Web Interface:** GUI for agent management
6. **Real-time Monitoring:** Dashboard for pipeline progress
7. **A/B Testing:** Test different greeting styles for effectiveness
8. **Multi-language Support:** Generate feedback in multiple languages

---

## Resources

### Documentation
- Claude CLI Documentation: https://docs.anthropic.com/claude/docs
- Gmail API: https://developers.google.com/gmail/api
- GitHub API: https://docs.github.com/en/rest

### Support
- Review agent logs in `./log/`
- Check skill implementations in `./skills/`
- Consult PRD.md for requirements
- See README.md for general usage

---

**Last Updated:** 2025-11-25
**Maintainer:** Yair Levi
