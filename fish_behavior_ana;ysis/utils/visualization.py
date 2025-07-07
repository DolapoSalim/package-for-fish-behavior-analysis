"""Visualization utilities for analysis results."""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class FlowVisualizer:
    """Handles visualization of analysis results."""
    
    def __init__(self, figsize: tuple = (10, 6)):
        """
        Initialize visualizer.
        
        Args:
            figsize: Default figure size for plots
        """
        self.figsize = figsize
        plt.style.use('default')
    
    def plot_speed_timeline(self, 
                          speeds: List[float], 
                          show: bool = True, 
                          save_path: Optional[str] = None,
                          title: str = "Fish Average Swim Speed Over Time"):
        """
        Plot speed timeline.
        
        Args:
            speeds: List of average speeds per frame
            show: Whether to display the plot
            save_path: Path to save the plot
            title: Plot title
        """
        plt.figure(figsize=self.figsize)
        plt.plot(speeds, label="Average swim speed", linewidth=2)
        plt.xlabel("Frame")
        plt.ylabel("Average speed (pixels/frame)")
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Speed timeline saved to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_direction_histogram(self, 
                               angles: List[float], 
                               show: bool = True, 
                               save_path: Optional[str] = None,
                               bins: int = 36,
                               title: str = "Preferred Swim Directions"):
        """
        Plot direction histogram.
        
        Args:
            angles: List of angle values in radians
            show: Whether to display the plot
            save_path: Path to save the plot
            bins: Number of histogram bins
            title: Plot title
        """
        angles_deg = (np.degrees(np.array(angles)) + 360) % 360
        
        plt.figure(figsize=(8, 6))
        plt.hist(angles_deg, bins=bins, range=(0, 360), 
                color='purple', alpha=0.7, edgecolor='black')
        plt.xlabel("Direction (degrees)")
        plt.ylabel("Frequency")
        plt.title(title)
        plt.grid(True, alpha=0.3)
        
        # Add directional labels
        plt.xticks([0, 90, 180, 270, 360], 
                  ['E', 'N', 'W', 'S', 'E'])
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Direction histogram saved to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def show_movement_heatmap(self, 
                            heatmap: np.ndarray, 
                            show: bool = True, 
                            save_path: Optional[str] = None,
                            colormap: int = cv2.COLORMAP_JET,
                            title: str = "Movement Heatmap"):
        """
        Display movement heatmap.
        
        Args:
            heatmap: Accumulated movement magnitude
            show: Whether to display the heatmap
            save_path: Path to save the heatmap
            colormap: OpenCV colormap to use
            title: Window title
        """
        heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        colored_heatmap = cv2.applyColorMap(heatmap_norm, colormap)
        
        if save_path:
            cv2.imwrite(save_path, colored_heatmap)
            logger.info(f"Movement heatmap saved to {save_path}")
        
        if show:
            cv2.imshow(title, colored_heatmap)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    def plot_sudden_changes(self, 
                          speeds: List[float], 
                          change_frames: List[int],
                          show: bool = True, 
                          save_path: Optional[str] = None):
        """
        Plot speed timeline with sudden changes highlighted.
        
        Args:
            speeds: List of average speeds
            change_frames: Frame indices where sudden changes occurred
            show: Whether to display the plot
            save_path: Path to save the plot
        """
        plt.figure(figsize=self.figsize)
        plt.plot(speeds, label="Average swim speed", linewidth=2)
        
        # Highlight sudden changes
        for frame in change_frames:
            if frame < len(speeds):
                plt.axvline(x=frame, color='red', linestyle='--', alpha=0.7)
                plt.scatter(frame, speeds[frame], color='red', s=100, zorder=5)
        
        plt.xlabel("Frame")
        plt.ylabel("Average speed (pixels/frame)")
        plt.title("Fish Speed with Sudden Changes Highlighted")
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Sudden changes plot saved to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()