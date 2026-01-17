#!/usr/bin/env python3
"""
Generate all node files for the BST structure
Corrected structure: Root is 5_01, decreasing to leaves at 1_xx
"""
import json
import os
from pathlib import Path

# Node definitions: (folder_name, node_name, parent, description, is_leaf)
NODES = [
    # Root (Level 1)
    ("5_01", "Main Orchestrator", None, "Main orchestration and coordination, high-level decision making", False),

    # Level 2
    ("4_01", "Analysis Pipeline", "5_01", "Coordinates all detection/analysis modules", False),
    ("4_02", "Infrastructure and I/O Pipeline", "5_01", "Manages video I/O operations and reporting", False),

    # Level 3
    ("3_01", "Facial and Visual Analysis", "4_01", "Facial feature consistency and visual artifact detection", False),
    ("3_02", "Temporal and ML Analysis", "4_01", "Temporal consistency checks and ML model management", False),
    ("3_03", "Video Processing Pipeline", "4_02", "Video file handling and frame extraction", False),
    ("3_04", "Reporting and Monitoring", "4_02", "Report generation and logging aggregation", False),

    # Level 4
    ("2_01", "Facial Features Analysis", "3_01", "Face detection and landmark extraction coordination", False),
    ("2_02", "Lighting and Shadow Analysis", "3_01", "Light source detection and shadow validation", False),
    ("2_03", "Temporal Motion Analysis", "3_02", "Motion detection and optical flow coordination", False),
    ("2_04", "ML Model Coordination", "3_02", "Model loading and inference pipeline management", False),
    ("2_05", "Video Input Handler", "3_03", "Video file reading and format validation", False),
    ("2_06", "Frame Processing", "3_03", "Frame decoding and buffer management", False),
    ("2_07", "Report Generation", "3_04", "JSON report and visualization creation", False),
    ("2_08", "Log and Status Management", "3_04", "Log aggregation and status collection", False),

    # Level 5 (Leaves)
    ("1_01", "Face Detection Service", "2_01", "Calls face detection libraries (dlib/face-recognition)", True),
    ("1_02", "Facial Landmark Extractor", "2_01", "Calls landmark detection APIs, reads models", True),
    ("1_03", "Eye and Blink Analyzer", "2_02", "Analyzes eye regions and detects blink patterns", True),
    ("1_04", "Shadow Geometry Validator", "2_02", "Validates shadow consistency and light direction", True),
    ("1_05", "Optical Flow Computer", "2_03", "Computes optical flow using OpenCV", True),
    ("1_06", "Motion Vector Analyzer", "2_03", "Analyzes motion patterns and detects anomalies", True),
    ("1_07", "ML Model Loader", "2_04", "Loads models from disk and initializes weights", True),
    ("1_08", "ML Inference Engine", "2_04", "Runs inference on frames using PyTorch/TensorFlow", True),
    ("1_09", "Video File Reader", "2_05", "Opens video files from disk and reads streams", True),
    ("1_10", "Metadata Extractor", "2_05", "Extracts video metadata and codec information", True),
    ("1_11", "Frame Decoder", "2_06", "Decodes video frames from compressed data", True),
    ("1_12", "Frame Buffer Manager", "2_06", "Manages frame cache and temporary storage", True),
    ("1_13", "JSON Report Writer", "2_07", "Writes final report to disk in JSON format", True),
    ("1_14", "Visualization Generator", "2_07", "Generates heatmaps and plots using matplotlib", True),
    ("1_15", "Log File Writer", "2_08", "Writes logs to disk with ring buffer rotation", True),
    ("1_16", "Metrics Aggregator", "2_08", "Collects performance metrics and aggregates statistics", True),
]

def create_config_yaml(folder, node_name, parent, is_leaf):
    """Create config.yaml for a node"""
    content = f"""# Configuration for {node_name}
node_id: "{folder}"
node_name: "{node_name}"
parent_node: "{parent if parent else 'null'}"
node_type: "{'leaf' if is_leaf else 'internal'}"

# Resource limits
max_memory_mb: 512
max_cpu_percent: 50
timeout_seconds: 300

# Token tracking
token_limit_per_operation: 1000
enable_token_tracking: true

# Logging
log_level: "INFO"
log_to_parent: true
log_buffer_size: 100

# Status reporting
status_report_interval_seconds: 60
aggregate_child_status: {'false' if is_leaf else 'true'}

# Decision escalation
auto_escalate_on_error: true
escalation_threshold: 0.7
"""
    return content

