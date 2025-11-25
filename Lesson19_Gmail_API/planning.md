# Exercise Checking System - Planning Document

**Author:** Yair Levi
**Project:** Exercise Checking System
**Version:** 1.0
**Date:** 2025-11-25

---

## Executive Summary

This document outlines the planning, architecture decisions, and implementation strategy for the Exercise Checking System - an automated workflow for grading student exercises submitted via Gmail.

---

## Project Goals

### Primary Objectives
1. Automate the retrieval of student exercise submissions from Gmail
2. Clone and analyze Python code from GitHub repositories
3. Generate objective grades based on code quality metrics
4. Create personalized feedback in engaging character styles
5. Automate draft email creation for student feedback

### Success Criteria
- Process multiple submissions in parallel (4 URLs simultaneously)
- Complete full pipeline in under 10 minutes for 4 submissions
- Generate unique, non-template greetings for each student
- Maintain comprehensive logs for debugging and auditing
- Achieve zero manual intervention for standard workflows

---

## Architecture Decisions

### 1. Multi-Agent Architecture

**Decision:** Use separate agents for each major task

**Rationale:**
- **Separation of Concerns:** Each agent has a single, well-defined purpose
- **Modularity:** Agents can be developed and tested independently
- **Reusability:** Skills can be shared across agents
- **Maintainability:** Easier to update or replace individual components
- **Debugging:** Issues can be isolated to specific agents

**Alternatives Considered:**
- Monolithic script: Rejected due to complexity and maintainability issues
- Microservices: Overkill for a local processing system

---

### 2. CSV for Data Exchange

**Decision:** Use CSV files as the primary data exchange format between agents

**Rationale:**
- **Simplicity:** Easy to read, write, and debug
- **Portability:** Works across different tools and languages
- **Human-readable:** Can be inspected manually
- **Excel-compatible:** Can be opened in spreadsheet applications
- **Status tracking:** Easy to add 'status' column for completion tracking

**Alternatives Considered:**
- JSON: More structured but harder to inspect manually
- Database: Too heavy for this use case
- Message queue: Unnecessary complexity for sequential processing

---

### 3. Ring Buffer Logging

**Decision:** Implement 20 files × 16MB ring buffer for logs

**Rationale:**
- **Disk space management:** Prevents unbounded log growth
- **Long-term operation:** System can run indefinitely
- **Debugging history:** Retains recent history for troubleshooting
- **Performance:** No need to compress or archive old logs
- **Simplicity:** Built-in RotatingFileHandler in Python

**Configuration:**
- 20 files = enough history for several weeks of operation
- 16MB per file = sufficient for detailed logging
- Total: 320MB maximum log storage

---

### 4. Python with Virtual Environment

**Decision:** Use Python 3.8+ with virtual environment on WSL

**Rationale:**
- **Gmail API:** Excellent Python client library
- **GitHub API:** PyGithub provides comprehensive access
- **Data Processing:** Pandas excels at CSV manipulation
- **Multiprocessing:** Built-in support for parallel operations
- **WSL Compatibility:** Native Linux environment on Windows

---

### 5. Relative Paths Only

**Decision:** All file paths are relative to project root

**Rationale:**
- **Portability:** System can be moved to any directory
- **Packaging:** Easy to create distributable package
- **Testing:** Can be tested in different environments
- **Deployment:** No hardcoded paths to update

**Implementation:**
```python
BASE_DIR = Path(__file__).parent
FILES_DIR = BASE_DIR / "files"
TEMP_DIR = BASE_DIR / "temp"
```

---

### 6. Package Structure

**Decision:** Organize as proper Python package with `__init__.py`

**Rationale:**
- **Professional:** Follows Python best practices
- **Importable:** Modules can import from each other cleanly
- **Installable:** Can be installed via pip if needed
- **Namespace:** Prevents naming conflicts

---

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Application                        │
│                      (main.py)                              │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Menu System │  │ Agent Runner │  │ Log Manager  │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Agent 1       │   │ Agent 2       │   │ Agent 3       │
│ Gmail         │   │ Code Analyzer │   │ Greeting Gen  │
│ Retrieval     │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────────────────────────────────────────────┐
│              File System (CSV Files)                  │
└───────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────┐
│ Agent 4       │
│ Draft Sender  │
└───────────────┘
```

### Data Flow Architecture

```
Input Layer:
├── Gmail API (Exercise submissions)
└── GitHub API (Student repositories)

Processing Layer:
├── Agent 1: Email parsing and URL extraction
├── Agent 2: Code cloning and analysis
├── Agent 3: Grade categorization and greeting generation
└── Agent 4: Data aggregation and draft creation

Storage Layer:
├── CSV Files (Structured data exchange)
├── Temp Directory (Repository clones)
└── Log Files (Ring buffer)

