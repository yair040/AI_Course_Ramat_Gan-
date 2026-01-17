# Log, Status, and Token Aggregation System

## Overview
The BST implements a hierarchical aggregation system where each level filters, summarizes, and aggregates information from its children before passing it up the tree. This prevents information overload at higher levels while maintaining critical details.

## Core Principles

### 1. Progressive Filtering
Each level filters data more aggressively:
- **Level 5 (Leaves)**: Detailed logs, full status
- **Level 4**: Component summaries, filtered logs
- **Level 3**: Pipeline summaries, key metrics
- **Level 2**: Subsystem summaries, critical alerts
- **Root**: System overview, final metrics

### 2. Information Preservation
Critical information is never filtered:
- Errors and warnings always propagate
- Security alerts always propagate
- Performance anomalies always propagate
- Token limit violations always propagate

### 3. Cumulative Tracking
Some metrics accumulate:
- Token usage (sum of all children)
- Operation counts (sum of all children)
- Error counts (sum of all children)
- Timing information (aggregated statistics)

## Log Aggregation

### Log Levels
- **ERROR**: Always propagated
- **WARNING**: Always propagated
- **INFO**: Sampled/filtered
- **DEBUG**: Rarely propagated (only on demand)

### Filtering Rules by Level

#### Leaves (1_xx) → Level 4 (2_xx)
**Keep**:
- All ERROR and WARNING logs
- First 5 INFO logs per operation
- INFO logs with anomalies
- Last INFO log (completion status)

**Sample**:
- 1 out of every 10 routine INFO logs

**Discard**:
- Most DEBUG logs
- Repetitive INFO logs

**Example Filter**:
```python
def filter_leaf_logs(logs):
    filtered = []
    info_count = 0

    for log in logs:
        if log['level'] in ['ERROR', 'WARNING']:
            filtered.append(log)
        elif log['level'] == 'INFO':
            if info_count < 5 or log.get('anomaly') or log.get('is_final'):
                filtered.append(log)
                info_count += 1
            elif info_count % 10 == 0:
                filtered.append(log)
                info_count += 1

    return filtered
```

#### Level 4 (2_xx) → Level 3 (3_xx)
**Keep**:
- All ERROR and WARNING logs
- Component summary logs
- Performance anomalies
- First and last INFO per operation

**Aggregate**:
- Multiple similar errors → single error with count
- Routine INFO → summary statistics

**Example Aggregation**:
```python
def aggregate_component_logs(child_logs):
    aggregated = {
        'errors': {},
        'warnings': {},
        'summary': {}
    }

    for node_id, logs in child_logs.items():
        for log in logs:
            if log['level'] == 'ERROR':
                error_key = log.get('error_type', 'unknown')
                if error_key not in aggregated['errors']:
                    aggregated['errors'][error_key] = {
                        'count': 0,
                        'first_occurrence': log['timestamp'],
                        'sample_message': log['message']
                    }
                aggregated['errors'][error_key]['count'] += 1

    return format_aggregated_logs(aggregated)
```

#### Level 3 (3_xx) → Level 2 (4_xx)
**Keep**:
- All ERROR logs (may aggregate similar ones)
- Critical WARNING logs
- Pipeline summaries
- Performance metrics

**Aggregate**:
- Similar warnings → summary with count
- Operation metrics → pipeline statistics

#### Level 2 (4_xx) → Root (5_01)
**Keep**:
- System-critical ERROR logs
- High-priority WARNING logs
- Subsystem summaries
- Overall metrics

**Aggregate**:
- All logs → executive summary
- Metrics → system-wide statistics

### Log Entry Format

#### Detailed Log (Leaves)
```json
{
  "timestamp": "2026-01-13T12:34:56.789Z",
  "node_id": "1_09",
  "level": "INFO",
  "operation_id": "uuid-v4",
  "message": "Successfully read video file",
  "details": {
    "file_path": "video.mp4",
    "file_size_mb": 145.7,
    "duration_seconds": 62.3,
    "format": "mp4",
    "codec": "h264"
  },
  "metrics": {
    "read_time_ms": 234,
    "decode_time_ms": 1234
  }
}
```

#### Aggregated Log (Level 4)
```json
{
  "timestamp": "2026-01-13T12:35:00.000Z",
  "node_id": "2_05",
  "level": "INFO",
  "operation_id": "uuid-v4",
  "message": "Video Input Handler completed processing",
  "summary": {
    "total_operations": 5,
    "successful": 4,
    "failed": 1,
    "total_data_mb": 523.4,
    "total_time_ms": 3456
  },
  "child_nodes": ["1_09", "1_10"],
  "notable_events": [
    {
      "node": "1_09",
      "level": "WARNING",
      "message": "Codec conversion required for 1 file"
    }
  ]
}
```

