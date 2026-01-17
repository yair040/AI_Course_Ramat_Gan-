# Test Scenarios for BST DeepFake Detection System

## Overview
This document defines comprehensive test scenarios covering the entire BST structure. Each scenario specifies inputs, expected outputs, data flow through nodes, and success criteria.

## Test Coverage Goals
- **Node Coverage**: All 31 nodes (16 leaves + 15 internal) must be used
- **Flow Coverage**: All communication paths tested
- **Edge Cases**: Error handling, timeouts, resource limits
- **Integration**: Full system tests and subsystem tests
- **Performance**: Latency, throughput, resource usage

---

## Scenario 1: Happy Path - Complete Video Analysis

### Description
End-to-end deepfake detection on a valid MP4 video file with clear facial features.

### Input
```json
{
  "operation": "analyze_video",
  "video_path": "test_videos/sample_real.mp4",
  "video_properties": {
    "duration_seconds": 30,
    "resolution": "1080p",
    "format": "mp4",
    "codec": "h264",
    "size_mb": 45.2
  },
  "analysis_config": {
    "enable_all_detectors": true,
    "confidence_threshold": 0.7,
    "quality": "high"
  }
}
```

### Expected Data Flow

```
5_01 (Root) receives request
  ↓
4_01 (Analysis Pipeline) + 4_02 (Infrastructure)
  ↓                           ↓
3_01 + 3_02                3_03 + 3_04
  ↓                           ↓
2_01 + 2_02 + 2_03 + 2_04   2_05 + 2_06 + 2_07 + 2_08
  ↓                           ↓
ALL 16 LEAF NODES (1_01 to 1_16) perform I/O operations
```

### Node-by-Node Execution

#### Phase 1: Video Input (4_02 → 3_03 → 2_05 → 1_09, 1_10)
1. **1_09 (Video File Reader)**: Reads video.mp4 file
   - Output: Video stream handle, basic properties
2. **1_10 (Metadata Extractor)**: Extracts metadata
   - Output: Codec, timestamps, resolution, frame rate

#### Phase 2: Frame Processing (3_03 → 2_06 → 1_11, 1_12)
3. **1_11 (Frame Decoder)**: Decodes video frames
   - Output: 900 frames (30 fps × 30 sec)
4. **1_12 (Frame Buffer Manager)**: Manages frame buffers
   - Output: Buffered frames for analysis

#### Phase 3: Facial Analysis (4_01 → 3_01 → 2_01 → 1_01, 1_02)
5. **1_01 (Face Detection Service)**: Detects faces in frames
   - Output: 900 face bounding boxes
6. **1_02 (Facial Landmark Extractor)**: Extracts facial landmarks
   - Output: 68 landmarks × 900 frames

#### Phase 4: Lighting Analysis (3_01 → 2_02 → 1_03, 1_04)
7. **1_03 (Eye & Blink Analyzer)**: Analyzes eyes and blinks
   - Output: Blink rate, pupil dilation data
8. **1_04 (Shadow Geometry Validator)**: Validates shadows
   - Output: Shadow consistency scores

#### Phase 5: Temporal Analysis (4_01 → 3_02 → 2_03 → 1_05, 1_06)
9. **1_05 (Optical Flow Computer)**: Computes optical flow
   - Output: Motion vectors for 899 frame pairs
10. **1_06 (Motion Vector Analyzer)**: Analyzes motion
    - Output: Motion consistency scores, anomaly detection

#### Phase 6: ML Inference (3_02 → 2_04 → 1_07, 1_08)
11. **1_07 (ML Model Loader)**: Loads deepfake detection models
    - Output: 3 loaded models (face-swap, lip-sync, GAN detector)
12. **1_08 (ML Inference Engine)**: Runs inference
    - Output: 900 × 3 predictions (confidence scores)

#### Phase 7: Reporting (4_02 → 3_04 → 2_07 → 1_13, 1_14)
13. **1_13 (JSON Report Writer)**: Writes final JSON report
    - Output: detailed_report.json
