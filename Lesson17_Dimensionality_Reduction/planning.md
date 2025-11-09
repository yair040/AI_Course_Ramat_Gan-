# Technical Planning Document
## PCA and t-SNE Text Vectorization System

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    main.py                          │
│           (Orchestration & Execution)               │
└──────────────────┬──────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┬─────────────┬─────────────┐
    │              │              │             │             │
    ▼              ▼              ▼             ▼             ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Task 1  │  │  Task 2  │  │  Task 3  │  │  Task 4  │  │  Task 5  │
│Generate │  │Vectorize │  │ Manual   │  │  sklearn │  │  t-SNE   │
│Sentences│  │   Text   │  │   PCA    │  │   PCA    │  │          │
└─────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
     │            │              │              │             │
     └────────────┴──────────────┴──────────────┴─────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   │                           │
                   ▼                           ▼
            ┌─────────────┐           ┌──────────────┐
            │   utils.py  │           │visualization │
            │   (Helpers) │           │     .py      │
            └─────────────┘           └──────────────┘
```

### Module Design

#### 1. main.py (Orchestration Layer)
**Purpose**: Entry point and task coordination

**Responsibilities**:
- Parse command-line arguments (optional)
- Initialize environment
- Execute tasks in sequence
- Handle errors gracefully
- Display summary results

**Key Functions**:
```python
def main():
    """Main orchestration function"""
    # Setup
    # Execute task 1
    # Execute task 2
    # Execute task 3
    # Execute task 4
    # Execute task 5
    # Summary

def print_summary(results):
    """Display summary of all results"""
```

**Line Count Estimate**: ~100 lines

---

#### 2. task1_generate.py (Sentence Generation)
**Purpose**: Generate 100 categorized sentences

**Responsibilities**:
- Generate sentences with random category assignment
- Ensure variety and quality
- Save to sentences.txt
- Display to console

**Key Functions**:
```python
def generate_sentences(n=100, seed=42) -> list[str]:
    """Generate n sentences across categories"""

def save_sentences(sentences, filepath='sentences.txt'):
    """Save sentences to file"""

def print_sentences(sentences):
    """Print sentences to console"""
```

**Data Structure**:
```python
CATEGORIES = ['sport', 'food', 'work']
TEMPLATES = {
    'sport': [...],
    'food': [...],
    'work': [...]
}
```

**Line Count Estimate**: ~150 lines

---

#### 3. task2_vectorize.py (Text Vectorization)
**Purpose**: Convert sentences to normalized vectors

**Responsibilities**:
- Load sentence embeddings model
- Convert text to vectors
- Normalize vectors to unit length
- Save vectors to file

**Key Functions**:
```python
def load_model():
    """Load sentence transformer model"""

def vectorize_sentences(sentences: list[str]) -> np.ndarray:
    """Convert sentences to vectors"""

def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    """L2 normalization to unit length"""

def save_vectors(vectors, filepath='normalized.txt'):
    """Save vectors to file"""
```

**Model Choice**: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Fast inference
- Good quality

**Line Count Estimate**: ~120 lines

---

#### 4. task3_manual_pca.py (Manual PCA Implementation)
**Purpose**: Implement PCA from mathematical principles

**Responsibilities**:
- Implement all 11 steps (a-k)
- Time each step
- Use only NumPy (no sklearn)
- Generate 3D visualization

**Key Functions**:
```python
def calculate_mean(vectors: np.ndarray) -> np.ndarray:
    """Step a: Calculate feature means"""

def center_data(vectors: np.ndarray, mean: np.ndarray) -> np.ndarray:
    """Step b: Center around zero"""

def build_matrix_x(centered_vectors: np.ndarray) -> np.ndarray:
    """Step c: Arrange vectors as columns"""

def compute_covariance_matrix(X: np.ndarray) -> np.ndarray:
    """Step d: Compute S = (X.T @ X) / (n-1)"""

def calculate_eigenvalues(S: np.ndarray) -> np.ndarray:
    """Step e: Compute eigenvalues"""

def calculate_eigenvectors(S: np.ndarray, eigenvalues: np.ndarray) -> np.ndarray:
    """Step f: Compute eigenvectors"""

def build_transformation_matrix(eigenvectors: np.ndarray, eigenvalues: np.ndarray, k=3) -> np.ndarray:
    """Step g: Build P from top k eigenvectors"""

def transpose_matrix(P: np.ndarray) -> np.ndarray:
    """Step h: Compute P.T"""

def transform_vectors(vectors: np.ndarray, P_T: np.ndarray) -> np.ndarray:
    """Step i: Project to new space"""

def kmeans_clustering(vectors_3d: np.ndarray, k=3, seed=42) -> np.ndarray:
    """Step j: K-means clustering"""

