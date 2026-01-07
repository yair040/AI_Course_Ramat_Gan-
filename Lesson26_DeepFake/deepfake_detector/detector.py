"""
Main DeepFake detector orchestrator.
Author: Yair Levi
"""

import time
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
from multiprocessing import Pool, cpu_count
from .config import DetectorConfig
from .utils import VideoProcessor, get_logger
from .analyzers import (
    FacialAnalyzer, TemporalAnalyzer, MetadataAnalyzer,
    LightingAnalyzer, GeometryAnalyzer, MLDetector
)


class DeepFakeDetector:
    """Main orchestrator for deepfake detection."""
    
    def __init__(self, config: DetectorConfig = None):
        """Initialize detector with configuration."""
        self.config = config or DetectorConfig()
        self.logger = get_logger('detector')
        
        # Initialize analyzers
        self.analyzers = self._init_analyzers()
        
        self.logger.info(f"Initialized detector with {len(self.analyzers)} analyzers")
    
    def _init_analyzers(self) -> Dict:
        """Initialize all enabled analyzers."""
        analyzers = {}
        
        if self.config.analyzers['facial'].enabled:
            analyzers['facial'] = FacialAnalyzer(
                threshold=self.config.get_analyzer_threshold('facial')
            )
        
        if self.config.analyzers['temporal'].enabled:
            analyzers['temporal'] = TemporalAnalyzer(
                threshold=self.config.get_analyzer_threshold('temporal')
            )
        
        if self.config.analyzers['metadata'].enabled:
            analyzers['metadata'] = MetadataAnalyzer(
                threshold=self.config.get_analyzer_threshold('metadata')
            )
        
        if self.config.analyzers['lighting'].enabled:
            analyzers['lighting'] = LightingAnalyzer(
                threshold=self.config.get_analyzer_threshold('lighting')
            )
        
        if self.config.analyzers['geometry'].enabled:
            analyzers['geometry'] = GeometryAnalyzer(
                threshold=self.config.get_analyzer_threshold('geometry')
            )
        
        if self.config.analyzers['ml'].enabled:
            analyzers['ml'] = MLDetector(
                models_dir=self.config.models_dir,
                threshold=self.config.get_analyzer_threshold('ml'),
                use_gpu=self.config.use_gpu
            )
        
        return analyzers
    
    def analyze(self, video_path: Path) -> Dict[str, Any]:
        """
        Analyze video for deepfake detection.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with detection results
        """
        start_time = time.time()
        video_path = Path(video_path)
        
        self.logger.info(f"Starting analysis: {video_path.name}")
        
        # Initialize result structure
        results = {
            'video_path': str(video_path),
            'verdict': 'UNKNOWN',
            'confidence': 0.0,
            'scores': {},
            'anomalies': [],
            'metadata': {},
            'processing_time': 0.0,
        }
        
        try:
            # Extract video frames
            with VideoProcessor(video_path, self.config.frame_skip) as vp:
                results['metadata'] = vp.metadata
                
                # Collect frames in batches
                frame_batches = self._collect_frame_batches(vp)
                
                # Run analyzers
                analyzer_results = self._run_analyzers(frame_batches, video_path)
                
                # Aggregate results
                results['scores'] = analyzer_results
                results['confidence'], results['verdict'] = self._calculate_verdict(
                    analyzer_results
                )
                
                # Detect anomalies
                results['anomalies'] = self._detect_anomalies(
                    frame_batches, analyzer_results
                )
            
            results['processing_time'] = time.time() - start_time
            
            self.logger.info(
                f"Analysis complete: {results['verdict']} "
                f"({results['confidence']:.2%} confidence) "
                f"in {results['processing_time']:.2f}s"
            )
        
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}", exc_info=True)
            results['error'] = str(e)
        
        return results
    
    def _collect_frame_batches(self, vp: VideoProcessor) -> List[List]:
        """Collect frames in batches."""
        batches = []
        current_batch = []
        
        for frame_num, timestamp, frame in vp.read_frames():
            current_batch.append((frame_num, timestamp, frame))
            
            if len(current_batch) >= self.config.batch_size:
                batches.append(current_batch)
                current_batch = []
        
        if current_batch:
            batches.append(current_batch)
        
        self.logger.info(f"Collected {len(batches)} batches")
        return batches
    
    def _run_analyzers(self, frame_batches: List[List], 
                      video_path: Path) -> Dict:
        """Run all analyzers on frame batches."""
        all_scores = {}
        
        # Extract just frames from batches for analysis
        all_frames = [frame for batch in frame_batches 
                     for _, _, frame in batch]
        
        # Run frame-based analyzers
        for name, analyzer in self.analyzers.items():
            if name == 'metadata':
                continue  # Handle separately
            
            try:
                self.logger.info(f"Running {name} analyzer...")
                scores = analyzer.analyze(all_frames)
                all_scores[name] = scores.get('overall', 0.0)
            except Exception as e:
                self.logger.error(f"{name} analyzer failed: {e}")
                all_scores[name] = 0.5  # Neutral score on failure
        
        # Run metadata analyzer
        if 'metadata' in self.analyzers:
            try:
                self.logger.info("Running metadata analyzer...")
                scores = self.analyzers['metadata'].analyze(video_path)
                all_scores['metadata'] = scores.get('overall', 0.0)
            except Exception as e:
                self.logger.error(f"Metadata analyzer failed: {e}")
                all_scores['metadata'] = 0.5
        
        return all_scores
    
    def _calculate_verdict(self, scores: Dict) -> tuple:
        """Calculate overall verdict and confidence."""
        if not scores:
            return 0.5, 'UNKNOWN'
        
        # Weighted average
        weighted_sum = 0.0
        total_weight = 0.0
        
        for name, score in scores.items():
            weight = self.config.get_analyzer_weight(name)
            weighted_sum += score * weight
            total_weight += weight
        
        confidence = weighted_sum / total_weight if total_weight > 0 else 0.5
        
        # Determine verdict
        # Lower score = more likely fake (inverted for intuitive reading)
        if confidence < 0.4:
            verdict = 'FAKE'
        elif confidence > 0.6:
            verdict = 'REAL'
        else:
            verdict = 'UNCERTAIN'
        
        return confidence, verdict
    
    def _detect_anomalies(self, frame_batches: List[List], 
                         scores: Dict) -> List[Dict]:
        """Detect and report anomalies."""
        anomalies = []
        
        # Check for low scores in specific analyzers
        for name, score in scores.items():
            threshold = self.config.get_analyzer_threshold(name)
            if score < threshold:
                anomalies.append({
                    'timestamp': 0.0,
                    'frame': 0,
                    'type': f'{name}_anomaly',
                    'severity': 'high' if score < threshold * 0.5 else 'medium',
                    'description': f'{name} score below threshold: {score:.2f}'
                })
        
        return anomalies
