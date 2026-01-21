# Quick Reference Guide
## Image Frequency Filter Application

**Author:** Yair Levi

---

## Quick Start

```bash
# Setup
cd /mnt/c/Users/yair0/AI_continue/Lesson32_imageProcessing/imageFilter
./setup.sh
source ../../venv/bin/activate

# Run with all filters
python main.py --input your_image.jpg --filter all
```

---

## Command Cheat Sheet

### Basic Commands

```bash
# All filters (HPF, LPF, BPF)
python main.py --input image.jpg --filter all

# High-Pass Filter only
python main.py --input image.jpg --filter hpf

# Low-Pass Filter only
python main.py --input image.jpg --filter lpf

# Band-Pass Filter only
python main.py --input image.jpg --filter bpf
```

### Custom Parameters

```bash
# HPF with custom cutoff
python main.py --input image.jpg --filter hpf --hpf-cutoff 40

# LPF with custom cutoff
python main.py --input image.jpg --filter lpf --lpf-cutoff 20

# BPF with custom band
python main.py --input image.jpg --filter bpf --low-cutoff 30 --high-cutoff 70

# All filters with custom settings
python main.py --input image.jpg --filter all \
    --hpf-cutoff 35 --lpf-cutoff 25 \
    --low-cutoff 30 --high-cutoff 70
```

### Options

```bash
# Display results (if X11 available)
--show

# Don't save outputs
--no-save

# Disable multiprocessing
--no-multiprocessing
```

---

## Filter Quick Reference

| Filter | CLI Option | Effect | Cutoff Parameter | Result |
|--------|-----------|--------|------------------|--------|
| **HPF** | `--filter hpf` | Edge enhance | `--hpf-cutoff` | Sharp edges |
| **LPF** | `--filter lpf` | Smooth/blur | `--lpf-cutoff` | Blurred |
| **BPF** | `--filter bpf` | Band isolate | `--low-cutoff` `--high-cutoff` | Mid-freq only |

---

## Output Files

```
output/
├── [image]_spectrum_original.png          # Original frequency spectrum
├── [image]_spectrum_HighPassFilter.png    # HPF spectrum
├── [image]_spectrum_LowPassFilter.png     # LPF spectrum
├── [image]_spectrum_BandPassFilter.png    # BPF spectrum
├── [image]_HighPassFilter.png             # HPF result
├── [image]_LowPassFilter.png              # LPF result
├── [image]_BandPassFilter.png             # BPF result
└── [image]_comparison.png                 # Side-by-side comparison
```

---

## Parameter Guidelines

### HPF Cutoff (--hpf-cutoff)
- **Range:** 1-100 (pixels from center)
- **Low (10-20):** Strong edge enhancement, removes more
- **Medium (30-40):** Balanced edge enhancement
- **High (50+):** Subtle edge enhancement, keeps more detail

### LPF Cutoff (--lpf-cutoff)
- **Range:** 1-100 (pixels from center)
- **Low (10-20):** Heavy smoothing, very blurred
- **Medium (30-40):** Moderate smoothing
- **High (50+):** Light smoothing, keeps detail

### BPF Band (--low-cutoff, --high-cutoff)
- **Narrow Band (20-40):** Specific frequencies only
- **Medium Band (20-70):** Wider range
- **Wide Band (10-90):** Most frequencies

---

## Common Use Cases

### Edge Detection
```bash
python main.py --input photo.jpg --filter hpf --hpf-cutoff 30
```
**Use:** Find object boundaries, detect features

### Noise Reduction
```bash
python main.py --input noisy.jpg --filter lpf --lpf-cutoff 25
```
**Use:** Remove high-frequency noise, smooth image

### Texture Analysis
```bash
python main.py --input texture.jpg --filter bpf --low-cutoff 30 --high-cutoff 70
```
**Use:** Isolate specific texture patterns

### Compare All Methods
```bash
python main.py --input photo.jpg --filter all
```
**Use:** Educational, see all filter effects

---

## Troubleshooting

### Display Not Working
**Problem:** `--show` doesn't display images  
**Solution:** Remove `--show` flag, images are still saved in `output/`

### Import Errors
**Problem:** Module not found  
**Solution:** 
```bash
source ../../venv/bin/activate
pip install -r requirements.txt
```

### Input File Not Found
**Problem:** Can't find input image  
**Solution:** Place image in `input/` directory
```bash
cp /path/to/image.jpg input/
python main.py --input image.jpg --filter all
```

### Memory Issues
**Problem:** Large images cause memory errors  
**Solution:** Use `--no-multiprocessing`
```bash
python main.py --input large.jpg --filter all --no-multiprocessing
```

---

## Project Structure (Simplified)

```
imageFilter/
├── main.py              # Run this
├── input/               # Put images here
├── output/              # Results go here
├── log/                 # Log files
├── filters/             # Filter implementations
│   ├── high_pass.py     # HPF
│   ├── low_pass.py      # LPF
│   └── band_pass.py     # BPF
├── tasks/               # Processing steps
└── utils/               # Helpers
```

---

## Log Files

**Location:** `./log/`  
**Format:** 20 files × 16MB (ring buffer)  
**View logs:**
```bash
tail -f log/main.log
```

---

## Help Command

```bash
python main.py --help
```

---

## Typical Workflow

1. **Place image in input/**
   ```bash
   cp ~/Pictures/photo.jpg input/
   ```

2. **Run with all filters**
   ```bash
   python main.py --input photo.jpg --filter all
   ```

3. **Check results in output/**
   ```bash
   ls output/
   ```

4. **View specific outputs**
   ```bash
   # View with image viewer
   eog output/photo_comparison.png
   
   # Or copy to Windows
   cp output/*.png /mnt/c/Users/yair0/Desktop/
   ```

---

## Performance Tips

- **Parallel Processing:** Enabled by default for multiple filters
- **Single Filter:** No overhead, runs directly
- **Large Images:** Use `--no-multiprocessing` to reduce memory
- **Batch Processing:** Process multiple images sequentially

---

## Example Session

```bash
# Activate environment
source ../../venv/bin/activate

# Process image with all filters
python main.py --input landscape.jpg --filter all

# View results
ls output/landscape_*

# Output:
# landscape_comparison.png
# landscape_HighPassFilter.png
# landscape_LowPassFilter.png
# landscape_BandPassFilter.png
# landscape_spectrum_original.png
# landscape_spectrum_HighPassFilter.png
# landscape_spectrum_LowPassFilter.png
# landscape_spectrum_BandPassFilter.png
```

---

## Filter Selection Guide

**Want to:**
- **Detect edges?** → Use HPF
- **Reduce noise?** → Use LPF
- **Find textures?** → Use BPF
- **Compare all?** → Use all

---

## Quick Tips

✅ **DO:**
- Put images in `input/` folder
- Use meaningful image names
- Check `output/` for results
- Review `log/` if issues occur

❌ **DON'T:**
- Use absolute paths
- Forget to activate venv
- Process very large images without `--no-multiprocessing`
- Delete `log/` directory

---

## Support

**Check logs:**
```bash
cat log/main.log
```

**Verify setup:**
```bash
python -c "import numpy, cv2, matplotlib; print('OK')"
```

**Re-run setup:**
```bash
./setup.sh
```

---

**Last Updated:** January 20, 2026