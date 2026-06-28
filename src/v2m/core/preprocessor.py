import os
import subprocess
from pathlib import Path
from v2m.utils.logger import setup_logger

logger = setup_logger(__name__)

class Preprocessor:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def process_video(self, video_path: str) -> bool:
        """
        Process the video: extract frames and run COLMAP via ns-process-data.
        
        Args:
            video_path (str): Path to the input video file.
            
        Returns:
            bool: True if preprocessing was successful, False otherwise.
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return False
            
        logger.info(f"Starting video preprocessing for: {video_path}")
        
        # We use Nerfstudio's ns-process-data to handle ffmpeg and colmap
        cmd = [
            "ns-process-data",
            "video",
            "--data", video_path,
            "--output-dir", str(self.output_dir)
        ]
        
        try:
            logger.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("Preprocessing completed successfully.")
            logger.debug(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Preprocessing failed with error: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("ns-process-data not found. Is nerfstudio installed and in PATH?")
            return False
