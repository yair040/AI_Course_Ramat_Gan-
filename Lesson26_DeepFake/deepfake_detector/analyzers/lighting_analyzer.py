"""
Lighting, shadow, and reflection consistency analyzer.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from ..utils.logger import get_logger


class LightingAnalyzer:
    """Analyzes lighting consistency, shadows, and reflections."""
    
    def __init__(self, threshold: float = 0.5):
        """Initialize lighting analyzer."""
        self.threshold = threshold
        self.logger = get_logger('lighting_analyzer')
    
    def analyze(self, frames: List[np.ndarray]) -> Dict:
        """
        Analyze lighting consistency across frames.
        
        Args:
            frames: List of video frames
            
        Returns:
            Dictionary with lighting analysis scores
        """
        scores = {
            'direction_consistency': 0.0,
            'color_temperature': 0.0,
            'shadow_geometry': 0.0,
            'reflection_consistency': 0.0,
            'overall': 0.0,
        }
        
        if not frames:
            return scores
        
        try:
            direction_scores = []
            temp_scores = []
            shadow_scores = []
            reflection_scores = []
            
            for frame in frames:
                # Analyze lighting direction
                dir_score = self._analyze_direction(frame)
                if dir_score is not None:
                    direction_scores.append(dir_score)
                
                # Analyze color temperature
                temp_score = self._analyze_color_temperature(frame)
                if temp_score is not None:
                    temp_scores.append(temp_score)
                
                # Analyze shadows
                shadow_score = self._analyze_shadows(frame)
                if shadow_score is not None:
                    shadow_scores.append(shadow_score)
                
                # Analyze reflections
                refl_score = self._analyze_reflections(frame)
                if refl_score is not None:
                    reflection_scores.append(refl_score)
            
            # Aggregate scores
            if direction_scores:
                scores['direction_consistency'] = np.mean(direction_scores)
            if temp_scores:
                scores['color_temperature'] = np.mean(temp_scores)
            if shadow_scores:
                scores['shadow_geometry'] = np.mean(shadow_scores)
            if reflection_scores:
                scores['reflection_consistency'] = np.mean(reflection_scores)
            
            scores['overall'] = np.mean([v for v in scores.values() if v > 0])
        
        except Exception as e:
            self.logger.error(f"Lighting analysis error: {e}")
        
        return scores
    
    def _analyze_direction(self, frame: np.ndarray) -> Optional[float]:
        """Analyze lighting direction consistency."""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate gradients
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            
            # Compute dominant gradient direction
            magnitude = np.sqrt(grad_x**2 + grad_y**2)
            direction = np.arctan2(grad_y, grad_x)
            
            # Analyze consistency - natural lighting has consistent direction
            # Deepfakes may have inconsistent lighting across face
            direction_std = np.std(direction[magnitude > np.mean(magnitude)])
            
            # Lower std = more consistent = higher score
            score = 1.0 - min(direction_std / np.pi, 1.0)
            
            return score
        
        except Exception as e:
            self.logger.debug(f"Direction analysis error: {e}")
            return None
    
    def _analyze_color_temperature(self, frame: np.ndarray) -> Optional[float]:
        """Analyze color temperature consistency."""
        try:
            # Convert to LAB color space
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Analyze color temperature via a/b channels
            # Consistent temperature = consistent a/b ratio
            a_mean = np.mean(a)
            b_mean = np.mean(b)
            
            # Calculate color temperature ratio
            temp_ratio = b_mean / max(a_mean, 1.0)
            
            # Check for natural range (warm to cool)
            # Score based on whether ratio is in expected range
            if 0.5 < temp_ratio < 2.0:
                score = 1.0
            else:
                score = 0.6
            
            return score
        
        except Exception as e:
            self.logger.debug(f"Color temperature error: {e}")
            return None
    
    def _analyze_shadows(self, frame: np.ndarray) -> Optional[float]:
        """Analyze shadow geometry and consistency."""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect dark regions (potential shadows)
            _, shadow_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
            
            # Analyze shadow properties
            contours, _ = cv2.findContours(
                shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return 0.8  # No strong shadows detected
            
            # Analyze shadow shapes - natural shadows have smooth edges
            smoothness_scores = []
            for contour in contours[:5]:  # Analyze top 5 shadows
                if len(contour) > 10:
                    perimeter = cv2.arcLength(contour, True)
                    area = cv2.contourArea(contour)
                    if area > 0:
                        circularity = 4 * np.pi * area / (perimeter ** 2)
                        smoothness_scores.append(circularity)
            
            if smoothness_scores:
                avg_smoothness = np.mean(smoothness_scores)
                # Natural shadows are moderately smooth (not too circular)
                score = 1.0 - abs(0.5 - avg_smoothness)
                return max(0.0, min(1.0, score))
            
            return 0.8
        
        except Exception as e:
            self.logger.debug(f"Shadow analysis error: {e}")
            return None
    
    def _analyze_reflections(self, frame: np.ndarray) -> Optional[float]:
        """Analyze reflection consistency (eyes, glasses, surfaces)."""
        try:
            # Detect bright spots (potential reflections)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, bright_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            # Count and analyze bright spots
            num_bright = cv2.countNonZero(bright_mask)
            frame_size = frame.shape[0] * frame.shape[1]
            bright_ratio = num_bright / frame_size
            
            # Natural reflections: small, discrete bright spots
            # Unnatural: too many or too few bright spots
            if 0.001 < bright_ratio < 0.05:
                score = 1.0
            elif bright_ratio < 0.001:
                score = 0.7  # Too few reflections
            else:
                score = 0.6  # Too many bright spots
            
            return score
        
        except Exception as e:
            self.logger.debug(f"Reflection analysis error: {e}")
            return None