def create_prd_md(folder, node_name, description, is_leaf, parent):
    """Create prd.md for a node"""
    content = f"""# PRD: {node_name} ({folder})

## Overview
{description}

## Node Information
- **Node Type**: {'Leaf Node (External I/O)' if is_leaf else 'Internal Node (Coordination)'}
- **Parent Node**: {parent if parent else 'None (Root)'}
- **Level**: {folder[0]}

## Responsibilities

### Primary Functions
"""
    if is_leaf:
        content += f"""- Perform external I/O operations (file/network/API calls)
- Interface with external libraries and services
- Return processed results to parent node
- Log all I/O operations with details
- Track token usage for external API calls
- Handle I/O errors and timeouts
- Implement retry logic for transient failures
"""
    else:
        content += f"""- Coordinate operations of child nodes
- Aggregate results from multiple children
- Make component-level policy decisions
- Escalate complex decisions to parent node
- Filter and aggregate logs from children
- Monitor child node health and status
- Manage resource allocation for children
"""

    content += f"""
## Input/Output Specification

### Inputs
- Configuration from parent node
- Data to process from parent or sibling nodes (via parent)
{'- External data from files, APIs, or external systems' if is_leaf else '- Results and status updates from child nodes'}

### Outputs
- Processed results (to parent)
- Status updates (health, progress)
- Filtered log entries
- Aggregated token usage metrics
- Error and warning notifications
- Performance metrics

## Decision Making

### Local Decisions
"""
    if is_leaf:
        content += """- Retry logic for failed I/O operations
- Timeout handling and cancellation
- Input data validation and sanitization
- Output format selection
- Caching decisions for performance
"""
    else:
        content += """- Child node task distribution
- Result aggregation strategy selection
- Resource allocation among children
- Log filtering criteria
- When to batch vs stream results
"""

    content += """
### Escalation Criteria
When to escalate decisions to parent:
- Unrecoverable errors encountered
- Configuration or policy violations detected
- Resource exhaustion (memory, time, tokens)
- Confidence/quality below acceptable threshold
- Conflicting requirements or constraints
- Security or safety concerns

## Performance Requirements
- Response time: < 5 seconds for typical operations
- Memory usage: < 512 MB per operation
- Token usage: < 1000 tokens per operation
- CPU usage: < 50% sustained

## Error Handling
- **Graceful Degradation**: Continue with reduced functionality
- **Detailed Logging**: Log all errors with context
- **Automatic Retry**: 3 retries with exponential backoff for transient failures
- **Escalation**: Notify parent on persistent failures
- **Cleanup**: Release resources on error

## Dependencies
"""
    if is_leaf:
        content += """- External libraries (OpenCV, PyTorch, TensorFlow, dlib, etc.)
- File system access for reading/writing
- Network connectivity (if applicable)
- Shared level 1 utilities (I/O helpers)
"""
    else:
        content += """- Child nodes must be operational and responsive
- Shared utilities from appropriate level
- Communication protocol implementation
"""

    content += """
## Testing Requirements
- Unit tests for core functionality
- Integration tests with parent node
- Integration tests with child nodes (if applicable)
- Error condition and edge case testing
- Performance and stress testing
- Token usage tracking validation

## Monitoring and Metrics
- Operation success/failure rate
- Average response time
- Resource usage patterns
- Token consumption rate
- Error frequency and types
"""
    return content

def create_todo_md(node_name, is_leaf):
    """Create todo.md for a node"""
    return f"""# TODO List: {node_name}

## Implementation Tasks
- [ ] Implement core processing logic
- [ ] Add comprehensive error handling
- [ ] Implement logging with appropriate filtering
- [ ] Add token tracking and reporting
- [ ] Implement decision escalation logic
{'- [ ] Add retry logic for I/O operations' if is_leaf else '- [ ] Implement child node coordination'}
{'- [ ] Interface with external libraries' if is_leaf else '- [ ] Implement result aggregation'}
- [ ] Add configuration file parsing
- [ ] Implement status reporting
- [ ] Add unit tests
- [ ] Add integration tests with parent
- [ ] Add integration tests with children
- [ ] Performance optimization
- [ ] Documentation and comments

## Testing Tasks
- [ ] Test normal operation flow
- [ ] Test error conditions
- [ ] Test resource exhaustion scenarios
- [ ] Test decision escalation
- [ ] Test log aggregation and filtering
- [ ] Performance benchmarking

## Documentation Tasks
- [ ] Code documentation
- [ ] API documentation
- [ ] Usage examples
- [ ] Error handling guide

## Current Status
Status: Not started
Last updated: 2026-01-13
Progress: 0%
"""

