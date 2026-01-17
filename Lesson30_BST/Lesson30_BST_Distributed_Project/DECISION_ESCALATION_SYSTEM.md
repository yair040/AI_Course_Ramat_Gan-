# Decision Escalation System

## Overview
The BST-based DeepFake Detection System implements a hierarchical decision escalation protocol. Decisions are made at the lowest competent level, with complex or high-stakes decisions escalated up the tree.

## Escalation Principles

### 1. Subsidiarity
Decisions should be made at the lowest level with sufficient information and authority.

### 2. Clear Criteria
Each node has explicit criteria for when to escalate decisions.

### 3. Context Preservation
Escalation requests include full context for informed decision-making.

### 4. Timely Response
Escalations have timeouts; if parent doesn't respond, node uses safe defaults.

## Escalation Flow

```
Leaf Node (1_xx)
  ↓ (Escalates if: unrecoverable error, policy decision needed, low confidence)
Level 4 Node (2_xx)
  ↓ (Escalates if: cross-component impact, resource allocation, conflicting requirements)
Level 3 Node (3_xx)
  ↓ (Escalates if: pipeline coordination, major resource decision, priority conflicts)
Level 2 Node (4_xx)
  ↓ (Escalates if: subsystem coordination, system-wide policy, security concerns)
Root Node (5_01)
  ↓ (Makes final decision or fails safely)
```

## Decision Categories

### Category 1: Local I/O Decisions (Leaves - 1_xx)
**Decided Locally**:
- Retry logic parameters
- Timeout values (within bounds)
- Cache utilization
- Buffer sizes
- Request batching

**Escalate When**:
- All retries exhausted
- Resource limits exceeded
- Invalid/corrupted data detected
- Security threat identified
- Confidence below threshold (e.g., < 0.7)

**Example** (1_09 - Video File Reader):
```python
# Local decision
if file_size < 100MB:
    read_strategy = "load_all"
else:
    read_strategy = "stream"

# Escalation needed
if file_format == "unknown":
    escalate_to_parent({
        "reason": "unsupported_format",
        "file_format": detected_format,
        "options": ["skip", "attempt_conversion", "fail"]
    })
```

### Category 2: Component-Level Decisions (Level 4 - 2_xx)
**Decided Locally**:
- Child task distribution
- Result aggregation method
- Local resource allocation
- Error recovery strategy
- Performance optimizations

**Escalate When**:
- Child node failure
- Inconsistent results from children
- Cross-component dependency needed
- Resource contention
- Quality threshold not met

**Example** (2_01 - Facial Features Analysis):
```python
# Local decision
face_results = aggregate_from_children([1_01_result, 1_02_result])

# Escalation needed
if confidence(face_results) < 0.7:
    escalate_to_parent({
        "reason": "low_confidence_detection",
        "confidence": confidence(face_results),
        "options": ["retry_with_different_model", "flag_for_manual_review", "proceed_anyway"]
    })
```

### Category 3: Pipeline-Level Decisions (Level 3 - 3_xx)
**Decided Locally**:
- Pipeline stage ordering
- Inter-component data flow
- Pipeline-level caching
- Load balancing among components
- Error handling strategy

**Escalate When**:
- Pipeline deadlock or circular dependency
- Major performance degradation
- Cross-pipeline coordination needed
- Critical component failure
- Policy violation detected

**Example** (3_01 - Facial and Visual Analysis):
```python
# Local decision
if lighting_confidence > 0.8:
    weight_lighting_heavily_in_result()

# Escalation needed
if facial_results.contradict(lighting_results):
    escalate_to_parent({
        "reason": "contradictory_analysis",
        "facial_confidence": 0.85,
        "lighting_confidence": 0.20,
        "conflict": "Face detected with impossible lighting",
        "options": ["trust_facial", "trust_lighting", "flag_uncertain", "reanalyze"]
    })
```

### Category 4: Subsystem-Level Decisions (Level 2 - 4_xx)
**Decided Locally**:
- Overall analysis strategy
- Resource allocation between pipelines
- Priority and scheduling
- Quality vs performance trade-offs
- Subsystem-wide error recovery

**Escalate When**:
- Cross-subsystem coordination needed
- System-wide resource exhaustion
- Security or safety critical decision
- Conflicting objectives
- Major architectural decision needed

**Example** (4_01 - Analysis Pipeline):
```python
# Local decision
allocate_resources({
    "facial_analysis": 40%,
    "temporal_analysis": 35%,
    "ml_inference": 25%
})

# Escalation needed
if analysis_time > 2x_video_duration:
    escalate_to_parent({
        "reason": "performance_unacceptable",
        "current_time": analysis_time,
        "target_time": video_duration * 2,
        "options": ["reduce_quality", "skip_frames", "add_resources", "abort"]
    })
```

