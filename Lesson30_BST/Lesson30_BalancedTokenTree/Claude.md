# Claude Code Development Guide
## Balanced Token Tree Project

**Author:** Yair Levi
**Purpose:** Development context and guidelines for Claude Code AI assistance

---

## Project Context

This project implements a binary tree token balancing system with visualization capabilities. The project is designed to run on WSL (Windows Subsystem for Linux) using a Python virtual environment.

---

## Key Constraints

### File Size Limit
- **Maximum 150 lines per Python file**
- If a module exceeds this limit, split into multiple files
- Use clear naming conventions for split modules

### Path Management
- **Only use relative paths**
- Virtual environment: `../../venv/`
- Log directory: `./log/`
- Output directory: `./output/` (for visualizations)
- No absolute paths anywhere in the code

### Environment
- **WSL (Windows Subsystem for Linux)**
- Python 3.8+
- Virtual environment at `../../venv/`

---

## Logging Requirements

### Ring Buffer Configuration
```python
# Configuration details:
- Handler: RotatingFileHandler
- Location: ./log/
- File pattern: app_log_{1..20}.log
- Max file size: 16 MB (16 * 1024 * 1024 bytes)
- Backup count: 20
- Format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
- Level: INFO and above
```

### Ring Buffer Behavior
- Start writing to `app_log_1.log`
- When full, rotate to `app_log_2.log`
- Continue through `app_log_20.log`
- When `app_log_20.log` is full, overwrite `app_log_1.log`
- This creates a circular buffer of 320 MB total (20 × 16 MB)

---

## Architecture Guidelines

### Module Structure
```
balanced_token_tree/
├── __init__.py           # Package initialization
├── main.py               # Entry point
├── tree_structure.py     # Tree node and structure classes
├── token_manager.py      # Token assignment and management
├── balancing.py          # Balancing algorithm implementation
├── visualization.py      # Tree visualization with matplotlib
├── logger_config.py      # Logging setup
└── tasks.py              # Task orchestration
```

### Design Principles
1. **Single Responsibility:** Each module has one clear purpose
2. **Separation of Concerns:** Tree logic separate from visualization
3. **Testability:** Functions should be pure where possible
4. **Type Hints:** Use type annotations for clarity
5. **Documentation:** Docstrings for all public functions

---

## Implementation Notes

### Tree Structure
- Use a class-based approach for nodes
- Each node stores: name, level, token_count, children, parent
- Root node has level=5, leaves have level=1
- Build tree recursively or iteratively

### Balancing Algorithm
```python
# Key insight: Pairing largest with smallest
# This distributes extreme values across different parent nodes
# Minimizes variance in parent node totals

def balance_tree(leaf_tokens: List[int]) -> List[Tuple[int, int]]:
    """
    Args:
        leaf_tokens: List of token counts from leaves

    Returns:
        List of (left_child_tokens, right_child_tokens) pairs
    """
    sorted_tokens = sorted(leaf_tokens)
    pairs = []

    while sorted_tokens:
        smallest = sorted_tokens.pop(0)
        largest = sorted_tokens.pop()
        pairs.append((smallest, largest))

    return pairs
```

### Multiprocessing Opportunities
- **Visualization:** Generate multiple graphs in parallel
- **Token Assignment:** Could parallelize random generation (though not critical)
- **Calculations:** Parent node sum calculations could be parallelized by levels
- Use `multiprocessing.Pool` for parallel tasks

### Error Handling
- Validate tree structure before operations
- Handle missing log directory (create if not exists)
- Graceful failure if visualization backend unavailable
- Log all errors with full context

---

## Development Workflow

### Phase 1: Core Structure
1. Implement tree node class
2. Build tree structure with proper naming
3. Test tree creation and traversal

### Phase 2: Token Management
1. Implement random token assignment
2. Implement parent sum propagation
3. Test with known values

### Phase 3: Balancing Algorithm
1. Implement sorting and pairing logic
2. Implement token reassignment to leaves
3. Test balancing improves distribution

### Phase 4: Visualization
1. Set up matplotlib with networkx or custom drawing
2. Implement node positioning algorithm
3. Add labels with names and token counts
4. Save to files

### Phase 5: Integration
1. Create main task orchestrator
2. Set up logging system
3. Wire all components together
4. Test end-to-end flow

### Phase 6: Iteration
1. Implement multiple iteration support
2. Save visualizations with iteration numbers
3. Log statistics at each iteration

---

## Testing Strategy

### Manual Testing
- Run with fixed random seed for reproducibility
- Verify tree structure visually
- Check that balancing reduces variance
- Confirm log files rotate correctly

