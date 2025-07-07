# Fish Behavior Analysis

A comprehensive Python toolkit for analyzing fish behavior in video recordings using optical flow and computer vision techniques.

## Features

- **Frame Extraction**: Efficient extraction of video frames with configurable skipping
- **Optical Flow Analysis**: Dense optical flow computation using Farneback algorithm
- **Behavior Pattern Detection**: Identification of sudden movement changes and feeding behaviors
- **Visualization**: Rich plotting and heatmap generation for analysis results
- **Export Capabilities**: CSV, JSON export of all analysis results
- **Command Line Interface**: Easy-to-use CLI for batch processing
- **Configurable Parameters**: Flexible configuration system for different use cases

## Installation

### From PyPI (recommended)
```bash
pip install fish-behavior-analysis
```

### From source
```bash
git clone https://github.com/DolapoSalim/package-for-fish-behavior-analysis.git
cd fish-behavior-analysis
pip install -e .
```

### Development installation
```bash
git clone https://github.com/DolapoSalim/package-for-fish-behavior-analysis.git
cd fish-behavior-analysis
pip install -e ".[dev]"
```

## Quick Start

### Command Line Usage

```bash
# Basic analysis
fish-behavior-analysis video.mp4

# Skip every 2nd frame
fish-behavior-analysis video.mp4 --frame-skip 2

# Custom output directory
fish-behavior-analysis video.mp4 --results-dir my_results

# Show optical flow visualization
fish-behavior-analysis video.mp4 --visualize-flow
```

### Python API Usage

```python
from fish_behavior_analysis import FishBehaviorAnalyzer, Config

# Create analyzer with custom configuration
config = Config(
    frame_skip=2,
    sudden_change_threshold=5.0,
    results_dir="my_results"
)

analyzer = FishBehaviorAnalyzer("path/to/video.mp4", config)

# Run complete analysis
results = analyzer.run_full_analysis(
    force_reextract=False,
    visualize_flow=False,
    show_plots=True,
    save_results=True
)

# Access results
print(f"Average speed: {sum(results['avg_speeds'])/len(results['avg_speeds']):.2f}")
print(f"Sudden changes detected: {len(results['sudden_changes'])}")
```

### Step-by-Step Analysis

```python
from fish_behavior_analysis import FishBehaviorAnalyzer

analyzer = FishBehaviorAnalyzer("video.mp4")

# Step 1: Extract frames
frame_count = analyzer.extract_frames()

# Step 2: Compute optical flow
flow_count = analyzer.compute_optical_flow(visualize=True)

# Step 3: Analyze behavior patterns
results = analyzer.analyze_behavior()

# Step 4: Visualize results
analyzer.visualize_results()

# Step 5: Export results
export_paths = analyzer.export_results()
```

## Configuration

The package uses a flexible configuration system:

```python
from fish_behavior_analysis import Config

config = Config(
    frame_skip=1,                    # Extract every nth frame
    frames_dir="frames",             # Directory for extracted frames
    flow_vis_dir="flow_vis",         # Directory for flow visualizations
    results_dir="results",           # Directory for analysis results
    angle_sample_size=1000,          # Number of angles to sample per frame
    sudden_change_threshold=5.0,     # Threshold for sudden change detection
    plot_figsize=(10, 6),           # Default plot size
    plot_dpi=300                     # Plot resolution
)
```

## Output Files

The analysis generates several output files:

- `average_speeds.csv`: Time series of average swimming speeds
- `direction_histogram.json`: Histogram of swimming directions
- `sudden_changes.json`: Detected sudden behavior changes
- `analysis_metadata.json`: Analysis parameters and metadata
- `summary_statistics.json`: Statistical summary of results
- `speed_timeline.png`: Plot of speed over time
- `direction_histogram.png`: Direction preference histogram
- `movement_heatmap.png`: Spatial movement heatmap

## API Reference

### Core Classes

- `FishBehaviorAnalyzer`: Main analysis class
- `FrameExtractor`: Handles video frame extraction
- `OpticalFlowProcessor`: Computes optical flow between frames
- `FlowVisualizer`: Creates visualizations of results
- `ResultsExporter`: Exports results to various formats
- `Config`: Configuration management

### Key Methods

- `extract_frames()`: Extract frames from video
- `compute_optical_flow()`: Compute optical flow
- `analyze_behavior()`: Analyze behavior patterns
- `visualize_results()`: Create visualizations
- `export_results()`: Export all results
- `run_full_analysis()`: Complete analysis pipeline

## Requirements

- Python 3.8+
- OpenCV 4.5+
- NumPy 1.21+
- Matplotlib 3.5+
- Pandas 1.3+
- SciPy 1.7+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{fish_behavior_analysis,
  title={Fish Behavior Analysis: A Python Toolkit for Video-based Behavioral Analysis},
  author={Olatoye Dolapo Salim},
  year={2025},
  url={https://github.com/DolapoSalim/package-for-fish-behavior-analysis}
}
```

## Support

For questions and support, please open an issue on GitHub or contact [dolaposalim@gmail.com].
