# Implementation Tasks
## PCA and t-SNE Text Vectorization System

### Overview
This document breaks down the implementation into actionable tasks, organized by priority and dependencies.

---

## Phase 0: Environment Setup

### Task 0.1: Create Virtual Environment
**Priority**: Critical
**Estimated Time**: 10 minutes
**Dependencies**: None

**Steps**:
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate` (WSL)
3. Upgrade pip: `pip install --upgrade pip`

**Verification**:
- `which python` shows venv path
- `pip --version` works

---

### Task 0.2: Create requirements.txt
**Priority**: Critical
**Estimated Time**: 5 minutes
**Dependencies**: Task 0.1

**Content**:
```txt
numpy>=1.21.0
sentence-transformers>=2.2.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
torch>=1.10.0
```

**Steps**:
1. Create `requirements.txt` with above content
2. Install: `pip install -r requirements.txt`
3. Verify imports work

**Verification**:
```bash
python -c "import numpy; import sklearn; import sentence_transformers; import matplotlib"
```

---

### Task 0.3: Create Project Structure
**Priority**: Critical
**Estimated Time**: 5 minutes
**Dependencies**: None

**Steps**:
1. Create empty Python files:
   - `main.py`
   - `task1_generate.py`
   - `task2_vectorize.py`
   - `task3_manual_pca.py`
   - `task4_sklearn_pca.py`
   - `task5_tsne.py`
   - `utils.py`
   - `visualization.py`

**Verification**:
- All files exist
- Files are in project root

---

## Phase 1: Utilities and Helpers

### Task 1.1: Implement utils.py
**Priority**: High
**Estimated Time**: 30 minutes
**Dependencies**: Task 0.3

**Functions to Implement**:

#### 1.1.1: Timer Context Manager
```python
import time

class Timer:
    """Context manager for timing code blocks"""
    def __init__(self, description="Operation"):
        self.description = description
        self.duration = None

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"\n▶ {self.description}...")
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.duration = self.end - self.start
        print(f"  ⏱️  Completed in {self.duration:.4f} seconds")
```

#### 1.1.2: File I/O Helpers
```python
def save_sentences(sentences: list[str], filepath: str):
    """Save sentences to text file, one per line"""

def load_sentences(filepath: str) -> list[str]:
    """Load sentences from text file"""

def save_vectors(vectors: np.ndarray, filepath: str):
    """Save numpy array to text file (space-separated)"""

def load_vectors(filepath: str) -> np.ndarray:
    """Load numpy array from text file"""
```

#### 1.1.3: Constants
```python
# Configuration
RANDOM_SEED = 42
NUM_SENTENCES = 100
NUM_CLUSTERS = 3
PCA_COMPONENTS = 3
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# File paths
SENTENCES_FILE = 'sentences.txt'
NORMALIZED_FILE = 'normalized.txt'
MANUAL_PCA_FILE = 'pca_transformed_manual.txt'
SKLEARN_PCA_FILE = 'pca_transformed_sklearn.txt'
TSNE_FILE = 'tsne_transformed.txt'
```

**Testing**:
- Timer prints correct format
- File save/load roundtrip works
- Constants are accessible

**Line Count**: ~100 lines

---

### Task 1.2: Implement visualization.py
**Priority**: High
**Estimated Time**: 45 minutes
**Dependencies**: Task 0.2

**Functions to Implement**:

#### 1.2.1: Main Plotting Function
```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_3d_clusters(
    points_3d: np.ndarray,
    labels: np.ndarray,
    title: str,
    sentence_ids: np.ndarray = None,
    save_path: str = None,
    show: bool = True
):
    """
    Create 3D scatter plot with cluster colors

    Args:
        points_3d: (N, 3) array of 3D points
        labels: (N,) array of cluster labels
        title: Plot title
        sentence_ids: Optional (N,) array of sentence IDs to display
        save_path: Optional path to save figure
        show: Whether to display plot
    """
    # Create figure
    # Add 3D scatter
    # Color by cluster
    # Optionally add point labels
    # Configure axes
    # Save/show
```

#### 1.2.2: Helper Function
```python
def configure_3d_axes(ax, title: str):
    """Configure 3D plot styling"""
    ax.set_xlabel('Component 1', fontsize=10)
    ax.set_ylabel('Component 2', fontsize=10)
    ax.set_zlabel('Component 3', fontsize=10)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
