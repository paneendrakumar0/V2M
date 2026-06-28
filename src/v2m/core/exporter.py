import subprocess
import json
from pathlib import Path
from v2m.utils.logger import setup_logger

logger = setup_logger(__name__)

class Exporter:
    def __init__(self, config_path: str, output_path: str):
        self.config_path = Path(config_path)
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
    def export_mesh(self) -> bool:
        """
        Exports the trained model to a 3D mesh (.obj or .ply).
        
        Returns:
            bool: True if export was successful.
        """
        if not self.config_path.exists():
            logger.error(f"Config file not found: {self.config_path}")
            return False
            
        logger.info("Starting mesh export...")
        
        # Depending on the output extension, ns-export will choose the right format
        cmd = [
            "ns-export",
            "poisson",
            "--load-config", str(self.config_path),
            "--output-dir", str(self.output_path.parent),
            "--target-num-faces", "50000"
        ]
        
        try:
            logger.info(f"Running command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Export completed successfully. Mesh saved to {self.output_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Export failed with error: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("ns-export not found. Is nerfstudio installed and in PATH?")
            return False
