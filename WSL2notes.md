# WSL2 Development Setup Notes

## Environment Setup
1. **Windows Side**:
   - Windsurf IDE for code editing and Git operations
   - Project location: `C:\Users\krasn\WindowsProjects\geetools`

2. **Ubuntu WSL2 Side**:
   - Project path: `/mnt/c/Users/krasn/WindowsProjects/geetools`
   - Python virtual environment in `geescan/venv`
   - Oh My Zsh with agnoster theme (shows venv status)

## Daily Development Workflow
1. **Start Development**:
   ```bash
   cd /mnt/c/Users/krasn/WindowsProjects/geetools/geescan
   ```

2. **Run Application**:
   ```bash
   python test_window.py  # or main.py when developed
   ```

3. **Install New Dependencies**:
   ```bash
   pip install package_name
   pip freeze > requirements.txt
   ```

## Environment Management
- **Update Ubuntu**: `sudo apt update && sudo apt upgrade -y`
- **Virtual Environment**:
  - Activate: `source venv/bin/activate`
  - Deactivate: `deactivate`
  - Check status: `which python` should show `.../geescan/venv/bin/python`

## Development Tools
- **Testing**: pytest, pytest-qt
- **Code Formatting**: black, isort
- **GUI**: PyQt6 with X11/WSLg support

## Notes
- Edit code in Windsurf IDE on Windows
- Run Python commands in WSL2 Ubuntu terminal
- Git operations through IDE
- GUI apps work through WSL2's X11 forwarding
