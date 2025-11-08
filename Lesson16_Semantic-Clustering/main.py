#!/usr/bin/env python3
"""
Semantic Clustering System - Main Program
Author: Yair Levi

This program demonstrates semantic clustering using AI-generated sentences.
It follows a two-step process:
1. Cluster Creation: Generate 100 sentences, vectorize, and cluster them
2. Testing: Generate 10 new sentences and classify them using KNN
"""

import os
import sys
from typing import List, Tuple
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

# Import utility functions
from utils import (
    load_api_key,
    generate_sentences_with_api,
    convert_sentences_to_vectors,
    normalize_vectors,
    print_vector_info
)

from visualization import (
    create_cluster_visualization,
    create_cluster_table,
    print_cluster_summary,
    display_cluster_samples,
    save_table_to_csv,
    create_confusion_matrix
)


def step1_create_clusters(
    api_key: str,
    num_sentences: int = 100,
    subjects: List[str] = None
) -> Tuple[np.ndarray, np.ndarray, List[str], List[str]]:
    """
    Step 1: Generate sentences, vectorize, and create clusters.

    Args:
        api_key: Anthropic API key
        num_sentences: Number of sentences to generate
        subjects: List of subjects for sentence generation

    Returns:
        Tuple of (normalized_vectors, labels, centroids, sentences, actual_subjects)
    """
    if subjects is None:
        subjects = ['sport', 'work', 'food']

    print("\n" + "="*80)
    print("STEP 1: CLUSTER CREATION")
    print("="*80)

    # Generate sentences using API
    print(f"\nGenerating {num_sentences} sentences about: {', '.join(subjects)}")
    sentence_data = generate_sentences_with_api(api_key, num_sentences, subjects)
    sentences = [s[0] for s in sentence_data]
    actual_subjects = [s[1] for s in sentence_data]

    print(f"Generated {len(sentences)} sentences")

    # Display sample sentences
    print("\nSample sentences:")
    for i in range(min(5, len(sentences))):
        print(f"  {i+1}. [{actual_subjects[i]}] {sentences[i]}")

    # Convert to vectors
    print("\n" + "-"*80)
    vectors = convert_sentences_to_vectors(sentences)

    # Check if vectors are normalized
    print_vector_info(vectors, "Original Vectors")

    # Normalize vectors (convert2vector agent returns normalized vectors)
    # But we normalize anyway to ensure consistency
    normalized_vectors = normalize_vectors(vectors)
    print_vector_info(normalized_vectors, "Normalized Vectors")

    # Perform K-means clustering with k=3
    print("-"*80)
    print("Performing K-means clustering (k=3)...")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(normalized_vectors)
    centroids = kmeans.cluster_centers_

    print(f"Clustering complete!")
    print(f"Cluster sizes: {np.bincount(labels)}")

    # Create visualizations
    print("\n" + "-"*80)
    print("Creating visualizations...")

    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)

    # Cluster visualization
    create_cluster_visualization(
        normalized_vectors,
        labels,
        centroids,
        "Semantic Clustering of 100 Sentences (Step 1)",
        save_path='output/step1_clusters.png'
    )

    # Create and display table
    df = create_cluster_table(sentences, labels, actual_subjects)
    print_cluster_summary(df, "Step 1: Cluster Summary")
    display_cluster_samples(df, n_samples=3)

    # Save table
    save_table_to_csv(df, 'output/step1_clusters.csv')

    # Create confusion matrix
    create_confusion_matrix(df, save_path='output/step1_confusion_matrix.png')

    return normalized_vectors, labels, centroids, sentences, actual_subjects


