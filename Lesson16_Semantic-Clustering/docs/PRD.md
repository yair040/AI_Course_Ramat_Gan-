# Product Requirements Document
## Semantic Sentence Clustering System

### 1. Project Overview

**Project Name:** Semantic Sentence Clustering System  
**Version:** 1.0  
**Date:** November 5, 2025  
**Environment:** WSL (Windows Subsystem for Linux)
**Author:** Yair Levi

### 2. Executive Summary

A Python-based AI agent orchestration system that generates sentences, converts them to semantic vectors, and clusters them by topic similarity using machine learning. The system demonstrates unsupervised learning through K-means clustering and validates results using K-Nearest Neighbors classification.

### 3. Technical Environment

**Platform:** WSL (Ubuntu/Debian recommended)  
**Language:** Python 3.8+  
**API Key Location:** `/home/ro/api_key`  
**Security Requirement:** API key must never be exposed in code or version control

### 4. System Architecture

#### 4.1 Components

The system consists of:
- **Main Orchestrator:** Python program (<300 lines) coordinating all agents
- **Four AI Agents:** Created via Claude Code CLI using `/agents` command
- **ML Pipeline:** Sentence generation → Vectorization → Normalization → Clustering

#### 4.2 Agent Specifications

##### Agent 1: create_sentences
- **Purpose:** Generate random sentences about specified topics
- **Input:**
  - `num_sentences` (int): Number of sentences to generate
  - `subjects` (list): Topics for sentence generation
- **Output:** List of sentences (strings)
- **Behavior:** Each sentence covers exactly one subject, randomly selected

##### Agent 2: convert2vector
- **Purpose:** Convert sentences to semantic vector embeddings
- **Technology:** sentence-transformers library
- **Model:** Best model for semantic similarity (recommend: `all-MiniLM-L6-v2` or `all-mpnet-base-v2`)
- **Execution:** Local computer
- **Input:** List of sentences
- **Output:** NumPy array of sentence embeddings

##### Agent 3: normalize_vector
- **Purpose:** Normalize vectors to [0, 1] range
- **Execution:** Local Python script (if token-efficient) or AI agent
- **Input:** Array of vectors
- **Output:** Array of normalized vectors (0-1 range)
- **Method:** Min-max normalization

##### Agent 4: divide2clusters
- **Purpose:** Cluster vectors using K-means algorithm
- **Algorithm:** K-means (k=3)
- **Input:** Normalized vector array
- **Output:** Cluster assignments and centroids
- **Clusters:** Fixed at 3 (matching subjects: sport, work, food)

### 5. Functional Requirements

#### 5.1 Cluster Creation Phase

**Workflow:**
1. Generate 100 sentences using `create_sentences` agent
   - Subjects: ["sport", "work", "food"]
   - Random distribution across topics
2. Convert sentences to vectors using `convert2vector` agent
3. Normalize vectors using `normalize_vector` agent
4. Cluster vectors using `divide2clusters` agent (k=3)
5. Visualize results:
   - **Diagram:** 2D/3D scatter plot of clusters
   - **Table:** Sentence text, cluster assignment, sample from each cluster

#### 5.2 Test Phase

**Workflow:**
1. Generate 10 new test sentences using `create_sentences` agent
   - Same subjects: ["sport", "work", "food"]
2. Convert to vectors using `convert2vector` agent
3. Normalize vectors using `normalize_vector` agent
4. Classify using KNN algorithm:
   - Use cluster centroids from creation phase
   - Assign each test vector to nearest cluster
5. Visualize results:
   - **Diagram:** Test points overlaid on cluster visualization
   - **Table:** Test sentence, predicted cluster, confidence/distance

### 6. Non-Functional Requirements

#### 6.1 Code Quality
- Main program: Maximum 300 lines
- Modular design with clear function separation
- Type hints for function parameters
- Comprehensive error handling

#### 6.2 Security
- API key read from file: `/home/ro/api_key`
- Never hardcode API key in source
- Add `/home/ro/api_key` to `.gitignore`
- Use environment variables or secure file reading

#### 6.3 Performance
- Local execution of sentence-transformers (no API calls)
- Efficient vector operations using NumPy
- Batch processing where applicable

#### 6.4 Visualization
- Clear, labeled diagrams using matplotlib/seaborn
- Readable tables using pandas or tabulate
- Color-coded clusters for easy identification

### 7. Dependencies

```
anthropic>=0.50.0
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
```

### 8. Data Flow

```
[Cluster Creation Phase]
create_sentences(100, ["sport","work","food"]) 
  → convert2vector(sentences) 
  → normalize_vector(vectors) 
  → divide2clusters(normalized_vectors) 
  → Visualization (diagram + table)

[Test Phase]
create_sentences(10, ["sport","work","food"]) 
  → convert2vector(test_sentences) 
  → normalize_vector(test_vectors) 
  → KNN classification(test_normalized, cluster_centroids) 
  → Visualization (diagram + table)
```

### 9. Success Criteria

1. **Accuracy:** Clusters should roughly align with true topics (>70% purity)
2. **Reproducibility:** Consistent results with same random seed
3. **Visualization:** Clear, interpretable diagrams and tables
4. **Code Quality:** Passes linting, under 300 lines
5. **Security:** No API key exposure in code or logs

### 10. Deliverables

1. **Documentation:**
   - PRD.md (this document)
   - Claude.md (Claude Code agent definitions)
   - Planning.md (implementation plan)
   - tasks.md (task breakdown)

2. **Code:**
   - `main.py` - Main orchestrator (<300 lines)
   - `agents/` - Agent definition files for Claude Code
   - `requirements.txt` - Python dependencies
   - `.gitignore` - Including API key path

3. **Outputs:**
   - Cluster visualization images
   - Results tables (CSV/console)

### 11. Future Enhancements

- Support for variable number of clusters
- Additional evaluation metrics (silhouette score, Davies-Bouldin)
- Interactive visualization with Plotly
- Topic coherence analysis
- Support for custom subjects
- Persistent storage of trained models

### 12. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Poor cluster quality | Low | Use high-quality sentence-transformer model |
| API rate limits | Medium | Implement retry logic with exponential backoff |
| API key exposure | High | Secure file reading, .gitignore, code review |
| Agent communication failure | Medium | Robust error handling, timeouts |
| Memory issues with large vectors | Low | Use float32 precision, batch processing |

### 13. Assumptions

1. Claude API accessible from WSL environment
2. Sufficient memory for 100 sentence embeddings
3. sentence-transformers models downloadable in WSL
4. Python 3.8+ installed in WSL
5. User has file access to `/home/ro/api_key`

### 14. Glossary

- **Semantic Similarity:** Measure of meaning similarity between texts
- **Embedding:** Dense vector representation of text
- **K-means:** Unsupervised clustering algorithm
- **KNN:** K-Nearest Neighbors classification algorithm
- **Normalization:** Scaling vectors to [0,1] range
- **Agent:** AI-powered component performing specific task