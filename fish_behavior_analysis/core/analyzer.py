"""Main analyzer class combining all functionality."""

import os
import json
import numpy as np
import pandas as pd
import cv2
from typing import Dict, List, Tuple, Optional
import logging

from .frame_extractor import FrameExtractor
from .flow_processor import OpticalFlowProcessor
from ..utils.visualization import FlowVisualizer
from ..utils.file_utils import ResultsExporter
from ..config.settings import Config

logger = logging.getLogger(__name__)

class FishBehaviorAnalyzer:
    """Main class for fish behavior analysis."""
    
    def __init__(self, video_path: str, config: Optional[Config] = None):
        """
        Initialize fish behavior analyzer.
        
        Args:
            video_path: Path to input video
            config: Configuration object (uses defaults if None)
        """
        self.video_path = video_path
        self.config = config or Config()
        
        # Initialize components
        self.frame_extractor = FrameExtractor(
            video_path, 
            self.config.frame_skip, 
            self.config.frames_dir
        )
        self.flow_processor = OpticalFlowProcessor(
            self.config.frames_dir,
            self.config.flow_vis_dir
        )
        self.visualizer = FlowVisualizer()
        self.exporter = ResultsExporter(self.config.results_dir)
        
        # Analysis results
        self.analysis_results = {}
    
    def extract_frames(self, force_reextract: bool = False) -> int:
        """Extract frames from video."""
        return self.frame_extractor.extract_frames(force_reextract)
    
    def compute_optical_flow(self, visualize: bool = False, save_vis: bool = True) -> int:
        """Compute optical flow between frames."""
        return self.flow_processor.compute_optical_flow(visualize, save_vis)
    
    def analyze_behavior(self) -> Dict:
        """
        Analyze fish behavior patterns from optical flow.
        
        Returns:
            Dictionary containing analysis results
        """
        logger.info("Analyzing fish behavior patterns...")
        
        frame_files = self.flow_processor._get_frame_files()
        if len(frame_files) < 2:
            raise ValueError("Not enough frames for analysis.")
        
        avg_speeds = []
        all_angles = []
        sudden_changes = []
        heatmap = None
        
        for i in range(1, len(frame_files)):
            # Load frames
            frame = cv2.imread(frame_files[i])
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            prev_gray = cv2.cvtColor(
                cv2.imread(frame_files[i - 1]), 
                cv2.COLOR_BGR2GRAY
            )
            
            # Compute flow
            flow, magnitude = self.flow_processor.compute_flow_between_frames(
                prev_gray, gray
            )
            
            # Analyze speed
            avg_speed = np.mean(magnitude)
            avg_speeds.append(avg_speed)
            
            # Analyze directions (memory-efficient sampling)
            _, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            angle_flat = angle.flatten()
            sample_size = min(self.config.angle_sample_size, len(angle_flat))
            sample_indices = np.random.choice(
                len(angle_flat), size=sample_size, replace=False
            )
            sampled_angles = angle_flat[sample_indices]
            all_angles.extend(sampled_angles)
            
            # Build heatmap
            if heatmap is None:
                heatmap = magnitude.copy()
            else:
                heatmap += magnitude
            
            # Detect sudden changes
            if i > 1:
                speed_diff = abs(avg_speeds[-1] - avg_speeds[-2])
                if speed_diff > self.config.sudden_change_threshold:
                    sudden_changes.append({
                        'frame': i,
                        'speed_change': speed_diff,
                        'description': 'Possible snapping/grazing behavior'
                    })
                    logger.info(f"Sudden change detected at frame {i}!")
        
        # Store results
        self.analysis_results = {
            'avg_speeds': avg_speeds,
            'angles': all_angles,
            'sudden_changes': sudden_changes,
            'heatmap': heatmap,
            'metadata': {
                'video_path': self.video_path,
                'frame_skip': self.config.frame_skip,
                'frames_analyzed': len(avg_speeds),
                'sudden_changes_count': len(sudden_changes)
            }
        }
        
        logger.info(f"Analysis complete! Found {len(sudden_changes)} sudden changes.")
        return self.analysis_results
    
    def visualize_results(self, show_plots: bool = True, save_plots: bool = True):
        """Visualize analysis results."""
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze_behavior() first.")
        
        self.visualizer.plot_speed_timeline(
            self.analysis_results['avg_speeds'],
            show=show_plots,
            save_path=os.path.join(self.config.results_dir, "speed_timeline.png") if save_plots else None
        )
        
        self.visualizer.plot_direction_histogram(
            self.analysis_results['angles'],
            show=show_plots,
            save_path=os.path.join(self.config.results_dir, "direction_histogram.png") if save_plots else None
        )
        
        self.visualizer.show_movement_heatmap(
            self.analysis_results['heatmap'],
            show=show_plots,
            save_path=os.path.join(self.config.results_dir, "movement_heatmap.png") if save_plots else None
        )
    
    def export_results(self) -> Dict[str, str]:
        """Export analysis results to files."""
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze_behavior() first.")
        
        return self.exporter.export_all(self.analysis_results)
    
    def run_full_analysis(self, 
                         force_reextract: bool = False,
                         visualize_flow: bool = False,
                         show_plots: bool = True,
                         save_results: bool = True) -> Dict:
        """
        Run complete analysis pipeline.
        
        Args:
            force_reextract: Force frame re-extraction
            visualize_flow: Show optical flow in real-time
            show_plots: Display analysis plots
            save_results: Save all results to disk
            
        Returns:
            Analysis results dictionary
        """
        logger.info("Starting full fish behavior analysis pipeline...")
        
        # Step 1: Extract frames
        logger.info("Step 1: Extracting frames...")
        frame_count = self.extract_frames(force_reextract)
        logger.info(f"Frame extraction complete. {frame_count} frames available.")
        
        # Step 2: Compute optical flow
        logger.info("Step 2: Computing optical flow...")
        flow_count = self.compute_optical_flow(visualize_flow, save_results)
        logger.info(f"Optical flow computation complete. {flow_count} flows computed.")
        
        # Step 3: Analyze behavior
        logger.info("Step 3: Analyzing behavior patterns...")
        results = self.analyze_behavior()
        
        # Step 4: Visualize results
        logger.info("Step 4: Generating visualizations...")
        self.visualize_results(show_plots, save_results)
        
        # Step 5: Export results
        if save_results:
            logger.info("Step 5: Exporting results...")
            export_paths = self.export_results()
            logger.info(f"Results exported to: {export_paths}")
        
        logger.info("Full analysis pipeline complete!")
        return results