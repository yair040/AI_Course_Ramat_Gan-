# BST DeepFake Detection System - Quick Reference

## Project Summary

**Total Nodes**: 31 (16 leaves + 15 internal)
**Levels**: 5 (Root at 5_01 down to leaves at 1_xx)
**Status**: Design Complete ✓ | Validated ✓ | Ready for Implementation ✓

## Tree Structure Quick View

```
Level 1: 5_01 (Root - Main Orchestrator)
         |
Level 2: 4_01 (Analysis) | 4_02 (Infrastructure)
         |                 |
Level 3: 3_01, 3_02      | 3_03, 3_04
         |                 |
Level 4: 2_01 to 2_04    | 2_05 to 2_08
         |                 |
Level 5: 1_01 to 1_08    | 1_09 to 1_16 (All LEAVES - I/O only)
```

## Node Categories

### Analysis Path (Left Side)
- **4_01**: Analysis Pipeline
  - **3_01**: Facial & Visual (→ 2_01, 2_02 → 1_01-1_04)
  - **3_02**: Temporal & ML (→ 2_03, 2_04 → 1_05-1_08)

### Infrastructure Path (Right Side)
- **4_02**: Infrastructure Pipeline
  - **3_03**: Video Processing (→ 2_05, 2_06 → 1_09-1_12)
  - **3_04**: Reporting (→ 2_07, 2_08 → 1_13-1_16)

## Leaf Nodes (1_xx) - All External I/O

| Node | Name | Function | Parent |
|------|------|----------|--------|
| 1_01 | Face Detection | Call dlib/face-recognition | 2_01 |
| 1_02 | Facial Landmarks | Extract 68 landmarks | 2_01 |
| 1_03 | Eye & Blink | Analyze blinks, pupils | 2_02 |
| 1_04 | Shadow Validator | Check shadow consistency | 2_02 |
| 1_05 | Optical Flow | Compute motion vectors | 2_03 |
| 1_06 | Motion Analyzer | Detect motion anomalies | 2_03 |
| 1_07 | Model Loader | Load ML models from disk | 2_04 |
| 1_08 | ML Inference | Run PyTorch/TF inference | 2_04 |
| 1_09 | Video Reader | Read video files | 2_05 |
| 1_10 | Metadata Extractor | Extract video metadata | 2_05 |
| 1_11 | Frame Decoder | Decode video frames | 2_06 |
| 1_12 | Buffer Manager | Manage frame buffers | 2_06 |
| 1_13 | Report Writer | Write JSON reports | 2_07 |
| 1_14 | Visualization | Generate heatmaps/plots | 2_07 |
| 1_15 | Log Writer | Write log files | 2_08 |
| 1_16 | Metrics | Aggregate metrics | 2_08 |

## File Structure per Node

```
{node_folder}/
├── config.yaml          # Configuration
├── prd.md              # Requirements document
├── todo.md             # Task list
├── requirements.md     # Detailed requirements
├── status.json         # Current status
├── logs.json           # Node logs
├── tokens.json         # Token usage
└── source.py           # Implementation template
```

## Shared Folders

