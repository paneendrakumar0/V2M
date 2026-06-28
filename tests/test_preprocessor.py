import pytest
from pathlib import Path
from v2m.core.preprocessor import Preprocessor

def test_preprocessor_missing_file():
    """Test that preprocessor handles missing files gracefully."""
    preprocessor = Preprocessor(output_dir="dummy_output")
    result = preprocessor.process_video("non_existent_video.mp4")
    assert result is False

def test_preprocessor_init():
    """Test that preprocessor initializes output directory."""
    preprocessor = Preprocessor(output_dir="dummy_output")
    assert Path("dummy_output").exists()
