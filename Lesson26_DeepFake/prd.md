# Product Requirements Document: DeepFake Video Detection Tool

## Project Overview
**Author:** Yair Levi  
**Version:** 1.0  
**Date:** December 28, 2025  
**Target Platform:** WSL (Windows Subsystem for Linux) with Python virtual environment

## Executive Summary
A Python-based tool for analyzing video files to determine authenticity by detecting deepfake manipulations through multi-criteria analysis including facial inconsistencies, temporal anomalies, metadata inspection, and deep learning models.

## Project Structure
```
Lesson26_DeepFake/
├── deepfake_detector/          # Main package
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuration management
│   ├── detector.py             # Main detection orchestrator
│   ├── analyzers/              # Analysis modules
│   │   ├── __init__.py
│   │   ├── facial_analyzer.py
│   │   ├── temporal_analyzer.py
│   │   ├── metadata_analyzer.py
│   │   ├── lighting_analyzer.py
│   │   ├── geometry_analyzer.py
│   │   └── ml_detector.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       ├── video_processor.py  # Video frame extraction
│       └── report_generator.py # Results compilation
├── log/                        # Log files (ring buffer)
├── models/                     # Pre-trained ML models
├── tests/                      # Unit tests
├── requirements.txt
├── README.md
├── PRD.md
├── Claude.md
├── planning.md
└── tasks.md
```

## Technical Requirements

### Environment
- **Platform:** WSL (Ubuntu/Debian-based)
- **Python Version:** 3.9+
- **Virtual Environment:** Located at `../../venv` (relative to project)
- **Path Management:** All paths must be relative

### Code Organization
- **Max Lines per File:** 150 lines
- **Architecture:** Modular package structure
- **Concurrency:** Multiprocessing where applicable
- **Logging:** Ring buffer with 20 files × 16MB each in `log/` subfolder

### Logging Specifications
- **Level:** INFO and above
- **Format:** Ring buffer rotation
- **Files:** 20 × 16MB = 320MB total capacity
- **Behavior:** Circular overwrite when full
- **Location:** `./log/` subdirectory

## Core Features

### Detection Criteria

#### 1. Facial Expression Inconsistencies
- Micro-expression analysis (smile lines, frown creases)
- Eye shape symmetry verification
- Teeth alignment consistency
- Jaw angle naturalness
- Face-boundary artifacts (hair, ears, neck transitions)
- Color gradient anomalies at facial boundaries

#### 2. Temporal Movement Analysis
- Unnatural motion detection
- Velocity consistency checks
- Acceleration pattern analysis
- Jitter and smoothness evaluation

#### 3. Metadata Inspection
- Container format analysis
- Codec verification
- Timestamp consistency
- Creation vs. modification time discrepancies
- Stream metadata anomalies

#### 4. Source Verification
- File origin tracking
- Encoding history analysis
- Re-encoding signature detection

#### 5. Frame-to-Frame Consistency
- Posture change detection
- Lighting variation analysis
- Sudden environmental shifts
- Background consistency

#### 6. Eye Blink Analysis
- Blink frequency measurement
- Blink duration consistency
- Natural blink pattern verification
- Missing blink detection

#### 7. Lighting and Shadow Analysis
- **Lighting Consistency:**
  - Color temperature matching across face/body/background
  - Intensity distribution verification
  - Direction consistency
- **Reflection Analysis:**
  - Specular highlights in eyes
  - Skin micro-reflections
  - Catchlight validation in pupils
  - Surface reflection consistency (glasses, jewelry)
- **Shadow Geometry:**
  - Shadow direction alignment
  - Softness/hardness consistency with light source
  - Multi-light source validation

#### 8. Pupil Dilation Analysis
- Environmental light response
- Focus distance correlation
- Dilation speed naturalness
- Bilateral consistency

#### 9. Skin and Feature Analysis
- Texture uniformity detection
- Wrinkle presence/absence
- Pore structure verification
- Age-appropriate feature consistency
- Skin tone variation naturalness

#### 10. Deep Learning Detection
- **Model Ensemble:**
  - Face-swap detectors
  - Lip-sync analyzers
  - GAN-detection networks
  - Temporal CNNs/RNNs
  - Transformer-based sequence models
- **Explainability:**
  - Saliency map generation
  - Region-of-interest highlighting
  - Confidence scoring per criterion
- **Training Capability:**
  - External database integration
  - Model fine-tuning support
  - Transfer learning implementation

#### 11. Geometry and Physiology
- Eye spacing consistency
- Ear position verification
- Jawline continuity tracking
- Micro-expression detection
- Saccade (eye movement) naturalness
- Head rotation parallax verification
- 3D consistency validation

#### 12. Compression Artifacts
- Re-encoding pattern detection
- GOP structure analysis
- Bitrate anomaly identification
- Quantization noise patterns
- Frame duplication detection
- Interpolation artifact identification
- Upsampling signature recognition

## Technical Implementation

### Video Processing
- Frame extraction with configurable FPS
- Face detection and tracking
- Facial landmark extraction
- Optical flow computation
- Multi-scale analysis

### Multiprocessing Strategy
- Frame batch processing
- Parallel analyzer execution
- Result aggregation pipeline
- Resource-aware process pooling

### Machine Learning Models
- Pre-trained model integration
- Model ensemble voting
- Confidence thresholding
- Feature extraction pipeline
- Optional training mode with external datasets

### Output Format
- JSON report with per-criterion scores
- Overall authenticity probability
- Confidence intervals
- Anomaly timestamps
- Visual heatmaps (optional)
- Detailed explanation of findings

## Performance Requirements
- Process 1080p video at minimum 5 FPS
- Memory usage < 4GB for typical videos
- Support videos up to 1 hour duration
- Graceful degradation for resource constraints

## Dependencies (requirements.txt)
- opencv-python
- numpy
- torch / tensorflow (for ML models)
- face-recognition / dlib
- scikit-learn
- scipy
- pandas
- ffmpeg-python
- pillow
- matplotlib (for visualization)
- mediainfo / pymediainfo (for metadata)

## Success Criteria
- Accuracy > 85% on standard deepfake datasets
- False positive rate < 10%
- Processing time < 2× video duration
- Clear, actionable reports
- Robust error handling
- Comprehensive logging

## Future Enhancements
- Audio analysis integration
- Real-time processing capability
- GPU acceleration
- Web interface
- Batch processing mode
- Custom model training UI

## References
1. [TechTarget: How to detect deepfakes manually and using AI](http://techtarget.com/searchsecurity/tip/How-to-detect-deepfakes-manually-and-using-AI)
2. [Resemble.ai: Deepfake Detection Methods & Techniques](https://www.resemble.ai/deepfake-detection-methods-techniques/)
3. [Quora: How does an expert detect fake videos from real videos](https://www.quora.com/How-does-an-expert-detect-fake-videos-from-real-videos)

## Constraints and Assumptions
- Audio analysis excluded from scope
- WSL environment available
- Sufficient disk space for logs and models
- Internet connectivity for initial model download
- Video input in standard formats (mp4, avi, mkv)