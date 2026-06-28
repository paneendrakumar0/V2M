import subprocess
from pathlib import Path
from v2m.utils.logger import setup_logger

logger = setup_logger(__name__)

class Reconstructor:
    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def train(self, method: str = "splatfacto") -> bool:
        """
        Trains the 3D model using Nerfstudio.
        
        Args:
            method (str): The nerfstudio method to use (default: splatfacto).
            
        Returns:
            bool: True if training was successful.
        """
        if not self.data_dir.exists():
            logger.error(f"Data directory not found: {self.data_dir}")
            return False
            
        logger.info(f"Starting 3D reconstruction using method: {method}")
        
        cmd = [
            "ns-train",
            method,
            "--data", str(self.data_dir),
            "--output-dir", str(self.output_dir)
        ]
        
        try:
            logger.info(f"Running command: {' '.join(cmd)}")
            # For training, we stream the output to console as it takes a while
            subprocess.run(cmd, check=True)
            logger.info("Training completed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Training failed.")
            return False
        except FileNotFoundError:
            logger.error("ns-train not found. Is nerfstudio installed and in PATH?")
            return False