14. **1_14 (Visualization Generator)**: Creates visualizations
    - Output: heatmap.png, timeline.png

#### Phase 8: Monitoring (3_04 → 2_08 → 1_15, 1_16)
15. **1_15 (Log File Writer)**: Writes system logs
    - Output: Updated log files with operation details
16. **1_16 (Metrics Aggregator)**: Aggregates metrics
    - Output: Performance metrics summary

### Expected Output
```json
{
  "status": "completed",
  "verdict": "authentic",
  "overall_confidence": 0.92,
  "analysis_duration_seconds": 58.3,
  "video_duration_seconds": 30.0,
  "analysis_ratio": 1.94,
  "detections": {
    "facial_consistency": {
      "score": 0.94,
      "confidence": 0.91,
      "anomalies": []
    },
    "lighting_consistency": {
      "score": 0.89,
      "confidence": 0.87,
      "anomalies": ["minor shadow discrepancy at frame 456"]
    },
    "temporal_consistency": {
      "score": 0.95,
      "confidence": 0.93,
      "anomalies": []
    },
    "ml_detection": {
      "face_swap_probability": 0.03,
      "lip_sync_probability": 0.02,
      "gan_probability": 0.04,
      "ensemble_confidence": 0.95
    }
  },
  "frames_analyzed": 900,
  "faces_detected": 900,
  "reports_generated": [
    "detailed_report.json",
    "heatmap.png",
    "timeline.png"
  ],
  "resource_usage": {
    "total_tokens": 45678,
    "peak_memory_mb": 2345,
    "total_disk_io_mb": 523
  }
}
```

### Success Criteria
- ✓ All 16 leaf nodes executed
- ✓ All 15 internal nodes coordinated properly
- ✓ Analysis completed in < 2× video duration
- ✓ Confidence > 0.7
- ✓ All reports generated
- ✓ No errors or warnings
- ✓ Logs properly aggregated
- ✓ Token usage within budget

---

## Scenario 2: Deepfake Detected

### Description
Analyze a known deepfake video, system should detect manipulation.

### Input
```json
{
  "operation": "analyze_video",
  "video_path": "test_videos/sample_fake.mp4",
  "video_properties": {
    "duration_seconds": 25,
    "resolution": "1080p",
    "format": "mp4",
    "size_mb": 38.7
  }
}
```

### Expected Anomalies Detected By
- **1_01, 1_02 (Face Detection)**: Facial boundary artifacts
- **1_03 (Eye Analyzer)**: Unnatural blink patterns
- **1_04 (Shadow Validator)**: Shadow inconsistencies
- **1_06 (Motion Analyzer)**: Jitter in motion vectors
- **1_08 (ML Inference)**: High deepfake probability (> 0.8)

### Expected Output
```json
{
  "status": "completed",
  "verdict": "likely_manipulated",
  "overall_confidence": 0.87,
  "deepfake_probability": 0.84,
  "analysis_duration_seconds": 48.2,
  "detections": {
    "facial_consistency": {
      "score": 0.42,
      "confidence": 0.89,
      "anomalies": [
        "facial boundary artifacts detected in 234 frames",
        "unnatural skin texture in 456 frames"
      ]
    },
    "lighting_consistency": {
      "score": 0.38,
      "confidence": 0.91,
      "anomalies": [
        "shadow direction inconsistent in 189 frames",
        "reflection missing in eyes"
      ]
    },
    "temporal_consistency": {
      "score": 0.56,
      "confidence": 0.85,
      "anomalies": [
        "jitter detected in motion vectors",
        "unnatural head movement at frame 234"
      ]
    },
    "ml_detection": {
      "face_swap_probability": 0.87,
      "lip_sync_probability": 0.23,
      "gan_probability": 0.78,
      "ensemble_confidence": 0.89
    }
  },
  "recommendation": "manual_review_recommended",
  "flagged_frames": [123, 234, 345, 456, 567, 678, 789]
}
```

