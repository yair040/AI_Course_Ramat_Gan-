# Quick Start Guide - Package Mode

## Directory Structure

```
jpeg_compressing/              # Package root
├── __init__.py
├── __main__.py               # Enables python -m jpeg_compressing
├── main.py                   # Main program
├── requirements.txt
├── README.md
│
├── input/                    # INPUT FOLDER - Place images here
│   └── goldhill.bmp
│
├── output/                   # All outputs go here
│   ├── compressed/
│   ├── decompressed/
│   ├── metrics/
│   ├── plots/
│   └── logs/
│
├── tasks/
│   ├── __init__.py
│   ├── compress_task.py
│   ├── decompress_task.py
│   ├── error_task.py
│   └── visualize_task.py
│
└── utils/
    ├── __init__.py
    ├── config.py
    └── logger.py
```

## Setup

### 1. Create Virtual Environment
```bash
cd /mnt/c/Users/yair0/AI_continue
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
cd Lesson33_jpeg_compressing/jpeg_compressing
pip install -r requirements.txt
```

### 3. Create Input Directory (if not exists)
```bash
mkdir -p input
```

### 4. Add Your Image
```bash
# Copy your BMP file to input folder
cp /path/to/your/image.bmp input/
# Or if already there:
mv ./input/goldhill.bmp input/
```

## Running the Package

### Method 1: Run as Package (Recommended)
```bash
# From the parent directory (Lesson33_jpeg_compressing/)
cd /mnt/c/Users/yair0/AI_continue/Lesson33_jpeg_compressing
python3 -m jpeg_compressing --input jpeg_compressing/input/goldhill.bmp

# Or from inside jpeg_compressing/
cd jpeg_compressing
python3 -m jpeg_compressing --input input/goldhill.bmp
```

### Method 2: Run main.py Directly
```bash
# From inside jpeg_compressing/
cd /mnt/c/Users/yair0/AI_continue/Lesson33_jpeg_compressing/jpeg_compressing
python3 main.py --input input/goldhill.bmp
```

### Method 3: Simple Path
```bash
# Simplest - just provide the filename if in input/
python3 main.py --input input/goldhill.bmp
```

## Command Examples

### Basic Usage
```bash
python3 main.py --input input/goldhill.bmp
```

### Custom Quality Levels
```bash
python3 main.py --input input/goldhill.bmp --quality-levels 10,50,90
```

### Save Decompressed Images
```bash
python3 main.py --input input/goldhill.bmp --save-decompressed
```

### Package Mode
```bash
python3 -m jpeg_compressing --input input/goldhill.bmp
```

## Expected Output

After running, you'll find:

```
output/
├── compressed/
│   ├── compressed_q10.jpg    # 10 JPEG files
│   ├── compressed_q20.jpg
│   └── ...
├── metrics/
│   └── metrics.csv            # Quality metrics
├── plots/
│   ├── byte_histogram_original.png
│   ├── byte_histogram_compressed.png
│   └── error_vs_quality.png
└── logs/
    └── app.log                # Detailed logs
```

## Troubleshooting

### "No module named 'jpeg_compressing'"
Run from the parent directory or use `main.py` directly.

### "FileNotFoundError: Input image not found"
Make sure your image is in the `input/` folder:
```bash
ls -la input/
```

### Import Errors
Make sure you're in the virtual environment:
```bash
which python3
# Should show: .../venv/bin/python3
```

## Quick Test

```bash
# Full test sequence
cd /mnt/c/Users/yair0/AI_continue/Lesson33_jpeg_compressing/jpeg_compressing
source ../../venv/bin/activate
python3 main.py --input input/goldhill.bmp

# Check results
ls -lh output/compressed/
cat output/metrics/metrics.csv
```

## Tips

1. **Input folder is now `./input`** not `data/input`
2. **Use relative paths** from the project root
3. **BMP files work best** for uncompressed baseline
4. **Check logs** for detailed information: `tail -f output/logs/app.log`
5. **View plots** from WSL: `explorer.exe output/plots/`

Done! 🚀