def create_requirements_md(folder, node_name, description, is_leaf, parent):
    """Create requirements.md for a node"""
    content = f"""# Requirements: {node_name} ({folder})

## Functional Requirements

### FR1: Core Functionality
**Description**: {description}

**Acceptance Criteria**:
- Process inputs according to specification
- Produce outputs in expected format
- Handle all specified input types
- Meet response time requirements

### FR2: Parent-Child Communication
**Description**: Must communicate effectively with parent node{' and child nodes' if not is_leaf else ''}

**Acceptance Criteria**:
- Send results to parent in standard format
- Receive configuration from parent
- Send status updates at regular intervals
- Report errors and warnings immediately
{'- Receive results from child nodes' if not is_leaf else ''}
{'- Send commands to child nodes' if not is_leaf else ''}

### FR3: Logging and Monitoring
**Description**: Comprehensive logging with appropriate filtering

**Acceptance Criteria**:
- Log all operations at INFO level or above
- Include timestamps, node ID, and operation ID in logs
- Filter logs before sending to parent
- Keep detailed logs locally
- Support log level configuration

### FR4: Token Tracking
**Description**: Track and report token/resource usage

**Acceptance Criteria**:
- Track tokens for all operations
- Report cumulative usage to parent
- Alert when approaching limits
- Support token budgeting

### FR5: Decision Escalation
**Description**: Escalate decisions when necessary

**Acceptance Criteria**:
- Identify decisions requiring escalation
- Format escalation requests properly
- Handle escalation responses
- Document escalation reasons

"""
    if not is_leaf:
        content += """### FR6: Child Coordination
**Description**: Coordinate multiple child nodes

**Acceptance Criteria**:
- Distribute work to children
- Aggregate results from children
- Monitor child health
- Handle child failures

### FR7: Result Aggregation
**Description**: Combine results from children

**Acceptance Criteria**:
- Aggregate results correctly
- Handle partial results
- Detect inconsistencies
- Apply aggregation rules

"""
    else:
        content += """### FR6: External I/O Operations
**Description**: Perform external I/O safely and efficiently

**Acceptance Criteria**:
- Handle file operations correctly
- Make API calls with proper error handling
- Implement timeout mechanisms
- Validate external data

### FR7: Retry Logic
**Description**: Retry failed operations appropriately

**Acceptance Criteria**:
- Retry transient failures
- Use exponential backoff
- Limit retry attempts
- Log retry attempts

"""

    content += """## Non-Functional Requirements

### NFR1: Performance
**Description**: Meet performance targets
- Process requests within 5 seconds (typical)
- Maintain memory usage below 512 MB
- Efficient resource utilization
- Low CPU overhead

### NFR2: Reliability
**Description**: High reliability and availability
- Handle errors gracefully without crashes
- Implement retry logic for transient failures
- 99% uptime during normal operations
- Recover from failures automatically

### NFR3: Scalability
**Description**: Scale efficiently
- Support concurrent operations where applicable
- Efficient batching of operations
- Resource-aware processing
- Handle increased load gracefully

### NFR4: Maintainability
**Description**: Easy to maintain and extend
- Clear, well-documented code
- Modular design with clear interfaces
- Comprehensive test coverage (>80%)
- Follow coding standards

### NFR5: Security
**Description**: Secure operation
- Validate all inputs
- Sanitize external data
- No code injection vulnerabilities
- Secure credential handling

## Interface Requirements

### Parent Interface
- **Input Format**: JSON or Python dict
- **Output Format**: JSON or Python dict
- **Status Format**: JSON with standard fields
- **Log Format**: JSON with timestamp, level, message

"""
    if not is_leaf:
        content += """### Child Interface
- **Command Format**: JSON or Python dict
- **Result Format**: JSON or Python dict
- **Status Query**: Standard status request/response

"""

    content += """## Constraints

### Technical Constraints
- Must use relative paths only
- Must not duplicate code (use shared folders)
"""
    if is_leaf:
        content += "- External I/O only (no internal coordination)\n"
    else:
        content += "- No external I/O (delegate to leaf nodes)\n"
    content += """- All decisions must follow escalation protocol
- Must respect resource limits

### Environmental Constraints
- WSL environment
- Python 3.9+
- Limited memory and CPU
- Shared file system

## Dependencies

### Internal Dependencies
"""
    if parent:
        content += f"- Parent node: {parent}\n"
    if not is_leaf:
        # Determine children based on folder structure
        level = int(folder[0])
        if level > 1:
            child_level = level - 1
            content += f"- Child nodes at level {child_level}\n"

    level = int(folder[0])
    content += f"- Shared utilities: shared_level_{level}/\n"

    content += """
### External Dependencies
"""
    if is_leaf:
        content += """- OpenCV (cv2)
- NumPy
- PyTorch or TensorFlow (for ML nodes)
- dlib or face-recognition (for face nodes)
- ffmpeg-python (for video nodes)
- Other domain-specific libraries
"""
    else:
        content += """- Child node implementations
- Communication protocol
"""

    content += """
## Validation Criteria

### Unit Test Coverage
- Core functionality: 100%
- Error handling: 100%
- Edge cases: 90%+
- Overall coverage: 80%+

### Integration Test Coverage
- Parent communication: 100%
"""
    if not is_leaf:
        content += "- Child communication: 100%\n"
    content += """- Error scenarios: 80%+

### Performance Validation
- Response time < 5s for 95% of requests
- Memory usage < 512 MB sustained
- No memory leaks over 1000 operations
- Token usage within budget

### Quality Metrics
- No critical bugs
- No high-severity security issues
- Code review approved
- Documentation complete
"""
    return content