Output Layer:
└── Gmail Drafts (Feedback emails)
```

---

## Implementation Strategy

### Phase 1: Foundation (Completed)
- ✓ Project structure setup
- ✓ Logging configuration with ring buffer
- ✓ Package initialization
- ✓ Configuration management

### Phase 2: Core Components (Completed)
- ✓ Agent runner framework
- ✓ Status monitoring system
- ✓ Error handling infrastructure
- ✓ Main menu application

### Phase 3: Agent Integration (Pre-existing)
- ✓ Gmail retrieval agent and skill
- ✓ Code analyzer agent and skill
- ✓ Greeting generator agent and skill
- ✓ Draft sender agent and skill

### Phase 4: Testing and Documentation (Completed)
- ✓ PRD documentation
- ✓ README for users
- ✓ Claude.md for AI integration
- ✓ Planning.md (this document)
- ✓ Setup scripts

### Phase 5: Future Enhancements
- Advanced grading algorithms
- Web interface
- Real-time monitoring
- Multi-language support

---

## Module Design

### 1. log_config.py

**Purpose:** Centralized logging configuration

**Key Classes:**
- `RingBufferLogger`: Manages ring buffer configuration

**Features:**
- 20 file rotation
- 16MB per file
- Console and file output
- Per-agent log files

**Design Pattern:** Singleton factory

---

### 2. agent_runner.py

**Purpose:** Agent execution and monitoring

**Key Classes:**
- `AgentRunner`: Manages individual agent lifecycle

**Features:**
- Python script execution
- Claude CLI integration
- Status monitoring
- Timeout handling

**Design Pattern:** Command pattern

---

### 3. main.py

**Purpose:** User interface and workflow orchestration

**Key Classes:**
- `ExerciseCheckingSystem`: Main application controller

**Features:**
- Menu-driven interface
- Individual agent execution
- Pipeline mode
- System reset

**Design Pattern:** Facade pattern

---

## Workflow Design

### Individual Agent Execution

```
1. User selects agent from menu
2. System initializes AgentRunner
3. Agent executes (Python script or Claude CLI)
4. System monitors for completion
5. Status checked via CSV 'done' field
6. Results displayed to user
7. Log entries created
```

### Pipeline Execution

```
1. User selects pipeline mode
2. For each agent in sequence:
   a. Initialize AgentRunner
   b. Execute agent
   c. Wait for status='done' in output CSV
   d. If error: stop pipeline and report
   e. If success: proceed to next agent
3. All agents complete
4. Report success to user
```

### Reset Operation

```
1. User confirms reset
2. Iterate through files/ directory
   a. Delete all files
   b. Delete all subdirectories
3. Iterate through temp/ directory
   a. Delete all files
   b. Delete all subdirectories
