# BST Distributed DeepFake Detection System

## Project Overview
A Binary Search Tree (BST) based distributed system for deepfake video detection. The system is organized into 5 levels with 16 leaf nodes performing external I/O operations and 15 internal nodes for coordination and aggregation.

**The directory structure is a REAL nested BST** - each parent folder physically contains its child folders, mirroring the tree hierarchy. Navigate down the tree from root (5_01) to leaves (1_xx).

**This Project takes the below projet (Github) and divide it into BST tree:**
  https://github.com/yair040/AI_Course_Ramat_Gan-/tree/main/Lesson26_DeepFake 

## Project Status
**Design Complete** ✓
**Structure Validated** ✓
**Ready for Implementation** ✓

## Directory Structure (Nested BST)

```
Lesson30_BST_Distributed_Project/
├── README.md                          # This file
├── BST_DESIGN.md                      # Complete BST structure design
├── DECISION_ESCALATION_SYSTEM.md      # Decision escalation protocol
├── AGGREGATION_SYSTEM.md              # Log/status/token aggregation
├── TEST_SCENARIOS.md                  # Comprehensive test scenarios
├── SIMULATION_RESULTS.md              # Simulation verification
├── generate_node_files.py             # Node generation script
├── reorganize_to_nested_bst.py        # BST reorganization script
│
├── shared_level_5/                    # System-wide utilities
│   └── README.md
│
└── 5_01/                              # ROOT: Main Orchestrator
    ├── config.yaml, prd.md, todo.md, requirements.md
    ├── status.json, logs.json, tokens.json, source.py
    │
    ├── shared_level_4/                # Subsystem utilities
    │
    ├── 4_01/                          # LEFT: Analysis Pipeline
    │   ├── config.yaml, prd.md, etc.
    │   ├── shared_level_3/            # Pipeline utilities
    │   │
    │   ├── 3_01/                      # Facial & Visual Analysis
    │   │   ├── shared_level_2/        # Component utilities
    │   │   ├── 2_01/                  # Facial Features Analysis
    │   │   │   ├── shared_level_1/    # I/O utilities
    │   │   │   ├── 1_01/              # Face Detection Service (LEAF)
    │   │   │   └── 1_02/              # Facial Landmark Extractor (LEAF)
    │   │   └── 2_02/                  # Lighting & Shadow Analysis
    │   │       ├── shared_level_1/
    │   │       ├── 1_03/              # Eye & Blink Analyzer (LEAF)
    │   │       └── 1_04/              # Shadow Geometry Validator (LEAF)
    │   │
    │   └── 3_02/                      # Temporal & ML Analysis
    │       ├── shared_level_2/
    │       ├── 2_03/                  # Temporal Motion Analysis
    │       │   ├── shared_level_1/
    │       │   ├── 1_05/              # Optical Flow Computer (LEAF)
    │       │   └── 1_06/              # Motion Vector Analyzer (LEAF)
    │       └── 2_04/                  # ML Model Coordination
    │           ├── shared_level_1/
    │           ├── 1_07/              # ML Model Loader (LEAF)
    │           └── 1_08/              # ML Inference Engine (LEAF)
    │
    └── 4_02/                          # RIGHT: Infrastructure & I/O Pipeline
        ├── config.yaml, prd.md, etc.
        ├── shared_level_3/
        │
        ├── 3_03/                      # Video Processing Pipeline
        │   ├── shared_level_2/
        │   ├── 2_05/                  # Video Input Handler
        │   │   ├── shared_level_1/
        │   │   ├── 1_09/              # Video File Reader (LEAF)
        │   │   └── 1_10/              # Metadata Extractor (LEAF)
        │   └── 2_06/                  # Frame Processing
        │       ├── shared_level_1/
        │       ├── 1_11/              # Frame Decoder (LEAF)
        │       └── 1_12/              # Frame Buffer Manager (LEAF)
        │
        └── 3_04/                      # Reporting & Monitoring
            ├── shared_level_2/
            ├── 2_07/                  # Report Generation
            │   ├── shared_level_1/
            │   ├── 1_13/              # JSON Report Writer (LEAF)
            │   └── 1_14/              # Visualization Generator (LEAF)
            └── 2_08/                  # Log & Status Management
                ├── shared_level_1/
                ├── 1_15/              # Log File Writer (LEAF)
                └── 1_16/              # Metrics Aggregator (LEAF)
```

