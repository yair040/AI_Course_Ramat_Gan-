# Processing Pipeline Diagram
## Image Frequency Filter Application

**Author:** Yair Levi

---

## Complete Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT IMAGE (Grayscale)                      │
│                     input/your_image.jpg                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 1: Load Image                            │
│              utils/image_loader.py → load_image()                │
│                  Convert to grayscale array                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 2: Apply FFT                             │
│            tasks/fft_transform.py → apply_fft()                  │
│                  Spatial → Frequency Domain                      │
│                    fft2() + fftshift()                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 3: Visualize Original Spectrum                 │
│          tasks/frequency_display.py → save_spectrum()            │
│                                                                   │
│  OUTPUT: [image]_spectrum_original.png                           │
│          Shows original frequency distribution                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
         ┌─────────────────┐   ┌──────────────┐
         │ Multiprocessing │   │  Sequential  │
         │    Enabled      │   │   Processing │
         └────────┬────────┘   └──────┬───────┘
                  │                   │
                  └────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ High-Pass    │  │  Low-Pass    │  │  Band-Pass   │
│   Filter     │  │   Filter     │  │   Filter     │
│   (HPF)      │  │   (LPF)      │  │   (BPF)      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Create Mask  │  │ Create Mask  │  │ Create Mask  │
│  Distance    │  │  Distance    │  │  Distance    │
│  > cutoff    │  │  ≤ cutoff    │  │  In band     │
│   = 1        │  │   = 1        │  │   = 1        │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Apply Mask   │  │ Apply Mask   │  │ Apply Mask   │
│ FFT × Mask   │  │ FFT × Mask   │  │ FFT × Mask   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────┐
│         Show Filtered Spectrum (Each Filter)        │
│     tasks/frequency_display.py → save_spectrum()    │
│                                                      │
│  OUTPUTS:                                            │
│  - [image]_spectrum_HighPassFilter.png               │
│  - [image]_spectrum_LowPassFilter.png                │
│  - [image]_spectrum_BandPassFilter.png               │
└──────┬────────────────┬────────────────┬────────────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Inverse FFT  │  │ Inverse FFT  │  │ Inverse FFT  │
│  ifftshift() │  │  ifftshift() │  │  ifftshift() │
│    ifft2()   │  │    ifft2()   │  │    ifft2()   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Normalize   │  │  Normalize   │  │  Normalize   │
│  to [0,255]  │  │  to [0,255]  │  │  to [0,255]  │
│  → uint8     │  │  → uint8     │  │  → uint8     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Save Image  │  │  Save Image  │  │  Save Image  │
│              │  │              │  │              │
│ HPF Result   │  │ LPF Result   │  │ BPF Result   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └────────┬────────┴────────┬────────┘
                │                 │
                ▼                 ▼
    ┌────────────────────────────────────┐
    │  STEP 6: Create Comparison Grid    │
    │  tasks/image_display.py            │
    │                                     │
    │  Original | HPF | LPF | BPF        │
    └────────────────┬───────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   OUTPUT FILES        │
         │   (in output/)        │
         └───────────────────────┘

OUTPUT SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Frequency Spectra (4 files):
  ✓ [image]_spectrum_original.png
  ✓ [image]_spectrum_HighPassFilter.png
  ✓ [image]_spectrum_LowPassFilter.png
  ✓ [image]_spectrum_BandPassFilter.png

Filtered Images (3 files):
  ✓ [image]_HighPassFilter.png
  ✓ [image]_LowPassFilter.png
  ✓ [image]_BandPassFilter.png

Comparison:
  ✓ [image]_comparison.png
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Filter Mask Visualization

```
HIGH-PASS FILTER (HPF)          LOW-PASS FILTER (LPF)
Remove Low Frequencies          Remove High Frequencies

     Frequency Space                 Frequency Space
┌─────────────────────┐        ┌─────────────────────┐
│█████████████████████│        │                     │
│█████████████████████│        │                     │
│█████████████████████│        │     ┌─────────┐     │
│████████┌───┐████████│        │     │█████████│     │
│████████│   │████████│        │     │█████████│     │
│████████│ 0 │████████│   VS   │     │█████████│     │
│████████│   │████████│        │     │█████████│     │
│████████└───┘████████│        │     └─────────┘     │
│█████████████████████│        │                     │
│█████████████████████│        │                     │
│█████████████████████│        │                     │
└─────────────────────┘        └─────────────────────┘
  Keep Edges (1)                  Keep Center (1)
  Remove Center (0)                Remove Edges (0)


BAND-PASS FILTER (BPF)
Keep Frequency Band

     Frequency Space
┌─────────────────────┐
│                     │
│  ┌─────────────┐    │
│  │█████████████│    │
│  │███┌─────┐███│    │
│  │███│     │███│    │
│  │███│  0  │███│    │
│  │███│     │███│    │
│  │███└─────┘███│    │
│  │█████████████│    │
│  └─────────────┘    │
│                     │
└─────────────────────┘
   Keep Band (1)
   Remove Center & Edges (0)
```

---

## Data Flow by Module