### Success Criteria
- ✓ All detectors identify anomalies
- ✓ Overall deepfake probability > 0.7
- ✓ Detailed anomaly explanations provided
- ✓ Flagged frames identified
- ✓ Visualizations show problem areas

---

## Scenario 3: Unsupported Format - Decision Escalation

### Description
User provides video in unsupported format, triggering decision escalation.

### Input
```json
{
  "operation": "analyze_video",
  "video_path": "test_videos/sample.mov",
  "video_properties": {
    "format": "QuickTime MOV",
    "codec": "ProRes 422"
  }
}
```

### Expected Flow with Escalation

```
5_01 → 4_02 → 3_03 → 2_05 → 1_09 (Video File Reader)
                                ↓ (detects unsupported format)
1_09 escalates to 2_05 → "Should we convert?"
2_05 decides → "Yes, attempt conversion with ffmpeg"
                                ↓
1_09 performs conversion → continues with analysis
```

### Decision Escalation Details
```json
{
  "escalation_request": {
    "from_node": "1_09",
    "to_node": "2_05",
    "reason": "unsupported_format",
    "context": {
      "detected_format": "QuickTime MOV",
      "codec": "ProRes 422",
      "supported_formats": ["mp4", "avi", "mkv"]
    },
    "options": [
      {"id": "skip", "risk": "low", "cost": "low"},
      {"id": "convert", "risk": "medium", "cost": "high"},
      {"id": "fail", "risk": "high", "cost": "low"}
    ],
    "default_action": "skip",
    "recommendation": "convert"
  },
  "decision_response": {
    "from_node": "2_05",
    "decision": "convert",
    "reason": "Conversion acceptable for analysis",
    "conditions": {
      "max_conversion_time": 60,
      "fallback_on_failure": "skip"
    }
  }
}
```

### Expected Output
```json
{
  "status": "completed_with_warnings",
  "verdict": "authentic",
  "overall_confidence": 0.88,
  "warnings": [
    "Video format conversion was required (MOV → MP4)",
    "Some quality loss may have occurred during conversion"
  ],
  "conversion_details": {
    "original_format": "QuickTime MOV",
    "converted_to": "MP4",
    "conversion_time_seconds": 23.4
  },
  "detections": { /* normal detection results */ }
}
```

### Success Criteria
- ✓ Escalation properly triggered
- ✓ Decision made at appropriate level
- ✓ Decision logged for audit
- ✓ Conversion performed successfully
- ✓ Analysis continued after conversion
- ✓ Warning included in final report

---

## Scenario 4: Low Confidence - Multi-Level Escalation

### Description
Analysis produces conflicting results, requiring escalation to root for final decision.

### Input
```json
{
  "operation": "analyze_video",
  "video_path": "test_videos/borderline_case.mp4"
}
```

### Escalation Chain

```
1_08 (ML Inference) → confidence 0.52 → escalates to 2_04
2_04 → conflicting child results → escalates to 3_02
3_02 → cannot resolve → escalates to 4_01
4_01 → policy decision needed → escalates to 5_01 (Root)
5_01 → makes final decision: "Flag for manual review"
```

### Escalation at Each Level

#### Level 1: 1_08 → 2_04
```json
{
  "reason": "low_confidence_prediction",
  "confidence": 0.52,
  "threshold": 0.70,
  "options": ["retry", "accept", "escalate"]
}
```

#### Level 2: 2_04 → 3_02
```json
{
  "reason": "conflicting_ml_models",
  "model_results": {
    "face_swap_detector": 0.78,
    "lip_sync_detector": 0.23,
    "gan_detector": 0.67
  },
  "options": ["trust_majority", "weighted_average", "escalate"]
}
```

