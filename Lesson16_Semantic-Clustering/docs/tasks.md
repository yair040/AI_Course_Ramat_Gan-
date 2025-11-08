# Tasks Breakdown and Checklist
## Semantic Sentence Clustering System

---

## 🚀 Sprint 1: Environment and Setup (Day 1)

### Task 1.1: WSL Environment Verification ⏱️ 30 min
- [ ] Verify WSL is running Ubuntu 20.04+ or Debian
- [ ] Check Python version: `python3 --version` (must be 3.8+)
- [ ] Update system packages: `sudo apt update && sudo apt upgrade`
- [ ] Install python3-venv if missing: `sudo apt install python3-venv`

**Acceptance Criteria:**
- Python 3.8+ available in WSL
- Can create virtual environments

---

### Task 1.2: Project Structure Creation ⏱️ 15 min
- [ ] Create main project directory: `semantic-clustering`
- [ ] Create subdirectories: `agents/`, `output/`, `tests/`, `docs/`
- [ ] Initialize git repository: `git init`
- [ ] Create initial README.md

**Commands:**
```bash
mkdir -p semantic-clustering/{agents,output,tests,docs}
cd semantic-clustering
git init
```

**Acceptance Criteria:**
- Directory structure matches Planning.md specification
- Git initialized

---

### Task 1.3: Virtual Environment Setup ⏱️ 15 min
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate environment: `source venv/bin/activate`
- [ ] Upgrade pip: `pip install --upgrade pip`
- [ ] Verify activation: `which python` (should show venv path)

**Acceptance Criteria:**
- Virtual environment created and activated
- Pip upgraded to latest version

---

### Task 1.4: Dependencies Installation ⏱️ 30 min
- [ ] Create `requirements.txt` with all dependencies
- [ ] Install packages: `pip install -r requirements.txt`
- [ ] Verify installations: `pip list`
- [ ] Test sentence-transformers import

**requirements.txt:**
```txt
anthropic>=0.50.0
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
pandas>=2.0.0
python-dotenv>=1.0.0
```

**Test command:**
```python
python3 -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

**Acceptance Criteria:**
- All packages installed without errors
- Can import all required libraries

---

### Task 1.5: Model Pre-download ⏱️ 20 min
- [ ] Download sentence-transformer model
- [ ] Verify model cached locally
- [ ] Test model loading speed

**Script:**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"Model loaded: {model}")
```

**Acceptance Criteria:**
- Model downloads successfully (~90MB)
- Subsequent loads are fast (<1 sec)

---

### Task 1.6: API Key Security Setup ⏱️ 20 min
- [ ] Verify API key exists: `cat /home/ro/api_key`
- [ ] Create `.gitignore` with API key path
- [ ] Create `config.py` with secure key reading
- [ ] Test key loading without exposure

**config.py skeleton:**
```python
def load_api_key():
    with open('/home/ro/api_key', 'r') as f:
        return f.read().strip()

# Never print or log the key
API_KEY = load_api_key()
```

**.gitignore:**
```
venv/
__pycache__/
*.pyc
.env
/home/ro/api_key
*.log
output/*
!output/.gitkeep
.DS_Store
```

**Acceptance Criteria:**
- API key loads successfully
- Key never appears in code or logs
- `.gitignore` prevents accidental commit

---

### Task 1.7: Claude Code CLI Verification ⏱️ 15 min
- [ ] Check Claude Code CLI installed: `claude-code --version`
- [ ] Test CLI launch: `claude-code`
- [ ] Verify `/agents` command available
- [ ] Exit CLI: `exit` or Ctrl+D

**Acceptance Criteria:**
- Claude Code CLI functional
- Can access agent creation commands

---

## 🤖 Sprint 2: Agent Development (Day 2)

### Task 2.1: Create Agent 1 - create_sentences ⏱️ 45 min
- [ ] Start Claude Code CLI: `claude-code`
- [ ] Run `/agents` command
- [ ] Input configuration from Claude.md
- [ ] Test with sample: 5 sentences, 3 subjects
- [ ] Document agent identifier
- [ ] Save agent reference for main.py

**Test input:**
```json
{
  "num_sentences": 5,
  "subjects": ["sport", "work", "food"]
}
```

**Expected output:**
```json
{
  "sentences": [
    "The basketball game was intense",
    "She completed the budget report",
    "Homemade pizza smells amazing",
    "Soccer practice starts at 6pm",
    "Coffee breaks improve productivity"
  ]
}
```

