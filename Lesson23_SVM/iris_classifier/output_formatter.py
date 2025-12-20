"""
Output formatting module for displaying results.
Author: Yair Levi
"""

from iris_classifier.logger_setup import get_logger

logger = get_logger(__name__)


def print_summary(aggregated_stats):
    """
    Print summary to console.
    
    Args:
        aggregated_stats: Aggregated statistics
    """
    print("\n" + "="*70)
    print(" " * 20 + "FINAL RESULTS SUMMARY")
    print("="*70)
    print(f"\nNumber of iterations: {aggregated_stats['num_iterations']}")
    
    print("\n" + "-"*70)
    print("STAGE 1 (Group A vs Group B):")
    print("-"*70)
    acc = aggregated_stats['stage1']['accuracy']
    print(f"  Accuracy: {acc['mean']:.4f} ± {acc['std']:.4f}")
    print(f"  Range:    [{acc['min']:.4f}, {acc['max']:.4f}]")
    
    print("\n" + "-"*70)
    print("STAGE 2 (Class 1 vs Class 2):")
    print("-"*70)
    acc = aggregated_stats['stage2']['accuracy']
    print(f"  Accuracy: {acc['mean']:.4f} ± {acc['std']:.4f}")
    print(f"  Range:    [{acc['min']:.4f}, {acc['max']:.4f}]")
    
    print("\n" + "-"*70)
    print("OVERALL (All 3 Classes):")
    print("-"*70)
    acc = aggregated_stats['overall']['accuracy']
    print(f"  Accuracy: {acc['mean']:.4f} ± {acc['std']:.4f}")
    print(f"  Range:    [{acc['min']:.4f}, {acc['max']:.4f}]")
    
    print("\n" + "="*70)
    print("Results and visualizations saved to: ./results/")
    print("="*70 + "\n")
    
    logger.info("Summary printed to console")