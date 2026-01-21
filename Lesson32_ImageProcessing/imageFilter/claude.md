# Claude AI Interaction Guide
## Image Frequency Filter Application

**Author:** Yair Levi  
**Project:** Image Filtering with FFT  
**Location:** `C:\Users\yair0\AI_continue\Lesson32_imageProcessing\imageFilter\`

---

## Overview

This document provides guidance for effective interaction with Claude AI when developing, debugging, and extending the Image Frequency Filter application.

---

## Best Practices for Claude Interaction

### 1. Providing Context

When asking Claude for help, always provide:

```markdown
- **Current Task:** Which task from tasks.md you're working on
- **File Name:** The specific file you're working with
- **Line Limit:** Reminder that files must be ≤150 lines
- **Error Message:** Full error traceback if applicable
- **What You've Tried:** Steps already attempted
```

**Example:**
```
I'm working on T5 (FFT Transform Task) in tasks/fft_transform.py.
The file is currently at 145 lines. I'm getting a ValueError when 
applying fftshift. Here's the error: [paste error]. I've tried...
```

### 2. Code Review Requests

When requesting code review:

```markdown
Please review [file_name] for:
- Line count (must be ≤150)
- Relative path usage (no absolute paths)
- Logging implementation (INFO level+)
- Error handling
- Docstring completeness
- Compliance with PRD requirements
```

### 3. Implementation Requests

When requesting new implementations:

```markdown
Context:
- Task: [Task number and name]
- File: [filename] (current lines: X/150)
- Dependencies: [required modules/utilities]

Requirements:
- [Specific functionality needed]
- Must use relative paths
- Must include logging
- Must handle errors gracefully

Constraints:
- Keep under 150 lines total
- Follow existing code style
```

---

## Common Request Patterns

### Pattern 1: File Implementation

```markdown
Implement [filename] for [Task TX]:

Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

Technical specs:
- Input: [data type and format]
- Output: [data type and format]
- Dependencies: [list modules]
- Max lines: 150

Please include:
- Module docstring
- Function docstrings
- Type hints
- Error handling
- Logging statements
```

### Pattern 2: Debugging Assistance

```markdown
Debug assistance needed for [filename]:

Issue:
[Describe the problem]

Error message:
```
[Paste full traceback]
```

Current code:
```python
[Paste relevant code section]
```

Expected behavior:
[What should happen]

Actual behavior:
[What is happening]

Environment:
- WSL Ubuntu
- Python 3.x
- Virtual env at ../../venv/
```

### Pattern 3: Optimization Request

```markdown
Optimize [filename] (currently X/150 lines):

Goal:
[What needs optimization]

Current approach:
[Describe current implementation]

Constraints:
- Must remain under 150 lines
- Cannot sacrifice functionality
- Maintain readability
- Keep relative paths

Areas to optimize:
1. [Area 1]
2. [Area 2]
```

### Pattern 4: Feature Addition

```markdown
Add [feature] to [filename]:

Current state:
- Lines used: X/150
- Available lines: Y

Feature requirements:
[Detailed description]

Integration points:
[Where it fits in the code]

Must maintain:
- Line count under 150
- Relative path usage
- Logging integration
- Error handling
```

---

## File-Specific Interaction Strategies

### For `main.py`:

**When asking about main.py:**
```markdown
The main.py file orchestrates the entire pipeline. Current concerns:
- Argument parsing for [specific flag]
- Integration of [specific task]
- Error handling for [scenario]
- Multiprocessing for [operation]

The file is currently at X/150 lines. Please suggest...
```

### For Task Files (`tasks/`):

**When asking about task files:**
```markdown
This task file handles [specific operation]. It should:
- Accept [input type]
- Return [output type]
- Log at INFO level
- Handle [specific errors]

Current implementation is X/150 lines. I need help with...
```

### For Filter Files (`filters/`):

**When asking about filters:**
```markdown
This filter implements [filter type]. Requirements:
- Inherits from BaseFilter
- Creates [type of mask]
- Cutoff frequency: [value]
- Should produce [expected output]

