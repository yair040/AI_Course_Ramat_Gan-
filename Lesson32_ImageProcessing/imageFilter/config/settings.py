"""
Configuration settings for image filter application.
Author: Yair Levi

Defines configuration classes for filters and application settings.
"""

import logging
from dataclasses import dataclass
from typing import Literal

FilterType = Literal['ideal', 'gaussian', 'butterworth']


@dataclass
class FilterConfig:
    """Base configuration for frequency filters."""
    filter_type: FilterType = 'ideal'
    
    def validate(self) -> bool:
        """Validate filter configuration."""
        return self.filter_type in ['ideal', 'gaussian', 'butterworth']


@dataclass
class HPFConfig(FilterConfig):
    """High-Pass Filter configuration."""
    cutoff: float = 30.0
    
    def validate(self) -> bool:
        """Validate HPF configuration."""
        if not super().validate():
            return False
        return 0.0 < self.cutoff < 100.0


@dataclass
class LPFConfig(FilterConfig):
    """Low-Pass Filter configuration."""
    cutoff: float = 30.0
    
    def validate(self) -> bool:
        """Validate LPF configuration."""
        if not super().validate():
            return False
        return 0.0 < self.cutoff < 100.0


@dataclass
class BPFConfig(FilterConfig):
    """Band-Pass Filter configuration."""
    low_cutoff: float = 20.0
    high_cutoff: float = 80.0
    
    def validate(self) -> bool:
        """Validate BPF configuration."""
        if not super().validate():
            return False
        if self.low_cutoff >= self.high_cutoff:
            return False
        return 0.0 < self.low_cutoff < self.high_cutoff < 100.0


@dataclass
class AppConfig:
    """Application-wide configuration."""
    log_level: int = logging.INFO
    max_image_size: int = 4096
    show_display: bool = True
    save_output: bool = True
    use_multiprocessing: bool = True
    num_processes: int = 4
    
    def validate(self) -> bool:
        """Validate application configuration."""
        if self.log_level not in [logging.DEBUG, logging.INFO, logging.WARNING, 
                                   logging.ERROR, logging.CRITICAL]:
            return False
        if self.max_image_size <= 0:
            return False
        if self.num_processes <= 0:
            return False
        return True


# Default configurations
DEFAULT_HPF_CONFIG = HPFConfig(cutoff=30.0)
DEFAULT_LPF_CONFIG = LPFConfig(cutoff=30.0)
DEFAULT_BPF_CONFIG = BPFConfig(low_cutoff=20.0, high_cutoff=80.0)
DEFAULT_APP_CONFIG = AppConfig()


def get_default_hpf_config() -> HPFConfig:
    """Get default HPF configuration."""
    return HPFConfig(cutoff=30.0)


def get_default_lpf_config() -> LPFConfig:
    """Get default LPF configuration."""
    return LPFConfig(cutoff=30.0)


def get_default_bpf_config() -> BPFConfig:
    """Get default BPF configuration."""
    return BPFConfig(low_cutoff=20.0, high_cutoff=80.0)


def get_default_app_config() -> AppConfig:
    """Get default application configuration."""
    return AppConfig()