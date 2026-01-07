# Claude.md - AI Assistant Development Notes

**Author:** Yair Levi  
**AI Assistant:** Claude (Anthropic)  
**Project:** DeepFake Detection Tool  
**Date:** December 28, 2025

## Project Context

This document contains notes, decisions, and implementation guidance for the DeepFake Detection Tool development, as discussed with Claude AI.

## Key Design Decisions

### 1. Architecture Pattern
**Decision:** Modular analyzer pattern with central orchestrator  
**Rationale:** 
- Each analyzer focuses on specific detection criteria (< 150 lines)
- Easy to add/remove/test analyzers independently
- Facilitates multiprocessing parallelization
- Clear separation of concerns

### 2. Logging Strategy
**Decision:** Ring buffer with 20 files × 16MB  
**Rationale:**
- Prevents disk space exhaustion
- Maintains detailed history (320MB total)
- Automatic cleanup via rotation
- Suitable for long-running analysis

**Implementation Notes:**
```python
# Use RotatingFileHandler with proper configuration
handler = RotatingFileHandler(
    filename='log/deepfake.log',
    maxBytes=16 * 1024 * 1024,  # 16MB
    backupCount=20,
    encoding='utf-8'
)
```

### 3. Path Management
**Decision:** All relative paths from project root  
**Rationale:**
- Portability across systems
- No hardcoded absolute paths
- Works seamlessly in WSL
- Virtual environment at `../../venv`

**Implementation Pattern:**
```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
LOG_DIR = PROJECT_ROOT / "log"
MODELS_DIR = PROJECT_ROOT / "models"
VENV_DIR = PROJECT_ROOT / ".." / ".." / "venv"
```

### 4. Multiprocessing Strategy
**Decision:** Process pool for analyzer parallelization  
**Rationale:**
- Python GIL limits threading effectiveness
- Each analyzer is CPU-intensive
- Process isolation prevents state corruption
- Better CPU utilization on multi-core systems

**Concurrency Model:**
```
Main Process (coordinator)
├── Video Reader Process
├── Analyzer Pool (4-8 workers)
│   ├── Worker 1: Facial Analysis
│   ├── Worker 2: Temporal Analysis
│   ├── Worker 3: Lighting Analysis
│   └── Worker 4: ML Detection
└── Result Aggregator Process
```

## Critical Implementation Guidelines

### File Size Constraint (150 lines)
Each Python file must remain under 150 lines. Strategies:

1. **Split Complex Analyzers:**
   ```
   facial_analyzer.py (base class + expression)
   facial_geometry.py (geometry checks)
   facial_skin.py (skin analysis)
   ```

