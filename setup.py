"""Setup script for development environment."""
import os
import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Create virtual environment and install dependencies."""
    venv_path = Path("venv")
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Activate venv and install dependencies
    if sys.platform == "win32":
        python = venv_path / "Scripts" / "python.exe"
    else:
        python = venv_path / "bin" / "python"
    
    subprocess.run([str(python), "-m", "pip", "install", "-r", "requirements.txt"], check=True)

if __name__ == "__main__":
    setup_environment()