def step2_test_classification(
    api_key: str,
    training_vectors: np.ndarray,
    training_labels: np.ndarray,
    centroids: np.ndarray,
    num_test_sentences: int = 10,
    subjects: List[str] = None
) -> None:
    """
    Step 2: Generate test sentences and classify them using KNN.

    Args:
        api_key: Anthropic API key
        training_vectors: Vectors from step 1 (for KNN training)
        training_labels: Labels from step 1 (for KNN training)
        centroids: Cluster centroids from step 1
        num_test_sentences: Number of test sentences to generate
        subjects: List of subjects for sentence generation
    """
    if subjects is None:
        subjects = ['sport', 'work', 'food']

    print("\n" + "="*80)
    print("STEP 2: TESTING WITH KNN CLASSIFICATION")
    print("="*80)

    # Generate test sentences
    print(f"\nGenerating {num_test_sentences} test sentences about: {', '.join(subjects)}")
    sentence_data = generate_sentences_with_api(api_key, num_test_sentences, subjects)
    test_sentences = [s[0] for s in sentence_data]
    test_subjects = [s[1] for s in sentence_data]

    print(f"Generated {len(test_sentences)} test sentences")

    # Display all test sentences
    print("\nTest sentences:")
    for i, (sentence, subject) in enumerate(zip(test_sentences, test_subjects)):
        print(f"  {i+1}. [{subject}] {sentence}")

    # Convert to vectors
    print("\n" + "-"*80)
    test_vectors = convert_sentences_to_vectors(test_sentences)

    # Normalize test vectors (convert2vector already returns normalized, but we ensure it)
    test_vectors = normalize_vectors(test_vectors)
    print_vector_info(test_vectors, "Test Vectors (Normalized)")

    # Train KNN classifier on training data
    print("-"*80)
    print("Training KNN classifier (k=3)...")
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(training_vectors, training_labels)

    # Predict cluster assignments for test sentences
    test_predictions = knn.predict(test_vectors)
    test_probabilities = knn.predict_proba(test_vectors)

    print("Classification complete!")

    # Display predictions
    print("\n" + "-"*80)
    print("Test Sentence Predictions:")
    print("-"*80)
    for i, (sentence, subject, cluster, probs) in enumerate(
        zip(test_sentences, test_subjects, test_predictions, test_probabilities)
    ):
        print(f"\n{i+1}. [{subject}] {sentence}")
        print(f"   Assigned to: Cluster {cluster}")
        print(f"   Confidence: {probs[cluster]:.1%}")
        print(f"   All probabilities: [C0: {probs[0]:.1%}, C1: {probs[1]:.1%}, C2: {probs[2]:.1%}]")

    # Create visualizations
    print("\n" + "-"*80)
    print("Creating visualizations...")

    # Visualize test points with training clusters
    create_cluster_visualization(
        test_vectors,
        test_predictions,
        centroids,
        "KNN Classification of 10 Test Sentences (Step 2)",
        save_path='output/step2_classification.png'
    )

    # Create and display table
    df = create_cluster_table(test_sentences, test_predictions, test_subjects)
    print_cluster_summary(df, "Step 2: Classification Summary")

    # Save table
    save_table_to_csv(df, 'output/step2_classification.csv')

    # Create confusion matrix
    create_confusion_matrix(df, save_path='output/step2_confusion_matrix.png')

    print("\n" + "="*80)
    print("STEP 2 COMPLETE")
    print("="*80)


def main():
    """Main execution function."""
    try:
        print("="*80)
        print("SEMANTIC CLUSTERING SYSTEM")
        print("Author: Yair Levi")
        print("="*80)

        # Load API key
        print("\nLoading API key...")
        api_key = load_api_key()
        print("API key loaded successfully")

        # Configuration
        subjects = ['sport', 'work', 'food']

        # Step 1: Create clusters
        training_vectors, training_labels, centroids, train_sentences, train_subjects = (
            step1_create_clusters(
                api_key,
                num_sentences=100,
                subjects=subjects
            )
        )

        # Step 2: Test classification
        step2_test_classification(
            api_key,
            training_vectors,
            training_labels,
            centroids,
            num_test_sentences=10,
            subjects=subjects
        )

        # Final summary
        print("\n" + "="*80)
        print("PROGRAM COMPLETE")
        print("="*80)
        print("\nResults saved to:")
        print("  - output/step1_clusters.png")
        print("  - output/step1_clusters.csv")
        print("  - output/step1_confusion_matrix.png")
        print("  - output/step2_classification.png")
        print("  - output/step2_classification.csv")
        print("  - output/step2_confusion_matrix.png")
        print("\n" + "="*80)

    except Exception as e:
        print(f"\nERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
