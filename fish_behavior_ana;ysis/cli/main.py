"""Command-line interface for fish behavior analysis."""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from ..core.analyzer import FishBehaviorAnalyzer
from ..config.settings import Config

def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('fish_behavior_analysis.log')
        ]
    )

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Fish Behavior Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  fish-behavior-analysis video.mp4
  
  # Skip every 2nd frame and force re-extraction
  fish-behavior-analysis video.mp4 --frame-skip 2 --force-reextract
  
  # Custom output directory
  fish-behavior-analysis video.mp4 --results-dir my_results
  
  # Show optical flow visualization
  fish-behavior-analysis video.mp4 --visualize-flow
        """
    )
    
    # Required arguments
    parser.add_argument(
        'video_path',
        help='Path to input video file'
    )
    
    # Optional arguments
    parser.add_argument(
        '--frame-skip',
        type=int,
        default=1,
        help='Extract every nth frame (default: 1)'
    )
    
    parser.add_argument(
        '--frames-dir',
        default='frames',
        help='Directory to store extracted frames (default: frames)'
    )
    
    parser.add_argument(
        '--flow-vis-dir',
        default='flow_vis',
        help='Directory to store flow visualizations (default: flow_vis)'
    )
    
    parser.add_argument(
        '--results-dir',
        default='results',
        help='Directory to store analysis results (default: results)'
    )
    
    parser.add_argument(
        '--sudden-change-threshold',
        type=float,
        default=5.0,
        help='Threshold for detecting sudden speed changes (default: 5.0)'
    )
    
    parser.add_argument(
        '--force-reextract',
        action='store_true',
        help='Force re-extraction of frames even if they exist'
    )
    
    parser.add_argument(
        '--visualize-flow',
        action='store_true',
        help='Show optical flow visualization in real-time'
    )
    
    parser.add_argument(
        '--no-save-results',
        action='store_true',
        help='Do not save results to disk'
    )
    
    parser.add_argument(
        '--no-show-plots',
        action='store_true',
        help='Do not display plots'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Validate video path
        video_path = Path(args.video_path)
        if not video_path.exists():
            logger.error(f"Video file not found: {video_path}")
            sys.exit(1)
        
        # Create configuration
        config = Config(
            frame_skip=args.frame_skip,
            frames_dir=args.frames_dir,
            flow_vis_dir=args.flow_vis_dir,
            results_dir=args.results_dir,
            sudden_change_threshold=args.sudden_change_threshold
        )
        
        # Initialize analyzer
        analyzer = FishBehaviorAnalyzer(str(video_path), config)
        
        # Run analysis
        logger.info(f"Starting analysis of {video_path}")
        results = analyzer.run_full_analysis(
            force_reextract=args.force_reextract,
            visualize_flow=args.visualize_flow,
            show_plots=not args.no_show_plots,
            save_results=not args.no_save_results
        )
        
        # Print summary
        logger.info("Analysis Summary:")
        logger.info(f"  Frames analyzed: {results['metadata']['frames_analyzed']}")
        logger.info(f"  Sudden changes detected: {len(results['sudden_changes'])}")
        logger.info(f"  Average speed: {sum(results['avg_speeds'])/len(results['avg_speeds']):.2f} pixels/frame")
        
        logger.info("Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()