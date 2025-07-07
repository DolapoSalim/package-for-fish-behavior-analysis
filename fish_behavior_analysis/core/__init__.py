"""Core modules for fish behavior analysis."""

from .analyzer import FishBehaviorAnalyzer
from .flow_processor import OpticalFlowProcessor
from .frame_extractor import FrameExtractor

__all__ = ['FishBehaviorAnalyzer', 'OpticalFlowProcessor', 'FrameExtractor']