**Acceptance Criteria:**
- Agent created successfully
- Returns 5 varied sentences
- Each sentence clearly about one subject
- JSON output format correct

---

### Task 2.2: Create Agent 2 - convert2vector ⏱️ 45 min
- [ ] Create agent via Claude Code CLI `/agents`
- [ ] Input configuration from Claude.md
- [ ] Test with 3-5 sample sentences
- [ ] Verify output shape: (n_sentences, 384)
- [ ] Check vector value ranges
- [ ] Measure processing time

**Test input:**
```json
{
  "sentences": [
    "The soccer match was exciting",
    "She finished the project report",
    "Pizza is delicious with extra cheese"
  ]
}
```

**Expected output:**
```json
{
  "vectors": [[0.1, 0.2, ...], [0.3, 0.1, ...], [0.2, 0.4, ...]],
  "shape": [3, 384],
  "model_used": "all-MiniLM-L6-v2"
}
```

**Acceptance Criteria:**
- Agent returns embeddings
- Shape is (n_sentences, 384)
- Vectors are float arrays
- Processing completes in <5 seconds

---

### Task 2.3: Create Agent 3 - normalize_vector ⏱️ 30 min
- [ ] Create agent via Claude Code CLI `/agents`
- [ ] Input configuration from Claude.md
- [ ] Test with sample vectors
- [ ] Verify output range [0, 1]
- [ ] Check shape preservation

**Alternative:** Create local function
- [ ] Implement `normalize_vectors()` in `utils.py`
- [ ] Create agent wrapper for consistency
- [ ] Test both implementations
- [ ] Decide based on performance

**Test input:**
```json
{
  "vectors": [[0.5, 1.0, 0.2], [0.8, 0.3, 0.9], [0.1, 0.7, 0.4]]
}
```

**Expected output:**
```json
{
  "normalized_vectors": [[0.57, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.57, 0.4]],
  "shape": [3, 3]
}
```

**Acceptance Criteria:**
- All values in [0, 1] range
- Shape unchanged
- Min value per dimension = 0
- Max value per dimension = 1

---

### Task 2.4: Create Agent 4 - divide2clusters ⏱️ 45 min
- [ ] Create agent via Claude Code CLI `/agents`
- [ ] Input configuration from Claude.md
- [ ] Test with 20-30 sample vectors
- [ ] Verify 3 clusters created
- [ ] Check centroid dimensions
- [ ] Validate inertia calculation

**Test input:**
```json
{
  "normalized_vectors": [[0.5, 0.8], [0.9, 0.1], [0.2, 0.9], ...]
}
```

**Expected output:**
```json
{
  "labels": [0, 1, 2, 0, 1, ...],
  "centroids": [[0.55, 0.75], [0.85, 0.15], [0.25, 0.88]],
  "inertia": 12.34,
  "n_clusters": 3
}
```

**Acceptance Criteria:**
- Exactly 3 clusters (labels: 0, 1, 2)
- Centroids shape: (3, n_features)
- Inertia is positive float
- Reproducible with same seed

---

### Task 2.5: Create Agent Test Suite ⏱️ 1 hour
- [ ] Create `tests/test_agents.py`
- [ ] Write test for each agent
- [ ] Test error handling
- [ ] Test edge cases (empty input, large input)
- [ ] Document test results

**Test cases:**
1. Empty input handling
2. Large batch processing (100 sentences)
3. Invalid input types
4. API timeout scenarios
5. Malformed responses

**Acceptance Criteria:**
- All agents pass unit tests
- Error handling works correctly
- Edge cases handled gracefully

---

## 💻 Sprint 3: Main Program Development (Day 3)

### Task 3.1: Create config.py ⏱️ 30 min
- [ ] Implement `load_api_key()` function
- [ ] Define constants (SUBJECTS, NUM_TRAIN, NUM_TEST, RANDOM_SEED)
- [ ] Set up paths (OUTPUT_DIR, MODEL_NAME)
- [ ] Add configuration validation

**config.py:**
```python
import os

def load_api_key():
    """Securely load API key from file."""
    key_path = '/home/ro/api_key'
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"API key not found at {key_path}")
    with open(key_path, 'r') as f:
        return f.read().strip()

# Configuration
API_KEY = load_api_key()
SUBJECTS = ["sport", "work", "food"]
NUM_TRAIN_SENTENCES = 100
NUM_TEST_SENTENCES = 10
N_CLUSTERS = 3
RANDOM_SEED = 42
MODEL_NAME = 'all-MiniLM-L6-v2'
OUTPUT_DIR = 'output'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
```

