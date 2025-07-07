"""
Fish Behavior Analysis Package

A comprehensive toolkit for analyzing fish behavior in video recordings using 
optical flow and computer vision techniques.
"""

__version__ = "0.1.0"
__author__ = "dolapo_salim"
__email__ = "dolaposalim@gmail.com"

from .core.analyzer import FishBehaviorAnalyzer
from .core.flow_processor import OpticalFlowProcessor
from .core.frame_extractor import FrameExtractor
from .utils.visualization import FlowVisualizer
from .config.settings import Config

__all__ = [
    'FishBehaviorAnalyzer',
    'OpticalFlowProcessor', 
    'FrameExtractor',
    'FlowVisualizer',
    'Config'
]
