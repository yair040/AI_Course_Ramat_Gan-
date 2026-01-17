# BST Structure Design for DeepFake Detection System

## Overview
5-level Binary Search Tree with 16 leaves organizing DeepFake detection components.
External I/O operations confined to leaf nodes. Decision escalation flows upward.
**Folder naming: Root is 5_01, decreasing to leaves at 1_xx level.**

## Tree Structure

```
Level 1 (Root):
└── 5_01: Main Orchestrator & Controller

Level 2 (2 nodes):
├── 4_01: Analysis Pipeline (all detection/analysis)
└── 4_02: Infrastructure & I/O Pipeline

Level 3 (4 nodes):
├── 3_01: Facial & Visual Analysis (parent: 4_01)
├── 3_02: Temporal & ML Analysis (parent: 4_01)
├── 3_03: Video Processing Pipeline (parent: 4_02)
└── 3_04: Reporting & Monitoring (parent: 4_02)

Level 4 (8 nodes):
├── 2_01: Facial Features Analysis (parent: 3_01)
├── 2_02: Lighting & Shadow Analysis (parent: 3_01)
├── 2_03: Temporal Motion Analysis (parent: 3_02)
├── 2_04: ML Model Coordination (parent: 3_02)
├── 2_05: Video Input Handler (parent: 3_03)
├── 2_06: Frame Processing (parent: 3_03)
├── 2_07: Report Generation (parent: 3_04)
└── 2_08: Log & Status Management (parent: 3_04)

Level 5 (16 leaves - all external I/O):
├── 1_01: Face Detection Service (parent: 2_01)
├── 1_02: Facial Landmark Extractor (parent: 2_01)
├── 1_03: Eye & Blink Analyzer (parent: 2_02)
├── 1_04: Shadow Geometry Validator (parent: 2_02)
├── 1_05: Optical Flow Computer (parent: 2_03)
├── 1_06: Motion Vector Analyzer (parent: 2_03)
├── 1_07: ML Model Loader (parent: 2_04)
├── 1_08: ML Inference Engine (parent: 2_04)
├── 1_09: Video File Reader (parent: 2_05)
├── 1_10: Metadata Extractor (parent: 2_05)
├── 1_11: Frame Decoder (parent: 2_06)
├── 1_12: Frame Buffer Manager (parent: 2_06)
├── 1_13: JSON Report Writer (parent: 2_07)
├── 1_14: Visualization Generator (parent: 2_07)
├── 1_15: Log File Writer (parent: 2_08)
└── 1_16: Metrics Aggregator (parent: 2_08)
```

## Node Responsibilities

### Root (5_01)
- Main orchestration and coordination
- High-level decision making
- Configuration management
- Final result aggregation
- Overall system status

### Level 2

**4_01: Analysis Pipeline**
- Coordinates all detection/analysis modules
- Aggregates detection results
- Manages analysis workflow
- Escalates complex detection decisions

**4_02: Infrastructure & I/O Pipeline**
- Manages video I/O operations
- Handles logging and reporting
- Resource management
- Performance monitoring

### Level 3

**3_01: Facial & Visual Analysis**
- Facial feature consistency
- Visual artifact detection
- Expression analysis coordination
- Lighting/shadow analysis

**3_02: Temporal & ML Analysis**
- Temporal consistency checks
- Motion analysis coordination
- ML model management
- Deep learning inference coordination

**3_03: Video Processing Pipeline**
- Video file handling
- Frame extraction management
- Metadata processing
- Buffer management

**3_04: Reporting & Monitoring**
- Report generation coordination
- Logging aggregation
- Status monitoring
- Metrics collection

### Level 4

**2_01: Facial Features Analysis**
- Face detection coordination
- Landmark extraction management
- Facial geometry validation
- Expression consistency

**2_02: Lighting & Shadow Analysis**
- Light source detection
- Shadow geometry validation
- Reflection analysis
- Color temperature consistency

**2_03: Temporal Motion Analysis**
- Motion detection
- Optical flow coordination
- Velocity/acceleration analysis
- Jitter detection

**2_04: ML Model Coordination**
- Model loading and initialization
- Inference pipeline management
- Ensemble voting
- Confidence scoring

**2_05: Video Input Handler**
- Video file reading
- Format validation
- Metadata extraction
- Stream management

**2_06: Frame Processing**
- Frame decoding
- Buffer management
- Frame batching
- Multi-scale processing

**2_07: Report Generation**
- JSON report creation
- Visualization generation
- Result formatting
- Anomaly highlighting

**2_08: Log & Status Management**
- Log aggregation from all nodes
- Status collection and filtering
- Token usage tracking
- Performance metrics

