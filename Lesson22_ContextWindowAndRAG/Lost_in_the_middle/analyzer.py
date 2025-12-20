"""
Analyzer Module

Statistical analysis of experiment results.

Author: Yair Levi
"""

from typing import Dict

from config import (
    TEST_ITERATIONS,
    DOCUMENTS_PER_POSITION,
    get_statistics_path
)
from utils import get_logger


logger = get_logger(__name__)


# ============================================================================
# CALCULATIONS
# ============================================================================

def calculate_success_rates(counters: Dict[str, int], iterations: int) -> Dict[str, float]:
    """
    Calculate success rate percentages for each position.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations

    Returns:
        Dictionary of success rates (percentages) by position
    """
    tests_per_position = DOCUMENTS_PER_POSITION * iterations

    rates = {}
    for position, count in counters.items():
        rate = (count / tests_per_position) * 100
        rates[position] = rate

        logger.info(f"{position.capitalize()} position: {count}/{tests_per_position} = {rate:.1f}%")

    return rates


def calculate_overall_accuracy(counters: Dict[str, int], iterations: int) -> float:
    """
    Calculate overall accuracy across all positions.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations

    Returns:
        Overall accuracy percentage
    """
    total_correct = sum(counters.values())
    total_tests = len(counters) * DOCUMENTS_PER_POSITION * iterations

    accuracy = (total_correct / total_tests) * 100

    logger.info(f"Overall accuracy: {total_correct}/{total_tests} = {accuracy:.1f}%")

    return accuracy


# ============================================================================
# STATISTICS GENERATION
# ============================================================================

def generate_statistics(counters: Dict[str, int], iterations: int = TEST_ITERATIONS) -> Dict:
    """
    Generate comprehensive statistical summary.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations

    Returns:
        Dictionary containing all statistics
    """
    logger.info("Generating statistical summary...")

    rates = calculate_success_rates(counters, iterations)
    overall = calculate_overall_accuracy(counters, iterations)

    tests_per_position = DOCUMENTS_PER_POSITION * iterations

    statistics = {
        'counters': counters,
        'rates': rates,
        'overall_accuracy': overall,
        'iterations': iterations,
        'tests_per_position': tests_per_position,
        'total_tests': len(counters) * tests_per_position
    }

    return statistics


# ============================================================================
# FORMATTING
# ============================================================================

def format_results(statistics: Dict) -> str:
    """
    Format statistics as readable string.

    Args:
        statistics: Statistics dictionary from generate_statistics()

    Returns:
        Formatted results string
    """
    counters = statistics['counters']
    rates = statistics['rates']
    overall = statistics['overall_accuracy']
    iterations = statistics['iterations']
    tests_per_position = statistics['tests_per_position']

    lines = [
        "="*70,
        "EXPERIMENT RESULTS: Lost in the Middle",
        "="*70,
        "",
        f"Test Iterations: {iterations}",
        f"Documents per Position: {DOCUMENTS_PER_POSITION}",
        f"Total Tests per Position: {tests_per_position}",
        "",
        "-"*70,
        "RESULTS BY POSITION:",
        "-"*70,
        ""
    ]

    # Results for each position
    for position in ['start', 'middle', 'end']:
        count = counters[position]
        rate = rates[position]

        lines.append(f"{position.upper():10} | {count:2}/{tests_per_position} correct | {rate:5.1f}%")

    lines.extend([
        "",
        "-"*70,
        f"OVERALL ACCURACY: {overall:.1f}%",
        "-"*70,
        "",
        "INTERPRETATION:",
        ""
    ])

    # Add interpretation
    if rates['middle'] < rates['start'] and rates['middle'] < rates['end']:
        lines.append("✓ HYPOTHESIS SUPPORTED: Middle position shows lowest accuracy")
    elif abs(rates['start'] - rates['middle']) < 5 and abs(rates['end'] - rates['middle']) < 5:
        lines.append("○ INCONCLUSIVE: All positions show similar accuracy")
    else:
        lines.append("✗ HYPOTHESIS NOT SUPPORTED: Middle position does not show lowest accuracy")

    lines.extend([
        "",
        "="*70
    ])

    return '\n'.join(lines)


# ============================================================================
# FILE OUTPUT
# ============================================================================

def save_statistics(statistics: Dict, formatted_results: str) -> None:
    """
    Save statistics to file.

    Args:
        statistics: Statistics dictionary
        formatted_results: Formatted results string
    """
    output_path = get_statistics_path()

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_results)

        logger.info(f"Statistics saved to: {output_path}")

    except Exception as e:
        logger.error(f"Error saving statistics: {e}")
        raise


def print_summary(statistics: Dict) -> None:
    """
    Print summary to console and log.

    Args:
        statistics: Statistics dictionary
    """
    formatted = format_results(statistics)

    # Print to console
    print("\n" + formatted)

    # Also log
    for line in formatted.split('\n'):
        if line.strip():
            logger.info(line)


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_results(counters: Dict[str, int], iterations: int = TEST_ITERATIONS) -> Dict:
    """
    Complete analysis workflow.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations

    Returns:
        Statistics dictionary
    """
    logger.info("="*60)
    logger.info("STATISTICAL ANALYSIS")
    logger.info("="*60)

    # Generate statistics
    statistics = generate_statistics(counters, iterations)

    # Format results
    formatted_results = format_results(statistics)

    # Save to file
    save_statistics(statistics, formatted_results)

    # Print summary
    print_summary(statistics)

    logger.info("="*60)
    logger.info("Analysis complete")
    logger.info("="*60)

    return statistics