```

**Features**:
- Distinct colors for 3 clusters (colorblind-friendly)
- Optional serial numbers on points
- Proper 3D perspective
- Legend with cluster labels
- Configurable figure size

**Testing**:
- Create dummy data and verify plot displays
- Test with/without labels
- Verify save functionality

**Line Count**: ~120 lines

---

## Phase 2: Task Implementations

### Task 2.1: Implement task1_generate.py
**Priority**: High
**Estimated Time**: 1 hour
**Dependencies**: Task 1.1

**Functions to Implement**:

#### 2.1.1: Sentence Templates
```python
import random

SPORT_TEMPLATES = [
    "I enjoy playing {sport}",
    "The {team} won the championship",
    "Training for the {event} is challenging",
    # ... more templates
]

FOOD_TEMPLATES = [
    "I love eating {food}",
    "The {dish} tastes delicious",
    "Cooking {meal} is my hobby",
    # ... more templates
]

WORK_TEMPLATES = [
    "The meeting starts at {time}",
    "I finished the {task} project",
    "Working on {activity} today",
    # ... more templates
]

SPORT_WORDS = ['basketball', 'soccer', 'tennis', ...]
FOOD_WORDS = ['pizza', 'sushi', 'pasta', ...]
WORK_WORDS = ['presentation', 'analysis', 'report', ...]
```

#### 2.1.2: Generation Function
```python
def generate_sentence(category: str) -> str:
    """Generate one sentence for given category"""

def generate_sentences(n: int = 100, seed: int = 42) -> list[str]:
    """Generate n sentences with random categories"""
    random.seed(seed)
    sentences = []
    categories = ['sport', 'food', 'work']

    for i in range(n):
        category = random.choice(categories)
        sentence = generate_sentence(category)
        sentences.append(sentence)

    return sentences
```

#### 2.1.3: Main Function
```python
def main():
    """Main execution for Task 1"""
    print("=" * 60)
    print("TASK 1: Generate Sentences")
    print("=" * 60)

    sentences = generate_sentences()

    # Print to console
    print(f"\nGenerated {len(sentences)} sentences:\n")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i:3d}. {sentence}")

    # Save to file
    from utils import save_sentences, SENTENCES_FILE
    save_sentences(sentences, SENTENCES_FILE)
    print(f"\n✓ Sentences saved to {SENTENCES_FILE}")

    return sentences
```

**Testing**:
- Run standalone: `python task1_generate.py`
- Verify 100 sentences generated
- Verify mix of categories
- Verify file created

**Line Count**: ~150 lines

---

### Task 2.2: Implement task2_vectorize.py
**Priority**: High
**Estimated Time**: 45 minutes
**Dependencies**: Task 1.1, Task 2.1

**Functions to Implement**:

#### 2.2.1: Model Loading
```python
from sentence_transformers import SentenceTransformer
import numpy as np

def load_embedding_model(model_name: str):
    """Load sentence transformer model"""
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"✓ Model loaded (embedding dimension: {model.get_sentence_embedding_dimension()})")
    return model
```

#### 2.2.2: Vectorization
```python
def vectorize_sentences(sentences: list[str], model) -> np.ndarray:
    """Convert sentences to embeddings"""
    embeddings = model.encode(sentences, show_progress_bar=True)
    return embeddings
```

#### 2.2.3: Normalization
```python
def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    """L2 normalization to unit length"""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized = vectors / norms
    return normalized
```

#### 2.2.4: Main Function
```python
def main():
    """Main execution for Task 2"""
    from utils import load_sentences, save_vectors, Timer
    from utils import SENTENCES_FILE, NORMALIZED_FILE, EMBEDDING_MODEL

    print("=" * 60)
    print("TASK 2: Vectorize Sentences")
    print("=" * 60)

    # Load sentences
    sentences = load_sentences(SENTENCES_FILE)
    print(f"\n✓ Loaded {len(sentences)} sentences")

    # Load model
    with Timer("Loading embedding model"):
        model = load_embedding_model(EMBEDDING_MODEL)

    # Vectorize
    with Timer("Vectorizing sentences"):
        vectors = vectorize_sentences(sentences, model)

    # Normalize
    with Timer("Normalizing vectors"):
        normalized = normalize_vectors(vectors)

    # Verify normalization
    norms = np.linalg.norm(normalized, axis=1)
    print(f"\n✓ Vector shape: {normalized.shape}")
    print(f"✓ Norm check - Min: {norms.min():.6f}, Max: {norms.max():.6f}")

    # Save
    save_vectors(normalized, NORMALIZED_FILE)
    print(f"✓ Normalized vectors saved to {NORMALIZED_FILE}")

    return normalized
