# Implementation Planning Document
## Semantic Sentence Clustering System

### Project Timeline: 3-5 Days

---

## Phase 1: Environment Setup (Day 1)

### 1.1 WSL Environment Preparation
- [ ] Verify Python 3.8+ installation in WSL
- [ ] Create project directory structure
- [ ] Set up virtual environment
- [ ] Install base dependencies

**Commands:**
```bash
# Check Python version
python3 --version

# Create project structure
mkdir -p semantic-clustering/{agents,output,tests}
cd semantic-clustering

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 1.2 Dependency Installation
- [ ] Create requirements.txt
- [ ] Install Python packages
- [ ] Verify sentence-transformers installation
- [ ] Download sentence-transformer model

**Dependencies:**
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

### 1.3 Security Setup
- [ ] Verify API key file at `/home/ro/api_key`
- [ ] Create .gitignore file
- [ ] Set up environment variable reading
- [ ] Test API key loading without exposure

**.gitignore template:**
```
venv/
__pycache__/
*.pyc
.env
/home/ro/api_key
*.log
output/*.png
output/*.csv
.DS_Store
```

### 1.4 Claude Code CLI Setup
- [ ] Verify Claude Code CLI installation
- [ ] Test CLI connectivity
- [ ] Prepare agent definition files
- [ ] Plan agent creation sequence

---

## Phase 2: Agent Development (Day 2)

### 2.1 Agent Creation Order
1. **create_sentences** - Foundation for data generation
2. **convert2vector** - Core vectorization (test model download)
3. **normalize_vector** - Simple transformation
4. **divide2clusters** - Complex clustering logic

### 2.2 Agent Creation Process (Per Agent)
- [ ] Start Claude Code CLI: `claude-code`
- [ ] Run `/agents` command
- [ ] Input agent configuration from Claude.md
- [ ] Test agent with sample data
- [ ] Document agent ID/reference
- [ ] Verify output format

### 2.3 Local Function Evaluation
**Decision: Agent vs. Local Function**

For `normalize_vector`:
- **Option A:** AI Agent (flexibility, consistency with other agents)
- **Option B:** Local Python function (efficiency, no API calls)

**Recommendation:** Start with Agent, optionally convert to local function if:
- Token usage becomes concern
- Performance bottleneck identified
- Simple normalization logic doesn't require AI

### 2.4 Agent Testing Strategy
Create test script: `tests/test_agents.py`
- [ ] Test each agent independently
- [ ] Verify input/output formats
- [ ] Check error handling
- [ ] Measure performance metrics
- [ ] Validate data flow compatibility

---

## Phase 3: Main Program Development (Day 3-4)

### 3.1 Project Structure
```
semantic-clustering/
├── main.py                  # Main orchestrator (<300 lines)
├── config.py               # Configuration and API key loading
├── utils.py                # Helper functions
├── visualize.py            # Plotting functions
├── agents/
│   ├── __init__.py
│   └── agent_client.py     # Agent communication wrapper
├── output/
│   ├── cluster_plot.png
│   ├── test_plot.png
│   ├── cluster_results.csv
│   └── test_results.csv
├── tests/
│   ├── test_agents.py
│   └── test_main.py
├── requirements.txt
├── .gitignore
├── README.md
└── docs/
    ├── PRD.md
    ├── Claude.md
    ├── Planning.md
    └── tasks.md
```

### 3.2 Module Breakdown

#### config.py (20 lines)
```python
# Load API key securely
# Define constants (subjects, num_sentences, random_seed)
# Path configurations
```

#### agent_client.py (40 lines)
```python
# Wrapper for Claude API agent calls
# Error handling and retries
# Response parsing
```

#### utils.py (50 lines)
```python
# KNN classification function
# Data validation helpers
# Result formatting functions
# CSV export utilities
```

#### visualize.py (60 lines)
```python
# Cluster visualization (2D PCA/t-SNE)
# Test point overlay
# Table generation
# Color schemes and styling
```

#### main.py (130 lines max)
```python
# Cluster creation phase
# Test phase
# Result aggregation
# Main execution flow
```

### 3.3 Core Algorithms to Implement

#### KNN Classification (for test phase)
```python
def knn_classify(test_vector, centroids, k=1):
    """
    Assign test vector to nearest cluster centroid.
    
    Args:
        test_vector: normalized embedding
        centroids: cluster centers from K-means
        k: number of neighbors (default 1)
    
    Returns:
        cluster_id: assigned cluster (0, 1, or 2)
        distance: distance to nearest centroid
    """
    # Use Euclidean distance
    # Return nearest cluster
```

#### Dimensionality Reduction (for visualization)
```python
def reduce_dimensions(vectors, method='pca', n_components=2):
    """
    Reduce vectors to 2D for visualization.
    
    Options: PCA, t-SNE, UMAP
    """
```

### 3.4 Visualization Requirements

#### Cluster Plot (Creation Phase)
- **Type:** 2D scatter plot
- **Elements:**
  - 100 points (training data)
  - 3 colors (one per cluster)
  - Cluster centroids marked with X
  - Legend with cluster labels
  - Title: "Sentence Clusters (K-means, k=3)"

#### Test Plot (Test Phase)
- **Type:** 2D scatter plot overlay
- **Elements:**
  - Same as cluster plot (background)
  - 10 new test points (different markers)
  - Lines connecting test points to assigned centroids
  - Legend distinguishing training vs test
  - Title: "Test Sentence Classification (KNN)"

#### Tables
- **Cluster Table:** sentence, cluster_id, sample_sentences_per_cluster
- **Test Table:** test_sentence, true_subject, predicted_cluster, distance

---

## Phase 4: Integration and Testing (Day 4-5)

### 4.1 Integration Testing
- [ ] Test full pipeline with small data (10 sentences)
- [ ] Verify agent communication
- [ ] Check data flow between phases
- [ ] Validate output formats

### 4.2 Full System Testing
- [ ] Run cluster creation with 100 sentences
- [ ] Execute test phase with 10 sentences
- [ ] Verify visualizations generated
- [ ] Check CSV outputs
- [ ] Validate cluster quality metrics

### 4.3 Quality Assurance
- [ ] Code review (line count <300 for main.py)
- [ ] API key security audit
- [ ] Error handling verification
- [ ] Performance profiling
- [ ] Documentation review

### 4.4 Evaluation Metrics
- **Cluster Purity:** Percentage of dominant subject per cluster
- **Silhouette Score:** Cluster separation quality (-1 to 1)
- **Test Accuracy:** Correct cluster assignments for test data
- **Execution Time:** Total pipeline runtime

**Success Criteria:**
- Cluster purity > 70%
- Silhouette score > 0.3
- Test accuracy > 60%
- Execution time < 5 minutes

---

## Phase 5: Documentation and Delivery (Day 5)

### 5.1 Code Documentation
- [ ] Add docstrings to all functions
- [ ] Include type hints
- [ ] Comment complex logic
- [ ] Create usage examples

### 5.2 README Creation
- [ ] Installation instructions
- [ ] Usage guide
- [ ] Example outputs
- [ ] Troubleshooting section

### 5.3 Final Deliverables
- [ ] All documentation (PRD, Claude, Planning, tasks)
- [ ] Complete source code
- [ ] requirements.txt
- [ ] .gitignore
- [ ] Sample outputs
- [ ] Test results

---

## Risk Mitigation Strategies

### Risk 1: Agent Communication Failures
**Mitigation:**
- Implement retry logic (3 attempts)
- Add exponential backoff
- Detailed error logging
- Graceful degradation

### Risk 2: Poor Cluster Quality
**Mitigation:**
- Use high-quality sentence-transformer model
- Increase diversity in sentence generation
- Test different random seeds
- Validate with silhouette score

### Risk 3: API Rate Limits
**Mitigation:**
- Minimize API calls (local normalization)
- Implement rate limit detection
- Add delay between requests
- Use batch processing

### Risk 4: Memory Issues
**Mitigation:**
- Use float32 instead of float64
- Process in batches if needed
- Clear unused variables
- Monitor memory usage

### Risk 5: Model Download Failures in WSL
**Mitigation:**
- Pre-download models during setup
- Check internet connectivity
- Use model cache directory
- Provide manual download instructions

---

## Technical Decisions Log

### Decision 1: Sentence-Transformer Model
**Options:**
1. `all-MiniLM-L6-v2` (384 dim, 90MB, fast)
2. `all-mpnet-base-v2` (768 dim, 420MB, higher quality)

**Choice:** Start with MiniLM for speed, upgrade if quality insufficient

### Decision 2: Dimensionality Reduction for Visualization
**Options:**
1. PCA (deterministic, fast)
2. t-SNE (better separation, slower)
3. UMAP (best quality, additional dependency)

**Choice:** PCA with option for t-SNE if visualization unclear

### Decision 3: Normalization Implementation
**Options:**
1. AI Agent (consistent with architecture)
2. Local Python function (efficient)

**Choice:** Local function, wrapped to match agent interface

### Decision 4: Random Seed Management
**Strategy:**
- Global seed in config.py
- Apply to: sentence generation, K-means, train/test split
- Document seed for reproducibility

---

## Development Best Practices

### Code Style
- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Meaningful variable names

### Error Handling
```python
try:
    result = call_agent(...)
except APIError as e:
    logger.error(f"Agent call failed: {e}")
    # Retry or fail gracefully
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Testing
- Unit tests for utility functions
- Integration tests for agent communication
- End-to-end tests for full pipeline

---

## Next Steps After Completion

1. **Performance Optimization:**
   - Profile bottlenecks
   - Optimize vector operations
   - Cache model loading

2. **Feature Enhancements:**
   - Support variable cluster counts
   - Add more subjects
   - Interactive visualizations
   - Web interface

3. **Deployment:**
   - Containerization (Docker)
   - CI/CD pipeline
   - Cloud deployment (optional)

4. **Monitoring:**
   - Log aggregation
   - Performance metrics
   - Error tracking
   - Usage analytics

---

## Resources and References

### Documentation
- [Sentence Transformers](https://www.sbert.net/)
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Code CLI](https://docs.claude.com/claude-code)

### Tutorials
- Semantic similarity with sentence-transformers
- K-means clustering best practices
- Visualization with matplotlib

### Tools
- WSL documentation
- Python virtual environments
- Git best practices