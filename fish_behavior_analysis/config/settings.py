"""Configuration settings for fish behavior analysis."""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Config:
    """Configuration class for fish behavior analysis."""
    
    # Frame extraction settings
    frame_skip: int = 1
    frames_dir: str = "frames"
    
    # Optical flow settings
    flow_vis_dir: str = "flow_vis"
    flow_params: Dict[str, Any] = None
    
    # Analysis settings
    results_dir: str = "results"
    angle_sample_size: int = 1000
    sudden_change_threshold: float = 5.0
    
    # Visualization settings
    plot_figsize: tuple = (10, 6)
    plot_dpi: int = 300
    
    def __post_init__(self):
        """Initialize default flow parameters if not provided."""
        if self.flow_params is None:
            self.flow_params = {
                'pyr_scale': 0.5,
                'levels': 3,
                'winsize': 15,
                'iterations': 3,
                'poly_n': 5,
                'poly_sigma': 1.2,
                'flags': 0
            }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create Config from dictionary."""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Config to dictionary."""
        return {
            'frame_skip': self.frame_skip,
            'frames_dir': self.frames_dir,
            'flow_vis_dir': self.flow_vis_dir,
            'flow_params': self.flow_params,
            'results_dir': self.results_dir,
            'angle_sample_size': self.angle_sample_size,
            'sudden_change_threshold': self.sudden_change_threshold,
            'plot_figsize': self.plot_figsize,
            'plot_dpi': self.plot_dpi
        }