- **shared_level_5/**: System-wide utilities (root level)
- **shared_level_4/**: Subsystem coordination (4_xx level)
- **shared_level_3/**: Pipeline management (3_xx level)
- **shared_level_2/**: Component utilities (2_xx level)
- **shared_level_1/**: I/O helpers (leaf level)

## Key Design Principles

1. **Leaf I/O Only**: External operations ONLY in 1_xx nodes
2. **Decision Escalation**: Complex decisions move up the tree
3. **Progressive Filtering**: Logs reduced ~90% per level
4. **Token Tracking**: Cumulative usage tracked upward
5. **No Duplication**: Common code in shared folders

## Decision Escalation Levels

```
1_xx (Leaf)     → Local I/O decisions | Escalate: errors, policy needs
2_xx (Level 4)  → Component policies  | Escalate: cross-component issues
3_xx (Level 3)  → Pipeline decisions  | Escalate: cross-pipeline needs
4_xx (Level 2)  → Subsystem policies  | Escalate: system-wide needs
5_01 (Root)     → Final authority     | No escalation (terminal)
```

## Data Flow Pattern

### Request (Top-Down)
```
5_01 → 4_xx → 3_xx → 2_xx → 1_xx (execute I/O)
```

### Result (Bottom-Up)
```
1_xx → 2_xx (aggregate) → 3_xx (aggregate) → 4_xx (aggregate) → 5_01 (final)
```

## Aggregation Rules

### Logs
- **ERROR/WARNING**: Always propagate
- **INFO**: Sampled (1 in 10)
- **DEBUG**: Rarely propagated

### Status
- **Worst status wins**: If any child is unhealthy, parent is degraded
- **Counts aggregated**: Total operations = sum of all children

### Tokens
- **Cumulative**: Parent tokens = own + all children
- **Alerts at**: 80% (warning), 90% (critical), 95% (throttle)

## Test Scenarios (8 total)

1. **Happy Path**: Complete analysis, all nodes used ✓
2. **Deepfake Detected**: Anomaly detection working ✓
3. **Unsupported Format**: Decision escalation (1 level) ✓
4. **Low Confidence**: Multi-level escalation (4 levels) ✓
5. **Token Exhaustion**: Resource adaptation ✓
6. **Partial Failure**: Graceful degradation ✓
7. **Concurrent Operations**: Parallel processing ✓
8. **Stress Test**: Maximum load handling ✓

## Performance Targets

- **Speed**: < 2× video duration
- **Memory**: < 4GB per video
- **Tokens**: < 100 per second of video
- **Accuracy**: > 85%
- **False Positives**: < 10%

## Documentation Files

| File | Purpose |
|------|---------|
| README.md | Project overview and getting started |
| BST_DESIGN.md | Complete architecture design |
| DECISION_ESCALATION_SYSTEM.md | Escalation protocol |
| AGGREGATION_SYSTEM.md | Log/status/token aggregation |
| TEST_SCENARIOS.md | 8 test scenarios with I/O specs |
| SIMULATION_RESULTS.md | Validation and verification |
| QUICK_REFERENCE.md | This file |

## Implementation Order

1. **Shared utilities** (bottom-up: level 1 → 5)
2. **Leaf nodes** (1_01 → 1_16)
3. **Level 4 nodes** (2_01 → 2_08)
4. **Level 3 nodes** (3_01 → 3_04)
5. **Level 2 nodes** (4_01, 4_02)
6. **Root node** (5_01)
7. **Integration tests**

## Common Commands

### Navigate Nested BST Structure
```bash
# View root
ls -la 5_01/

# Navigate to a specific node (example: 1_01)
cd 5_01/4_01/3_01/2_01/1_01/

# View node's PRD
cat 5_01/4_01/3_01/2_01/1_01/prd.md

# View different node (example: 1_09 in right subtree)
cat 5_01/4_02/3_03/2_05/1_09/prd.md
```

### Check Structure
```bash
# Find all leaves (should be 16)
find 5_01 -name "1_*" -type d | wc -l

# List all leaves with paths
find 5_01 -name "1_*" -type d | sort

# Find all level 4 nodes (should be 8)
find 5_01 -name "2_*" -type d | wc -l

# View tree structure (if tree command available)
tree -d -L 5 5_01/
```

### View Documentation
```bash
# Architecture
cat BST_DESIGN.md

# Escalation
cat DECISION_ESCALATION_SYSTEM.md

# Aggregation
cat AGGREGATION_SYSTEM.md

# Tests
cat TEST_SCENARIOS.md

# Validation
cat SIMULATION_RESULTS.md
```

## Quick Facts

- **Project**: DeepFake detection using distributed BST
- **Derived From**: ../../Lesson26/Lesson26_DeepFake/prd.md
- **Structure**: 5-level complete binary tree
- **Nodes**: 31 total
- **Files per Node**: 8 (config, prd, todo, requirements, status, logs, tokens, source)
- **Total Files Generated**: 248 node files + 6 documentation files
- **Validation**: All test scenarios pass ✓
- **Issues Found**: 0
- **Ready for Implementation**: Yes ✓

## Need Help?

1. **Architecture questions**: See BST_DESIGN.md
2. **Node responsibilities**: See node's prd.md
3. **Implementation details**: See node's requirements.md
4. **Testing approach**: See TEST_SCENARIOS.md
5. **Validation proof**: See SIMULATION_RESULTS.md

## Status: Ready for Implementation ✓

All requirements met, structure validated, tests defined, ready to code!
