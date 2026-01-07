"""
Machine learning-based deepfake detector.
Author: Yair Levi
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import torch
import torch.nn as nn
from ..utils.logger import get_logger


class MLDetector:
    """Machine learning ensemble for deepfake detection."""
    
    def __init__(self, models_dir: Path, threshold: float = 0.7, 
                 use_gpu: bool = False):
        """Initialize ML detector."""
        self.models_dir = Path(models_dir)
        self.threshold = threshold
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_gpu else 'cpu')
        self.logger = get_logger('ml_detector')
        
        # Model placeholders
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models."""
        try:
            # Check for model files
            model_files = {
                'face_swap': self.models_dir / 'face_swap_detector.pth',
                'lip_sync': self.models_dir / 'lip_sync_detector.pth',
                'gan': self.models_dir / 'gan_detector.pth',
            }
            
            # Load available models
            for name, path in model_files.items():
                if path.exists():
                    self.models[name] = self._load_model(path)
                    self.logger.info(f"Loaded model: {name}")
                else:
                    self.logger.warning(f"Model not found: {name}")
            
            if not self.models:
                self.logger.warning("No ML models loaded, using heuristic fallback")
        
        except Exception as e:
            self.logger.error(f"Model loading error: {e}")
    
    def _load_model(self, path: Path):
        """Load individual model (placeholder)."""
        # In production, this would load actual trained models
        # For now, return a simple placeholder
        return None
    
    def analyze(self, frames: List[np.ndarray]) -> Dict:
        """
        Run ML detection on frames.
        
        Args:
            frames: List of video frames
            
        Returns:
            Dictionary with ML detection scores
        """
        scores = {
            'face_swap_score': 0.0,
            'lip_sync_score': 0.0,
            'gan_score': 0.0,
            'ensemble_score': 0.0,
            'overall': 0.0,
        }
        
        if not frames:
            return scores
        
        try:
            # Process frames through models
            if self.models:
                face_swap_scores = []
                lip_sync_scores = []
                gan_scores = []
                
                for frame in frames:
                    # Preprocess frame
                    processed = self._preprocess_frame(frame)
                    
                    # Run through each model
                    if 'face_swap' in self.models:
                        fs_score = self._run_face_swap_detector(processed)
                        if fs_score is not None:
                            face_swap_scores.append(fs_score)
                    
                    if 'lip_sync' in self.models:
                        ls_score = self._run_lip_sync_detector(processed)
                        if ls_score is not None:
                            lip_sync_scores.append(ls_score)
                    
                    if 'gan' in self.models:
                        gan_score = self._run_gan_detector(processed)
                        if gan_score is not None:
                            gan_scores.append(gan_score)
                
                # Aggregate scores
                if face_swap_scores:
                    scores['face_swap_score'] = np.mean(face_swap_scores)
                if lip_sync_scores:
                    scores['lip_sync_score'] = np.mean(lip_sync_scores)
                if gan_scores:
                    scores['gan_score'] = np.mean(gan_scores)
                
                # Ensemble voting
                model_scores = [
                    scores['face_swap_score'],
                    scores['lip_sync_score'],
                    scores['gan_score']
                ]
                scores['ensemble_score'] = np.mean([s for s in model_scores if s > 0])
            else:
                # Fallback heuristic
                scores['ensemble_score'] = self._heuristic_detection(frames)
            
            scores['overall'] = scores['ensemble_score']
        
        except Exception as e:
            self.logger.error(f"ML detection error: {e}")
        
        return scores
    
    def _preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess frame for model input."""
        # Resize to standard size
        resized = cv2.resize(frame, (224, 224))
        
        # Normalize
        normalized = resized.astype(np.float32) / 255.0
        
        # Convert to tensor
        tensor = torch.from_numpy(normalized).permute(2, 0, 1).unsqueeze(0)
        
        return tensor.to(self.device)
    
    def _run_face_swap_detector(self, frame_tensor: torch.Tensor) -> Optional[float]:
        """Run face swap detection model."""
        # Placeholder - in production, run actual model inference
        return 0.75
    
    def _run_lip_sync_detector(self, frame_tensor: torch.Tensor) -> Optional[float]:
        """Run lip sync detection model."""
        # Placeholder
        return 0.80
    
    def _run_gan_detector(self, frame_tensor: torch.Tensor) -> Optional[float]:
        """Run GAN detection model."""
        # Placeholder
        return 0.70
    
    def _heuristic_detection(self, frames: List[np.ndarray]) -> float:
        """Fallback heuristic detection when no models available."""
        # Simple heuristic based on frame statistics
        scores = []
        
        for frame in frames[:min(len(frames), 10)]:  # Sample 10 frames
            # Calculate various statistics
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Frequency domain analysis
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = np.abs(fshift)
            
            # High frequency content (deepfakes often have artifacts)
            high_freq = np.mean(magnitude_spectrum[magnitude_spectrum.shape[0]//3:])
            
            # Normalize score
            score = min(high_freq / 1000.0, 1.0)
            scores.append(score)
        
        return np.mean(scores) if scores else 0.5
