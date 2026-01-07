"""
Report generation for detection results.
Author: Yair Levi
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from .logger import get_logger


class ReportGenerator:
    """Generates detection reports in various formats."""
    
    def __init__(self):
        """Initialize report generator."""
        self.logger = get_logger('report_generator')
    
    def generate_json_report(self, results: Dict[str, Any],
                            output_path: Path) -> Path:
        """
        Generate JSON report.
        
        Args:
            results: Detection results dictionary
            output_path: Path to save report
            
        Returns:
            Path to saved report
        """
        report = {
            'video_path': str(results.get('video_path', '')),
            'verdict': results.get('verdict', 'UNKNOWN'),
            'confidence': round(results.get('confidence', 0.0), 4),
            'analysis_date': datetime.now().isoformat(),
            'processing_time_sec': round(results.get('processing_time', 0.0), 2),
            'scores': self._format_scores(results.get('scores', {})),
            'anomalies': results.get('anomalies', []),
            'metadata': results.get('metadata', {}),
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Report saved to: {output_path}")
        return output_path
    
    def _format_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Format scores to 4 decimal places."""
        return {k: round(v, 4) for k, v in scores.items()}
    
    def create_anomaly_entry(self, timestamp: float, frame: int,
                            anom_type: str, severity: str,
                            description: str) -> Dict:
        """Create anomaly dictionary entry."""
        return {
            'timestamp': round(timestamp, 2),
            'frame': frame,
            'type': anom_type,
            'severity': severity,
            'description': description,
        }
    
    def generate_summary_text(self, results: Dict[str, Any]) -> str:
        """Generate human-readable summary."""
        verdict = results.get('verdict', 'UNKNOWN')
        confidence = results.get('confidence', 0.0) * 100
        
        summary = [
            f"DeepFake Detection Report",
            f"=" * 50,
            f"Video: {Path(results.get('video_path', '')).name}",
            f"Verdict: {verdict}",
            f"Confidence: {confidence:.2f}%",
            f"",
            f"Scores by Criterion:",
        ]
        
        for name, score in results.get('scores', {}).items():
            summary.append(f"  {name}: {score*100:.2f}%")
        
        anomalies = results.get('anomalies', [])
        if anomalies:
            summary.append(f"")
            summary.append(f"Anomalies Detected: {len(anomalies)}")
            for anom in anomalies[:5]:  # Show first 5
                summary.append(
                    f"  [{anom['timestamp']:.2f}s] {anom['type']}: "
                    f"{anom['description']}"
                )
        
        return "\n".join(summary)
    
    def save_text_report(self, results: Dict[str, Any],
                        output_path: Path) -> Path:
        """Save text report."""
        summary = self.generate_summary_text(results)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        self.logger.info(f"Text report saved to: {output_path}")
        return output_path
