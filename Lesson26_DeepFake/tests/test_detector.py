"""
Unit tests for DeepFake detector.
Author: Yair Levi
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from deepfake_detector.config import DetectorConfig, AnalyzerConfig
from deepfake_detector.detector import DeepFakeDetector
from deepfake_detector.analyzers import FacialAnalyzer, TemporalAnalyzer


class TestConfig:
    """Test configuration classes."""
    
    def test_analyzer_config_defaults(self):
        """Test AnalyzerConfig default values."""
        config = AnalyzerConfig()
        assert config.enabled is True
        assert config.weight == 1.0
        assert config.threshold == 0.5
    
    def test_detector_config_initialization(self):
        """Test DetectorConfig initialization."""
        config = DetectorConfig()
        assert config.frame_skip == 1
        assert config.batch_size == 16
        assert config.num_workers == 4
        assert config.log_dir.exists()
    
    def test_enabled_analyzers(self):
        """Test getting enabled analyzers."""
        config = DetectorConfig()
        enabled = config.get_enabled_analyzers()
        assert 'facial' in enabled
        assert 'temporal' in enabled


class TestFacialAnalyzer:
    """Test facial analyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = FacialAnalyzer(threshold=0.6)
        assert analyzer.threshold == 0.6
    
    def test_analyze_empty_frames(self):
        """Test analysis with empty frame list."""
        analyzer = FacialAnalyzer()
        results = analyzer.analyze([])
        assert 'overall' in results
        assert results['overall'] == 0.0
    
    def test_analyze_with_frames(self):
        """Test analysis with sample frames."""
        analyzer = FacialAnalyzer()
        
        # Create dummy frames
        frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) 
                 for _ in range(5)]
        
        results = analyzer.analyze(frames)
        assert 'overall' in results
        assert 0.0 <= results['overall'] <= 1.0


class TestTemporalAnalyzer:
    """Test temporal analyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = TemporalAnalyzer(threshold=0.7)
        assert analyzer.threshold == 0.7
    
    def test_analyze_insufficient_frames(self):
        """Test with insufficient frames."""
        analyzer = TemporalAnalyzer()
        results = analyzer.analyze([np.zeros((480, 640, 3), dtype=np.uint8)])
        assert results['overall'] == 0.0
    
    def test_analyze_motion(self):
        """Test motion analysis."""
        analyzer = TemporalAnalyzer()
        
        # Create frames with motion
        frames = []
        for i in range(10):
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add moving square
            x = i * 10
            frame[200:250, x:x+50] = 255
            frames.append(frame)
        
        results = analyzer.analyze(frames)
        assert 'motion_consistency' in results


class TestDetector:
    """Test main detector."""
    
    def test_initialization(self):
        """Test detector initialization."""
        config = DetectorConfig()
        detector = DeepFakeDetector(config)
        assert len(detector.analyzers) > 0
    
    def test_calculate_verdict(self):
        """Test verdict calculation."""
        config = DetectorConfig()
        detector = DeepFakeDetector(config)
        
        # Test with high scores (likely real)
        scores = {
            'facial': 0.9,
            'temporal': 0.85,
            'lighting': 0.88,
        }
        confidence, verdict = detector._calculate_verdict(scores)
        assert verdict == 'REAL'
        assert confidence > 0.6
        
        # Test with low scores (likely fake)
        scores = {
            'facial': 0.3,
            'temporal': 0.25,
            'lighting': 0.35,
        }
        confidence, verdict = detector._calculate_verdict(scores)
        assert verdict == 'FAKE'
        assert confidence < 0.4


class TestVideoProcessing:
    """Test video processing utilities."""
    
    def test_metadata_extraction(self):
        """Test metadata extraction."""
        # This would require a real video file
        # Placeholder for now
        pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