### Category 5: System-Level Decisions (Root - 5_01)
**Decided Locally**:
- Overall system behavior
- Final report generation
- User-facing decisions
- System-wide resource allocation
- Abort or proceed decisions

**No Escalation** (Root is final authority):
- Makes final decision or fails safely
- May log decisions for audit trail
- May prompt user if configured

**Example** (5_01 - Main Orchestrator):
```python
# Final decision
if overall_confidence < 0.6:
    final_decision = {
        "verdict": "uncertain",
        "confidence": overall_confidence,
        "recommendation": "manual_review_needed",
        "reason": "Multiple analysis components reported low confidence"
    }
```

## Escalation Request Format

### Standard Escalation Request
```json
{
  "escalation_id": "uuid-v4",
  "from_node": "1_09",
  "to_node": "2_05",
  "timestamp": "2026-01-13T12:34:56Z",
  "priority": "normal",
  "timeout_seconds": 30,
  "reason": "unsupported_format",
  "context": {
    "operation": "read_video_file",
    "file_path": "video.mov",
    "detected_format": "QuickTime MOV",
    "supported_formats": ["mp4", "avi", "mkv"],
    "error": "Codec not supported"
  },
  "options": [
    {
      "id": "skip",
      "description": "Skip this file and report error",
      "risk": "low",
      "cost": "low"
    },
    {
      "id": "attempt_conversion",
      "description": "Try to convert using ffmpeg",
      "risk": "medium",
      "cost": "high"
    },
    {
      "id": "fail",
      "description": "Fail the entire operation",
      "risk": "high",
      "cost": "low"
    }
  ],
  "default_action": "skip",
  "recommendation": "attempt_conversion"
}
```

### Escalation Response
```json
{
  "escalation_id": "uuid-v4",
  "from_node": "2_05",
  "to_node": "1_09",
  "timestamp": "2026-01-13T12:35:01Z",
  "decision": "attempt_conversion",
  "reason": "Format conversion is acceptable for non-critical operations",
  "conditions": {
    "max_conversion_time": 60,
    "fallback_on_failure": "skip"
  },
  "metadata": {
    "decided_by": "2_05",
    "confidence": 0.85,
    "logged": true
  }
}
```

## Timeout Handling

### Timeout Values by Level
- **Leaf to Level 4**: 5 seconds
- **Level 4 to Level 3**: 10 seconds
- **Level 3 to Level 2**: 15 seconds
- **Level 2 to Root**: 30 seconds

### On Timeout
1. Log timeout event
2. Execute `default_action` from escalation request
3. Report timeout to parent (for monitoring)
4. Continue operation

## Safe Defaults

Each escalation request MUST specify a safe default action.

### Default Action Guidelines
- **Prefer safety over performance**: When in doubt, fail safe
- **Prefer reversible actions**: Choose actions that can be undone
- **Prefer conservative behavior**: Err on the side of caution
- **Prefer data integrity**: Don't corrupt or lose data

### Examples of Safe Defaults
- **Unknown format**: Skip with error report
- **Low confidence**: Flag for manual review
- **Resource exhaustion**: Reduce quality/resolution
- **Timeout**: Use cached/previous results if available
- **Corruption detected**: Quarantine and report

## Decision Logging

All escalations and decisions are logged for audit trail.

### Log Entry Format
```json
{
  "timestamp": "2026-01-13T12:34:56Z",
  "escalation_id": "uuid-v4",
  "from_node": "1_09",
  "to_node": "2_05",
  "reason": "unsupported_format",
  "decision": "attempt_conversion",
  "decision_time_ms": 150,
  "outcome": "success",
  "confidence": 0.85
}
```

## Performance Considerations

### Minimizing Escalations
- Cache common decisions
- Learn from previous escalations
- Provide comprehensive configuration
- Empower nodes with clear policies

### Escalation Metrics
- Track escalation frequency by node
- Measure decision latency
- Monitor timeout rate
- Analyze decision outcomes

## Security Considerations

### Escalate Immediately For
- Suspected malicious input
- Security policy violations
- Access control violations
- Suspicious patterns detected

### Security Escalation Priority
All security escalations have `priority: "critical"` with shorter timeouts (2 seconds) and mandatory logging.

## Testing Escalation System

### Test Scenarios
1. **Normal escalation**: Leaf to parent, parent decides, leaf executes
2. **Timeout**: Leaf escalates, parent doesn't respond, default action executed
3. **Multi-level**: Leaf → Level 4 → Level 3 → decision made at Level 3
4. **Concurrent escalations**: Multiple children escalate simultaneously
5. **Cascading failures**: Multiple levels fail, reaches root
6. **Security escalation**: Critical security issue escalated with priority

### Success Criteria
- All escalations reach appropriate decision-maker
- Timeouts handled gracefully
- Safe defaults always specified
- Audit trail complete
- Performance acceptable (< 100ms overhead)