Current line count: X/150. Question: ...
```

### For Utility Files (`utils/`):

**When asking about utilities:**
```markdown
This utility provides [functionality]. It's used by:
- [Module 1]
- [Module 2]

Must maintain compatibility with existing code while [requirement].
Current lines: X/150.
```

---

## Multiprocessing-Specific Queries

When dealing with multiprocessing issues:

```markdown
Multiprocessing context:
- Python version: 3.x on WSL
- Parallel operation: [describe what's being parallelized]
- Data being shared: [describe data]
- Current implementation: [Pool/Process/Queue]

Issue:
[Describe the problem]

Error (if any):
[Paste error]

Need help with:
- [Specific aspect of multiprocessing]
```

---

## Logging-Specific Queries

When dealing with logging issues:

```markdown
Logging setup:
- Ring buffer: 20 files × 16MB
- Location: ./log/
- Format: %(asctime)s - %(name)s - %(levelname)s - %(message)s

Issue:
[Describe logging problem]

Current configuration:
```python
[Paste logger setup code]
```

Expected: [what should happen]
Actual: [what is happening]
```

---

## Path-Related Queries

When dealing with path issues on WSL:

```markdown
Path issue on WSL:

Context:
- Project root: C:\Users\yair0\AI_continue\Lesson32_imageProcessing\imageFilter\
- WSL path: /mnt/c/Users/yair0/AI_continue/Lesson32_imageProcessing/imageFilter/
- Virtual env: ../../venv/ (relative to project root)

Issue:
[Describe path problem]

Current code:
```python
[Paste path handling code]
```

Attempted:
- [What you've tried]
```

---

## Testing and Validation Queries

When asking Claude to help with testing:

```markdown
Testing request for [component]:

Test scenarios:
1. [Scenario 1]
2. [Scenario 2]
3. [Scenario 3]

Expected outcomes:
[What should happen in each scenario]

Please provide:
- Test code
- Validation checks
- Edge cases to consider
```

---

## Code Refactoring Queries

When the file is approaching 150 lines:

```markdown
[filename] is at 140/150 lines. Need to refactor to stay under limit.

Current structure:
- [List main components]
- [Line counts per section]

Refactoring options:
1. Extract [utility functions]
2. Simplify [complex logic]
3. Merge [related functions]

Please suggest the best approach while maintaining:
- Functionality
- Readability
- Maintainability
```

---

## Integration Queries

When integrating multiple components:

```markdown
Integration task: Connect [Component A] with [Component B]

Component A (file: X):
- Outputs: [data type]
- Current state: [description]

Component B (file: Y):
- Expects: [data type]
- Current state: [description]

Integration point: [where they connect]

Challenges:
- [Challenge 1]
- [Challenge 2]

Both files must stay under 150 lines. Please suggest...
```

---

## Documentation Queries

When you need documentation help:

```markdown
Documentation needed for [file/function]:

Current code:
```python
[Paste code]
```

Please provide:
- Module-level docstring
- Function docstrings with:
  - Description
  - Args (with types)
  - Returns (with type)
  - Raises (exceptions)
- Critical inline comments

Keep it concise to save line count (currently X/150).
```

---

## Performance Optimization Queries

When you need performance improvements:

```markdown
Performance optimization for [operation]:

Current performance:
- Time: [X seconds]
- Memory: [Y MB]
- Image size: [dimensions]

Bottleneck analysis:
[Describe where time is spent]

Current implementation:
```python
[Paste relevant code]
```

Constraints:
- Must maintain accuracy
- File must stay under 150 lines
- Should use multiprocessing if beneficial

Please suggest optimizations...
```

---

## Error Handling Queries

When implementing error handling:

```markdown
Error handling for [operation]:

Possible errors:
1. [Error type 1] - when [condition]
2. [Error type 2] - when [condition]
3. [Error type 3] - when [condition]

Current handling:
```python
[Paste current try/except code]
```

Requirements:
- Log errors at appropriate level
- Provide helpful error messages
- Clean up resources
- Maintain line count under 150

Please improve error handling...
```

---

## Questions About Project Structure

### How do I ask about overall architecture?

```markdown
Architecture question:

Current structure:
[Describe current organization]

Concern:
[What you're unsure about]

Alternatives considered:
1. [Option 1]
2. [Option 2]

PRD requirements:
- [Relevant requirements]

Which approach best fits the requirements while maintaining:
- Modularity
- File size limits
- Maintainability
```

---

## Iterative Development Approach

### Step-by-step requests:

```markdown
Starting [Task TX] - [Task Name]

Step 1 request: Implement basic structure
- [Requirement 1]
- [Requirement 2]

Once Step 1 is complete, I'll test and return for Step 2.

This iterative approach ensures:
- Each step is validated
- Line count is managed
- Issues are caught early
```

---

## Code Review Checklist

When asking Claude to review code:

```markdown
Code review for [filename]:

Checklist:
- [ ] Under 150 lines
- [ ] Uses relative paths only
- [ ] Includes logging (INFO+)
- [ ] Has error handling
- [ ] Has docstrings
- [ ] Has type hints
- [ ] Follows project conventions
- [ ] Integrates with existing code
- [ ] Handles edge cases

Current code:
```python
[Paste code]
```

Please review against checklist and suggest improvements.
```

---

## Final Integration Testing

When ready for final testing:

```markdown
Final integration test for [component/feature]:

Components involved:
1. [Component 1]
2. [Component 2]
3. [Component 3]

Test plan:
1. [Test step 1]
2. [Test step 2]
3. [Test step 3]

Success criteria:
- [Criterion 1]
- [Criterion 2]

Please help verify the integration and suggest any final tests.
```

---

## Tips for Effective Claude Interaction

### DO:
✓ Be specific about which file and task you're working on  
✓ Include relevant error messages in full  
✓ Mention current line count when near the limit  
✓ Provide context about dependencies  
✓ Ask for explanations of suggestions  
✓ Request code review before moving to next task  
✓ Verify relative path usage  
✓ Check logging integration  

### DON'T:
✗ Ask vague questions without context  
✗ Forget to mention the 150-line limit  
✗ Omit error messages or stack traces  
✗ Skip testing before asking for next steps  
✗ Ignore path requirements (absolute paths)  
✗ Forget about multiprocessing considerations  
✗ Neglect to mention WSL environment  

---

## Example Complete Interaction

```markdown
Task: T5 - FFT Transform (tasks/fft_transform.py)

Context:
- File is new, starting from 0 lines
- Must stay under 150 lines
- Dependencies: numpy, logging, utils.logger
- Called by: main.py
- Calls: None (uses numpy.fft)

Request:
Implement the FFT transform task with:

1. apply_fft(image: np.ndarray) -> np.ndarray
   - Apply 2D FFT
   - Apply fftshift to center frequencies
   - Return complex FFT result

2. get_magnitude_spectrum(fft_image: np.ndarray) -> np.ndarray
   - Calculate magnitude
   - Return for visualization

3. get_phase_spectrum(fft_image: np.ndarray) -> np.ndarray
   - Calculate phase
   - Return for analysis

Requirements:
- Include module docstring
- Add function docstrings with type hints
- Log each operation at INFO level
- Handle errors (invalid input, memory issues)
- Use relative imports

Please provide complete implementation.
```

---

## Conclusion

Effective communication with Claude accelerates development. Always provide:
1. **Context** - What you're working on
2. **Constraints** - Line limits, paths, dependencies
3. **Specifics** - Exact requirements and errors
4. **Verification** - How to test the solution

This ensures Claude can provide targeted, useful assistance for your Image Frequency Filter application.

---

**Document Version:** 1.0  
**Last Updated:** January 19, 2026