**Acceptance Criteria:**
- API key loads without errors
- Constants defined and documented
- Output directory created

---

### Task 3.2: Create agent_client.py ⏱️ 1 hour
- [ ] Implement `AgentClient` class
- [ ] Add methods for each agent call
- [ ] Implement retry logic
- [ ] Add error handling and logging
- [ ] Test with actual agents

**agent_client.py structure:**
```python
import anthropic
import json
import time

class AgentClient:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def create_sentences(self, num_sentences, subjects):
        """Call create_sentences agent."""
        pass
    
    def convert2vector(self, sentences):
        """Call convert2vector agent."""
        pass
    
    def normalize_vector(self, vectors):
        """Call normalize_vector agent or local function."""
        pass
    
    def divide2clusters(self, normalized_vectors):
        """Call divide2clusters agent."""
        pass
    
    def _call_agent_with_retry(self, agent_name, input_data, max_retries=3):
        """Generic agent call with retry logic."""
        pass
```

**Acceptance Criteria:**
- All agent methods implemented
- Retry logic works (3 attempts)
- Errors logged appropriately
- Responses parsed correctly

---

### Task 3.3: Create utils.py ⏱️ 1 hour
- [ ] Implement `knn_classify()` function
- [ ] Add `reduce_dimensions()` for PCA
- [ ] Create `calculate_cluster_purity()` metric
- [ ] Add `format_results_table()` helper
- [ ] Write unit tests

**Key functions:**
```python
def knn_classify(test_vector, centroids, k=1):
    """Assign test vector to nearest cluster."""
    pass

def reduce_dimensions(vectors, method='pca', n_components=2):
    """Reduce vectors to 2D for visualization."""
    pass

def calculate_cluster_purity(sentences, labels, subjects):
    """Calculate cluster purity score."""
    pass

def format_results_table(data):
    """Format results as pandas DataFrame."""
    pass
```

**Acceptance Criteria:**
- KNN correctly assigns vectors
- PCA reduces dimensions properly
- Purity calculation accurate
- Table formatting clean

---

### Task 3.4: Create visualize.py ⏱️ 1.5 hours
- [ ] Implement `plot_clusters()` function
- [ ] Add `plot_test_results()` function
- [ ] Create `save_results_table()` function
- [ ] Configure color schemes
- [ ] Add labels and legends

**Visualization requirements:**
```python
def plot_clusters(vectors_2d, labels, centroids_2d, output_path):
    """
    Create scatter plot of clusters.
    - 3 colors for clusters
    - Centroids marked with X
    - Legend and title
    """
    pass

def plot_test_results(train_vectors_2d, train_labels, 
                     test_vectors_2d, test_labels, output_path):
    """
    Overlay test points on cluster plot.
    - Different marker for test points
    - Lines to assigned centroids
    """
    pass

def save_results_table(data, output_path):
    """Save results as CSV and display sample."""
    pass
```

**Acceptance Criteria:**
- Plots are clear and labeled
- Colors distinguish clusters
- Test points visible on overlay
- Tables saved correctly

---

### Task 3.5: Create main.py - Phase 1 (Cluster Creation) ⏱️ 2 hours
- [ ] Import all modules
- [ ] Initialize AgentClient
- [ ] Implement cluster creation workflow
- [ ] Add logging and progress tracking
- [ ] Handle errors gracefully

**Workflow:**
1. Call create_sentences(100, subjects)
2. Call convert2vector(sentences)
3. Call normalize_vector(vectors)
4. Call divide2clusters(normalized_vectors)
5. Reduce dimensions for visualization
6. Plot clusters
7. Save results table

**Acceptance Criteria:**
- Generates 100 sentences
- Creates 3 clusters
- Saves visualization
- Exports results CSV
- Completes without errors

---

### Task 3.6: Create main.py - Phase 2 (Test Classification) ⏱️ 1.5 hours
- [ ] Implement test workflow
- [ ] Use stored centroids from training
- [ ] Apply KNN classification
- [ ] Generate overlay visualization
- [ ] Create test results table