2. **Use Helper Functions in utils/**
3. **Import reusable code from shared modules**
4. **Keep docstrings concise but informative**

### Error Handling Philosophy
- **Fail gracefully:** One analyzer failure shouldn't crash entire pipeline
- **Log everything:** Errors, warnings, and recovery actions
- **Return partial results:** If 9/10 analyzers succeed, report that
- **Provide context:** Include video info, frame numbers, timestamps

Example:
```python
try:
    score = analyzer.analyze(frame)
except AnalyzerError as e:
    logger.warning(f"Analyzer {analyzer.name} failed: {e}")
    score = None  # Partial result acceptable
```

## ML Model Integration Strategy

### Model Selection
Recommended pre-trained models:

1. **FaceForensics++ trained networks:**
   - XceptionNet for face manipulation
   - EfficientNet for GAN detection

2. **Commercial/Academic models:**
   - Microsoft's Video Authenticator
   - Sensity AI models (if available)
   - Facebook DFDC challenge winners

3. **Custom lightweight models:**
   - MobileNet-based for edge deployment
   - Temporal shift modules for video

### Model Storage & Loading
```
models/
├── face_swap_detector.pth
├── lip_sync_detector.pth
├── gan_detector.onnx
└── ensemble_config.json
```

**Lazy loading:** Only load models when needed to conserve memory.

**Download on first run:** Check if models exist, download if missing.

## Performance Optimization Tips

### Memory Management
1. **Frame batching:** Process 10-30 frames at once
2. **Generator pattern:** Yield frames instead of loading all
3. **Release resources:** Explicitly delete large numpy arrays
4. **Limit face tracking:** Only track primary face if multiple present

### CPU Optimization
1. **Worker count:** `cpu_count() - 1` or configurable
2. **Batch size:** Tune based on available memory
3. **Frame skipping:** Analyze every Nth frame for speed (configurable)
4. **Early exit:** If high confidence reached, stop analysis

### I/O Optimization
1. **Video codec:** Use hardware-accelerated decoders
2. **Frame caching:** Cache frequently accessed frames
3. **Parallel I/O:** Read next batch while processing current

## Testing Strategy

### Test Data Requirements
1. **Real videos:**
   - Various resolutions (480p - 4K)
   - Different lighting conditions
   - Multiple subjects and poses

2. **Deepfake videos:**
   - Face-swap variants
   - Face reenactment samples
   - Audio-driven animations
   - Different quality levels

3. **Edge cases:**
   - Very short clips (< 1 second)
   - Static images as video
   - Low resolution
   - Heavy compression artifacts

### Test Coverage Goals
- Unit tests: 80%+ coverage
- Integration tests: All analyzers + pipeline
- Performance tests: Baseline benchmarks
- Regression tests: Known failure cases

## Logging Best Practices

### Log Levels
- **DEBUG:** Frame-level details, intermediate values
- **INFO:** Pipeline stages, analyzer start/end, results summary
- **WARNING:** Degraded performance, missing optional features
- **ERROR:** Analyzer failures, invalid inputs, recoverable errors
- **CRITICAL:** Unrecoverable errors, system failures

### Log Format
```
[2025-12-28 10:30:45.123] [INFO] [facial_analyzer] Starting analysis on frame 150
[2025-12-28 10:30:45.234] [WARNING] [ml_detector] Model not found, using fallback
[2025-12-28 10:30:46.100] [INFO] [detector] Analysis complete: 0.73 confidence FAKE
```

### Structured Logging
Consider adding JSON logging for machine parsing:
```python
logger.info("analysis_complete", extra={
    "video_path": video_path,
    "confidence": 0.73,
    "verdict": "FAKE",
    "duration_sec": 45.2
})
```

## Configuration Management

### Config Structure
```python
@dataclass
class AnalyzerConfig:
    enabled: bool = True
    weight: float = 1.0
    threshold: float = 0.5

@dataclass
class DetectorConfig:
    frame_skip: int = 1
    batch_size: int = 16
    num_workers: int = 4
    analyzers: Dict[str, AnalyzerConfig]
    output_format: str = "json"
```

### Environment Variables
```bash
DEEPFAKE_LOG_LEVEL=INFO
DEEPFAKE_NUM_WORKERS=8
DEEPFAKE_MODEL_DIR=/path/to/models
DEEPFAKE_GPU_ENABLED=true
```

## Common Pitfalls & Solutions

### Pitfall 1: Memory Leaks in Video Processing
**Solution:** Use context managers, explicitly close video captures
```python
with VideoCapture(video_path) as cap:
    for frame in cap.read_frames():
        process(frame)
# Automatically released
```

### Pitfall 2: GIL Contention with Threading
**Solution:** Use multiprocessing, not threading, for CPU-bound work

### Pitfall 3: Model Download Blocking
**Solution:** Implement async download or download on first run with progress

### Pitfall 4: Absolute Paths Breaking Portability
**Solution:** Always use `Path(__file__).parent` relative resolution

### Pitfall 5: Overconfident Predictions
**Solution:** Use probability calibration and confidence intervals

## Future Enhancement Ideas

### Short-term (Next 3 months)
- [ ] Audio deepfake detection integration
- [ ] Web UI with drag-and-drop
- [ ] Batch processing mode
- [ ] GPU acceleration with CUDA
- [ ] Docker containerization

### Medium-term (6 months)
- [ ] Real-time video stream analysis
- [ ] Browser extension for online videos
- [ ] API endpoint with REST interface
- [ ] Model training UI
- [ ] Crowdsourced verification

### Long-term (1 year)
- [ ] Mobile app (iOS/Android)
- [ ] Cloud-based processing
- [ ] Blockchain-based verification
- [ ] Integration with social media platforms
- [ ] Federated learning for privacy

## References & Resources

### Academic Papers
1. "FaceForensics++: Learning to Detect Manipulated Facial Images" (Rossler et al.)
2. "The Eyes Tell All: Detecting Political Orientation from Eye Movement Data" (Cognitive methods)
3. "Detecting Face Synthesis Using Convolutional Neural Networks" (GAN detection)

### Datasets
1. **FaceForensics++:** 1000+ manipulated videos
2. **Deepfake Detection Challenge (DFDC):** 100k+ videos
3. **Celeb-DF:** High-quality celebrity deepfakes
4. **UADFV:** Diverse manipulation techniques

### Tools & Libraries
1. **face_recognition:** Simplifies dlib facial landmarks
2. **OpenCV:** Video I/O and computer vision
3. **MediaPipe:** Real-time face mesh detection
4. **PyTorch/TensorFlow:** ML model inference
5. **ffmpeg-python:** Advanced video manipulation

### Online Resources
1. [TechTarget Deepfake Detection Guide](http://techtarget.com/searchsecurity/tip/How-to-detect-deepfakes-manually-and-using-AI)
2. [Resemble.ai Methods & Techniques](https://www.resemble.ai/deepfake-detection-methods-techniques/)
3. [Quora Expert Detection Discussion](https://www.quora.com/How-does-an-expert-detect-fake-videos-from-real-videos)

## Development Environment Setup

### WSL Configuration
```bash
# Install dependencies
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
sudo apt install ffmpeg libsm6 libxext6 libxrender-dev

# Create virtual environment
cd ../..
python3 -m venv venv
source venv/bin/activate

# Install requirements
cd Lesson26/Lesson26_DeepFake
pip install -r requirements.txt
```

### IDE Recommendations
- **VSCode:** With Python, Pylint, Black extensions
- **PyCharm:** Professional with WSL integration
- **Vim/Neovim:** With coc-python or ALE

### Debugging Tips
1. Use `pdb.set_trace()` for interactive debugging
2. Enable verbose logging during development
3. Profile with `cProfile` to find bottlenecks
4. Use `memory_profiler` for memory issues

## Contact & Collaboration

**Project Lead:** Yair Levi  
**Repository:** [To be added]  
**Issues:** [To be added]  
**Documentation:** See README.md and PRD.md

---

**Note:** This document is a living guide and should be updated as the project evolves and new insights are gained.