```
┌──────────────────────────────────────────────────────────┐
│                    MODULE INTERACTIONS                    │
└──────────────────────────────────────────────────────────┘

main.py
  │
  ├─→ utils.image_loader.load_image()
  │     └─→ Returns: np.ndarray (grayscale)
  │
  ├─→ tasks.fft_transform.apply_fft()
  │     └─→ Returns: np.ndarray (complex FFT)
  │
  ├─→ tasks.fft_transform.get_magnitude_spectrum()
  │     └─→ Returns: np.ndarray (magnitude)
  │
  ├─→ tasks.frequency_display.save_spectrum()
  │     └─→ Saves: [image]_spectrum_original.png
  │
  ├─→ filters.high_pass.HighPassFilter()
  │     ├─→ create_mask() → Returns: np.ndarray (mask)
  │     └─→ apply() → Returns: np.ndarray (filtered FFT)
  │
  ├─→ filters.low_pass.LowPassFilter()
  │     ├─→ create_mask() → Returns: np.ndarray (mask)
  │     └─→ apply() → Returns: np.ndarray (filtered FFT)
  │
  ├─→ filters.band_pass.BandPassFilter()
  │     ├─→ create_mask() → Returns: np.ndarray (mask)
  │     └─→ apply() → Returns: np.ndarray (filtered FFT)
  │
  ├─→ tasks.filter_apply.apply_filters_parallel()
  │     └─→ Returns: dict {filter_name: filtered_fft}
  │
  ├─→ FOR EACH filtered_fft:
  │     │
  │     ├─→ tasks.fft_transform.get_magnitude_spectrum()
  │     │     └─→ Returns: np.ndarray (filtered magnitude)
  │     │
  │     ├─→ tasks.frequency_display.save_spectrum()
  │     │     └─→ Saves: [image]_spectrum_[filter].png
  │     │
  │     ├─→ tasks.inverse_transform.reconstruct_image()
  │     │     └─→ Returns: np.ndarray (reconstructed uint8)
  │     │
  │     └─→ utils.image_loader.save_image()
  │           └─→ Saves: [image]_[filter].png
  │
  └─→ tasks.image_display.create_comparison()
        └─→ Saves: [image]_comparison.png
```

---

## Frequency Domain Visualization

```
ORIGINAL IMAGE              FREQUENCY SPECTRUM
                           (Logarithmic Scale)

  ┌──────────┐               ┌──────────┐
  │          │               │▓▓▓▓▓▓▓▓▓▓│
  │  Photo   │    FFT        │▓▓████▓▓▓▓│  ← High frequencies
  │          │   ───→        │▓██▓▓██▓▓▓│
  │          │               │▓█▓▓▓▓▓█▓▓│
  │          │               │▓▓▓▓◉▓▓▓▓▓│  ← DC component (center)
  └──────────┘               │▓█▓▓▓▓▓█▓▓│
                             │▓██▓▓██▓▓▓│
                             │▓▓████▓▓▓▓│
                             │▓▓▓▓▓▓▓▓▓▓│
                             └──────────┘
                              ↑
                              Low frequencies
                              (smooth areas)

Legend:
◉ = DC (zero frequency, brightest)
█ = High magnitude (bright)
▓ = Medium magnitude (gray)
  = Low magnitude (dark)
```

---

## Filter Effect Comparison

```
INPUT IMAGE: Photograph of a building

┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  ORIGINAL          HPF             LPF             BPF       │
│  ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐      │
│  │Photo │       │Edges │       │Blur  │       │Lines │      │
│  │      │       │      │       │      │       │      │      │
│  │▓▓▓▓▓▓│  →    │█   █ │  →    │▓▓▓▓▓▓│  →    │  ══  │      │
│  │▓▓██▓▓│       │█   █ │       │▓▓▓▓▓▓│       │  ══  │      │
│  │▓▓▓▓▓▓│       │█████ │       │▓▓▓▓▓▓│       │  ══  │      │
│  └──────┘       └──────┘       └──────┘       └──────┘      │
│   Normal      Sharp Edges     Smoothed      Mid-Freq Only   │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Effect Summary:
• HPF: Emphasizes edges, removes smooth gradients
• LPF: Removes noise, blurs details
• BPF: Keeps texture patterns, removes extremes
```

---

## Logging Flow

```
┌────────────────────────────────────────────┐
│         LOGGING ARCHITECTURE               │
└────────────────────────────────────────────┘

Application Start
  │
  ├─→ utils.logger.setup_logger('main')
  │     └─→ Creates: log/main.log
  │
  ├─→ Each module gets logger
  │     ├─→ log/tasks_fft_transform.log
  │     ├─→ log/filters_high_pass.log
  │     ├─→ log/filters_low_pass.log
  │     └─→ log/filters_band_pass.log
  │
  └─→ Ring Buffer (per logger)
        ├─→ File 1: [name].log       (current, 0-16MB)
        ├─→ File 2: [name].log.1     (backup, 16MB)
        ├─→ File 3: [name].log.2     (backup, 16MB)
        │   ...
        └─→ File 20: [name].log.19   (backup, 16MB)
              │
              └─→ When full, overwrites File 1

Total Log Capacity: 20 files × 16MB = 320MB per logger
```

---

**Diagram Status:** ✅ Complete  
**Last Updated:** January 20, 2026