**Workflow:**
1. Call create_sentences(10, subjects)
2. Call convert2vector(test_sentences)
3. Call normalize_vector(test_vectors)
4. Apply KNN to assign clusters
5. Reduce dimensions for visualization
6. Plot test overlay
7. Save test results

**Acceptance Criteria:**
- Classifies 10 test sentences
- Uses training centroids
- Visualization shows overlay
- Results table complete

---

### Task 3.7: Code Optimization and Line Count ⏱️ 1 hour
- [ ] Count lines in main.py: `wc -l main.py`
- [ ] Refactor if >300 lines
- [ ] Move helper functions to utils.py
- [ ] Optimize imports
- [ ] Add docstrings

**Optimization strategies:**
- Extract repeated code to functions
- Use list comprehensions
- Combine similar operations
- Remove unnecessary comments

**Acceptance Criteria:**
- main.py <300 lines
- Code is readable and maintainable
- All functions documented

---

## 🧪 Sprint 4: Testing and Integration (Day 4)

### Task 4.1: Unit Testing ⏱️ 2 hours
- [ ] Test config.py functions
- [ ] Test utils.py functions
- [ ] Test visualize.py functions
- [ ] Test agent_client.py methods
- [ ] Achieve >80% code coverage

**Test framework:**
```python
import unittest
from config import load_api_key
from utils import knn_classify, reduce_dimensions

class TestUtils(unittest.TestCase):
    def test_knn_classify(self):
        # Test KNN logic
        pass
    
    def test_reduce_dimensions(self):
        # Test PCA reduction
        pass
```

**Acceptance Criteria:**
- All unit tests pass
- Edge cases covered
- No breaking changes

---

### Task 4.2: Integration Testing ⏱️ 2 hours
- [ ] Test agent communication pipeline
- [ ] Test data flow between phases
- [ ] Verify file outputs created
- [ ] Check visualization quality
- [ ] Validate CSV formats

**Integration tests:**
1. End-to-end small batch (10 sentences)
2. Full pipeline (100 sentences)
3. Error recovery scenarios
4. Output file verification

**Acceptance Criteria:**
- Full pipeline completes successfully
- All outputs generated correctly
- No data loss between phases

---

### Task 4.3: Performance Testing ⏱️ 1 hour
- [ ] Measure execution time
- [ ] Profile memory usage
- [ ] Identify bottlenecks
- [ ] Optimize slow operations
- [ ] Document performance metrics

**Metrics to track:**
- Total execution time (<5 minutes target)
- Time per phase
- Memory peak usage
- API call latency

**Acceptance Criteria:**
- Execution time acceptable
- Memory usage reasonable
- Bottlenecks identified

---

### Task 4.4: Quality Metrics Calculation ⏱️ 1 hour
- [ ] Calculate cluster purity
- [ ] Calculate silhouette score
- [ ] Measure test accuracy
- [ ] Generate evaluation report
- [ ] Compare against success criteria

**Evaluation metrics:**
```python
def evaluate_clustering(sentences, labels, true_subjects):
    """
    Calculate:
    - Cluster purity (>70% target)
    - Silhouette score (>0.3 target)
    - Test accuracy (>60% target)
    """
    pass
```

**Acceptance Criteria:**
- Cluster purity >70%
- Silhouette score >0.3
- Test accuracy >60%

---

### Task 4.5: Security Audit ⏱️ 30 min
- [ ] Search codebase for API key exposure
- [ ] Verify .gitignore coverage
- [ ] Check logs for sensitive data
- [ ] Review error messages
- [ ] Test with dummy API key

**Security checklist:**
- [ ] No API key in any .py file
- [ ] No API key in git history
- [ ] .gitignore includes key path
- [ ] Logs don't contain key
- [ ] Error messages safe

**Acceptance Criteria:**
- No security vulnerabilities found
- API key fully protected

---

## 📚 Sprint 5: Documentation and Delivery (Day 5)

### Task 5.1: Code Documentation ⏱️ 2 hours
- [ ] Add docstrings to all functions
- [ ] Add type hints everywhere
- [ ] Comment complex algorithms
- [ ] Document function parameters
- [ ] Add usage examples

**Docstring format:**
```python
def knn_classify(test_vector: np.ndarray, 
                 centroids: np.ndarray, 
                 k: int = 1) -> tuple:
    """
    Classify test vector using K-Nearest Neighbors.
    
    Args:
        test_vector: Normalized embedding vector
        centroids: Cluster centers from K-means
        k: Number of neighbors (default: 1)
    
    Returns:
        tuple: (cluster_id, distance)
    
    Example:
        >>> cluster, dist = knn_classify(vec, centroids)
        >>> print(f"Assigned to cluster {cluster}")
    """
```

