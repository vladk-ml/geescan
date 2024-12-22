#!/usr/bin/env python3
"""
Main window for the SAR AOI Manager application.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QMessageBox,
    QWidget, QLabel, QDateEdit, QSpinBox, QHBoxLayout
)
from PyQt5.QtCore import QSize, QObject, pyqtSlot, QDate
from PyQt5.QtWebChannel import QWebChannel
from ui.main_window_ui import Ui_MainWindow
from gee_interface.image_viewer import MapViewer

class WebChannelHandler(QObject):
    """Handles communication between JavaScript and Python."""
    
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.window = window
    
    @pyqtSlot(str, dict)
    def handleMessage(self, type_str, data):
        """Handle messages from JavaScript."""
        if type_str == 'geometry':
            self.window.on_geometry_drawn(data)
        elif type_str == 'bounds':
            self.window.on_bounds_changed(data)

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Set up the user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Customize the UI after loading
        self.customize_ui()
        
        # Create and add the map viewer
        self.setup_map_viewer()
        
        # Set up the right panel
        self.setup_right_panel()
        
        # Connect signals
        self.setup_connections()
        
        # Initialize state
        self.current_aoi = None

    def customize_ui(self):
        """Customize the UI after it's loaded from the .ui file."""
        # Set minimum window size
        self.setMinimumSize(1200, 800)
        
        # Configure the splitter for three equal panes
        self.ui.main_splitter.setHandleWidth(2)
        self.ui.main_splitter.setChildrenCollapsible(False)
        self.ui.main_splitter.setSizes([1000, 1000, 1000])
        
        # Style the buttons
        for button in [self.ui.add_aoi_button, self.ui.import_aoi_button, self.ui.delete_aoi_button]:
            button.setFixedSize(80, 30)
        
        # Center the buttons in their container
        if hasattr(self.ui, 'aoi_buttons'):
            self.ui.aoi_buttons.insertStretch(0)
            self.ui.aoi_buttons.addStretch()
        
        # Apply dark mode styling
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QSplitter::handle {
                background-color: #2d2d2d;
            }
            QListWidget {
                background-color: #252526;
                border: 1px solid #3e3e42;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #0e639c;
            }
            QPushButton {
                background-color: #0e639c;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                color: white;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5289;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: #3c3c3c;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 4px;
                color: white;
            }
            QGroupBox {
                border: 1px solid #3e3e42;
                border-radius: 3px;
                margin-top: 0.5em;
                padding-top: 0.5em;
            }
            QGroupBox::title {
                color: #ffffff;
            }
        """)

    def setup_map_viewer(self):
        """Set up the map viewer widget."""
        self.map_viewer = MapViewer(self)
        self.ui.map_container.layout().addWidget(self.map_viewer)
        
        # Set up web channel for map communication
        self.channel = QWebChannel(self.map_viewer.page())
        self.handler = WebChannelHandler(self)
        self.channel.registerObject('callback', self.handler)
        self.map_viewer.page().setWebChannel(self.channel)
    
    def setup_right_panel(self):
        """Set up the right panel with SAR parameters."""
        # Create right panel widget
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Section title
        title = QLabel("SAR Image Parameters")
        title.setStyleSheet("font-weight: bold; font-size: 12px;")
        right_layout.addWidget(title)
        
        # Date range section
        date_range_widget = QWidget()
        date_range_layout = QVBoxLayout(date_range_widget)
        
        # Start date
        start_date_widget = QWidget()
        start_date_layout = QHBoxLayout(start_date_widget)
        start_date_layout.addWidget(QLabel("Start Date:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addYears(-1))
        start_date_layout.addWidget(self.start_date)
        date_range_layout.addWidget(start_date_widget)
        
        # End date
        end_date_widget = QWidget()
        end_date_layout = QHBoxLayout(end_date_widget)
        end_date_layout.addWidget(QLabel("End Date:"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        end_date_layout.addWidget(self.end_date)
        date_range_layout.addWidget(end_date_widget)
        
        right_layout.addWidget(date_range_widget)
        
        # Image count
        count_widget = QWidget()
        count_layout = QHBoxLayout(count_widget)
        count_layout.addWidget(QLabel("Available Images:"))
        self.image_count = QLabel("0")
        count_layout.addWidget(self.image_count)
        right_layout.addWidget(count_widget)
        
        # Buttons section with centered, fixed-width buttons
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(6)
        
        # Container for Query button
        query_container = QWidget()
        query_layout = QHBoxLayout(query_container)
        query_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add stretches to center the button
        query_layout.addStretch()
        self.query_button = QPushButton("Query Images")
        self.query_button.setFixedSize(120, 30)  # Slightly wider for longer text
        self.query_button.clicked.connect(self.on_query_images)
        query_layout.addWidget(self.query_button)
        query_layout.addStretch()
        
        buttons_layout.addWidget(query_container)
        
        # Container for Export button
        export_container = QWidget()
        export_layout = QHBoxLayout(export_container)
        export_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add stretches to center the button
        export_layout.addStretch()
        self.export_button = QPushButton("Export to GeoTIFF")
        self.export_button.setFixedSize(160, 30)  # Increased width to 160px for longer text
        self.export_button.clicked.connect(self.on_export)
        export_layout.addWidget(self.export_button)
        export_layout.addStretch()
        
        buttons_layout.addWidget(export_container)
        
        right_layout.addWidget(buttons_widget)
        
        # Add right panel to the UI
        self.ui.right_panel.layout().addWidget(right_panel)
        
        # Add stretch to push everything to the top
        self.ui.right_panel.layout().addStretch()
    
    def setup_connections(self):
        """Connect UI signals to slots."""
        # AOI buttons
        self.ui.add_aoi_button.clicked.connect(self.on_add_aoi)
        self.ui.import_aoi_button.clicked.connect(self.on_import_aoi)
        self.ui.delete_aoi_button.clicked.connect(self.on_delete_aoi)
        
        # Date pickers
        self.start_date.dateChanged.connect(self.on_date_changed)
        self.end_date.dateChanged.connect(self.on_date_changed)
    
    def on_geometry_drawn(self, geometry):
        """Handle new geometry drawn on map."""
        self.current_aoi = geometry
        print(f"New AOI drawn: {geometry}")
        
        # Update image count (simulated for now)
        self.update_image_info(['2024-01-01', '2024-12-31'], 42)
    
    def update_image_info(self, dates, count):
        """Update the parameters panel with image information."""
        if dates and len(dates) >= 2:
            start = QDate.fromString(dates[0], "yyyy-MM-dd")
            end = QDate.fromString(dates[-1], "yyyy-MM-dd")
            self.start_date.setDate(start)
            self.end_date.setDate(end)
        self.image_count.setText(str(count))
    
    def on_bounds_changed(self, bounds):
        """Handle map bounds changed."""
        print(f"Map bounds: {bounds}")
    
    def on_date_changed(self):
        """Handle date picker changes."""
        if self.current_aoi:
            start = self.start_date.date().toString("yyyy-MM-dd")
            end = self.end_date.date().toString("yyyy-MM-dd")
            print(f"Date range changed: {start} to {end}")
            # TODO: Query GEE for new date range
    
    def on_add_aoi(self):
        """Handle Add AOI button click."""
        self.map_viewer.enable_drawing()
        self.statusBar().showMessage("Draw an Area of Interest on the map")
    
    def on_import_aoi(self):
        """Handle Import AOI button click."""
        # TODO: Implement file dialog for GeoJSON import
        QMessageBox.information(
            self,
            "Import AOI",
            "GeoJSON import will be implemented here"
        )
    
    def on_delete_aoi(self):
        """Handle Delete AOI button click."""
        if self.current_aoi:
            self.map_viewer.clear_aoi()
            self.current_aoi = None
            self.image_count.setText("0")
            self.statusBar().showMessage("AOI deleted")
        else:
            self.statusBar().showMessage("No AOI to delete")
    
    def on_query_images(self):
        """Query available SAR images for the current AOI and date range."""
        if self.current_aoi:
            start = self.start_date.date().toString("yyyy-MM-dd")
            end = self.end_date.date().toString("yyyy-MM-dd")
            self.statusBar().showMessage(f"Querying SAR images from {start} to {end}...")
            # TODO: Query GEE for images
        else:
            self.statusBar().showMessage("Draw an AOI first")
    
    def on_export(self):
        """Handle Export button click."""
        if self.current_aoi:
            # TODO: Implement GeoTIFF export
            QMessageBox.information(
                self,
                "Export",
                "GeoTIFF export will be implemented here"
            )
        else:
            QMessageBox.warning(
                self,
                "Export",
                "Draw an Area of Interest first"
            )
