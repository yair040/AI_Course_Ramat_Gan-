"""
Facial expression and feature consistency analyzer.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
from ..utils.logger import get_logger


class FacialAnalyzer:
    """Analyzes facial expressions and feature consistency."""
    
    def __init__(self, threshold: float = 0.5):
        """Initialize facial analyzer."""
        self.threshold = threshold
        self.logger = get_logger('facial_analyzer')
        self.prev_landmarks = None
        
        if not FACE_RECOGNITION_AVAILABLE:
            self.logger.warning("face_recognition not available, using OpenCV")
    
    def analyze(self, frames: List[np.ndarray]) -> Dict:
        """
        Analyze facial consistency across frames.
        
        Args:
            frames: List of video frames
            
        Returns:
            Dictionary with analysis scores
        """
        scores = {
            'expression_consistency': 0.0,
            'boundary_artifacts': 0.0,
            'feature_alignment': 0.0,
            'overall': 0.0,
        }
        
        if not frames:
            return scores
        
        try:
            # Analyze each frame
            frame_scores = []
            for frame in frames:
                frame_score = self._analyze_frame(frame)
                if frame_score is not None:
                    frame_scores.append(frame_score)
            
            if frame_scores:
                # Average scores
                scores['expression_consistency'] = np.mean([s[0] for s in frame_scores])
                scores['boundary_artifacts'] = np.mean([s[1] for s in frame_scores])
                scores['feature_alignment'] = np.mean([s[2] for s in frame_scores])
                scores['overall'] = np.mean([scores[k] for k in 
                                            ['expression_consistency', 
                                             'boundary_artifacts',
                                             'feature_alignment']])
        
        except Exception as e:
            self.logger.error(f"Facial analysis error: {e}")
        
        return scores
    
    def _analyze_frame(self, frame: np.ndarray) -> Optional[Tuple]:
        """Analyze single frame for facial anomalies."""
        if FACE_RECOGNITION_AVAILABLE:
            return self._analyze_with_face_recognition(frame)
        else:
            return self._analyze_with_opencv(frame)
    
    def _analyze_with_face_recognition(self, frame: np.ndarray) -> Optional[Tuple]:
        """Analyze using face_recognition library."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks_list = face_recognition.face_landmarks(rgb_frame)
        
        if not landmarks_list:
            return None
        
        landmarks = landmarks_list[0]
        
        # Check expression consistency
        expr_score = self._check_expression_consistency(landmarks)
        
        # Check boundary artifacts
        boundary_score = self._check_boundary_artifacts(frame, landmarks)
        
        # Check feature alignment
        align_score = self._check_feature_alignment(landmarks)
        
        self.prev_landmarks = landmarks
        
        return (expr_score, boundary_score, align_score)
    
    def _analyze_with_opencv(self, frame: np.ndarray) -> Optional[Tuple]:
        """Fallback analysis using OpenCV."""
        # Basic face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        
        # Simple heuristic scores
        return (0.7, 0.7, 0.7)
    
    def _check_expression_consistency(self, landmarks: Dict) -> float:
        """Check for micro-expression anomalies."""
        # Simplified check - in production, use more sophisticated methods
        score = 1.0
        
        # Check mouth symmetry
        if 'top_lip' in landmarks and 'bottom_lip' in landmarks:
            mouth_width = abs(landmarks['top_lip'][0][0] - landmarks['top_lip'][6][0])
            if mouth_width < 10:  # Unnaturally small
                score -= 0.3
        
        return max(0.0, score)
    
    def _check_boundary_artifacts(self, frame: np.ndarray, 
                                  landmarks: Dict) -> float:
        """Check for blurring/artifacts at face boundaries."""
        # Simplified - check color gradients at face edges
        score = 1.0
        
        # This is a placeholder - real implementation would analyze
        # gradient transitions at chin, hairline, etc.
        
        return score
    
    def _check_feature_alignment(self, landmarks: Dict) -> float:
        """Check alignment of facial features."""
        score = 1.0
        
        # Check eye symmetry
        if 'left_eye' in landmarks and 'right_eye' in landmarks:
            left_center = np.mean(landmarks['left_eye'], axis=0)
            right_center = np.mean(landmarks['right_eye'], axis=0)
            
            # Eyes should be roughly horizontal
            y_diff = abs(left_center[1] - right_center[1])
            if y_diff > 10:
                score -= 0.2
        
        return max(0.0, score)