### Level 5 (Leaves - External I/O Only)

**1_01: Face Detection Service**
- Calls face detection libraries (dlib/face-recognition)
- Reads face detection models from disk
- Returns detected face regions

**1_02: Facial Landmark Extractor**
- Calls landmark detection APIs
- Reads landmark models from disk
- Returns facial keypoints

**1_03: Eye & Blink Analyzer**
- Analyzes eye regions
- Detects blink patterns
- Measures pupil dilation
- Writes analysis results

**1_04: Shadow Geometry Validator**
- Validates shadow consistency
- Analyzes light direction
- Writes validation results

**1_05: Optical Flow Computer**
- Computes optical flow (OpenCV)
- Reads flow algorithms from libraries
- Returns motion vectors

**1_06: Motion Vector Analyzer**
- Analyzes motion patterns
- Detects anomalies
- Writes analysis results

**1_07: ML Model Loader**
- Loads models from disk
- Reads model configurations
- Initializes model weights

**1_08: ML Inference Engine**
- Runs inference on frames
- Calls PyTorch/TensorFlow
- Returns predictions

**1_09: Video File Reader**
- Opens video files from disk
- Reads video streams
- Validates file format

**1_10: Metadata Extractor**
- Extracts video metadata
- Reads codec information
- Analyzes timestamps

**1_11: Frame Decoder**
- Decodes video frames
- Reads compressed data
- Returns raw frame data

**1_12: Frame Buffer Manager**
- Manages frame cache
- Writes frames to temporary storage
- Reads cached frames

**1_13: JSON Report Writer**
- Writes final report to disk
- Formats JSON output
- Creates report file

**1_14: Visualization Generator**
- Generates heatmaps
- Writes visualization files
- Creates plots using matplotlib

**1_15: Log File Writer**
- Writes logs to disk
- Manages log rotation
- Ring buffer implementation

**1_16: Metrics Aggregator**
- Collects performance metrics
- Writes metrics to disk
- Aggregates statistics

## Decision Escalation Flow

```
Leaf Node (1_xx) → Makes local I/O decision
     ↓ (if requires policy decision)
Level 4 (2_xx) → Decides on component-level policies
     ↓ (if requires cross-component decision)
Level 3 (3_xx) → Decides on pipeline-level coordination
     ↓ (if requires system-wide decision)
Level 2 (4_xx) → Decides on major subsystem behavior
     ↓ (if requires overall system decision)
Root (5_01) → Makes final system-wide decision
```

## Log/Status/Token Aggregation Flow

```
Leaf (1_xx): Detailed logs → Filter → Summary
     ↓
Level 4 (2_xx): Component logs → Filter → Component summary
     ↓
Level 3 (3_xx): Pipeline logs → Filter → Pipeline summary
     ↓
Level 2 (4_xx): Subsystem logs → Filter → Subsystem summary
     ↓
Root (5_01): System logs → Final summary
```

### Aggregation Rules
- **Logs**: Filter by severity, keep errors/warnings, sample info logs
- **Status**: Aggregate success/failure counts, worst status propagates up
- **Tokens**: Sum of all token usage at each level

## Shared Folders per Level

Each level has a `shared_level_X/` folder containing:
- Common utilities
- Shared configurations
- Common data structures
- Reusable functions

**shared_level_5/**: System-wide utilities (for root 5_01)
**shared_level_4/**: Subsystem coordination utilities (for 4_01, 4_02)
**shared_level_3/**: Pipeline management utilities (for 3_01-3_04)
**shared_level_2/**: Component coordination utilities (for 2_01-2_08)
**shared_level_1/**: I/O helpers and file utilities (for leaves 1_01-1_16)

## Node File Structure

Each node contains:
```
{node_folder}/
├── config.yaml          # Node configuration
├── prd.md              # Node-specific requirements
├── todo.md             # Task list
├── requirements.md     # Detailed requirements
├── status.json         # Current status
├── logs.json           # Node logs
├── tokens.json         # Token usage tracking
└── source.py           # Source code (if applicable)
```

## Communication Protocol

1. **Child to Parent**: Results, status updates, decision requests
2. **Parent to Child**: Commands, configuration updates, decisions
3. **Sibling Communication**: Through parent node only
4. **Shared Resources**: Accessed via shared folders

## Key Principles

1. **No Code Duplication**: Common code in shared folders
2. **External I/O in Leaves Only**: All file/network I/O at leaf level (1_xx)
3. **Decision Escalation**: Complex decisions move up the tree
4. **Log Filtering**: Each level filters before passing up
5. **Token Tracking**: Cumulative tracking up the tree