def manual_pca_pipeline(vectors: np.ndarray) -> dict:
    """Execute full pipeline with timing"""
```

**Timing Strategy**:
```python
from utils import Timer

with Timer("Step a: Calculate means"):
    means = calculate_mean(vectors)
```

**Line Count Estimate**: ~200 lines (may need split into task3_manual_pca.py and task3_helpers.py)

---

#### 5. task4_sklearn_pca.py (sklearn PCA)
**Purpose**: Fast PCA using sklearn

**Responsibilities**:
- Apply sklearn PCA
- Reduce to 3D
- K-means clustering
- Visualization

**Key Functions**:
```python
def apply_pca(vectors: np.ndarray, n_components=3) -> tuple[np.ndarray, PCA]:
    """Apply sklearn PCA"""

def sklearn_pca_pipeline(vectors: np.ndarray) -> dict:
    """Execute pipeline with timing"""
```

**Line Count Estimate**: ~100 lines

---

#### 6. task5_tsne.py (t-SNE)
**Purpose**: Non-linear dimensionality reduction

**Responsibilities**:
- Apply t-SNE
- Reduce to 3D
- K-means clustering
- Visualization

**Key Functions**:
```python
def apply_tsne(vectors: np.ndarray, n_components=3, perplexity=30, seed=42) -> np.ndarray:
    """Apply sklearn t-SNE"""

def tsne_pipeline(vectors: np.ndarray) -> dict:
    """Execute pipeline with timing"""
```

**Line Count Estimate**: ~100 lines

---

#### 7. utils.py (Utilities)
**Purpose**: Shared helper functions

**Key Functions**:
```python
class Timer:
    """Context manager for timing code blocks"""
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.duration = self.end - self.start
        print(f"  ⏱️  {self.duration:.4f} seconds")

def load_sentences(filepath='sentences.txt') -> list[str]:
    """Load sentences from file"""

def load_vectors(filepath='normalized.txt') -> np.ndarray:
    """Load vectors from file"""

def save_numpy_array(arr, filepath):
    """Save numpy array to file"""

def format_time(seconds: float) -> str:
    """Format time for display"""
```

**Line Count Estimate**: ~100 lines

---

#### 8. visualization.py (Plotting)
**Purpose**: 3D visualization functions

**Key Functions**:
```python
def plot_3d_clusters(
    points_3d: np.ndarray,
    labels: np.ndarray,
    title: str,
    sentence_ids: np.ndarray = None,
    save_path: str = None,
    show: bool = True
):
    """Create 3D scatter plot with clusters"""
    # Set up figure
    # Color by cluster
    # Add point labels if requested
    # Style and format
    # Save or show

def configure_3d_plot(ax, title: str):
    """Configure 3D plot styling"""
```

**Visualization Details**:
- Use `matplotlib.pyplot` and `mpl_toolkits.mplot3d`
- Color palette: Distinct colors for 3 clusters
- Point labels: Use `ax.text()` for serial numbers
- Interactive rotation enabled
- Grid and axis labels

**Line Count Estimate**: ~120 lines

---

### Data Flow

```
Step 1: Generate
  └─> sentences.txt (100 lines)
  └─> List[str] in memory

Step 2: Vectorize
  └─> normalized.txt (100 x 384 matrix)
  └─> numpy array (100, 384)

Step 3: Manual PCA
  ├─> pca_transformed_manual.txt (100 x 3 matrix)
  ├─> Cluster labels (100,)
  └─> Visualization PNG/display

Step 4: sklearn PCA
  ├─> pca_transformed_sklearn.txt (100 x 3 matrix)
  ├─> Cluster labels (100,)
  └─> Visualization PNG/display

Step 5: t-SNE
  ├─> tsne_transformed.txt (100 x 3 matrix)
  ├─> Cluster labels (100,)
  └─> Visualization PNG/display
```

### File Format Specifications

#### sentences.txt
```
Format: Plain text, one sentence per line
Example:
The basketball game was exciting
I love eating pizza
The project deadline is tomorrow
...
```

#### normalized.txt
```
Format: Space-separated values, one vector per line
Dimensions: 100 rows x 384 columns
Example:
0.1234 -0.5678 0.9012 ... (384 values)
-0.3456 0.7890 -0.1234 ... (384 values)
...
```

#### Transformed vector files
```
Format: Space-separated values, one vector per line
Dimensions: 100 rows x 3 columns
Example:
2.345 -1.234 0.567
-3.456 2.789 1.234
...
```

### Configuration Constants

```python
# config.py or constants in utils.py
RANDOM_SEED = 42
NUM_SENTENCES = 100
NUM_CLUSTERS = 3
PCA_COMPONENTS = 3
TSNE_COMPONENTS = 3
TSNE_PERPLEXITY = 30
TSNE_LEARNING_RATE = 200
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# File paths
SENTENCES_FILE = 'sentences.txt'
NORMALIZED_FILE = 'normalized.txt'
MANUAL_PCA_FILE = 'pca_transformed_manual.txt'
SKLEARN_PCA_FILE = 'pca_transformed_sklearn.txt'
TSNE_FILE = 'tsne_transformed.txt'

