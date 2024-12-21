#!/usr/bin/env python3
"""Test file to verify PyQt6 and X11 forwarding in WSL2."""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class TestWindow(QMainWindow):
    """Simple test window with basic Qt widgets."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WSL2 Qt Test")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add some test widgets
        label = QLabel("If you can see this, PyQt6 is working in WSL2!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        button = QPushButton("Click me!")
        button.clicked.connect(lambda: label.setText("Button clicks work too!"))
        layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
