"""Tests for frame extraction functionality."""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
import cv2
import numpy as np

from fish_behavior_analysis.core.frame_extractor import FrameExtractor


class TestFrameExtractor:
    """Test cases for FrameExtractor class."""
    
    def test_init_with_nonexistent_video(self):
        """Test initialization with non-existent video file."""
        with pytest.raises(FileNotFoundError):
            FrameExtractor("nonexistent_video.mp4")
    
    @patch('cv2.VideoCapture')
    @patch('os.path.exists')
    def test_init_with_existing_video(self, mock_exists, mock_cap):
        """Test initialization with existing video file."""
        mock_exists.return_value = True
        
        extractor = FrameExtractor("test_video.mp4", frame_skip=2)
        
        assert extractor.video_path == "test_video.mp4"
        assert extractor.frame_skip == 2
        assert extractor.frames_dir == "frames"
    
    @patch('cv2.VideoCapture')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('cv2.imwrite')
    def test_extract_frames_success(self, mock_imwrite, mock_makedirs, mock_exists, mock_cap):
        """Test successful frame extraction."""
        mock_exists.return_value = True
        
        # Mock video capture
        mock_cap_instance = MagicMock()
        mock_cap.return_value = mock_cap_instance
        mock_cap_instance.isOpened.return_value = True
        
        # Mock frame reading
        mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap_instance.read.side_effect = [
            (True, mock_frame),
            (True, mock_frame),
            (False, None)
        ]
        
        extractor = FrameExtractor("test_video.mp4", frame_skip=1)
        
        with patch.object(extractor, '_frames_exist', return_value=False):
            frame_count = extractor.extract_frames()
        
        assert frame_count == 2
        assert mock_imwrite.call_count == 2
        mock_cap_instance.release.assert_called_once()