def create_status_json(folder, node_name):
    """Create status.json for a node"""
    status = {
        "node_id": folder,
        "node_name": node_name,
        "status": "initialized",
        "health": "healthy",
        "last_updated": "2026-01-13T00:00:00Z",
        "uptime_seconds": 0,
        "operations_completed": 0,
        "operations_failed": 0,
        "operations_in_progress": 0,
        "current_operation": None,
        "resource_usage": {
            "memory_mb": 0,
            "cpu_percent": 0,
            "disk_io_mb": 0
        },
        "child_statuses": {},
        "errors": [],
        "warnings": []
    }
    return json.dumps(status, indent=2)

def create_logs_json(folder):
    """Create logs.json for a node"""
    logs = {
        "node_id": folder,
        "logs": [],
        "log_count": 0,
        "last_log_time": None,
        "error_count": 0,
        "warning_count": 0,
        "info_count": 0,
        "debug_count": 0
    }
    return json.dumps(logs, indent=2)

def create_tokens_json(folder):
    """Create tokens.json for a node"""
    tokens = {
        "node_id": folder,
        "total_tokens": 0,
        "tokens_by_operation": {},
        "last_updated": "2026-01-13T00:00:00Z",
        "token_limit": 1000,
        "tokens_remaining": 1000,
        "alerts": [],
        "usage_history": []
    }
    return json.dumps(tokens, indent=2)

