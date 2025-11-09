#!/usr/bin/env python3
"""
Main orchestration program for PCA and t-SNE Text Vectorization System

This program executes all tasks in sequence:
1. Generate 100 random sentences
2. Convert sentences to normalized vectors
3. Apply manual PCA (NumPy only)
4. Apply sklearn PCA
5. Apply t-SNE
"""

import time
import sys


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 60)
    print(" " * 10 + "PCA AND t-SNE TEXT VECTORIZATION SYSTEM")
    print("=" * 60)
    print("\nThis program will execute the following tasks:")
    print("  1. Generate 100 categorized sentences")
    print("  2. Convert sentences to normalized vectors")
    print("  3. Manual PCA implementation (NumPy only)")
    print("  4. sklearn PCA implementation")
    print("  5. t-SNE dimensionality reduction")
    print("\nAll methods reduce to 3D and apply K-means clustering (K=3)")
    print("=" * 60)


def execute_task(task_number: int, task_name: str, task_function):
    """
    Execute a task with error handling and timing

    Args:
        task_number: Task number (1-5)
        task_name: Name of the task
        task_function: Function to execute

    Returns:
        Task results or None if error
    """
    print(f"\n\n{'█' * 60}")
    print(f"EXECUTING TASK {task_number}: {task_name}")
    print(f"{'█' * 60}")

    start_time = time.perf_counter()

    try:
        result = task_function()
        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"\n✓ Task {task_number} completed successfully in {duration:.2f} seconds")
        return result

    except Exception as e:
        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"\n✗ Task {task_number} failed after {duration:.2f} seconds")
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")

        import traceback
        traceback.print_exc()

        return None


def print_summary(results: dict):
    """
    Print final summary of all tasks

    Args:
        results: Dictionary of task results
    """
    print("\n\n" + "=" * 60)
    print(" " * 20 + "FINAL SUMMARY")
    print("=" * 60)

    # Task completion status
    print("\nTask Completion Status:")
    for task_num in range(1, 6):
        status = "✓ Completed" if results.get(f'task{task_num}') is not None else "✗ Failed"
        print(f"  Task {task_num}: {status}")

    # Data summary
    if results.get('task1'):
        sentences = results['task1']
        print(f"\nGenerated Data:")
        print(f"  Total sentences: {len(sentences)}")

    if results.get('task2') is not None:
        vectors = results['task2']
        print(f"  Vector dimensions: {vectors.shape}")

    # Method comparison
    print(f"\nDimensionality Reduction Methods:")
    methods = [
        ("Manual PCA", "task3"),
        ("sklearn PCA", "task4"),
        ("t-SNE", "task5")
    ]

    for method_name, task_key in methods:
        if results.get(task_key):
            print(f"  {method_name}: ✓ 3D transformation successful")
        else:
            print(f"  {method_name}: ✗ Failed")

    # Output files
    print(f"\nOutput Files Generated:")
    output_files = [
        "sentences.txt",
        "normalized.txt",
        "pca_transformed_manual.txt",
        "pca_transformed_sklearn.txt",
        "tsne_transformed.txt"
    ]

    from pathlib import Path
    for filename in output_files:
        exists = Path(filename).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {filename}")

    print("\n" + "=" * 60)
    print("All processing complete!")
    print("=" * 60)


def main():
    """Main execution pipeline"""
    # Print banner
    print_banner()

    # Wait for user to be ready
    print("\nPress Enter to begin...")
    input()

    # Track results
    results = {}
    overall_start = time.perf_counter()

    # Task 1: Generate sentences
    import task1_generate
    result = execute_task(1, "Generate Sentences", task1_generate.main)
    results['task1'] = result

    if result is None:
        print("\n⚠ Task 1 failed. Cannot proceed.")
        sys.exit(1)

    # Task 2: Vectorize sentences
    import task2_vectorize
    result = execute_task(2, "Vectorize Sentences", task2_vectorize.main)
    results['task2'] = result

    if result is None:
        print("\n⚠ Task 2 failed. Cannot proceed.")
        sys.exit(1)

    # Task 3: Manual PCA
    import task3_manual_pca
    result = execute_task(3, "Manual PCA Implementation", task3_manual_pca.main)
    results['task3'] = result

    # Task 4: sklearn PCA
    import task4_sklearn_pca
    result = execute_task(4, "sklearn PCA Implementation", task4_sklearn_pca.main)
    results['task4'] = result

    # Task 5: t-SNE
    import task5_tsne
    result = execute_task(5, "t-SNE Implementation", task5_tsne.main)
    results['task5'] = result

    # Calculate total time
    overall_end = time.perf_counter()
    total_time = overall_end - overall_start

    # Print summary
    print_summary(results)

    print(f"\nTotal execution time: {total_time:.2f} seconds")
    print("Thank you for using the PCA and t-SNE Text Vectorization System!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