# Visualization
FIGURE_SIZE = (10, 8)
POINT_SIZE = 50
COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1']
```

### Dependencies (requirements.txt)

```txt
numpy>=1.21.0
sentence-transformers>=2.2.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
torch>=1.10.0  # Required by sentence-transformers
```

### Error Handling Strategy

**Critical Points**:
1. File I/O operations
2. Model loading (might fail on first run)
3. Matrix operations (dimension mismatches)
4. Eigenvalue computation (numerical stability)
5. Clustering (empty clusters possible)

**Approach**:
- Try-except blocks around I/O
- Validate dimensions after each major step
- Check for NaN/Inf after computations
- Informative error messages
- Graceful degradation where possible

### Testing Strategy

#### Unit Tests
- `test_task1.py`: Verify sentence generation
- `test_task2.py`: Verify vectorization and normalization
- `test_task3.py`: Verify each PCA step
- `test_utils.py`: Verify helper functions

#### Integration Tests
- End-to-end pipeline execution
- Verify file outputs exist and have correct format
- Verify visualizations can be generated

#### Validation Tests
- Check vectors are normalized (||v|| ≈ 1)
- Check PCA output shape (100, 3)
- Check eigenvalues are sorted descending
- Check cluster assignments sum to 100

### Performance Considerations

**Bottlenecks**:
1. **Sentence vectorization**: Most time-consuming (model inference)
2. **t-SNE**: Second most expensive (iterative optimization)
3. **Manual PCA eigendecomposition**: Moderate
4. **K-means**: Fast for 100 points

**Optimizations**:
- Batch vectorization (all sentences at once)
- Cache model after loading
- Use NumPy vectorized operations
- Avoid Python loops where possible

### Development Phases

**Phase 1: Foundation** (Est. 2 hours)
- Set up virtual environment
- Create project structure
- Implement utils.py
- Implement task1_generate.py
- Test sentence generation

**Phase 2: Vectorization** (Est. 1 hour)
- Implement task2_vectorize.py
- Test vectorization and normalization
- Verify output format

**Phase 3: Visualization** (Est. 1 hour)
- Implement visualization.py
- Create test data
- Verify 3D plots work

**Phase 4: Manual PCA** (Est. 3-4 hours)
- Implement task3_manual_pca.py
- Test each step individually
- Verify mathematical correctness
- Add timing instrumentation

**Phase 5: Library Methods** (Est. 1 hour)
- Implement task4_sklearn_pca.py
- Implement task5_tsne.py
- Test and verify

**Phase 6: Integration** (Est. 1 hour)
- Implement main.py
- End-to-end testing
- Bug fixes
- Documentation

**Total Estimate**: 9-10 hours

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Eigenvalue computation unstable | Medium | High | Add numerical stability checks, use SVD if needed |
| t-SNE doesn't converge | Low | Medium | Adjust perplexity and learning rate |
| File line limits exceeded | Medium | Low | Split into helper modules |
| Model download fails | Low | High | Cache model, provide fallback |
| Visualization too crowded | Medium | Low | Make labels optional, adjust sizing |
| Memory issues | Low | Low | 100 vectors is small dataset |

### Success Metrics

**Functional**:
- ✅ All 100 sentences generated
- ✅ All vectors normalized (unit length)
- ✅ All three methods produce 3D output
- ✅ All visualizations display correctly
- ✅ Timing information displayed

**Code Quality**:
- ✅ No file exceeds 200 lines
- ✅ Clear function separation
- ✅ No code duplication
- ✅ Proper error handling

**Mathematical Correctness**:
- ✅ Eigenvalues sorted correctly
- ✅ Manual PCA ≈ sklearn PCA (sign invariance)
- ✅ Covariance matrix is symmetric
- ✅ Principal components are orthogonal

### Future Enhancements

**Phase 2 Ideas** (Out of scope for v1):
1. Interactive parameter tuning (CLI arguments)
2. Comparison metrics (silhouette score, explained variance)
3. Multiple clustering algorithms
4. Larger datasets
5. Real-time visualization updates
6. Export results to CSV
7. HTML report generation
8. GPU acceleration for t-SNE