def create_source_py(folder, node_name, is_leaf, parent):
    """Create source.py template for a node"""
    class_name = node_name.replace(" ", "").replace("&", "And").replace("-", "")

    content = f'''"""
{node_name} ({folder})
Implementation module for the BST DeepFake Detection System
"""
from typing import Dict, Any, Optional, List
import json
from pathlib import Path
from datetime import datetime

class {class_name}:
    """
    {node_name} implementation

    Responsibilities:
    - {'External I/O operations' if is_leaf else 'Child node coordination'}
    - Result processing and formatting
    - Error handling and recovery
    - Logging and monitoring
    - Token tracking
    """

    def __init__(self, config_path: str):
        """
        Initialize the node

        Args:
            config_path: Path to configuration file
        """
        self.node_id = "{folder}"
        self.node_name = "{node_name}"
        self.parent_id = "{parent if parent else None}"
        self.config = self._load_config(config_path)
        self.status = self._load_status()
        self.tokens = self._load_tokens()
        self.logs = []

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file

        Args:
            config_path: Path to config.yaml

        Returns:
            Configuration dictionary
        """
        # TODO: Implement YAML loading
        # import yaml
        # with open(config_path) as f:
        #     return yaml.safe_load(f)
        return {{
            "node_id": self.node_id,
            "max_memory_mb": 512,
            "timeout_seconds": 300,
            "token_limit": 1000
        }}

    def _load_status(self) -> Dict[str, Any]:
        """Load current status from status.json"""
        status_path = Path(__file__).parent / "status.json"
        if status_path.exists():
            with open(status_path) as f:
                return json.load(f)
        return {{"status": "initialized", "health": "healthy"}}

    def _load_tokens(self) -> Dict[str, Any]:
        """Load token tracking data from tokens.json"""
        tokens_path = Path(__file__).parent / "tokens.json"
        if tokens_path.exists():
            with open(tokens_path) as f:
                return json.load(f)
        return {{"total_tokens": 0, "token_limit": 1000}}

    def _save_status(self):
        """Save current status to status.json"""
        status_path = Path(__file__).parent / "status.json"
        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(status_path, 'w') as f:
            json.dump(self.status, f, indent=2)

    def _save_tokens(self):
        """Save token tracking data to tokens.json"""
        tokens_path = Path(__file__).parent / "tokens.json"
        self.tokens["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(tokens_path, 'w') as f:
            json.dump(self.tokens, f, indent=2)

    def _save_logs(self):
        """Save logs to logs.json"""
        logs_path = Path(__file__).parent / "logs.json"
        logs_data = {{
            "node_id": self.node_id,
            "logs": self.logs[-100:],  # Keep last 100 logs
            "log_count": len(self.logs),
            "last_log_time": datetime.utcnow().isoformat() + "Z" if self.logs else None
        }}
        with open(logs_path, 'w') as f:
            json.dump(logs_data, f, indent=2)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing function

        Args:
            input_data: Input data from parent or external source

        Returns:
            Processed results as dictionary
        """
        try:
            self.log("INFO", f"Starting processing: {{input_data.get('operation', 'unknown')}}")
            self.update_status("processing", "healthy")

            # TODO: Implement processing logic
            {'result = self._perform_io_operation(input_data)' if is_leaf else 'result = self._coordinate_children(input_data)'}

            self.status["operations_completed"] += 1
            self.update_status("idle", "healthy")
            self.log("INFO", "Processing completed successfully")

            return result

        except Exception as e:
            self.status["operations_failed"] += 1
            self.log("ERROR", f"Processing failed: {{str(e)}}")
            self.update_status("error", "degraded")

            # Check if should escalate
            if self._should_escalate(e):
                return self.escalate_decision({{
                    "error": str(e),
                    "input": input_data,
                    "reason": "unrecoverable_error"
                }})

            raise

'''

    if is_leaf:
        content += '''    def _perform_io_operation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform external I/O operation

        Args:
            input_data: Operation parameters

        Returns:
            Operation results
        """
        # TODO: Implement I/O operation
        # Examples:
        # - Read from file
        # - Call external API
        # - Run ML inference
        # - Process frames
        pass

    def _retry_operation(self, operation_func, max_retries: int = 3) -> Any:
        """
        Retry an operation with exponential backoff

        Args:
            operation_func: Function to retry
            max_retries: Maximum number of retries

        Returns:
            Operation result
        """
        import time

        for attempt in range(max_retries):
            try:
                return operation_func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = 2 ** attempt
                self.log("WARNING", f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
                time.sleep(wait_time)
'''
    else:
        content += '''    def _coordinate_children(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate child nodes to process input

        Args:
            input_data: Input to be processed by children

        Returns:
            Aggregated results from children
        """
        # TODO: Implement child coordination
        # 1. Distribute work to children
        # 2. Collect results
        # 3. Aggregate results
        # 4. Handle failures
        pass

    def _aggregate_results(self, child_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results from child nodes

        Args:
            child_results: List of results from children

        Returns:
            Aggregated result
        """
        # TODO: Implement aggregation logic
        pass

    def _aggregate_logs(self, child_logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aggregate and filter logs from children

        Args:
            child_logs: Logs from all children

        Returns:
            Filtered logs to pass to parent
        """
        # Filter: keep errors, warnings, and sample of info logs
        filtered = []
        for log in child_logs:
            if log.get("level") in ["ERROR", "WARNING"]:
                filtered.append(log)
            elif log.get("level") == "INFO" and len(filtered) < 20:
                filtered.append(log)
        return filtered
'''

    content += '''
    def log(self, level: str, message: str, **kwargs):
        """
        Log a message

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR)
            message: Log message
            **kwargs: Additional context
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "node_id": self.node_id,
            "level": level,
            "message": message,
            **kwargs
        }
        self.logs.append(log_entry)

        # Also print to console
        print(f"[{level}] {self.node_id}: {message}")

        # Periodically save logs
        if len(self.logs) % 10 == 0:
            self._save_logs()

    def update_status(self, status: str, health: str = "healthy"):
        """
        Update node status

        Args:
            status: Current status (idle, processing, error)
            health: Health status (healthy, degraded, unhealthy)
        """
        self.status["status"] = status
        self.status["health"] = health
        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self._save_status()

    def track_tokens(self, operation: str, token_count: int):
        """
        Track token usage for an operation

        Args:
            operation: Operation name
            token_count: Number of tokens used
        """
        self.tokens["total_tokens"] += token_count

        if operation not in self.tokens["tokens_by_operation"]:
            self.tokens["tokens_by_operation"][operation] = 0
        self.tokens["tokens_by_operation"][operation] += token_count

        # Check if approaching limit
        limit = self.tokens["token_limit"]
        if self.tokens["total_tokens"] > limit * 0.8:
            alert = f"Token usage at {self.tokens['total_tokens']}/{limit} (80%+)"
            self.log("WARNING", alert)
            if alert not in self.tokens["alerts"]:
                self.tokens["alerts"].append(alert)

        self._save_tokens()

    def escalate_decision(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Escalate a decision to parent node

        Args:
            decision_data: Decision context and options

        Returns:
            Decision from parent
        """
        self.log("INFO", f"Escalating decision: {decision_data.get('reason', 'unknown')}")

        escalation_request = {
            "from_node": self.node_id,
            "to_node": self.parent_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "decision_data": decision_data
        }

        # TODO: Implement actual communication with parent
        # For now, return a placeholder
        return {
            "decision": "proceed_with_caution",
            "reason": "placeholder_response"
        }

    def _should_escalate(self, error: Exception) -> bool:
        """
        Determine if an error should be escalated

        Args:
            error: The exception that occurred

        Returns:
            True if should escalate
        """
        # Escalate on certain error types
        escalate_types = (ValueError, RuntimeError, MemoryError)
        return isinstance(error, escalate_types)

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get comprehensive status report

        Returns:
            Status report dictionary
        """
        return {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "status": self.status,
            "tokens": {
                "total": self.tokens["total_tokens"],
                "limit": self.tokens["token_limit"],
                "alerts": self.tokens["alerts"]
            },
            "logs": {
                "count": len(self.logs),
                "recent_errors": [log for log in self.logs[-20:] if log.get("level") == "ERROR"]
            }
        }
'''

    return content