```

**Testing**:
- Run standalone
- Verify vectors are unit length
- Verify output shape (100, 384)
- Verify file saved

**Line Count**: ~120 lines

---

### Task 2.3: Implement task3_manual_pca.py
**Priority**: Critical
**Estimated Time**: 3-4 hours
**Dependencies**: Task 1.1, Task 1.2

This is the most complex task. Break into sub-tasks:

#### 2.3.1: Individual Step Functions

**Step a: Calculate Mean**
```python
def step_a_calculate_mean(vectors: np.ndarray) -> np.ndarray:
    """Calculate mean for each feature"""
    mean = np.mean(vectors, axis=0)
    return mean
```

**Step b: Center Data**
```python
def step_b_center_data(vectors: np.ndarray, mean: np.ndarray) -> np.ndarray:
    """Center data around zero"""
    centered = vectors - mean
    return centered
```

**Step c: Build Matrix X**
```python
def step_c_build_matrix_x(centered_vectors: np.ndarray) -> np.ndarray:
    """Arrange vectors as columns in matrix X"""
    X = centered_vectors.T  # Transpose so vectors are columns
    return X
```

**Step d: Compute Covariance Matrix**
```python
def step_d_covariance_matrix(X: np.ndarray) -> np.ndarray:
    """Compute covariance matrix S = (X.T @ X) / (n-1)"""
    n = X.shape[1]  # Number of vectors
    S = (X.T @ X) / (n - 1)
    return S
```

**Step e: Calculate Eigenvalues**
```python
def step_e_eigenvalues(S: np.ndarray) -> np.ndarray:
    """Calculate eigenvalues of covariance matrix"""
    eigenvalues, _ = np.linalg.eig(S)
    return eigenvalues.real