**Acceptance Criteria:**
- All functions documented
- Type hints complete
- Examples provided

---

### Task 5.2: Create README.md ⏱️ 1.5 hours
- [ ] Write project overview
- [ ] Add installation instructions
- [ ] Document usage steps
- [ ] Include example outputs
- [ ] Add troubleshooting section

**README structure:**
1. Project Description
2. Features
3. Requirements
4. Installation
5. Usage
6. Output Examples
7. Configuration
8. Troubleshooting
9. License

**Acceptance Criteria:**
- README is comprehensive
- Instructions are clear
- Examples are helpful

---

### Task 5.3: Create Example Outputs ⏱️ 30 min
- [ ] Run full pipeline
- [ ] Save all visualizations
- [ ] Export sample CSV data
- [ ] Screenshot key results
- [ ] Add to docs/ folder

**Output samples:**
- cluster_plot.png
- test_plot.png
- cluster_results.csv (first 10 rows)
- test_results.csv
- evaluation_metrics.txt

**Acceptance Criteria:**
- All output types represented
- Images are high quality
- Data samples informative

---

### Task 5.4: Final Testing ⏱️ 1 hour
- [ ] Fresh installation test (new venv)
- [ ] Follow README instructions exactly
- [ ] Verify all outputs match expectations
- [ ] Test with different random seeds
- [ ] Confirm reproducibility

**Fresh install test:**
```bash
# New terminal
python3 -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
python main.py
# Verify outputs
```

**Acceptance Criteria:**
- Installation works from scratch
- README instructions accurate
- Results reproducible

---

### Task 5.5: Create Presentation Materials ⏱️ 1 hour
- [ ] Create project summary slide deck
- [ ] Prepare demo script
- [ ] Document key findings
- [ ] Highlight metrics achieved
- [ ] Note future improvements

**Presentation outline:**
1. Problem statement
2. Solution architecture
3. Agent design
4. Results and metrics
5. Demo walkthrough
6. Lessons learned
7. Next steps

**Acceptance Criteria:**
- Presentation is professional
- Demo script tested
- Metrics clearly presented

---

## 📊 Final Checklist

### Deliverables Verification
- [ ] PRD.md - Complete and detailed
- [ ] Claude.md - All 4 agents defined
- [ ] Planning.md - Implementation plan documented
- [ ] tasks.md - This file, all tasks checked
- [ ] main.py - <300 lines, fully functional
- [ ] config.py - Secure API key loading
- [ ] agent_client.py - Agent communication wrapper
- [ ] utils.py - Helper functions
- [ ] visualize.py - Plotting functions
- [ ] requirements.txt - All dependencies listed
- [ ] .gitignore - Protects sensitive files
- [ ] README.md - Comprehensive guide
- [ ] tests/ - Unit and integration tests
- [ ] output/ - Sample results
- [ ] docs/ - All documentation

### Quality Metrics
- [ ] Cluster purity >70%
- [ ] Silhouette score >0.3
- [ ] Test accuracy >60%
- [ ] Execution time <5 minutes
- [ ] main.py <300 lines
- [ ] No API key exposure
- [ ] All tests passing
- [ ] Code documented

### Acceptance Criteria
- [ ] System generates 100 training sentences
- [ ] Creates 3 semantic clusters
- [ ] Classifies 10 test sentences
- [ ] Produces visualizations
- [ ] Exports results tables
- [ ] Runs end-to-end successfully
- [ ] Reproducible results
- [ ] Secure API key handling

---

## 🎯 Success Definition

Project is complete when:
1. All tasks checked off
2. All deliverables present
3. Quality metrics met
4. Security audit passed
5. Documentation comprehensive
6. Fresh installation test passed
7. Demo ready to present

**Estimated Total Time:** 3-5 days (20-30 hours)

**Project Status Tracking:**
- [ ] Sprint 1 Complete (Environment Setup)
- [ ] Sprint 2 Complete (Agent Development)
- [ ] Sprint 3 Complete (Main Program)
- [ ] Sprint 4 Complete (Testing)
- [ ] Sprint 5 Complete (Documentation)
- [ ] **PROJECT COMPLETE** 🎉