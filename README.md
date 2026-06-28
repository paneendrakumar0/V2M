# Video-to-Mesh (V2M) Industrial Pipeline

An enterprise-grade, automated AI pipeline that processes a raw video input and generates a high-quality 3D mesh (V2M) using Neural Radiance Fields and Gaussian Splatting via the Nerfstudio framework.

## Features
- **Automated Video Preprocessing**: Automatically extracts frames from video and estimates camera poses using COLMAP.
- **3D Reconstruction**: Triggers highly optimized Gaussian Splatting training.
- **Mesh Exporting**: Converts the trained Radiance Field / Splat into a standard 3D mesh format (`.obj` or `.ply`).
- **Production Ready**: Fully automated CLI, extensive logging, and unit tests built for CI/CD pipelines.

## Installation

### Prerequisites
- NVIDIA GPU (RTX 3060 or higher with minimum 8GB VRAM)
- WSL2 (Ubuntu) if running on Windows
- CUDA Toolkit 11.8+

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/paneendrakumar0/V2M.git
   cd V2M
   ```
2. Create a conda environment and install dependencies:
   ```bash
   conda create -n v2m python=3.10 -y
   conda activate v2m
   pip install -r requirements.txt
   ```
3. Ensure COLMAP and FFmpeg are installed on your system.
   ```bash
   sudo apt install colmap ffmpeg -y
   ```

## Usage
To process a video into a 3D mesh:

```bash
python -m v2m.cli --video path/to/video.mp4 --output_dir outputs/my_mesh/
```

## Testing
Run the automated test suite using pytest:
```bash
pytest tests/
```
