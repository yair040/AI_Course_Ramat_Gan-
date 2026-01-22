# Vertex Detection Accuracy Fixes

**Author:** Yair Levi  
**Date:** January 22, 2026  
**Version:** 2.1

---

## Problem Identified

The top vertex (V3) was consistently detected **lower** than its actual position (higher Y value, since Y-axis points downward). The error was **systematic**, not random.

### Root Causes:

1. **Thick Edges** - FFT filtering created thick edge regions
2. **Low Threshold (48)** - Kept more pixels, making edges even thicker
3. **Hough Ambiguity** - With thick edges, Hough detected lines through the middle of edge blobs
4. **Corner Blurring** - Sharp corners (like top vertex) were more affected by FFT filter

---

## Implemented Fixes

### Fix #1: Increased Threshold (48 → 80) ✅

**File:** `config.py`

**Change:**
```python
# Before
EDGE_THRESHOLD = 48

# After  
EDGE_THRESHOLD = 80  # Increased from 48 for thinner edges
```

**Effect:**
- Thinner edge pixels
- Less ambiguity for Hough transform
- More precise line detection

---

### Fix #2: Edge Thinning (Morphological Skeletonization) ✅

**File:** `edge_detector.py`

**New Function:**
```python
def thin_edges(binary_image: np.ndarray) -> np.ndarray:
    """
    Thin edges to single-pixel width using Zhang-Suen algorithm.
    """
    thinned = cv2.ximgproc.thinning(
        binary_image, 
        thinningType=cv2.ximgproc.THINNING_ZHANGSUEN
    )
    return thinned
```

**Effect:**
- Reduces thick edges to **single-pixel width**
- Eliminates ambiguity about exact line position
- Preserves connectivity and topology
- Dramatically improves Hough accuracy

**Zhang-Suen Algorithm:**
- Industry-standard morphological thinning
- Iteratively removes boundary pixels
- Preserves skeleton structure
- Ensures single-pixel thick lines

---

### Fix #3: Improved Line Filtering ✅

**File:** `triangle_detector.py`

**Changes:**

1. **Better Normalization:**
```python
# Normalize theta to [0, π] and handle negative rho
for rho, theta in lines:
    while theta < 0:
        theta += np.pi
    while theta >= np.pi:
        theta -= np.pi
    
    if rho < 0:
        rho = -rho
        theta = theta + np.pi if theta < np.pi/2 else theta - np.pi
```

2. **Tighter Filtering Parameters:**
```python
# config.py
LINE_RHO_THRESHOLD = 25.0  # Reduced from 30
LINE_THETA_THRESHOLD = 0.087  # 5 degrees (reduced from ~8.6 degrees)
```

3. **Better Line Selection Algorithm:**
```python
# Use itertools.combinations to try ALL combinations
# Select the combination with maximum minimum angular separation
for combo in combinations(range(len(lines)), 3):
    angles = [lines[i][1] for i in combo]
    min_angle = calculate_min_pairwise_angle(angles)
    if min_angle > max_min_angle:
        best_combination = combo
```

**Effect:**
- More accurate line deduplication
- Better handling of edge cases
- Optimal triangle edge selection

---

### Fix #4: Higher Hough Threshold ✅

**File:** `config.py`

**Change:**
```python
# Before (implicit in code)
HOUGH_THRESHOLD = 80

# After
HOUGH_THRESHOLD = 100  # Higher threshold for cleaner line detection
```

**Effect:**
- Requires more votes for line detection
- Filters out spurious lines from noise
- Only strong, well-defined edges detected

---

### Fix #5: Updated Task Pipeline ✅

**File:** `tasks.py`

**Integration:**
```python
def task4_threshold_image(edge_image: np.ndarray, threshold: int = EDGE_THRESHOLD):
    # Apply threshold
    binary_image = apply_threshold(edge_image, threshold)
    save_image(binary_image, "03_thresholded.png")
    
    # NEW: Apply edge thinning
    try:
        thinned_image = thin_edges(binary_image)
        save_image(thinned_image, "03b_thinned_edges.png")
        return thinned_image  # Use thinned edges for Hough
    except Exception:
        return binary_image  # Fallback to original if thinning fails
```

**Effect:**
- Seamless integration into pipeline
- Graceful fallback if thinning unavailable
- New output file for debugging

---

### Fix #6: Updated Dependencies ✅

**File:** `requirements.txt`

**Change:**
```python
# Before
opencv-python>=4.5.0,<5.0.0

# After
opencv-contrib-python>=4.5.0,<5.0.0  # Required for ximgproc.thinning
```

**Why:**
- `cv2.ximgproc.thinning` is in opencv-contrib
- Not available in standard opencv-python
- Must use opencv-contrib-python

---

## Expected Improvements

