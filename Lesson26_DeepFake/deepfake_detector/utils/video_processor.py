"""
Video frame extraction and processing utilities.
Author: Yair Levi
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Iterator, Tuple, Optional, Dict
from .logger import get_logger


class VideoProcessor:
    """Handles video frame extraction and metadata."""
    
    def __init__(self, video_path: Path, frame_skip: int = 1):
        """Initialize video processor."""
        self.video_path = Path(video_path)
        self.frame_skip = frame_skip
        self.logger = get_logger('video_processor')
        
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")
        
        self.metadata = self._extract_metadata()
        self.logger.info(f"Loaded video: {self.video_path.name}, "
                        f"{self.metadata['width']}x{self.metadata['height']}, "
                        f"{self.metadata['fps']:.2f} FPS, "
                        f"{self.metadata['duration']:.2f}s")
    
    def _extract_metadata(self) -> Dict:
        """Extract video metadata."""
        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration': self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / 
                       max(self.cap.get(cv2.CAP_PROP_FPS), 1),
            'codec': int(self.cap.get(cv2.CAP_PROP_FOURCC)),
        }
    
    def read_frames(self) -> Iterator[Tuple[int, float, np.ndarray]]:
        """
        Generator that yields frames.
        
        Yields:
            Tuple of (frame_number, timestamp, frame_array)
        """
        frame_num = 0
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                if frame_num % self.frame_skip == 0:
                    timestamp = frame_num / self.metadata['fps']
                    yield (frame_num, timestamp, frame)
                
                frame_num += 1
        finally:
            self.release()
    
    def get_frame_at(self, frame_number: int) -> Optional[np.ndarray]:
        """Get specific frame by number."""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def get_frame_batch(self, start: int, count: int) -> list:
        """Get batch of consecutive frames."""
        frames = []
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        
        for _ in range(count):
            ret, frame = self.cap.read()
            if not ret:
                break
            frames.append(frame)
        
        return frames
    
    def release(self):
        """Release video capture resources."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.logger.debug(f"Released video: {self.video_path.name}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()
    
    def __del__(self):
        """Ensure resources are released."""
        self.release()
