"""
Statistical analysis module for Iris classification results.
Author: Yair Levi
"""

import numpy as np
from iris_classifier.logger_setup import get_logger

logger = get_logger(__name__)


def calculate_statistics(results_list, metric_name):
    """
    Calculate statistics for a specific metric across iterations.
    
    Args:
        results_list: List of result dictionaries from iterations
        metric_name: Name of metric to analyze
    
    Returns:
        dict: Statistical summary
    """
    values = [r[metric_name] for r in results_list if metric_name in r]
    
    if not values:
        logger.warning(f"No values found for metric: {metric_name}")
        return {}
    
    stats = {
        'mean': np.mean(values),
        'std': np.std(values),
        'min': np.min(values),
        'max': np.max(values),
        'median': np.median(values)
    }
    
    return stats


def aggregate_results(all_iterations):
    """
    Aggregate results from all iterations.
    
    Args:
        all_iterations: List of iteration results
    
    Returns:
        dict: Aggregated statistics
    """
    logger.info(f"Aggregating results from {len(all_iterations)} iterations")
    
    # Collect metrics for each stage
    stage1_results = [it['stage1'] for it in all_iterations]
    stage2_results = [it['stage2'] for it in all_iterations]
    overall_results = [it['overall'] for it in all_iterations]
    
    aggregated = {
        'stage1': {
            'accuracy': calculate_statistics(stage1_results, 'accuracy'),
            'precision': calculate_statistics(stage1_results, 'precision'),
            'recall': calculate_statistics(stage1_results, 'recall'),
            'f1_score': calculate_statistics(stage1_results, 'f1_score'),
        },
        'stage2': {
            'accuracy': calculate_statistics(stage2_results, 'accuracy'),
            'precision': calculate_statistics(stage2_results, 'precision'),
            'recall': calculate_statistics(stage2_results, 'recall'),
            'f1_score': calculate_statistics(stage2_results, 'f1_score'),
        },
        'overall': {
            'accuracy': calculate_statistics(overall_results, 'accuracy'),
            'precision': calculate_statistics(overall_results, 'precision'),
            'recall': calculate_statistics(overall_results, 'recall'),
            'f1_score': calculate_statistics(overall_results, 'f1_score'),
        },
        'num_iterations': len(all_iterations)
    }
    
    # Log summary
    logger.info("="*60)
    logger.info("AGGREGATED RESULTS SUMMARY")
    logger.info("="*60)
    for stage in ['stage1', 'stage2', 'overall']:
        logger.info(f"\n{stage.upper()}:")
        acc_stats = aggregated[stage]['accuracy']
        logger.info(f"  Accuracy: {acc_stats['mean']:.4f} ± {acc_stats['std']:.4f}")
        logger.info(f"  Range: [{acc_stats['min']:.4f}, {acc_stats['max']:.4f}]")
    logger.info("="*60)
    
    return aggregated