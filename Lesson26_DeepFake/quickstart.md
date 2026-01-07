# Quick Start Guide

## Installation (5 minutes)

### 1. Make installation script executable
```bash
chmod +x install.sh
```

### 2. Run installation
```bash
./install.sh
```

This will:
- Install system dependencies
- Create virtual environment at `../../venv`
- Install Python packages
- Set up project structure

### 3. Activate virtual environment
```bash
source ../../venv/bin/activate
```

## Basic Usage

### Command Line

#### Analyze a video
```bash
python -m deepfake_detector.main video.mp4
```

#### With options
```bash
python -m deepfake_detector.main video.mp4 \
  --output report.json \
  --frame-skip 2 \
  --workers 8 \
  --verbose
```

### Python API

```python
from pathlib import Path
from deepfake_detector import DeepFakeDetector, DetectorConfig

# Configure
config = DetectorConfig(frame_skip=2, batch_size=16)

# Detect
detector = DeepFakeDetector(config)
results = detector.analyze(Path('video.mp4'))

# Results
print(f"Verdict: {results['verdict']}")
print(f"Confidence: {results['confidence']:.2%}")
```

## Output

### JSON Report
```json
{
  "verdict": "FAKE",
  "confidence": 0.87,
  "scores": {
    "facial": 0.65,
    "temporal": 0.72,
    "lighting": 0.55
  },
  "anomalies": [...]
}
```

### Verdicts
- **REAL**: Confidence > 60%
- **FAKE**: Confidence < 40%
- **UNCERTAIN**: Confidence 40-60%

## Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `--frame-skip` | Analyze every Nth frame | 1 |
| `--batch-size` | Frames per batch | 16 |
| `--workers` | Parallel workers | 4 |
| `--disable-ml` | Disable ML models | false |
| `--gpu` | Enable GPU | false |
| `--verbose` | Verbose output | false |

## Troubleshooting

### Installation fails
```bash
# Ensure you're in WSL
wsl --list

# Update packages
sudo apt update && sudo apt upgrade
```

### Module not found
```bash
# Ensure virtual environment is activated
source ../../venv/bin/activate

# Reinstall package
pip install -e .
```

### Out of memory
```bash
# Reduce batch size and skip frames
python -m deepfake_detector.main video.mp4 \
  --batch-size 8 \
  --frame-skip 3
```

## Next Steps

1. **Read full documentation**: See `README.md`
2. **Review examples**: Check `example_usage.py`
3. **Run tests**: `pytest tests/ -v`
4. **Configure**: Edit config or use CLI options

## Support

- Check logs in `log/` directory
- Review `Claude.md` for implementation details
- See `tasks.md` for development roadmap

---

**Author**: Yair Levi  
**Version**: 1.0.0
