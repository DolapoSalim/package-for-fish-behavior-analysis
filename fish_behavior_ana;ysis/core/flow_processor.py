"""Optical flow computation and processing."""

import os
import cv2
import numpy as np
from glob import glob
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class OpticalFlowProcessor:
    """Handles optical flow computation and visualization."""
    
    def __init__(self, frames_dir: str = "frames", flow_vis_dir: str = "flow_vis"):
        """
        Initialize optical flow processor.
        
        Args:
            frames_dir: Directory containing extracted frames
            flow_vis_dir: Directory to save flow visualizations
        """
        self.frames_dir = frames_dir
        self.flow_vis_dir = flow_vis_dir
        self.flow_params = {
            'pyr_scale': 0.5,
            'levels': 3,
            'winsize': 15,
            'iterations': 3,
            'poly_n': 5,
            'poly_sigma': 1.2,
            'flags': 0
        }
    
    def compute_optical_flow(self, visualize: bool = True, save_vis: bool = True) -> int:
        """
        Compute dense optical flow between frames.
        
        Args:
            visualize: Show flow visualization in real-time
            save_vis: Save flow visualizations to disk
            
        Returns:
            Number of flow computations performed
        """
        frame_files = self._get_frame_files()
        if len(frame_files) < 2:
            raise ValueError("Need at least two frames to compute optical flow.")
        
        if save_vis:
            os.makedirs(self.flow_vis_dir, exist_ok=True)
        
        logger.info("Computing dense optical flow from saved frames...")
        
        prev_frame = cv2.imread(frame_files[0])
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        flow_count = 0
        
        for i in range(1, len(frame_files)):
            frame = cv2.imread(frame_files[i])
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None, **self.flow_params
            )
            
            flow_img = self._visualize_flow(flow, frame)
            
            if visualize:
                cv2.imshow("Dense Optical Flow", flow_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            if save_vis:
                flow_filename = os.path.join(self.flow_vis_dir, f"flow_{i:05d}.png")
                cv2.imwrite(flow_filename, flow_img)
            
            prev_gray = gray
            flow_count += 1
        
        cv2.destroyAllWindows()
        logger.info(f"Computed optical flow for {flow_count} frame pairs.")
        return flow_count
    
    def _get_frame_files(self) -> list:
        """Get sorted list of frame files."""
        return sorted(glob(os.path.join(self.frames_dir, "*.png")))
    
    def _visualize_flow(self, flow: np.ndarray, frame: np.ndarray) -> np.ndarray:
        """Create HSV visualization of optical flow."""
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        
        hsv = np.zeros_like(frame)
        hsv[..., 1] = 255
        hsv[..., 0] = angle * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def compute_flow_between_frames(self, frame1: np.ndarray, frame2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute optical flow between two specific frames.
        
        Args:
            frame1: First frame (grayscale)
            frame2: Second frame (grayscale)
            
        Returns:
            Tuple of (flow, magnitude)
        """
        flow = cv2.calcOpticalFlowFarneback(
            frame1, frame2, None, **self.flow_params
        )
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        return flow, magnitude