#### Executive Summary (Root)
```json
{
  "timestamp": "2026-01-13T12:36:00.000Z",
  "node_id": "5_01",
  "level": "INFO",
  "operation_id": "uuid-v4",
  "message": "DeepFake detection analysis complete",
  "system_summary": {
    "overall_status": "completed_with_warnings",
    "total_operations": 47,
    "errors": 0,
    "warnings": 3,
    "duration_seconds": 125.4,
    "video_duration_seconds": 62.3,
    "analysis_ratio": 2.01
  },
  "subsystem_summaries": {
    "analysis_pipeline": {
      "status": "completed",
      "confidence": 0.87,
      "operations": 32
    },
    "infrastructure": {
      "status": "completed_with_warnings",
      "warnings": 3,
      "operations": 15
    }
  },
  "critical_alerts": []
}
```

## Status Aggregation

### Status States
- **healthy**: All good
- **degraded**: Operating with reduced functionality
- **unhealthy**: Not functioning properly
- **error**: Critical failure
- **unknown**: Cannot determine status

### Aggregation Rules

#### Child Status → Parent Status
```python
def aggregate_status(child_statuses):
    """
    Worst status propagates up.
    If any child is unhealthy/error, parent is degraded/unhealthy.
    """
    status_priority = {
        'error': 4,
        'unhealthy': 3,
        'degraded': 2,
        'healthy': 1,
        'unknown': 0
    }

    worst_status = 'healthy'
    error_count = 0
    unhealthy_count = 0
    degraded_count = 0

    for child_id, child_status in child_statuses.items():
        state = child_status['health']
        if status_priority[state] > status_priority[worst_status]:
            worst_status = state

        if state == 'error':
            error_count += 1
        elif state == 'unhealthy':
            unhealthy_count += 1
        elif state == 'degraded':
            degraded_count += 1

    # Parent status determination
    if error_count > 0:
        parent_status = 'unhealthy'
    elif unhealthy_count > 0:
        parent_status = 'degraded'
    elif degraded_count > 0:
        parent_status = 'degraded'
    else:
        parent_status = 'healthy'

    return {
        'health': parent_status,
        'child_summary': {
            'total': len(child_statuses),
            'error': error_count,
            'unhealthy': unhealthy_count,
            'degraded': degraded_count,
            'healthy': len(child_statuses) - error_count - unhealthy_count - degraded_count
        }
    }
```

### Status Report Format

#### Leaf Status
```json
{
  "node_id": "1_09",
  "node_name": "Video File Reader",
  "health": "healthy",
  "status": "idle",
  "last_updated": "2026-01-13T12:34:56Z",
  "uptime_seconds": 3245,
  "operations_completed": 47,
  "operations_failed": 2,
  "operations_in_progress": 0,
  "current_operation": null,
  "resource_usage": {
    "memory_mb": 234.5,
    "cpu_percent": 12.3,
    "disk_io_mb": 523.4
  },
  "recent_errors": []
}
```

#### Internal Node Status
```json
{
  "node_id": "2_05",
  "node_name": "Video Input Handler",
  "health": "healthy",
  "status": "idle",
  "last_updated": "2026-01-13T12:35:00Z",
  "uptime_seconds": 3250,
  "operations_completed": 15,
  "operations_failed": 0,
  "operations_in_progress": 0,
  "current_operation": null,
  "resource_usage": {
    "memory_mb": 456.7,
    "cpu_percent": 23.4,
    "disk_io_mb": 678.9
  },
  "child_summary": {
    "total_children": 2,
    "healthy": 2,
    "degraded": 0,
    "unhealthy": 0,
    "error": 0
  },
  "child_statuses": {
    "1_09": {
      "health": "healthy",
      "operations_completed": 47
    },
    "1_10": {
      "health": "healthy",
      "operations_completed": 12
    }
  }
}
```

#### Root Status
```json
{
  "node_id": "5_01",
  "node_name": "Main Orchestrator",
  "health": "healthy",
  "status": "idle",
  "last_updated": "2026-01-13T12:36:00Z",
  "system_uptime_seconds": 3600,
  "total_operations_completed": 1523,
  "total_operations_failed": 12,
  "overall_success_rate": 0.992,
  "resource_usage": {
    "total_memory_mb": 2345.6,
    "total_cpu_percent": 67.8,
    "total_disk_io_mb": 12345.6
  },
  "subsystem_health": {
    "analysis_pipeline": "healthy",
    "infrastructure": "healthy"
  },
  "system_alerts": [],
  "performance_metrics": {
    "avg_operation_time_ms": 234.5,
    "p95_operation_time_ms": 567.8,
    "p99_operation_time_ms": 890.1
  }
}
```

## Token Aggregation

### Token Tracking
- Each node tracks its own token usage
- Parents aggregate children's token usage
- Root has system-wide token count