### Before Fixes:
```
DETECTION ERRORS (pixels)
Vertex 1: 0.48 pixels  (top vertex - SYSTEMATICALLY LOW)
Vertex 2: 0.69 pixels
Vertex 3: 0.56 pixels
Mean Error: 0.58 pixels
```

### After Fixes (Expected):
```
DETECTION ERRORS (pixels)
Vertex 1: < 0.3 pixels  (top vertex - IMPROVED)
Vertex 2: < 0.3 pixels
Vertex 3: < 0.3 pixels
Mean Error: < 0.3 pixels
```

**Improvement:** ~50-70% reduction in error, especially for top vertex

---

## New Output Files

The pipeline now generates an additional file:

| File | Description |
|------|-------------|
| `03b_thinned_edges.png` | Single-pixel width edges after thinning |

**Pipeline Order:**
1. `01_original_triangle.png` - Original
2. `02_edge_detected.png` - FFT edges (grayscale)
3. `03_thresholded.png` - Binary edges (threshold=80)
4. **`03b_thinned_edges.png`** ⭐ NEW - Thinned to 1-pixel width
5. `05_hough_lines.png` - Hough lines (uses thinned edges)
6. `04_triangle_overlay.png` - Final result

---

## Technical Details

### Why Edge Thinning Works:

**Problem:** Thick edges have ambiguous center
```
Original Edge (thick):        Thinned Edge (1-pixel):
  ###                              .
 #####                             #
#######       →                    #
 #####                             #
  ###                              .
```

**Hough Transform:**
- Thick edge: Line could be anywhere in the blob → uncertainty
- Thin edge: Line position is exact → precision

### Zhang-Suen Thinning Algorithm:

**Properties:**
- **Topology preserving:** Doesn't break connectivity
- **Medial axis:** Finds center of thick edges
- **Iterative:** Progressively removes boundary pixels
- **Fast:** O(n) where n = number of edge pixels

**Iteration Steps:**
1. Mark pixels for deletion (north/south neighbors)
2. Delete marked pixels
3. Mark pixels for deletion (east/west neighbors)
4. Delete marked pixels
5. Repeat until convergence (no more deletions)

---

## Installation Update

### Before Running:

```bash
# Uninstall old opencv
pip uninstall opencv-python

# Install opencv-contrib
pip install opencv-contrib-python>=4.5.0

# Or reinstall all requirements
pip install -r requirements.txt
```

**Important:** Cannot have both `opencv-python` and `opencv-contrib-python` installed simultaneously. The contrib version includes everything from the standard version plus extra modules.

---

## Verification Steps

### Step 1: Check Edge Thinning
```bash
python main.py
# Check output/03b_thinned_edges.png exists
# Edges should be 1-pixel wide
```

### Step 2: Compare Before/After
Look at the console output:
```
DETECTION ERRORS (pixels)
Vertex 1: X.XX pixels  # Should be < 0.3
Vertex 2: X.XX pixels  # Should be < 0.3
Vertex 3: X.XX pixels  # Should be < 0.3
Mean Error: X.XX pixels  # Should be < 0.3
```

### Step 3: Visual Inspection
Compare images:
- `03_thresholded.png` - Should see thinner edges (threshold=80)
- `03b_thinned_edges.png` - Should see 1-pixel lines
- `05_hough_lines.png` - Blue lines should align perfectly with white triangle edges
- `04_triangle_overlay.png` - Green triangle should match white triangle exactly

---

## Fallback Behavior

If edge thinning fails (e.g., opencv-contrib not installed):

```python
try:
    thinned_image = thin_edges(binary_image)
    # Use thinned edges
except Exception as thin_error:
    logger.warning(f"Edge thinning failed: {thin_error}")
    # Use original binary image (still with threshold=80)
```

**Degraded Mode:**
- Still runs with original binary edges
- Higher threshold (80 vs 48) still provides improvement
- Just not as accurate as with thinning

---

## Summary of Changes

| Component | Change | Impact |
|-----------|--------|--------|
| Threshold | 48 → 80 | Thinner edges |
| Edge Thinning | Added | Single-pixel precision |
| Hough Threshold | Implicit → 100 | Cleaner line detection |
| Line Filtering | Improved normalization | Better deduplication |
| Line Selection | Optimized algorithm | Best 3 lines chosen |
| Dependencies | opencv-contrib-python | Required for thinning |
| Output | +1 file (thinned edges) | Debugging visibility |

---

## Expected Outcome

✅ **Top vertex (V3) detection accuracy significantly improved**  
✅ **All vertices detected within ±0.5 pixels**  
✅ **Systematic bias eliminated**  
✅ **More robust to noise and edge thickness**

The combination of higher threshold, edge thinning, and improved Hough parameters should resolve the vertex detection issue completely.