#### Level 3: 3_02 → 4_01
```json
{
  "reason": "temporal_vs_ml_conflict",
  "temporal_confidence": 0.85,
  "ml_confidence": 0.52,
  "options": ["trust_temporal", "trust_ml", "escalate"]
}
```

#### Level 4: 4_01 → 5_01
```json
{
  "reason": "ambiguous_result_policy",
  "overall_confidence": 0.63,
  "threshold": 0.70,
  "options": ["report_uncertain", "flag_manual_review", "retry_high_quality"]
}
```

#### Root Decision: 5_01
```json
{
  "decision": "flag_manual_review",
  "reason": "Confidence below threshold with conflicting signals",
  "policy": "Conservative approach for borderline cases"
}
```

### Expected Output
```json
{
  "status": "completed",
  "verdict": "uncertain",
  "overall_confidence": 0.63,
  "recommendation": "manual_review_required",
  "reason": "Conflicting analysis results, confidence below threshold",
  "escalation_chain": [
    {"from": "1_08", "to": "2_04", "reason": "low_confidence"},
    {"from": "2_04", "to": "3_02", "reason": "conflicting_models"},
    {"from": "3_02", "to": "4_01", "reason": "temporal_ml_conflict"},
    {"from": "4_01", "to": "5_01", "reason": "policy_decision"}
  ],
  "final_decision_by": "5_01",
  "detections": { /* detailed results */ }
}
```

### Success Criteria
- ✓ Escalation chain properly executed
- ✓ Each level made appropriate decision
- ✓ Root made final policy decision
- ✓ Full escalation audit trail
- ✓ Safe default (manual review) applied

---

## Scenario 5: Resource Exhaustion - Token Limit

### Description
Large video causes token usage to exceed budget, triggering throttling and adaptation.

### Input
```json
{
  "operation": "analyze_video",
  "video_path": "test_videos/long_video.mp4",
  "video_properties": {
    "duration_seconds": 600,
    "resolution": "4K",
    "size_mb": 3456
  }
}
```

### Token Usage Progression

```
Initial Budget: 100,000 tokens

After 100 seconds of video:
- Used: 45,000 tokens (45%)
- Projection: 270,000 tokens total (170% over budget!)
- 1_16 (Metrics Aggregator) detects projection
- Alert propagates: 1_16 → 2_08 → 3_04 → 4_02 → 5_01

Root (5_01) Decision: Reduce quality for remaining video
```

### Adaptation Strategy
```json
{
  "token_alert": {
    "current_usage": 45000,
    "budget": 100000,
    "projection": 270000,
    "video_progress": 16.7
  },
  "adaptation_decision": {
    "action": "reduce_quality",
    "changes": {
      "skip_frames": "analyze every 3rd frame instead of every frame",
      "reduce_ml_models": "disable lip-sync detector (lowest value)",
      "reduce_resolution": "downscale to 1080p for remaining frames"
    },
    "projected_savings": 120000,
    "new_projection": 95000
  }
}
```

### Expected Output
```json
{
  "status": "completed",
  "verdict": "authentic",
  "overall_confidence": 0.81,
  "warnings": [
    "Quality reduced after 100 seconds due to token budget constraints",
    "Frame sampling increased from 1:1 to 1:3",
    "Lip-sync detection disabled",
    "Resolution reduced to 1080p"
  ],
  "resource_usage": {
    "total_tokens": 94532,
    "token_budget": 100000,
    "utilization": 94.5,
    "adaptations_applied": 3
  },
  "quality_metrics": {
    "first_100s": "high_quality",
    "remaining_500s": "reduced_quality"
  }
}
```

### Success Criteria
- ✓ Token tracking accurate throughout
- ✓ Projection triggered alert at 80% budget
- ✓ Adaptation strategy applied
- ✓ Completed within budget
- ✓ Quality degradation documented
- ✓ Still produced valid results

---

## Scenario 6: Partial Failure - Node Error Recovery

### Description
One leaf node fails, system continues with degraded functionality.

