"""Frame extraction functionality."""

import os
import cv2
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FrameExtractor:
    """Handles video frame extraction and management."""
    
    def __init__(self, video_path: str, frame_skip: int = 1, frames_dir: str = "frames"):
        """
        Initialize frame extractor.
        
        Args:
            video_path: Path to input video file
            frame_skip: Extract every nth frame (default: 1)
            frames_dir: Directory to save extracted frames
        """
        self.video_path = video_path
        self.frame_skip = frame_skip
        self.frames_dir = frames_dir
        self._validate_video_path()
    
    def _validate_video_path(self):
        """Validate that video file exists."""
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
    
    def extract_frames(self, force_reextract: bool = False) -> int:
        """
        Extract frames from video and save as images.
        
        Args:
            force_reextract: Force re-extraction even if frames exist
            
        Returns:
            Number of frames extracted
        """
        if not force_reextract and self._frames_exist():
            logger.info(f"Frames already exist in '{self.frames_dir}'. Skipping extraction.")
            return len(self._get_existing_frames())
        
        os.makedirs(self.frames_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video {self.video_path}")
        
        frame_idx, saved_count = 0, 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_idx % self.frame_skip == 0:
                    frame_filename = os.path.join(
                        self.frames_dir, f"frame_{saved_count:05d}.png"
                    )
                    cv2.imwrite(frame_filename, frame)
                    saved_count += 1
                    
                frame_idx += 1
        finally:
            cap.release()
        
        logger.info(f"Extracted and saved {saved_count} frames in '{self.frames_dir}'.")
        return saved_count
    
    def _frames_exist(self) -> bool:
        """Check if frames already exist."""
        if not os.path.exists(self.frames_dir):
            return False
        return len(self._get_existing_frames()) > 0
    
    def _get_existing_frames(self) -> list:
        """Get list of existing frame files."""
        if not os.path.exists(self.frames_dir):
            return []
        return [f for f in os.listdir(self.frames_dir) if f.endswith(".png")]
    
    def get_frame_count(self) -> int:
        """Get total number of extracted frames."""
        return len(self._get_existing_frames())