### Test Cases
1. Tree creation with correct node count and naming
2. Token sum propagation accuracy
3. Balancing algorithm with simple inputs
4. Log file rotation after size limit
5. Visualization file generation

---

## Common Issues and Solutions

### Issue: Matplotlib on WSL
**Problem:** Display backend not available
**Solution:** Use `matplotlib.use('Agg')` for headless operation

### Issue: File Line Limit
**Problem:** Module exceeds 150 lines
**Solution:** Split into logical sub-modules or helper files

### Issue: Ring Buffer Not Rotating
**Problem:** `RotatingFileHandler` uses `backupCount` incorrectly
**Solution:** Ensure `backupCount=19` (0-indexed) or implement custom handler

### Issue: Path Problems
**Problem:** Absolute paths break on different systems
**Solution:** Use `pathlib.Path(__file__).parent` for relative resolution

---

## Output Examples

### Console Output
```
INFO: Starting Balanced Token Tree Program
INFO: Creating tree with 5 levels (16 leaves)
INFO: Tree structure created successfully
INFO: Assigning random tokens to leaves
INFO: Initial token distribution - Root total: 8542
INFO: Generating initial tree visualization
INFO: Applying balancing algorithm (Iteration 1)
INFO: Balanced tree - Root total: 8542
INFO: Variance reduced from 15234 to 8721
INFO: Generating balanced tree visualization
INFO: Applying balancing algorithm (Iteration 2)
INFO: Final tree - Root total: 8542
INFO: Variance reduced from 8721 to 8156
INFO: All visualizations saved to ./output/
INFO: Program completed successfully
```

### Visualization Naming
- `tree_iteration_0_initial.png`
- `tree_iteration_1_balanced.png`
- `tree_iteration_2_balanced.png`

---

## Dependencies Rationale

### matplotlib
- **Purpose:** Tree visualization
- **Alternatives:** networkx with matplotlib backend, graphviz
- **Choice:** matplotlib with custom positioning for full control

### networkx (optional)
- **Purpose:** Graph layout algorithms
- **Use Case:** If custom positioning is too complex
- **Trade-off:** Adds dependency but simplifies layout

---

## Code Quality Standards

### Naming Conventions
- Classes: `PascalCase` (e.g., `TreeNode`, `TokenManager`)
- Functions: `snake_case` (e.g., `assign_tokens`, `balance_tree`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TOKEN_VALUE`)
- Private: prefix with `_` (e.g., `_calculate_position`)

### Docstring Format
```python
def function_name(arg1: type1, arg2: type2) -> return_type:
    """
    Brief description of function.

    Detailed explanation if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When and why
    """
```

### Type Hints
- Use for all function signatures
- Import from `typing` module as needed
- Use `Optional[T]` for nullable values
- Use `List[T]`, `Dict[K, V]` for collections

---

## Performance Considerations

### Memory
- Tree with 16 leaves uses ~31 node objects (2^5 - 1)
- Minimal memory footprint
- Log buffer: 320 MB total (manageable)

### CPU
- Tree operations: O(n) where n = number of nodes
- Balancing: O(n log n) due to sorting
- Visualization: Most expensive operation
- Consider caching visualization if needed

### I/O
- Log writes: Buffered for efficiency
- Visualization saves: Use compression if files are large
- Consider async I/O for logs if performance critical

---

## Maintenance Notes

### Adding New Features
1. Follow existing module structure
2. Add to tasks.py if it's a new task
3. Update requirements.txt if new dependencies
4. Keep files under 150 lines
5. Update this document

### Debugging
1. Check logs in `./log/` directory
2. Increase log level to DEBUG if needed
3. Use fixed random seed for reproducibility
4. Add assertions for invariants

### Refactoring
1. Extract functions when approaching 150 lines
2. Keep related functionality together
3. Update imports when moving code
4. Test after each refactor

---

## Questions for Clarification

If implementing this project, consider clarifying:

1. **Visualization Style:** Preferred layout (horizontal/vertical, spacing)?
2. **Balancing Goal:** Minimize variance, or balance by tree depth?
3. **Random Seed:** Should it be configurable for reproducibility?
4. **Output Format:** PNG, PDF, SVG, or multiple formats?
5. **Statistics:** Should we calculate and display variance/std dev?

---

## Next Steps

1. Review PRD and this document
2. Examine planning.md for detailed design
3. Check tasks.md for implementation order
4. Set up virtual environment and install requirements
5. Begin implementation following tasks.md

---

**Document Version:** 1.0
**Last Updated:** 2026-01-15
**Status:** Ready for development
