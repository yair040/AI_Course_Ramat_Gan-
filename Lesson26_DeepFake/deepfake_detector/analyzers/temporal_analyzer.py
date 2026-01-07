"""
Temporal consistency and motion analysis.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import Dict, List, Optional
from ..utils.logger import get_logger


class TemporalAnalyzer:
    """Analyzes temporal consistency and motion patterns."""
    
    def __init__(self, threshold: float = 0.6):
        """Initialize temporal analyzer."""
        self.threshold = threshold
        self.logger = get_logger('temporal_analyzer')
        self.prev_frame = None
        self.prev_gray = None
        self.motion_history = []
    
    def analyze(self, frames: List[np.ndarray]) -> Dict:
        """
        Analyze temporal consistency across frames.
        
        Args:
            frames: List of consecutive video frames
            
        Returns:
            Dictionary with temporal analysis scores
        """
        scores = {
            'motion_consistency': 0.0,
            'blink_pattern': 0.0,
            'jitter_detection': 0.0,
            'overall': 0.0,
        }
        
        if len(frames) < 2:
            return scores
        
        try:
            motion_scores = []
            blink_scores = []
            jitter_scores = []
            
            for i in range(1, len(frames)):
                prev = frames[i-1]
                curr = frames[i]
                
                # Motion consistency
                motion_score = self._analyze_motion(prev, curr)
                if motion_score is not None:
                    motion_scores.append(motion_score)
                
                # Jitter detection
                jitter_score = self._detect_jitter(prev, curr)
                if jitter_score is not None:
                    jitter_scores.append(jitter_score)
            
            # Blink analysis across all frames
            blink_score = self._analyze_blink_pattern(frames)
            
            # Aggregate scores
            if motion_scores:
                scores['motion_consistency'] = np.mean(motion_scores)
            if jitter_scores:
                scores['jitter_detection'] = np.mean(jitter_scores)
            scores['blink_pattern'] = blink_score
            
            scores['overall'] = np.mean([
                scores['motion_consistency'],
                scores['blink_pattern'],
                scores['jitter_detection']
            ])
        
        except Exception as e:
            self.logger.error(f"Temporal analysis error: {e}")
        
        return scores
    
    def _analyze_motion(self, prev: np.ndarray, curr: np.ndarray) -> Optional[float]:
        """Analyze motion between consecutive frames."""
        try:
            prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, curr_gray, None,
                0.5, 3, 15, 3, 5, 1.2, 0
            )
            
            # Calculate flow magnitude
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            
            # Analyze flow consistency
            mean_mag = np.mean(mag)
            std_mag = np.std(mag)
            
            # Natural motion has consistent flow
            # Unnatural motion has high variance
            consistency = 1.0 - min(std_mag / max(mean_mag, 1.0), 1.0)
            
            self.motion_history.append(mean_mag)
            if len(self.motion_history) > 100:
                self.motion_history.pop(0)
            
            return consistency
        
        except Exception as e:
            self.logger.debug(f"Motion analysis error: {e}")
            return None
    
    def _detect_jitter(self, prev: np.ndarray, curr: np.ndarray) -> Optional[float]:
        """Detect unnatural jitter between frames."""
        try:
            # Compute frame difference
            diff = cv2.absdiff(prev, curr)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # Calculate jitter metric
            jitter_metric = np.mean(diff_gray)
            
            # Low jitter = high score (natural)
            # High jitter = low score (unnatural)
            score = 1.0 - min(jitter_metric / 50.0, 1.0)
            
            return score
        
        except Exception as e:
            self.logger.debug(f"Jitter detection error: {e}")
            return None
    
    def _analyze_blink_pattern(self, frames: List[np.ndarray]) -> float:
        """Analyze eye blink patterns across frames."""
        # Simplified blink detection
        # Real implementation would use eye aspect ratio from landmarks
        
        try:
            # Use face detection and eye ROI analysis
            blink_count = 0
            eye_aspect_ratios = []
            
            for frame in frames:
                ear = self._estimate_eye_aspect_ratio(frame)
                if ear is not None:
                    eye_aspect_ratios.append(ear)
            
            if not eye_aspect_ratios:
                return 0.7  # Neutral score if no eyes detected
            
            # Detect blinks (drops in EAR)
            threshold = 0.2
            for i in range(1, len(eye_aspect_ratios)):
                if eye_aspect_ratios[i] < threshold and eye_aspect_ratios[i-1] >= threshold:
                    blink_count += 1
            
            # Expected blink rate: ~15-20 per minute
            fps = 24  # Assume 24 fps
            duration_sec = len(frames) / fps
            expected_blinks = duration_sec / 60 * 17.5
            
            if expected_blinks == 0:
                return 0.7
            
            # Score based on blink rate
            blink_ratio = blink_count / expected_blinks
            score = 1.0 - abs(1.0 - blink_ratio)
            
            return max(0.0, min(1.0, score))
        
        except Exception as e:
            self.logger.debug(f"Blink analysis error: {e}")
            return 0.7
    
    def _estimate_eye_aspect_ratio(self, frame: np.ndarray) -> Optional[float]:
        """Estimate eye aspect ratio (placeholder)."""
        # Simplified - real implementation would use facial landmarks
        return 0.3  # Placeholder value
