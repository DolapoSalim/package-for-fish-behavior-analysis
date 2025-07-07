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