### Input
```json
{
  "operation": "analyze_video",
  "video_path": "test_videos/sample.mp4"
}
```

### Simulated Failure
- **1_03 (Eye & Blink Analyzer)** fails due to missing dependency
- Error propagates: 1_03 → 2_02 → 3_01 → 4_01 → 5_01

### Error Handling Flow

```
1_03 fails → logs error → notifies 2_02 (parent)
2_02 detects child failure → decides: "Continue without eye analysis"
2_02 notifies 3_01 → "Lighting analysis degraded"
3_01 adjusts confidence → reports to 4_01
4_01 continues analysis → marks as "completed_with_errors"
5_01 receives final result → includes error in report
```

### Expected Output
```json
{
  "status": "completed_with_errors",
  "verdict": "likely_authentic",
  "overall_confidence": 0.76,
  "errors": [
    {
      "node": "1_03",
      "component": "Eye & Blink Analyzer",
      "error": "Missing dependency: dlib",
      "impact": "Eye analysis unavailable",
      "severity": "medium"
    }
  ],
  "degraded_components": [
    "eye_blink_analysis",
    "pupil_dilation_analysis"
  ],
  "detections": {
    "facial_consistency": { /* results */ },
    "lighting_consistency": {
      "score": 0.78,
      "confidence": 0.71,
      "note": "Eye analysis unavailable, confidence reduced"
    },
    "temporal_consistency": { /* results */ },
    "ml_detection": { /* results */ }
  },
  "recommendation": "Results valid but eye analysis missing. Consider re-running with all components available."
}
```

### Success Criteria
- ✓ Failure detected and logged
- ✓ Error propagated to root
- ✓ System continued with remaining components
- ✓ Confidence adjusted for missing data
- ✓ Clear error message in output
- ✓ Recommendation provided

---

## Scenario 7: Concurrent Operations

### Description
Multiple videos analyzed simultaneously, testing parallelization and resource sharing.

### Input
```json
[
  {"video_path": "test_videos/video1.mp4", "priority": "high"},
  {"video_path": "test_videos/video2.mp4", "priority": "normal"},
  {"video_path": "test_videos/video3.mp4", "priority": "low"}
]
```

### Resource Allocation
```
Total Resources: 100% CPU, 4GB RAM, 100K tokens

Video 1 (high):    50% CPU, 2GB RAM, 50K tokens
Video 2 (normal):  30% CPU, 1GB RAM, 30K tokens
Video 3 (low):     20% CPU, 1GB RAM, 20K tokens
```

### Expected Behavior
- All three analyses run concurrently
- Resources allocated by priority
- Logs properly separated and aggregated
- Token budgets independently tracked
- No cross-contamination of results

### Expected Outputs
Three separate reports, all completed successfully with appropriate resource usage.

### Success Criteria
- ✓ All three videos analyzed
- ✓ No interference between operations
- ✓ Resource limits respected
- ✓ Priority ordering maintained
- ✓ Logs properly separated
- ✓ Token budgets independent

---

## Scenario 8: Full System Stress Test

### Description
Maximum load test with multiple concurrent operations, large videos, and resource constraints.

### Input
```json
{
  "concurrent_videos": 5,
  "video_properties": {
    "duration_seconds": 120,
    "resolution": "4K",
    "size_mb": 500
  },
  "resource_constraints": {
    "max_memory_gb": 4,
    "max_cpu_percent": 80,
    "token_budget": 100000
  }
}
```

### Expected Challenges
- Memory pressure → frame buffer management critical (1_12)
- Token budget stress → adaptive quality needed
- I/O bottleneck → buffering and caching crucial
- CPU saturation → prioritization needed

### Success Criteria
- ✓ System remains stable under load
- ✓ No crashes or deadlocks
- ✓ Resource limits respected
- ✓ Graceful degradation when needed
- ✓ All operations eventually complete
- ✓ Performance within acceptable bounds

---

## Test Execution Matrix

