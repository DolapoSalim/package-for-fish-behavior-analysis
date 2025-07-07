"""Tests for main analyzer functionality."""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
import numpy as np

from fish_behavior_analysis.core.analyzer import FishBehaviorAnalyzer
from fish_behavior_analysis.config.settings import Config


class TestFishBehaviorAnalyzer:
    """Test cases for FishBehaviorAnalyzer class."""
    
    @patch('os.path.exists')
    def test_init_with_config(self, mock_exists):
        """Test initialization with custom config."""
        mock_exists.return_value = True
        
        config = Config(frame_skip=2, results_dir="custom_results")
        analyzer = FishBehaviorAnalyzer("test_video.mp4", config)
        
        assert analyzer.video_path == "test_video.mp4"
        assert analyzer.config.frame_skip == 2
        assert analyzer.config.results_dir == "custom_results"
    
    @patch('os.path.exists')
    def test_init_without_config(self, mock_exists):
        """Test initialization without config uses defaults."""
        mock_exists.return_value = True
        
        analyzer = FishBehaviorAnalyzer("test_video.mp4")
        
        assert analyzer.config.frame_skip == 1
        assert analyzer.config.results_dir == "results"
    
    @patch('os.path.exists')
    def test_analyze_behavior_with_insufficient_frames(self, mock_exists):
        """Test behavior analysis with insufficient frames."""
        mock_exists.return_value = True
        
        analyzer = FishBehaviorAnalyzer("test_video.mp4")
        
        with patch.object(analyzer.flow_processor, '_get_frame_files', return_value=[]):
            with pytest.raises(ValueError, match="Not enough frames"):
                analyzer.analyze_behavior()