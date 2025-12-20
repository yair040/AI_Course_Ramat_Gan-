"""
Iteration execution module for running classification iterations.
Author: Yair Levi
"""

from multiprocessing import Pool, cpu_count
from iris_classifier.logger_setup import get_logger
from iris_classifier.config import NUM_ITERATIONS
from iris_classifier.evaluator import combine_stage_predictions, evaluate_predictions
from tasks.task_stage1 import run_stage1
from tasks.task_stage2 import run_stage2

logger = get_logger(__name__)


def run_single_iteration(iteration_num):
    """
    Execute a single iteration (both stages).
    
    Args:
        iteration_num: Iteration number (0-based)
    
    Returns:
        dict: Results for this iteration
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Starting Iteration {iteration_num + 1}/{NUM_ITERATIONS}")
    logger.info(f"{'='*60}")
    
    try:
        # Stage 1: Group A vs Group B
        stage1_results = run_stage1(iteration_num)
        
        # Stage 2: Separate classes 1 and 2
        stage2_results = run_stage2(iteration_num, stage1_results)
        
        # Combine predictions
        _, y_test_orig = stage1_results['test_data']
        y_pred_stage1 = stage1_results['predictions']
        y_pred_stage2 = stage2_results['predictions']
        group_b_indices = stage2_results['group_b_indices']
        
        final_predictions = combine_stage_predictions(
            y_test_orig, y_pred_stage1, y_pred_stage2, group_b_indices
        )
        
        # Evaluate overall performance
        overall_metrics = evaluate_predictions(
            y_test_orig, final_predictions, "Overall"
        )
        
        logger.info(f"Iteration {iteration_num + 1} completed successfully")
        logger.info(f"Overall Accuracy: {overall_metrics['accuracy']:.4f}")
        
        return {
            'iteration': iteration_num,
            'stage1': stage1_results,
            'stage2': stage2_results,
            'overall': {
                'accuracy': overall_metrics['accuracy'],
                'precision': overall_metrics['precision'],
                'recall': overall_metrics['recall'],
                'f1_score': overall_metrics['f1_score'],
                'confusion_matrix': overall_metrics['confusion_matrix']
            }
        }
    
    except Exception as e:
        logger.error(f"Iteration {iteration_num + 1} failed: {e}")
        raise


def run_with_multiprocessing():
    """
    Run all iterations using multiprocessing.
    
    Returns:
        list: Results from all iterations
    """
    # Determine number of workers (max 5 for 5 iterations, use 80% of CPUs)
    num_workers = min(NUM_ITERATIONS, max(1, int(cpu_count() * 0.8)))
    logger.info(f"Using multiprocessing with {num_workers} workers")
    
    try:
        with Pool(processes=num_workers) as pool:
            results = pool.map(run_single_iteration, range(NUM_ITERATIONS))
        
        logger.info("All iterations completed via multiprocessing")
        return results
    
    except Exception as e:
        logger.error(f"Multiprocessing failed: {e}")
        logger.info("Falling back to sequential execution")
        return run_sequentially()


def run_sequentially():
    """
    Run all iterations sequentially (fallback).
    
    Returns:
        list: Results from all iterations
    """
    logger.info("Running iterations sequentially")
    
    results = []
    for i in range(NUM_ITERATIONS):
        result = run_single_iteration(i)
        results.append(result)
    
    return results