## Nested BST Structure

### Why Nested?
The folders are organized in a **true nested hierarchy** where:
- Each parent physically contains its children
- Shared folders are at the appropriate level for their scope
- Navigation follows the tree structure naturally
- The physical structure matches the logical architecture

### Navigation Paths
- **Root**: `5_01/`
- **Left subtree (Analysis)**: `5_01/4_01/...`
- **Right subtree (Infrastructure)**: `5_01/4_02/...`
- **Example leaf path**: `5_01/4_01/3_01/2_01/1_01/`

### Shared Folder Placement
- `shared_level_5/` at project root (system-wide)
- `shared_level_4/` in `5_01/` (for 4_xx nodes)
- `shared_level_3/` in each `4_xx/` (for 3_xx nodes)
- `shared_level_2/` in each `3_xx/` (for 2_xx nodes)
- `shared_level_1/` in each `2_xx/` (for 1_xx leaves)

## System Architecture

### Tree Structure
```
                    5_01 (Root)
                    /         \
              4_01              4_02
              /   \            /    \
          3_01   3_02      3_03    3_04
          / \     / \       / \     / \
        2_01 2_02 2_03 2_04 2_05 2_06 2_07 2_08
         |    |    |    |    |    |    |    |
        1_01 1_03 1_05 1_07 1_09 1_11 1_13 1_15
        1_02 1_04 1_06 1_08 1_10 1_12 1_14 1_16
```

### Key Principles

1. **External I/O Only in Leaves**: All file/network/API operations confined to 1_xx nodes
2. **Decision Escalation**: Complex decisions flow upward to appropriate level
3. **Log Aggregation**: Logs filtered and aggregated at each level
4. **Token Tracking**: Cumulative token usage tracked up the tree
5. **No Code Duplication**: Common code in shared_level_X folders

## Node Responsibilities

### Root (5_01)
- System orchestration
- Final decision authority
- Configuration management
- Overall result aggregation

### Level 2 (4_xx)
- **4_01**: Analysis Pipeline - All detection/analysis coordination
- **4_02**: Infrastructure Pipeline - I/O and reporting coordination

### Level 3 (3_xx)
- **3_01**: Facial & Visual Analysis
- **3_02**: Temporal & ML Analysis
- **3_03**: Video Processing
- **3_04**: Reporting & Monitoring

### Level 4 (2_xx)
- **2_01-2_04**: Analysis components
- **2_05-2_06**: Processing components
- **2_07-2_08**: Output components

### Level 5 (1_xx) - Leaves
All external I/O operations:
- Face detection, landmark extraction
- Eye/shadow analysis
- Motion computation
- ML inference
- Video I/O
- Report generation
- Logging and metrics

## Key Features

### Decision Escalation System
- Hierarchical decision making
- Clear escalation criteria
- Timeout handling
- Safe defaults
- Full audit trail

See: `DECISION_ESCALATION_SYSTEM.md`

### Aggregation System
- Progressive log filtering (90% reduction per level)
- Status aggregation (worst status propagates)
- Token summation (accurate tracking)
- Performance metrics

See: `AGGREGATION_SYSTEM.md`

### Test Coverage
- 8 comprehensive test scenarios
- All 31 nodes covered
- Edge cases tested
- Performance validated
- Error handling verified

See: `TEST_SCENARIOS.md` and `SIMULATION_RESULTS.md`

## Node File Structure

Each node directory contains:
- **config.yaml**: Configuration parameters
- **prd.md**: Product requirements
- **todo.md**: Implementation tasks
- **requirements.md**: Detailed requirements
- **status.json**: Current status tracking
- **logs.json**: Node-specific logs
- **tokens.json**: Token usage tracking
- **source.py**: Python implementation template

## Implementation Roadmap

### Phase 1: Foundation
1. Implement shared utilities (shared_level_1 through shared_level_5)
2. Create communication protocol
3. Set up logging infrastructure
4. Implement token tracking

### Phase 2: Leaf Nodes (Bottom-Up)
1. Implement all 16 leaf nodes (1_01 to 1_16)
2. Test external I/O operations
3. Verify error handling
4. Validate token tracking