| Scenario | All Nodes Used | Escalation Tested | Aggregation Tested | Error Handling | Performance |
|----------|----------------|-------------------|--------------------|--------------------|-------------|
| 1. Happy Path | ✓ | - | ✓ | - | ✓ |
| 2. Deepfake | ✓ | - | ✓ | - | ✓ |
| 3. Unsupported Format | Partial | ✓ | ✓ | ✓ | - |
| 4. Low Confidence | ✓ | ✓✓✓ | ✓ | ✓ | - |
| 5. Token Limit | ✓ | ✓ | ✓✓ | ✓ | ✓ |
| 6. Partial Failure | Partial | ✓ | ✓ | ✓✓ | - |
| 7. Concurrent | ✓ | - | ✓✓ | - | ✓✓ |
| 8. Stress Test | ✓ | ✓ | ✓✓ | ✓ | ✓✓ |

**Legend**: ✓ = Tested, ✓✓ = Heavily Tested, ✓✓✓ = Primary Focus

---

## Node Coverage Checklist

### Level 5 (Leaves) - All Must Execute in Scenario 1
- [ ] 1_01: Face Detection Service
- [ ] 1_02: Facial Landmark Extractor
- [ ] 1_03: Eye & Blink Analyzer
- [ ] 1_04: Shadow Geometry Validator
- [ ] 1_05: Optical Flow Computer
- [ ] 1_06: Motion Vector Analyzer
- [ ] 1_07: ML Model Loader
- [ ] 1_08: ML Inference Engine
- [ ] 1_09: Video File Reader
- [ ] 1_10: Metadata Extractor
- [ ] 1_11: Frame Decoder
- [ ] 1_12: Frame Buffer Manager
- [ ] 1_13: JSON Report Writer
- [ ] 1_14: Visualization Generator
- [ ] 1_15: Log File Writer
- [ ] 1_16: Metrics Aggregator

### Level 4 - All Coordination Nodes
- [ ] 2_01: Facial Features Analysis
- [ ] 2_02: Lighting & Shadow Analysis
- [ ] 2_03: Temporal Motion Analysis
- [ ] 2_04: ML Model Coordination
- [ ] 2_05: Video Input Handler
- [ ] 2_06: Frame Processing
- [ ] 2_07: Report Generation
- [ ] 2_08: Log & Status Management

### Level 3 - All Pipeline Nodes
- [ ] 3_01: Facial & Visual Analysis
- [ ] 3_02: Temporal & ML Analysis
- [ ] 3_03: Video Processing Pipeline
- [ ] 3_04: Reporting & Monitoring

### Level 2 - Both Subsystems
- [ ] 4_01: Analysis Pipeline
- [ ] 4_02: Infrastructure & I/O Pipeline

### Root
- [ ] 5_01: Main Orchestrator

---

## Performance Benchmarks

### Target Metrics
- **Analysis Speed**: < 2× video duration
- **Memory Usage**: < 4GB per video
- **Token Efficiency**: < 100 tokens per second of video
- **Accuracy**: > 85% on test dataset
- **False Positive Rate**: < 10%
- **Latency**: First results within 5 seconds
- **Throughput**: 3+ concurrent videos on standard hardware

### Resource Usage Targets by Node Type
- **Leaf I/O Nodes**: < 256MB each
- **Component Coordinators**: < 512MB each
- **Pipeline Managers**: < 1GB each
- **Root**: < 512MB

---

## Simulation Approach (Without Code)

For each scenario, manually trace through:
1. **Entry Point**: Root receives request
2. **Distribution**: How request flows to children
3. **Leaf Operations**: What I/O each leaf performs
4. **Aggregation**: How results combine back up
5. **Decision Points**: Where decisions/escalations occur
6. **Output**: Final result format

Document any:
- **Bottlenecks**: Where flow slows
- **Inefficiencies**: Redundant operations
- **Missing Connections**: Nodes that aren't reached
- **Ambiguities**: Unclear responsibilities
