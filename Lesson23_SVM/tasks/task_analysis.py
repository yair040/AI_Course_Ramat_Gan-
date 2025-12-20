"""
Task module for results analysis and visualization.
Author: Yair Levi
"""

import json
from pathlib import Path
from iris_classifier.logger_setup import get_logger
from iris_classifier.statistics import aggregate_results
from iris_classifier.visualizer import generate_all_plots
from iris_classifier.config import RESULTS_DIR

logger = get_logger(__name__)


def analyze_results(all_iterations):
    """
    Analyze results from all iterations and generate visualizations.
    
    Args:
        all_iterations: List of results from all iterations
    
    Returns:
        dict: Aggregated statistics
    """
    logger.info("="*60)
    logger.info("ANALYZING RESULTS FROM ALL ITERATIONS")
    logger.info("="*60)
    
    try:
        # Aggregate statistics
        aggregated_stats = aggregate_results(all_iterations)
        
        # Generate visualizations
        generate_all_plots(all_iterations, aggregated_stats)
        
        # Save summary to JSON
        save_summary(aggregated_stats, all_iterations)
        
        logger.info("Results analysis completed successfully")
        
        return aggregated_stats
    
    except Exception as e:
        logger.error(f"Results analysis failed: {e}")
        raise


def save_summary(aggregated_stats, all_iterations):
    """
    Save results summary to JSON file.
    
    Args:
        aggregated_stats: Aggregated statistics
        all_iterations: All iteration results
    """
    logger.info("Saving results summary")
    
    # Prepare summary data (convert numpy arrays to lists for JSON)
    summary = {
        'num_iterations': aggregated_stats['num_iterations'],
        'stage1_accuracy': {
            'mean': float(aggregated_stats['stage1']['accuracy']['mean']),
            'std': float(aggregated_stats['stage1']['accuracy']['std']),
            'min': float(aggregated_stats['stage1']['accuracy']['min']),
            'max': float(aggregated_stats['stage1']['accuracy']['max'])
        },
        'stage2_accuracy': {
            'mean': float(aggregated_stats['stage2']['accuracy']['mean']),
            'std': float(aggregated_stats['stage2']['accuracy']['std']),
            'min': float(aggregated_stats['stage2']['accuracy']['min']),
            'max': float(aggregated_stats['stage2']['accuracy']['max'])
        },
        'overall_accuracy': {
            'mean': float(aggregated_stats['overall']['accuracy']['mean']),
            'std': float(aggregated_stats['overall']['accuracy']['std']),
            'min': float(aggregated_stats['overall']['accuracy']['min']),
            'max': float(aggregated_stats['overall']['accuracy']['max'])
        },
        'iterations': []
    }
    
    # Add individual iteration results
    for i, iteration in enumerate(all_iterations):
        summary['iterations'].append({
            'iteration': i + 1,
            'stage1_accuracy': float(iteration['stage1']['accuracy']),
            'stage2_accuracy': float(iteration['stage2']['accuracy']),
            'overall_accuracy': float(iteration['overall']['accuracy'])
        })
    
    # Save to file
    output_path = RESULTS_DIR / "results_summary.json"
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Results summary saved to: {output_path}")