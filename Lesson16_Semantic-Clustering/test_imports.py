#!/usr/bin/env python3
"""
Quick test to verify all imports work correctly.
"""

import sys

print("Testing imports...")

try:
    print("  - Importing utils...")
    from utils import load_api_key, generate_sentences_with_api, convert_sentences_to_vectors
    print("    ✓ utils imported successfully")

    print("  - Importing visualization...")
    from visualization import create_cluster_visualization, create_cluster_table
    print("    ✓ visualization imported successfully")

    print("  - Importing sklearn...")
    from sklearn.cluster import KMeans
    from sklearn.neighbors import KNeighborsClassifier
    print("    ✓ sklearn imported successfully")

    print("  - Importing sentence_transformers...")
    from sentence_transformers import SentenceTransformer
    print("    ✓ sentence_transformers imported successfully")

    print("  - Importing anthropic...")
    from anthropic import Anthropic
    print("    ✓ anthropic imported successfully")

    print("\n✓ All imports successful!")
    print("\nCode structure verification complete.")
    print("\nTo run the full program:")
    print("  python main.py")
    print("\nOr:")
    print("  ./main.py")

except Exception as e:
    print(f"\n✗ Error: {str(e)}", file=sys.stderr)
    sys.exit(1)
