#!/usr/bin/env python3
"""
Timeline widget for displaying SAR image distribution.
Similar to video editor timeline but for SAR images.
"""

from PyQt5.QtWidgets import (
    QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
)
from PyQt5.QtCore import Qt, QRectF, QDateTime
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter

class TimelineWidget(QWidget):
    """A timeline widget showing SAR image distribution over time."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.images = []  # List of (datetime, metadata) tuples
        
    def setup_ui(self):
        """Set up the timeline UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create graphics view and scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        
        # Configure view
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setMinimumHeight(100)
        
        layout.addWidget(self.view)
        
        # Set up pens and brushes
        self.axis_pen = QPen(QColor(200, 200, 200))
        self.tick_pen = QPen(QColor(150, 150, 150))
        self.image_brush = QBrush(QColor(100, 149, 237))  # Cornflower blue
        self.text_color = QColor(50, 50, 50)
        
    def set_images(self, images):
        """
        Set the images to display in the timeline.
        
        Args:
            images: List of tuples (datetime, metadata)
                   metadata should be a dict with image info
        """
        self.images = sorted(images, key=lambda x: x[0])
        self.update_timeline()
        
    def update_timeline(self):
        """Update the timeline visualization."""
        self.scene.clear()
        
        if not self.images:
            return
        
        # Get date range
        start_date = self.images[0][0]
        end_date = self.images[-1][0]
        date_range = end_date.toSecsSinceEpoch() - start_date.toSecsSinceEpoch()
        
        # Timeline dimensions
        width = max(800, self.width() - 20)  # Minimum width 800px
        height = 80
        top_margin = 20
        
        # Draw main timeline axis
        self.scene.addLine(0, height/2, width, height/2, self.axis_pen)
        
        # Draw time markers
        num_markers = 10
        for i in range(num_markers + 1):
            x = (width * i) / num_markers
            # Tick mark
            self.scene.addLine(x, height/2 - 5, x, height/2 + 5, self.tick_pen)
            # Date label
            secs = start_date.toSecsSinceEpoch() + (date_range * i) / num_markers
            date = QDateTime.fromSecsSinceEpoch(int(secs))
            text = QGraphicsTextItem(date.toString("yyyy-MM-dd"))
            text.setDefaultTextColor(self.text_color)
            text.setPos(x - 30, height/2 + 10)
            self.scene.addItem(text)
        
        # Draw image markers
        marker_width = 2
        marker_height = 20
        for date, metadata in self.images:
            # Calculate x position
            secs = date.toSecsSinceEpoch() - start_date.toSecsSinceEpoch()
            x = (width * secs) / date_range
            
            # Draw marker
            marker = QGraphicsRectItem(
                x - marker_width/2,
                height/2 - marker_height/2,
                marker_width,
                marker_height
            )
            marker.setBrush(self.image_brush)
            marker.setPen(QPen(Qt.NoPen))
            self.scene.addItem(marker)
            
            # Add tooltip with metadata
            marker.setToolTip(f"Date: {date.toString('yyyy-MM-dd')}\n"
                            f"Platform: {metadata.get('platform', 'Unknown')}\n"
                            f"Mode: {metadata.get('mode', 'Unknown')}")
        
        # Set scene rect
        padding = 10
        self.scene.setSceneRect(
            -padding,
            -padding,
            width + 2*padding,
            height + 2*padding
        )
        
        # Fit view to scene
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    
    def resizeEvent(self, event):
        """Handle resize events to update timeline scaling."""
        super().resizeEvent(event)
        if self.images:
            self.update_timeline()
