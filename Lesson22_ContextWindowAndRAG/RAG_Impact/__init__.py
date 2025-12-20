"""
Context Window vs RAG Comparison Package.

This package provides a comprehensive comparison between two document retrieval methods:
1. Context Window: Loading all documents into Claude's context window
2. RAG (Retrieval Augmented Generation): Using vector search to load only relevant chunks

The comparison measures:
- Response time
- Token usage
- Cost efficiency
- Answer quality

Usage:
    python -m context_window_vs_rag

Or programmatically:
    from context_window_vs_rag import main
    main()

Modules:
    - config: Configuration constants
    - logger_setup: Ring buffer logging (20 files × 16MB)
    - pdf_loader: PDF loading with multiprocessing
    - query_processor: API calls with timing and retry logic
    - context_window_method: Full context implementation
    - rag_method: RAG pipeline with vector search
    - results_analyzer: Statistical analysis and comparison
    - visualization: Graph generation
    - main: Main orchestration

Author: Yair Levi
Version: 1.0.0
Date: 2025-12-15
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__email__ = "yair@example.com"

# Import main function for easy access
from .main import main

__all__ = ["main"]
