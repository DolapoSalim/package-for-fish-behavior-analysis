"""File handling utilities."""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class ResultsExporter:
    """Handles exporting analysis results to various formats."""
    
    def __init__(self, results_dir: str = "results"):
        """
        Initialize results exporter.
        
        Args:
            results_dir: Directory to save results
        """
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)
    
    def export_speeds_csv(self, speeds: List[float]) -> str:
        """
        Export speed data to CSV.
        
        Args:
            speeds: List of average speeds
            
        Returns:
            Path to saved CSV file
        """
        df_speed = pd.DataFrame({
            "frame_idx": list(range(1, len(speeds) + 1)),
            "average_speed": speeds
        })
        
        csv_path = os.path.join(self.results_dir, "average_speeds.csv")
        df_speed.to_csv(csv_path, index=False)
        logger.info(f"Speed data exported to {csv_path}")
        
        return csv_path
    
    def export_directions_json(self, angles: List[float], bins: int = 36) -> str:
        """
        Export direction histogram to JSON.
        
        Args:
            angles: List of angle values in radians
            bins: Number of histogram bins
            
        Returns:
            Path to saved JSON file
        """
        angles_deg = (np.degrees(np.array(angles)) + 360) % 360
        hist, bin_edges = np.histogram(angles_deg, bins=bins, range=(0, 360))
        
        hist_data = {
            "angle_bins": bin_edges.tolist(),
            "counts": hist.tolist(),
            "total_samples": len(angles)
        }
        
        json_path = os.path.join(self.results_dir, "direction_histogram.json")
        with open(json_path, "w") as f:
            json.dump(hist_data, f, indent=2)
        
        logger.info(f"Direction histogram exported to {json_path}")
        return json_path
    
    def export_sudden_changes_json(self, changes: List[Dict]) -> str:
        """
        Export sudden changes data to JSON.
        
        Args:
            changes: List of sudden change events
            
        Returns:
            Path to saved JSON file
        """
        json_path = os.path.join(self.results_dir, "sudden_changes.json")
        with open(json_path, "w") as f:
            json.dump(changes, f, indent=2)
        
        logger.info(f"Sudden changes exported to {json_path}")
        return json_path
    
    def export_metadata_json(self, metadata: Dict[str, Any]) -> str:
        """
        Export analysis metadata to JSON.
        
        Args:
            metadata: Analysis metadata dictionary
            
        Returns:
            Path to saved JSON file
        """
        json_path = os.path.join(self.results_dir, "analysis_metadata.json")
        with open(json_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Metadata exported to {json_path}")
        return json_path
    
    def export_all(self, results: Dict[str, Any]) -> Dict[str, str]:
        """
        Export all analysis results.
        
        Args:
            results: Complete analysis results dictionary
            
        Returns:
            Dictionary of export paths
        """
        export_paths = {}
        
        # Export speeds
        export_paths['speeds_csv'] = self.export_speeds_csv(results['avg_speeds'])
        
        # Export directions
        export_paths['directions_json'] = self.export_directions_json(results['angles'])
        
        # Export sudden changes
        export_paths['changes_json'] = self.export_sudden_changes_json(results['sudden_changes'])
        
        # Export metadata
        export_paths['metadata_json'] = self.export_metadata_json(results['metadata'])
        
        # Export summary statistics
        export_paths['summary_json'] = self.export_summary_stats(results)
        
        return export_paths
    
    def export_summary_stats(self, results: Dict[str, Any]) -> str:
        """
        Export summary statistics.
        
        Args:
            results: Analysis results dictionary
            
        Returns:
            Path to saved JSON file
        """
        speeds = results['avg_speeds']
        angles = results['angles']
        
        summary = {
            "speed_statistics": {
                "mean": float(np.mean(speeds)),
                "std": float(np.std(speeds)),
                "min": float(np.min(speeds)),
                "max": float(np.max(speeds)),
                "median": float(np.median(speeds))
            },
            "direction_statistics": {
                "total_samples": len(angles),
                "mean_direction_deg": float(np.degrees(np.mean(angles))),
                "direction_variance": float(np.var(angles))
            },
            "behavior_events": {
                "sudden_changes_count": len(results['sudden_changes']),
                "sudden_changes_rate": len(results['sudden_changes']) / len(speeds) if speeds else 0
            }
        }
        
        json_path = os.path.join(self.results_dir, "summary_statistics.json")
        with open(json_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary statistics exported to {json_path}")
        return json_path