4. Log all deletions
5. Confirm completion to user
```

---

## Error Handling Strategy

### Error Categories

**1. Configuration Errors**
- Missing config files
- Invalid JSON
- Missing directories
→ Fail fast, log error, prompt user

**2. Agent Execution Errors**
- Script not found
- Python errors
- Timeout
→ Log error, return failure, allow retry

**3. Data Errors**
- Missing CSV columns
- Invalid data format
- Empty files
→ Log warning, continue with available data

**4. API Errors**
- Gmail API failure
- GitHub API rate limit
- Network issues
→ Log error, retry with exponential backoff

**5. System Errors**
- Disk full
- Permission denied
- Memory issues
→ Log critical, notify user, graceful shutdown

### Recovery Mechanisms

1. **Retry Logic:** Automatic retry for transient errors
2. **Graceful Degradation:** Continue with partial data when possible
3. **State Preservation:** CSV files allow resuming from any point
4. **User Notification:** Clear error messages with actionable advice
5. **Detailed Logging:** All errors logged with full context

---

## Performance Considerations

### Multiprocessing Strategy

**URL Analysis (Agent 2):**
- Process 4 URLs simultaneously
- Use `multiprocessing.Pool(4)`
- Each worker clones and analyzes independently
- Results aggregated in main process

**Benefits:**
- 4x speedup for code analysis
- Better resource utilization
- Reduced total execution time

**Limitations:**
- Limited to 4 concurrent operations
- No multiprocessing for sequential dependencies

### Optimization Opportunities

1. **Caching:** Cache cloned repositories (future enhancement)
2. **Parallel Pipeline:** Run independent pipeline stages in parallel
3. **Incremental Processing:** Process only new submissions
4. **Batch Processing:** Group multiple submissions

---

## Security Planning

### Credential Management

**Gmail API Credentials:**
- Stored in `credentials.json`
- Never committed to version control
- Excluded from package distribution
- Token stored in `token.pickle`
- Both files in `.gitignore`

**Access Control:**
- Read-only access to Gmail
- Draft creation only (no sending)
- Local processing only

### Data Privacy

**Student Information:**
- Emails processed locally
- No external transmission (except APIs)
- Temporary files deleted after processing
- Logs can be sanitized if needed

**Code Storage:**
- Repositories cloned to temp/
- Deleted on reset
- Not stored permanently

---

## Testing Strategy

### Unit Testing

Each module tested independently:
- `log_config.py`: Verify ring buffer behavior
- `agent_runner.py`: Mock agent execution
- `main.py`: Test menu logic

### Integration Testing

Test agent interactions:
- CSV format compatibility
- Status field updates
- Data flow between agents

### End-to-End Testing

Complete pipeline with test data:
- Sample emails
- Test GitHub repositories
- Verify draft creation

### Manual Testing

User acceptance testing:
- Menu navigation
- Error messages
- Log output
- Reset functionality

---

## Configuration Management

### config.json Structure

**System Settings:**
- Log directory
- File directories
- Log rotation parameters

**Agent Settings:**
- Individual agent configuration
- Timeout values
- Output patterns

**Pipeline Settings:**
- Execution order
- Status check intervals
- Error handling behavior

### Configuration Updates

When adding new features:
1. Update `config.json` with new parameters
2. Document in comments or separate file
3. Provide sensible defaults
4. Validate on startup

---

## Deployment Planning

### Prerequisites

- Python 3.8+
- WSL environment
- Gmail API credentials
- Internet connectivity

### Installation Steps

1. Clone/extract package
2. Run `setup.sh`
3. Add `credentials.json`
4. Test with `python3 main.py`

### Distribution

**Include:**
- All Python files
- Configuration files
- Documentation
- Setup scripts
- Skills and agents

**Exclude:**
- `credentials.json`
- `token.pickle`
- `venv/` directory
- `__pycache__/` directories
- `log/` directory contents
- `files/` directory contents
- `temp/` directory contents

---

## Maintenance Planning

### Regular Maintenance

**Weekly:**
- Review logs for errors
- Check disk space usage
- Verify API credentials valid

**Monthly:**
- Update dependencies
- Review and update documentation
- Check for Gmail API changes

**Quarterly:**
- Performance analysis
- User feedback review
- Feature planning

### Backup Strategy

**Important Files:**
- `credentials.json` (backed up securely)
- Configuration files
- Agent definitions
- Skill implementations

**Not Backed Up:**
- Temporary files
- Log files (rotated automatically)
- CSV outputs (regeneratable)

---

## Metrics and Monitoring

### Key Performance Indicators

1. **Processing Time:**
   - Average time per submission
   - Total pipeline duration
   - Agent-specific execution time

2. **Success Rate:**
   - Percentage of successful completions
   - Error frequency by type
   - Retry attempts

3. **Data Quality:**
   - Valid email extractions
   - Successful repository clones
   - Grade distribution

4. **System Health:**
   - Log file sizes
   - Disk space usage
   - Memory consumption

### Logging Standards

All agents log:
- Start and end times
- Input and output files
- Processing steps
- Errors and warnings
- Performance metrics

---

## Risk Management

### Identified Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Gmail API rate limit | High | Low | Implement retry logic |
| GitHub unavailable | Medium | Low | Queue for later processing |
| Disk space full | High | Medium | Ring buffer logging |
| Network failure | Medium | Medium | Retry with timeout |
| Invalid student code | Low | High | Error handling in analysis |
| Large repository | Medium | Medium | Timeout and size limits |

### Contingency Plans

1. **API Failure:** Manual processing workflow documented
2. **System Crash:** CSV files preserve state for resumption
3. **Corrupted Data:** Validation and error recovery
4. **Performance Issues:** Adjustable timeout and parallel settings

---

## Future Roadmap

### Short-term (1-3 months)
- Add more character styles
- Improve grading algorithms
- Web dashboard for monitoring
- Email templates customization

### Medium-term (3-6 months)
- Database for historical data
- Analytics and reporting
- Student progress tracking
- Automated email sending (optional)

### Long-term (6-12 months)
- Multi-language support
- Integration with LMS systems
- Machine learning for grade prediction
- API for external integrations

---

## Lessons Learned

### Design Decisions that Worked Well

1. **CSV for data exchange:** Simple and debuggable
2. **Separate agents:** Easy to maintain and test
3. **Ring buffer logging:** Prevents disk space issues
4. **Relative paths:** Makes deployment easy

### Areas for Improvement

1. **Configuration validation:** Need startup checks
2. **Error messages:** Could be more user-friendly
3. **Progress indicators:** Add visual feedback
4. **Documentation:** Could use more examples

### Best Practices Established

1. Each agent must validate its input
2. All operations must be logged
3. Status field required in all CSV outputs
4. Timeouts prevent hanging operations
5. Credentials never in logs or outputs

---

## Conclusion

The Exercise Checking System is designed as a modular, maintainable, and extensible solution for automated exercise grading. The multi-agent architecture provides flexibility, while the simple CSV-based data exchange ensures transparency and debuggability.

Key strengths:
- Clear separation of concerns
- Comprehensive logging
- Robust error handling
- Easy to deploy and maintain

The system is ready for production use and has a clear path for future enhancements.

---

**Document Status:** Complete
**Last Updated:** 2025-11-25
**Next Review:** 2025-12-25
**Maintained By:** Yair Levi
