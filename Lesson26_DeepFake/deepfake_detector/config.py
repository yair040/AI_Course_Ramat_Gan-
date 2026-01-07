"""
Configuration management for DeepFake detector.
Author: Yair Levi
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict
import os


@dataclass
class AnalyzerConfig:
    """Configuration for individual analyzers."""
    enabled: bool = True
    weight: float = 1.0
    threshold: float = 0.5


@dataclass
class DetectorConfig:
    """Main configuration for DeepFake detector."""
    
    # Processing parameters
    frame_skip: int = 1
    batch_size: int = 16
    num_workers: int = 4
    
    # Paths (all relative)
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    log_dir: Path = field(init=False)
    models_dir: Path = field(init=False)
    venv_dir: Path = field(init=False)
    
    # Analyzer configurations
    analyzers: Dict[str, AnalyzerConfig] = field(default_factory=lambda: {
        'facial': AnalyzerConfig(enabled=True, weight=1.0, threshold=0.5),
        'temporal': AnalyzerConfig(enabled=True, weight=1.2, threshold=0.6),
        'metadata': AnalyzerConfig(enabled=True, weight=0.8, threshold=0.5),
        'lighting': AnalyzerConfig(enabled=True, weight=1.1, threshold=0.5),
        'geometry': AnalyzerConfig(enabled=True, weight=1.0, threshold=0.5),
        'ml': AnalyzerConfig(enabled=True, weight=1.5, threshold=0.7),
    })
    
    # ML settings
    use_gpu: bool = False
    model_download: bool = True
    
    # Logging
    log_level: str = 'INFO'
    console_log: bool = True
    file_log: bool = True
    
    # Output
    output_format: str = 'json'
    generate_heatmap: bool = False
    
    def __post_init__(self):
        """Initialize relative paths."""
        self.log_dir = self.project_root / 'log'
        self.models_dir = self.project_root / 'models'
        self.venv_dir = self.project_root / '..' / '..' / 'venv'
        
        # Create directories if they don't exist
        self.log_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        
        # Override from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        if os.getenv('DEEPFAKE_LOG_LEVEL'):
            self.log_level = os.getenv('DEEPFAKE_LOG_LEVEL')
        
        if os.getenv('DEEPFAKE_NUM_WORKERS'):
            self.num_workers = int(os.getenv('DEEPFAKE_NUM_WORKERS'))
        
        if os.getenv('DEEPFAKE_GPU_ENABLED'):
            self.use_gpu = os.getenv('DEEPFAKE_GPU_ENABLED').lower() == 'true'
        
        if os.getenv('DEEPFAKE_MODEL_DIR'):
            self.models_dir = Path(os.getenv('DEEPFAKE_MODEL_DIR'))
    
    def get_enabled_analyzers(self) -> list:
        """Return list of enabled analyzer names."""
        return [name for name, cfg in self.analyzers.items() if cfg.enabled]
    
    def get_analyzer_weight(self, name: str) -> float:
        """Get weight for specific analyzer."""
        return self.analyzers.get(name, AnalyzerConfig()).weight
    
    def get_analyzer_threshold(self, name: str) -> float:
        """Get threshold for specific analyzer."""
        return self.analyzers.get(name, AnalyzerConfig()).threshold
