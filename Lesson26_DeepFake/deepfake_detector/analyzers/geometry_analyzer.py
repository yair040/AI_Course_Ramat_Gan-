"""
Facial geometry and physiology analyzer.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import Dict, List, Optional
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
from ..utils.logger import get_logger


class GeometryAnalyzer:
    """Analyzes facial geometry and physiological consistency."""
    
    def __init__(self, threshold: float = 0.5):
        """Initialize geometry analyzer."""
        self.threshold = threshold
        self.logger = get_logger('geometry_analyzer')
        self.reference_geometry = None
        
        if not FACE_RECOGNITION_AVAILABLE:
            self.logger.warning("face_recognition not available")
    
    def analyze(self, frames: List[np.ndarray]) -> Dict:
        """
        Analyze facial geometry consistency.
        
        Args:
            frames: List of video frames
            
        Returns:
            Dictionary with geometry scores
        """
        scores = {
            'feature_spacing': 0.0,
            'pupil_dilation': 0.0,
            'head_rotation': 0.0,
            'overall': 0.0,
        }
        
        if not frames or not FACE_RECOGNITION_AVAILABLE:
            return scores
        
        try:
            spacing_scores = []
            pupil_scores = []
            rotation_scores = []
            
            for i, frame in enumerate(frames):
                # Extract facial landmarks
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                landmarks_list = face_recognition.face_landmarks(rgb_frame)
                
                if not landmarks_list:
                    continue
                
                landmarks = landmarks_list[0]
                
                # Analyze feature spacing
                spacing = self._analyze_feature_spacing(landmarks)
                if spacing is not None:
                    spacing_scores.append(spacing)
                
                # Analyze pupil dilation
                pupil = self._analyze_pupil_dilation(landmarks, frame)
                if pupil is not None:
                    pupil_scores.append(pupil)
                
                # Analyze head rotation
                if i > 0 and self.reference_geometry:
                    rotation = self._analyze_head_rotation(landmarks)
                    if rotation is not None:
                        rotation_scores.append(rotation)
                
                # Store reference
                if i == 0:
                    self.reference_geometry = landmarks
            
            # Aggregate scores
            if spacing_scores:
                scores['feature_spacing'] = np.mean(spacing_scores)
            if pupil_scores:
                scores['pupil_dilation'] = np.mean(pupil_scores)
            if rotation_scores:
                scores['head_rotation'] = np.mean(rotation_scores)
            
            scores['overall'] = np.mean([v for v in scores.values() if v > 0])
        
        except Exception as e:
            self.logger.error(f"Geometry analysis error: {e}")
        
        return scores
    
    def _analyze_feature_spacing(self, landmarks: Dict) -> Optional[float]:
        """Analyze facial feature spacing consistency."""
        try:
            # Calculate inter-ocular distance
            if 'left_eye' not in landmarks or 'right_eye' not in landmarks:
                return None
            
            left_eye_center = np.mean(landmarks['left_eye'], axis=0)
            right_eye_center = np.mean(landmarks['right_eye'], axis=0)
            eye_distance = np.linalg.norm(left_eye_center - right_eye_center)
            
            # Calculate other feature distances
            if 'nose_tip' in landmarks:
                nose_tip = np.array(landmarks['nose_tip'][2])
                eye_to_nose = np.linalg.norm(
                    (left_eye_center + right_eye_center) / 2 - nose_tip
                )
                
                # Check ratio (should be relatively constant)
                ratio = eye_to_nose / eye_distance if eye_distance > 0 else 0
                
                # Natural ratio is around 0.8-1.2
                if 0.7 < ratio < 1.3:
                    return 1.0
                else:
                    return 0.6
            
            return 0.8
        
        except Exception as e:
            self.logger.debug(f"Feature spacing error: {e}")
            return None
    
    def _analyze_pupil_dilation(self, landmarks: Dict, 
                                frame: np.ndarray) -> Optional[float]:
        """Analyze pupil dilation patterns."""
        try:
            # Extract eye regions
            if 'left_eye' not in landmarks or 'right_eye' not in landmarks:
                return None
            
            left_eye = np.array(landmarks['left_eye'])
            right_eye = np.array(landmarks['right_eye'])
            
            # Calculate eye brightness (proxy for pupil size)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            left_brightness = self._get_region_brightness(gray, left_eye)
            right_brightness = self._get_region_brightness(gray, right_eye)
            
            # Pupils should have similar brightness in both eyes
            brightness_diff = abs(left_brightness - right_brightness)
            
            # Lower difference = higher score
            score = 1.0 - min(brightness_diff / 50.0, 1.0)
            
            return score
        
        except Exception as e:
            self.logger.debug(f"Pupil analysis error: {e}")
            return None
    
    def _get_region_brightness(self, gray: np.ndarray, 
                               points: np.ndarray) -> float:
        """Get average brightness in region defined by points."""
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.fillPoly(mask, [points.astype(np.int32)], 255)
        mean_val = cv2.mean(gray, mask=mask)[0]
        return mean_val
    
    def _analyze_head_rotation(self, landmarks: Dict) -> Optional[float]:
        """Analyze head rotation consistency."""
        try:
            if not self.reference_geometry:
                return None
            
            # Compare current landmarks with reference
            # Calculate angle differences
            
            # Get eye positions
            if ('left_eye' not in landmarks or 'right_eye' not in landmarks or
                'left_eye' not in self.reference_geometry or
                'right_eye' not in self.reference_geometry):
                return None
            
            curr_left = np.mean(landmarks['left_eye'], axis=0)
            curr_right = np.mean(landmarks['right_eye'], axis=0)
            ref_left = np.mean(self.reference_geometry['left_eye'], axis=0)
            ref_right = np.mean(self.reference_geometry['right_eye'], axis=0)
            
            # Calculate eye line angles
            curr_angle = np.arctan2(
                curr_right[1] - curr_left[1],
                curr_right[0] - curr_left[0]
            )
            ref_angle = np.arctan2(
                ref_right[1] - ref_left[1],
                ref_right[0] - ref_left[0]
            )
            
            angle_diff = abs(curr_angle - ref_angle)
            
            # Natural head rotation should have smooth angle changes
            # Sudden large changes might indicate manipulation
            score = 1.0 - min(angle_diff / (np.pi / 4), 1.0)
            
            return score
        
        except Exception as e:
            self.logger.debug(f"Head rotation error: {e}")
            return None