### Aggregation Formula
```python
def aggregate_tokens(node_tokens, child_tokens):
    """
    Parent tokens = Own tokens + Sum of all children's tokens
    """
    total = node_tokens['total_tokens']

    for child_id, child_token_data in child_tokens.items():
        total += child_token_data['total_tokens']

    return {
        'total_tokens': total,
        'own_tokens': node_tokens['total_tokens'],
        'child_tokens': total - node_tokens['total_tokens'],
        'by_child': {
            child_id: child_data['total_tokens']
            for child_id, child_data in child_tokens.items()
        }
    }
```

### Token Budget Management

#### Budget Allocation (Top-Down)
```
Root (5_01): 100,000 tokens total
  ├─ 4_01 (Analysis): 70,000 tokens (70%)
  │   ├─ 3_01: 35,000 tokens (50%)
  │   └─ 3_02: 35,000 tokens (50%)
  └─ 4_02 (Infrastructure): 30,000 tokens (30%)
      ├─ 3_03: 20,000 tokens (67%)
      └─ 3_04: 10,000 tokens (33%)
```

#### Token Alerts
- **80% threshold**: WARNING
- **90% threshold**: CRITICAL WARNING
- **95% threshold**: START THROTTLING
- **100% threshold**: STOP NEW OPERATIONS

### Token Report Format

#### Leaf Token Report
```json
{
  "node_id": "1_08",
  "node_name": "ML Inference Engine",
  "total_tokens": 12567,
  "token_limit": 15000,
  "utilization_percent": 83.8,
  "tokens_by_operation": {
    "face_detection": 5234,
    "landmark_detection": 4123,
    "deepfake_classification": 3210
  },
  "last_updated": "2026-01-13T12:34:56Z",
  "alerts": [
    {
      "level": "WARNING",
      "message": "Token usage at 83.8%, approaching limit",
      "timestamp": "2026-01-13T12:30:00Z"
    }
  ]
}
```

#### Aggregated Token Report (Internal Node)
```json
{
  "node_id": "2_04",
  "node_name": "ML Model Coordination",
  "total_tokens": 25134,
  "own_tokens": 234,
  "child_tokens": 24900,
  "token_limit": 30000,
  "utilization_percent": 83.8,
  "by_child": {
    "1_07": 12367,
    "1_08": 12567
  },
  "last_updated": "2026-01-13T12:35:00Z",
  "alerts": [
    {
      "level": "WARNING",
      "message": "Child 1_08 at 83.8% token usage",
      "timestamp": "2026-01-13T12:30:00Z"
    }
  ]
}
```

#### System-Wide Token Report (Root)
```json
{
  "node_id": "5_01",
  "node_name": "Main Orchestrator",
  "total_tokens": 87543,
  "token_budget": 100000,
  "utilization_percent": 87.5,
  "by_subsystem": {
    "analysis_pipeline": 65234,
    "infrastructure": 22309
  },
  "top_consumers": [
    {"node": "1_08", "tokens": 12567, "operation": "ML Inference"},
    {"node": "1_07", "tokens": 12367, "operation": "Model Loading"},
    {"node": "1_02", "tokens": 8765, "operation": "Landmark Detection"}
  ],
  "alerts": [
    {
      "level": "WARNING",
      "message": "System token usage at 87.5%",
      "timestamp": "2026-01-13T12:35:00Z"
    }
  ],
  "recommendations": [
    "Consider reducing analysis quality for remaining operations",
    "Monitor 1_08 (ML Inference Engine) - highest consumer"
  ]
}
```

## Aggregation Schedule

### Real-Time (Immediate)
- ERROR logs
- CRITICAL warnings
- Security alerts
- Token limit violations

### Periodic (Every 10 seconds)
- STATUS updates
- WARNING logs
- Resource usage metrics

### Periodic (Every 60 seconds)
- INFO log summaries
- Token usage reports
- Performance statistics

### On-Demand
- DEBUG logs
- Detailed metrics
- Historical data

## Performance Optimization

### Batching
- Aggregate multiple updates before sending to parent
- Reduce communication overhead
- Buffer non-critical updates

### Caching
- Cache aggregated results
- Invalidate on significant changes
- Reduce redundant calculations

### Compression
- Compress large log batches
- Use efficient serialization (MessagePack, Protocol Buffers)
- Delta encoding for status updates

## Testing Aggregation

### Test Scenarios
1. **Single leaf**: Verify leaf → parent aggregation
2. **Full tree**: Verify end-to-end aggregation (leaf → root)
3. **High volume**: 1000 logs/second, verify filtering
4. **Error propagation**: Ensure errors always reach root
5. **Token overflow**: Verify alerts at each level
6. **Performance**: Aggregation overhead < 5ms per node

### Success Criteria
- No information loss for critical logs
- Logs reduced by 80-90% at each level
- Token counts accurate within 1%
- Status updates < 1 second latency
- Aggregation CPU < 5% overhead
