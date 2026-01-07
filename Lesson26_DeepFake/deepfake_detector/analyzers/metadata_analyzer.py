"""
Video metadata and compression artifact analyzer.
Author: Yair Levi
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
try:
    from pymediainfo import MediaInfo
    MEDIAINFO_AVAILABLE = True
except ImportError:
    MEDIAINFO_AVAILABLE = False
from ..utils.logger import get_logger


class MetadataAnalyzer:
    """Analyzes video metadata for inconsistencies."""
    
    def __init__(self, threshold: float = 0.5):
        """Initialize metadata analyzer."""
        self.threshold = threshold
        self.logger = get_logger('metadata_analyzer')
        
        if not MEDIAINFO_AVAILABLE:
            self.logger.warning("pymediainfo not available, using OpenCV only")
    
    def analyze(self, video_path: Path) -> Dict:
        """
        Analyze video metadata.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with metadata scores
        """
        scores = {
            'timestamp_consistency': 0.0,
            'codec_integrity': 0.0,
            're_encoding_detection': 0.0,
            'overall': 0.0,
        }
        
        try:
            # Extract metadata
            metadata = self._extract_metadata(video_path)
            
            # Analyze timestamps
            scores['timestamp_consistency'] = self._check_timestamps(metadata)
            
            # Check codec integrity
            scores['codec_integrity'] = self._check_codec(metadata)
            
            # Detect re-encoding
            scores['re_encoding_detection'] = self._detect_reencoding(metadata)
            
            # Overall score
            scores['overall'] = np.mean([
                scores['timestamp_consistency'],
                scores['codec_integrity'],
                scores['re_encoding_detection']
            ])
        
        except Exception as e:
            self.logger.error(f"Metadata analysis error: {e}")
        
        return scores
    
    def _extract_metadata(self, video_path: Path) -> Dict:
        """Extract video metadata."""
        metadata = {}
        
        # OpenCV metadata
        cap = cv2.VideoCapture(str(video_path))
        if cap.isOpened():
            metadata['opencv'] = {
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fourcc': int(cap.get(cv2.CAP_PROP_FOURCC)),
            }
            cap.release()
        
        # File system metadata
        stat = video_path.stat()
        metadata['file'] = {
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
        }
        
        # MediaInfo metadata (if available)
        if MEDIAINFO_AVAILABLE:
            try:
                media_info = MediaInfo.parse(str(video_path))
                metadata['mediainfo'] = self._parse_mediainfo(media_info)
            except Exception as e:
                self.logger.debug(f"MediaInfo parsing error: {e}")
        
        return metadata
    
    def _parse_mediainfo(self, media_info) -> Dict:
        """Parse MediaInfo object."""
        info = {}
        
        for track in media_info.tracks:
            if track.track_type == 'Video':
                info['video'] = {
                    'codec': track.codec,
                    'bitrate': track.bit_rate,
                    'encoding_settings': track.encoding_settings,
                }
            elif track.track_type == 'General':
                info['general'] = {
                    'format': track.format,
                    'file_size': track.file_size,
                    'duration': track.duration,
                }
        
        return info
    
    def _check_timestamps(self, metadata: Dict) -> float:
        """Check timestamp consistency."""
        score = 1.0
        
        try:
            file_meta = metadata.get('file', {})
            created = file_meta.get('created')
            modified = file_meta.get('modified')
            
            if created and modified:
                # If modified is before created, suspicious
                if modified < created:
                    score -= 0.5
                    self.logger.warning("Modified timestamp before created timestamp")
                
                # If modified much later than created, might indicate editing
                time_diff = (modified - created).total_seconds()
                if time_diff > 3600:  # More than 1 hour
                    score -= 0.2
        
        except Exception as e:
            self.logger.debug(f"Timestamp check error: {e}")
        
        return max(0.0, score)
    
    def _check_codec(self, metadata: Dict) -> float:
        """Check codec integrity."""
        score = 1.0
        
        try:
            opencv_meta = metadata.get('opencv', {})
            fourcc = opencv_meta.get('fourcc', 0)
            
            # Check for common deepfake codecs
            # This is simplified - real implementation would be more sophisticated
            if fourcc == 0:
                score -= 0.3
        
        except Exception as e:
            self.logger.debug(f"Codec check error: {e}")
        
        return max(0.0, score)
    
    def _detect_reencoding(self, metadata: Dict) -> float:
        """Detect signs of re-encoding."""
        score = 1.0
        
        try:
            # Check for encoding settings that indicate re-encoding
            if MEDIAINFO_AVAILABLE:
                mediainfo_meta = metadata.get('mediainfo', {})
                video_info = mediainfo_meta.get('video', {})
                encoding_settings = video_info.get('encoding_settings', '')
                
                # Multiple encoding passes are suspicious
                if 'x264' in encoding_settings and 'pass' in encoding_settings:
                    score -= 0.2
        
        except Exception as e:
            self.logger.debug(f"Re-encoding detection error: {e}")
        
        return max(0.0, score)
