#!/usr/bin/env python3
"""
Main window for the SAR AOI Manager application.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QMessageBox,
    QWidget, QLabel, QDateEdit, QSpinBox, QHBoxLayout,
    QFileDialog, QListWidgetItem, QInputDialog, QListWidget,
    QSplitter, QLineEdit, QTextEdit, QFormLayout
)
from PyQt5.QtCore import QSize, QObject, pyqtSlot, QDate, Qt
from PyQt5.QtWebChannel import QWebChannel
from ui.main_window_ui import Ui_MainWindow
from gee_interface.image_viewer import MapViewer
from aoi_manager.aoi_manager import AOIManager
from datetime import datetime

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
        elif type_str == 'point':
            self.window.on_point_added(data)
        elif type_str == 'drawing_complete':
            self.window.on_drawing_complete(data)

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize state
        self.current_aoi = None
        self.current_editing = None
        self.current_points = []
        
        # Set up the user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize AOI manager
        self.aoi_manager = AOIManager()
        
        # Customize the UI after loading
        self.customize_ui()
        
        # Create and add the map viewer
        self.setup_map_viewer()
        
        # Set up the right panel
        self.setup_right_panel()
        
        # Set up the left panel
        self.setup_left_panel()
        
        # Set up the connections
        self.setup_connections()
        
        # Load existing AOIs
        self.load_existing_aois()
    
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
    
    def setup_left_panel(self):
        """Set up the left panel with AOI list and drawing interface."""
        # Create main vertical layout for left panel
        left_layout = QVBoxLayout()
        
        # Create splitter to divide the panel
        splitter = QSplitter(Qt.Vertical)
        
        # Top panel - AOI List
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
        # AOI List label
        list_label = QLabel("AOI List")
        list_label.setStyleSheet("font-weight: bold;")
        top_layout.addWidget(list_label)
        
        # AOI List widget
        self.ui.aoiList = QListWidget()
        top_layout.addWidget(self.ui.aoiList)
        
        # AOI List buttons
        list_buttons = QHBoxLayout()
        self.ui.import_aoi_button = QPushButton("Import")
        self.ui.export_aoi_button = QPushButton("Export")
        self.ui.edit_aoi_button = QPushButton("Edit")
        self.ui.delete_aoi_button = QPushButton("Delete")
        list_buttons.addWidget(self.ui.import_aoi_button)
        list_buttons.addWidget(self.ui.export_aoi_button)
        list_buttons.addWidget(self.ui.edit_aoi_button)
        list_buttons.addWidget(self.ui.delete_aoi_button)
        top_layout.addLayout(list_buttons)
        
        # Set layout for top panel
        top_panel.setLayout(top_layout)
        
        # Bottom panel - AOI Drawing Interface
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # Drawing interface label
        draw_label = QLabel("AOI Drawing")
        draw_label.setStyleSheet("font-weight: bold;")
        bottom_layout.addWidget(draw_label)
        
        # Points list
        points_label = QLabel("Points:")
        bottom_layout.addWidget(points_label)
        self.points_list = QListWidget()
        bottom_layout.addWidget(self.points_list)
        
        # AOI metadata form
        form_layout = QFormLayout()
        
        self.aoi_name_edit = QLineEdit()
        form_layout.addRow("Name:", self.aoi_name_edit)
        
        self.aoi_notes = QTextEdit()
        self.aoi_notes.setMaximumHeight(60)
        form_layout.addRow("Notes:", self.aoi_notes)
        
        bottom_layout.addLayout(form_layout)
        
        # Drawing control buttons
        draw_buttons = QHBoxLayout()
        self.ui.start_drawing_button = QPushButton("Start Drawing")
        self.ui.clear_drawing_button = QPushButton("Clear")
        self.ui.save_aoi_button = QPushButton("Save AOI")
        self.ui.save_aoi_button.setEnabled(False)  # Disabled until drawing is complete
        
        draw_buttons.addWidget(self.ui.start_drawing_button)
        draw_buttons.addWidget(self.ui.clear_drawing_button)
        draw_buttons.addWidget(self.ui.save_aoi_button)
        bottom_layout.addLayout(draw_buttons)
        
        # Set layout for bottom panel
        bottom_panel.setLayout(bottom_layout)
        
        # Add panels to splitter
        splitter.addWidget(top_panel)
        splitter.addWidget(bottom_panel)
        
        # Add splitter to left layout
        left_layout.addWidget(splitter)
        
        # Create a new widget to hold the left layout
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        
        # Clear any existing widgets in the left panel
        while self.ui.left_panel.layout().count():
            child = self.ui.left_panel.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Set the widget as the left panel's content
        self.ui.left_panel.layout().addWidget(left_widget)
        
    def setup_connections(self):
        """Connect UI signals to slots."""
        # AOI List buttons
        self.ui.import_aoi_button.clicked.connect(self.import_aoi)
        self.ui.export_aoi_button.clicked.connect(self.export_aoi)
        self.ui.edit_aoi_button.clicked.connect(self.edit_aoi)
        self.ui.delete_aoi_button.clicked.connect(self.delete_aoi)
        
        # Drawing interface buttons
        self.ui.start_drawing_button.clicked.connect(self.start_drawing)
        self.ui.clear_drawing_button.clicked.connect(self.clear_drawing)
        self.ui.save_aoi_button.clicked.connect(self.save_aoi)
        
        # Map viewer signals
        self.map_viewer.point_added.connect(self.on_point_added)
        self.map_viewer.drawing_complete.connect(self.on_drawing_complete)
        self.map_viewer.geometry_edited.connect(self.on_geometry_edited)
        
    def start_drawing(self):
        """Start AOI drawing mode."""
        # Clear any existing points
        self.clear_drawing()
        
        # Enable drawing mode in the map
        js_command = """
            if (typeof L !== 'undefined' && window.map) {
                // Clear existing drawings
                drawnItems.clearLayers();
                // Enable drawing mode
                new L.Draw.Polygon(window.map).enable();
            }
        """
        self.map_viewer.page().runJavaScript(js_command)
        self.statusBar().showMessage("Drawing mode enabled. Click on the map to add points.")
        
    def clear_drawing(self):
        """Clear the current drawing."""
        self.current_points = []
        self.points_list.clear()
        self.aoi_name_edit.clear()
        self.aoi_notes.clear()
        self.ui.save_aoi_button.setEnabled(False)
        
        # Clear drawing from map
        js_command = """
            if (typeof L !== 'undefined' && window.map) {
                drawnItems.clearLayers();
            }
        """
        self.map_viewer.page().runJavaScript(js_command)
        
    def on_point_added(self, point):
        """Handle a new point being added to the drawing.
        
        Args:
            point (dict): Point data with lat/lng coordinates
        """
        # Add point to our list
        self.current_points.append(point)
        
        # Add point to the list widget
        point_text = f"({point['lat']:.6f}, {point['lng']:.6f})"
        self.points_list.addItem(point_text)
        
    def on_drawing_complete(self, geometry):
        """Handle drawing completion.
        
        Args:
            geometry (dict): GeoJSON geometry object
        """
        # Store the geometry
        self.current_geometry = geometry
        
        # Enable save button
        self.ui.save_aoi_button.setEnabled(True)
        self.statusBar().showMessage("Drawing complete. Enter a name and notes, then click Save AOI.")
        
    def save_aoi(self):
        """Save the current AOI."""
        name = self.aoi_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a name for the AOI")
            return
            
        if not hasattr(self, 'current_geometry'):
            QMessageBox.warning(self, "Warning", "Please draw an AOI first")
            return
            
        # Create GeoJSON feature
        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "notes": self.aoi_notes.toPlainText().strip(),
                "created": datetime.now().isoformat()
            },
            "geometry": self.current_geometry
        }
        
        # Save the AOI
        if self.aoi_manager.save_aoi(name, feature):
            # Add to list if not already there
            items = self.ui.aoiList.findItems(name, Qt.MatchExactly)
            if not items:
                self.ui.aoiList.addItem(name)
            
            # Clear the form
            self.clear_drawing()
            
            self.statusBar().showMessage(f"AOI '{name}' saved successfully")
        else:
            QMessageBox.warning(self, "Error", f"Failed to save AOI '{name}'")
    
    def load_existing_aois(self):
        """Load existing AOIs from the AOI manager."""
        # Clear the list first
        self.ui.aoiList.clear()
        
        # Load AOIs from manager
        for name, aoi in self.aoi_manager.aois.items():
            self.ui.aoiList.addItem(name)
            
    def on_geometry_drawn(self, data):
        """Handle drawn geometry from the map."""
        name, ok = QInputDialog.getText(self, 'New AOI', 'Enter name for the AOI:')
        if ok and name:
            if self.aoi_manager.save_aoi(name, data):
                self.add_aoi_to_list(name)
                QMessageBox.information(self, "Success", f"AOI '{name}' saved successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Failed to save AOI '{name}'")
    
    def add_aoi_to_list(self, name):
        """Add an AOI to the UI list."""
        item = QListWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.ui.aoiList.addItem(item)
    
    def import_aoi(self):
        """Import an AOI from a GeoJSON file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Import AOI", "", "GeoJSON Files (*.geojson);;All Files (*)"
        )
        if filepath:
            name = self.aoi_manager.import_geojson(filepath)
            if name:
                self.add_aoi_to_list(name)
                QMessageBox.information(self, "Success", f"AOI '{name}' imported successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to import AOI")
    
    def export_aoi(self):
        """Export selected AOIs to GeoJSON files."""
        selected_items = self.ui.aoiList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an AOI to export")
            return
            
        for item in selected_items:
            name = item.text()
            filepath, _ = QFileDialog.getSaveFileName(
                self, f"Export AOI - {name}", f"{name}.geojson",
                "GeoJSON Files (*.geojson);;All Files (*)"
            )
            if filepath:
                if self.aoi_manager.export_aoi(name, filepath):
                    QMessageBox.information(self, "Success", f"AOI '{name}' exported successfully!")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to export AOI '{name}'")
    
    def delete_aoi(self):
        """Delete selected AOIs."""
        selected_items = self.ui.aoiList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an AOI to delete")
            return
            
        msg = "Are you sure you want to delete the selected AOI(s)?"
        if len(selected_items) > 1:
            msg = f"Are you sure you want to delete {len(selected_items)} AOIs?"
            
        reply = QMessageBox.question(self, "Confirm Delete", msg,
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
                                   
        if reply == QMessageBox.Yes:
            for item in selected_items:
                name = item.text()
                if self.aoi_manager.delete_aoi(name):
                    self.ui.aoiList.takeItem(self.ui.aoiList.row(item))
                    self.map_viewer.remove_geojson(name)
    
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
    
    def edit_aoi(self):
        """Start editing the selected AOI."""
        selected_items = self.ui.aoiList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an AOI to edit")
            return
            
        if len(selected_items) > 1:
            QMessageBox.warning(self, "Warning", "Please select only one AOI to edit")
            return
            
        name = selected_items[0].text()
        self.current_editing = name
        
        # Enable editing mode for this AOI
        self.map_viewer.enable_editing(name)
        self.statusBar().showMessage(f"Editing AOI '{name}'. Move points to adjust the shape.")
        
        # Load AOI data into form
        if name in self.aoi_manager.aois:
            aoi = self.aoi_manager.aois[name]
            self.aoi_name_edit.setText(name)
            self.aoi_notes.setText(aoi.get("properties", {}).get("notes", ""))
            self.ui.save_aoi_button.setEnabled(True)
    
    def on_geometry_edited(self, data):
        """Handle edited geometry from the map."""
        name = data["name"]
        geometry = data["geometry"]
        
        # Update the geometry in the AOI manager
        if name in self.aoi_manager.aois:
            aoi = self.aoi_manager.aois[name]
            aoi["geometry"] = geometry
            
            if self.aoi_manager.save_aoi(name, aoi):
                self.statusBar().showMessage(f"AOI '{name}' updated successfully")
            else:
                QMessageBox.warning(self, "Error", f"Failed to update AOI '{name}'")