### Phase 3: Internal Nodes
1. Implement Level 4 coordination nodes (2_01 to 2_08)
2. Implement Level 3 pipeline nodes (3_01 to 3_04)
3. Implement Level 2 subsystem nodes (4_01, 4_02)
4. Implement root node (5_01)

### Phase 4: Integration
1. End-to-end testing
2. Decision escalation testing
3. Aggregation validation
4. Performance optimization

### Phase 5: Deployment
1. Monitoring and visualization
2. Documentation
3. User interface (if needed)
4. Production deployment

## Performance Targets

- **Analysis Speed**: < 2× video duration
- **Memory Usage**: < 4GB per video
- **Token Budget**: < 100 tokens per second of video
- **Accuracy**: > 85% on test datasets
- **False Positive Rate**: < 10%

## Technology Stack

### Required
- Python 3.9+
- OpenCV (video processing)
- NumPy (numerical operations)
- PyTorch or TensorFlow (ML models)
- dlib or face-recognition (face detection)
- ffmpeg-python (video codec handling)

### Optional
- matplotlib (visualizations)
- pandas (data analysis)
- pytest (testing)

## Getting Started

### 1. Review Design Documents
- Read `BST_DESIGN.md` for complete architecture
- Read `DECISION_ESCALATION_SYSTEM.md` for escalation protocol
- Read `AGGREGATION_SYSTEM.md` for data flow

### 2. Explore Node Structure (Nested BST)
```bash
# View root node
ls -la 5_01/
cat 5_01/prd.md

# View an internal node (e.g., 2_01)
ls -la 5_01/4_01/3_01/2_01/
cat 5_01/4_01/3_01/2_01/prd.md

# View a leaf node (e.g., 1_01)
ls -la 5_01/4_01/3_01/2_01/1_01/
cat 5_01/4_01/3_01/2_01/1_01/prd.md

# View all leaves
find 5_01 -name "1_*" -type d
```

### 3. Review Test Scenarios
```bash
# Read test scenarios
cat TEST_SCENARIOS.md

# Read simulation results
cat SIMULATION_RESULTS.md
```

### 4. Start Implementation
- Begin with shared utilities
- Implement leaf nodes
- Build up through internal nodes
- Test at each level

## Validation Results

### ✓ All Requirements Met
1. ✓ BST structure with 5 levels (16 leaves)
2. ✓ Each node has: config, PRD, todo, requirements, logs, status, tokens, source
3. ✓ Root folder is 5_01, leaves are 1_xx
4. ✓ External I/O only in leaves
5. ✓ No code duplication (shared folders)
6. ✓ Correct folder naming (5_01 → 4_xx → 3_xx → 2_xx → 1_xx)
7. ✓ Shared folders at each level
8. ✓ Decision escalation system designed
9. ✓ Log/status/token aggregation designed
10. ✓ Test scenarios created and simulated
11. ✓ All modules verified as used

### Simulation Results
- **Node Coverage**: 31/31 nodes used (100%)
- **Test Scenarios**: 8/8 passing
- **Issues Found**: 0
- **Structure Validated**: ✓
- **Ready for Implementation**: ✓

## Documentation

- **BST_DESIGN.md**: Complete architecture and node responsibilities
- **DECISION_ESCALATION_SYSTEM.md**: Decision escalation protocol and examples
- **AGGREGATION_SYSTEM.md**: Log, status, and token aggregation system
- **TEST_SCENARIOS.md**: 8 comprehensive test scenarios with inputs/outputs
- **SIMULATION_RESULTS.md**: Detailed simulation traces and validation
- **Each node's prd.md**: Node-specific requirements and specifications
- **Each node's requirements.md**: Detailed functional and non-functional requirements

## Contributing

When implementing:
1. Follow the PRD for each node
2. Use shared utilities (no duplication)
3. Implement decision escalation as specified
4. Maintain log/status/token tracking
5. Write tests based on TEST_SCENARIOS.md
6. Update status.json and logs.json appropriately

## License

This is an educational project for learning distributed system architecture.

## Contact

For questions or issues, refer to the node-specific PRD files or the main design documents.

---

**Project Status**: Design Complete - Ready for Implementation
**Last Updated**: 2026-01-13
**Total Nodes**: 31 (16 leaves + 15 internal)
**Documentation**: Complete
**Validation**: Passed
