#!/usr/bin/env python3
"""
Main entry point for the SAR AOI Manager application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """Initialize and start the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