```

**Step f: Calculate Eigenvectors**
```python
def step_f_eigenvectors(S: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Calculate eigenvectors of covariance matrix"""
    eigenvalues, eigenvectors = np.linalg.eig(S)
    return eigenvalues.real, eigenvectors.real
```

**Step g: Build Transformation Matrix P**
```python
def step_g_build_p_matrix(eigenvectors: np.ndarray, eigenvalues: np.ndarray, k: int = 3) -> np.ndarray:
    """Build transformation matrix from top k eigenvectors"""
    # Sort by eigenvalue (descending)
    idx = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, idx]

    # Take top k
    P = sorted_eigenvectors[:, :k]
    return P
```

**Step h: Transpose P**
```python
def step_h_transpose_p(P: np.ndarray) -> np.ndarray:
    """Compute transpose of P"""
    P_T = P.T
    return P_T
```

**Step i: Transform Vectors**
```python
def step_i_transform_vectors(vectors: np.ndarray, P_T: np.ndarray, mean: np.ndarray) -> np.ndarray:
    """Transform vectors to new coordinate system"""
    centered = vectors - mean
    transformed = (P_T @ centered.T).T
    return transformed
```

**Step j: K-Means Clustering**
```python
def step_j_kmeans(vectors_3d: np.ndarray, k: int = 3, seed: int = 42) -> np.ndarray:
    """K-means clustering"""
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(vectors_3d)
    return labels
```

**Step k: Visualization**
```python
def step_k_visualize(vectors_3d: np.ndarray, labels: np.ndarray, title: str):
    """Visualize 3D clusters"""
    from visualization import plot_3d_clusters
    sentence_ids = np.arange(len(vectors_3d))
    plot_3d_clusters(vectors_3d, labels, title, sentence_ids=sentence_ids)
```

#### 2.3.2: Main Pipeline Function
```python
def manual_pca_pipeline(vectors: np.ndarray) -> dict:
    """Execute manual PCA pipeline with timing"""
    from utils import Timer, save_vectors, MANUAL_PCA_FILE

    print("=" * 60)
    print("TASK 3: Manual PCA Implementation")
    print("=" * 60)

    results = {}

    with Timer("Step a: Calculate mean"):
        mean = step_a_calculate_mean(vectors)
        results['mean'] = mean

    with Timer("Step b: Center data"):
        centered = step_b_center_data(vectors, mean)
        results['centered'] = centered

    # ... continue for all steps ...

    with Timer("Step k: Visualize"):
        step_k_visualize(vectors_3d, labels, "Manual PCA + K-Means Clustering")

    # Save results
    save_vectors(vectors_3d, MANUAL_PCA_FILE)
    print(f"\n✓ Transformed vectors saved to {MANUAL_PCA_FILE}")

    return results
```

**Testing**:
- Verify eigenvalues are sorted
- Verify output shape (100, 3)
- Check covariance matrix is symmetric
- Verify visualization displays

**Line Count**: ~200 lines (may need split)

---

### Task 2.4: Implement task4_sklearn_pca.py
**Priority**: Medium
**Estimated Time**: 30 minutes
**Dependencies**: Task 1.1, Task 1.2

**Functions to Implement**:

```python
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

def apply_pca(vectors: np.ndarray, n_components: int = 3) -> tuple:
    """Apply sklearn PCA"""
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(vectors)
    return transformed, pca

def apply_kmeans(vectors: np.ndarray, k: int = 3, seed: int = 42) -> np.ndarray:
    """Apply K-means clustering"""
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(vectors)
    return labels

def sklearn_pca_pipeline(vectors: np.ndarray) -> dict:
    """Execute sklearn PCA pipeline with timing"""
    from utils import Timer, save_vectors, SKLEARN_PCA_FILE
    from visualization import plot_3d_clusters

    print("=" * 60)
    print("TASK 4: sklearn PCA Implementation")
    print("=" * 60)

    results = {}

    with Timer("Apply PCA"):
        vectors_3d, pca = apply_pca(vectors)
        results['vectors_3d'] = vectors_3d
        results['pca'] = pca

    print(f"✓ Explained variance ratio: {pca.explained_variance_ratio_}")
    print(f"✓ Total variance explained: {pca.explained_variance_ratio_.sum():.4f}")

    with Timer("Apply K-means"):
        labels = apply_kmeans(vectors_3d)
        results['labels'] = labels

    with Timer("Visualize"):
        sentence_ids = np.arange(len(vectors_3d))
        plot_3d_clusters(vectors_3d, labels, "sklearn PCA + K-Means Clustering",
                        sentence_ids=sentence_ids)

    save_vectors(vectors_3d, SKLEARN_PCA_FILE)
    print(f"\n✓ Transformed vectors saved to {SKLEARN_PCA_FILE}")

    return results
```

**Testing**:
- Verify PCA output shape
- Check explained variance
- Verify visualization

**Line Count**: ~100 lines

---

### Task 2.5: Implement task5_tsne.py
**Priority**: Medium
**Estimated Time**: 30 minutes
**Dependencies**: Task 1.1, Task 1.2

**Functions to Implement**:

```python
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import numpy as np

def apply_tsne(vectors: np.ndarray, n_components: int = 3,
               perplexity: int = 30, seed: int = 42) -> np.ndarray:
    """Apply t-SNE dimensionality reduction"""
    tsne = TSNE(n_components=n_components, perplexity=perplexity,
                random_state=seed, n_iter=1000)
    transformed = tsne.fit_transform(vectors)
    return transformed

def apply_kmeans(vectors: np.ndarray, k: int = 3, seed: int = 42) -> np.ndarray:
    """Apply K-means clustering"""
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(vectors)
    return labels

def tsne_pipeline(vectors: np.ndarray) -> dict:
    """Execute t-SNE pipeline with timing"""
    from utils import Timer, save_vectors, TSNE_FILE
    from visualization import plot_3d_clusters

    print("=" * 60)
    print("TASK 5: t-SNE Implementation")
    print("=" * 60)

    results = {}

    with Timer("Apply t-SNE"):
        vectors_3d = apply_tsne(vectors)
        results['vectors_3d'] = vectors_3d

    with Timer("Apply K-means"):
        labels = apply_kmeans(vectors_3d)
        results['labels'] = labels

    with Timer("Visualize"):
        sentence_ids = np.arange(len(vectors_3d))
        plot_3d_clusters(vectors_3d, labels, "t-SNE + K-Means Clustering",
                        sentence_ids=sentence_ids)

    save_vectors(vectors_3d, TSNE_FILE)
    print(f"\n✓ Transformed vectors saved to {TSNE_FILE}")

    return results
```

**Testing**:
- Verify t-SNE output shape
- Verify clustering works
- Verify visualization

**Line Count**: ~100 lines

---

## Phase 3: Integration

### Task 3.1: Implement main.py
**Priority**: High
**Estimated Time**: 30 minutes
**Dependencies**: All task implementations

**Implementation**:

```python
#!/usr/bin/env python3
"""
Main orchestration program for PCA and t-SNE analysis
"""

import numpy as np
from utils import load_sentences, load_vectors

def main():
    """Main execution pipeline"""
    print("\n" + "=" * 60)
    print("PCA AND t-SNE TEXT VECTORIZATION SYSTEM")
    print("=" * 60)

    # Task 1: Generate sentences
    print("\n\n")
    import task1_generate
    sentences = task1_generate.main()

    # Task 2: Vectorize
    print("\n\n")
    import task2_vectorize
    vectors = task2_vectorize.main()

    # Task 3: Manual PCA
    print("\n\n")
    import task3_manual_pca
    manual_results = task3_manual_pca.manual_pca_pipeline(vectors)

    # Task 4: sklearn PCA
    print("\n\n")
    import task4_sklearn_pca
    sklearn_results = task4_sklearn_pca.sklearn_pca_pipeline(vectors)

    # Task 5: t-SNE
    print("\n\n")
    import task5_tsne
    tsne_results = task5_tsne.tsne_pipeline(vectors)

    # Summary
    print("\n\n")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Generated {len(sentences)} sentences")
    print(f"✓ Vectorized to {vectors.shape[1]} dimensions")
    print(f"✓ Reduced to 3D using:")
    print(f"  - Manual PCA (NumPy only)")
    print(f"  - sklearn PCA")
    print(f"  - t-SNE")
    print(f"✓ Applied K-means clustering (K=3)")
    print(f"✓ Generated 3 visualizations")
    print("\nAll tasks completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

**Testing**:
- Run full pipeline: `python main.py`
- Verify all tasks execute
- Verify all files created
- Verify all visualizations display

**Line Count**: ~80 lines

---

## Phase 4: Testing and Validation

### Task 4.1: Validation Tests
**Priority**: Medium
**Estimated Time**: 30 minutes

**Tests to Perform**:

1. **Sentence Count**: Verify 100 sentences
2. **Vector Normalization**: Check ||v|| = 1 for all vectors
3. **Output Shapes**:
   - Normalized vectors: (100, 384)
   - All 3D outputs: (100, 3)
4. **Eigenvalue Ordering**: Descending order
5. **Cluster Counts**: Sum to 100
6. **File Existence**: All output files created

**Create**: `test_validation.py`

---

### Task 4.2: Integration Test
**Priority**: Medium
**Estimated Time**: 15 minutes

**Test**:
- Run `python main.py` in clean environment
- Verify no errors
- Verify all outputs

---

## Phase 5: Documentation

### Task 5.1: Update README.md
**Priority**: Low
**Estimated Time**: 20 minutes

**Sections**:
- Project description
- Setup instructions
- Usage
- File structure
- Requirements
- Example output

---

### Task 5.2: Add Docstrings
**Priority**: Low
**Estimated Time**: 30 minutes

- Add docstrings to all functions
- Add module docstrings
- Add type hints

---

## Summary Checklist

### Critical Path
- [ ] Task 0.1: Create virtual environment
- [ ] Task 0.2: Create requirements.txt
- [ ] Task 0.3: Create project structure
- [ ] Task 1.1: Implement utils.py
- [ ] Task 1.2: Implement visualization.py
- [ ] Task 2.1: Implement task1_generate.py
- [ ] Task 2.2: Implement task2_vectorize.py
- [ ] Task 2.3: Implement task3_manual_pca.py
- [ ] Task 2.4: Implement task4_sklearn_pca.py
- [ ] Task 2.5: Implement task5_tsne.py
- [ ] Task 3.1: Implement main.py
- [ ] Task 4.1: Validation tests
- [ ] Task 4.2: Integration test

### Optional
- [ ] Task 5.1: Update README.md
- [ ] Task 5.2: Add docstrings

---

## Time Estimates

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 0: Setup | 3 | 20 min |
| Phase 1: Utilities | 2 | 1.25 hrs |
| Phase 2: Tasks | 5 | 6.5 hrs |
| Phase 3: Integration | 1 | 0.5 hrs |
| Phase 4: Testing | 2 | 0.75 hrs |
| Phase 5: Documentation | 2 | 0.83 hrs |
| **Total** | **15** | **~10 hours** |

---

## Risk Mitigation

**High-Risk Tasks**:
1. Task 2.3 (Manual PCA) - Most complex
   - Mitigation: Break into smallest sub-tasks
   - Test each step individually

2. Task 2.5 (t-SNE) - May be slow
   - Mitigation: Start with small perplexity
   - Monitor convergence

**Dependencies**:
- All task implementations depend on Phase 1
- Integration depends on all tasks
- Testing depends on integration

---

## Success Criteria

**Must Have**:
- ✅ All 100 sentences generated
- ✅ All vectors normalized
- ✅ Manual PCA completes successfully
- ✅ All three visualizations display
- ✅ All timing measurements shown
- ✅ No file exceeds 200 lines

**Nice to Have**:
- ✅ Clean, readable output
- ✅ Comprehensive documentation
- ✅ Validation tests pass
- ✅ Code is well-commented
