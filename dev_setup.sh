#!/bin/bash

# Exit on error
set -e

echo "Setting up development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install system dependencies for Qt and WebEngine
echo "Checking system dependencies..."
if ! dpkg -l | grep -q "libxcb-xinerama0"; then
    echo "Installing Qt system dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        libxcb-xinerama0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxkbcommon-x11-0
fi

echo "Setup complete! Run './run_dev.sh' to start the application."