def generate_all_files():
    """Generate all files for all nodes"""
    base_path = Path(".")

    print("Generating node files for BST structure...")
    print(f"Total nodes: {len(NODES)}")
    print()

    for folder, node_name, parent, description, is_leaf in NODES:
        node_path = base_path / folder

        print(f"Generating {folder}: {node_name}")

        # Create config.yaml
        with open(node_path / "config.yaml", "w") as f:
            f.write(create_config_yaml(folder, node_name, parent, is_leaf))

        # Create prd.md
        with open(node_path / "prd.md", "w") as f:
            f.write(create_prd_md(folder, node_name, description, is_leaf, parent))

        # Create todo.md
        with open(node_path / "todo.md", "w") as f:
            f.write(create_todo_md(node_name, is_leaf))

        # Create requirements.md
        with open(node_path / "requirements.md", "w") as f:
            f.write(create_requirements_md(folder, node_name, description, is_leaf, parent))

        # Create status.json
        with open(node_path / "status.json", "w") as f:
            f.write(create_status_json(folder, node_name))

        # Create logs.json
        with open(node_path / "logs.json", "w") as f:
            f.write(create_logs_json(folder))

        # Create tokens.json
        with open(node_path / "tokens.json", "w") as f:
            f.write(create_tokens_json(folder))

        # Create source.py
        with open(node_path / "source.py", "w") as f:
            f.write(create_source_py(folder, node_name, is_leaf, parent))

    print()
    print(f"✓ Generated files for {len(NODES)} nodes!")
    print("✓ Each node contains: config.yaml, prd.md, todo.md, requirements.md,")
    print("  status.json, logs.json, tokens.json, source.py")

if __name__ == "__main__":
    generate_all_files()
