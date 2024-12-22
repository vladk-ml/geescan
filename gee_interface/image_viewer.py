#!/usr/bin/env python3
"""
Map viewer component using Folium.
Handles map display, AOI drawing, and image visualization.
"""

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal, QFile
from PyQt5.QtWebChannel import QWebChannel
import folium
from folium.plugins import Draw, MousePosition
import json
import os
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MapViewer(QWebEngineView):
    """Map viewer widget using Folium."""
    
    # Signals for map interactions
    geometry_drawn = pyqtSignal(dict)  # Emitted when AOI is drawn
    bounds_changed = pyqtSignal(dict)  # Emitted when map bounds change
    
    def __init__(self, parent=None):
        """Initialize the map viewer."""
        super().__init__(parent)
        logger.debug("Initializing MapViewer")
        
        # Enable local file access and debugging
        self.settings().setAttribute(
            self.settings().WebAttribute.LocalContentCanAccessRemoteUrls, 
            True
        )
        self.page().setDevToolsPage(self.page())
        
        # Set up web channel
        self.channel = QWebChannel(self.page())
        self.page().setWebChannel(self.channel)
        
        # Create map
        self.create_map()
        
        # Load the map
        self.load_map()
        
        # Connect JavaScript
        self.page().loadFinished.connect(self.on_load_finished)
    
    def create_map(self):
        """Create the Folium map."""
        logger.debug("Creating Folium map")
        # Create a map centered on [0, 0]
        self.folium_map = folium.Map(
            location=[0, 0],
            zoom_start=2,
            tiles='CartoDB positron',
            prefer_canvas=True,
            width='100%',
            height='100%'
        )
        
        # Add mouse position display
        MousePosition().add_to(self.folium_map)
        
        # Add drawing controls
        draw = Draw(
            draw_options={
                'polyline': False,
                'rectangle': True,
                'polygon': True,
                'circle': False,
                'marker': False,
                'circlemarker': False
            },
            edit_options={
                'edit': True,
                'remove': True
            }
        )
        draw.add_to(self.folium_map)
        
        # Add QWebChannel script
        self.folium_map.get_root().header.add_child(folium.Element("""
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        """))
        
        # Add custom JavaScript for event handling
        self.folium_map.get_root().script.add_child(folium.Element("""
            // Wait for the map to be ready
            document.addEventListener('DOMContentLoaded', function() {
                // Initialize QWebChannel
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.callback = channel.objects.callback;
                    
                    // Add event listeners after map is initialized
                    window.map.on('draw:created', function(e) {
                        var layer = e.layer;
                        var geojson = layer.toGeoJSON();
                        if (window.callback) {
                            window.callback.handleMessage('geometry', geojson.geometry);
                        }
                    });
                    
                    window.map.on('moveend', function(e) {
                        var bounds = window.map.getBounds();
                        if (window.callback) {
                            window.callback.handleMessage('bounds', {
                                north: bounds.getNorth(),
                                south: bounds.getSouth(),
                                east: bounds.getEast(),
                                west: bounds.getWest()
                            });
                        }
                    });
                });
            });
        """))
        
        # Make map object available globally
        self.folium_map.get_root().script.add_child(folium.Element("""
            document.addEventListener('DOMContentLoaded', function() {
                // Make map available globally
                window.map = document.querySelector('#map')._leaflet_map;
            });
        """))
    
    def load_map(self):
        """Save the map to a temporary file and load it."""
        logger.debug("Loading map from temporary file")
        # Save map to temporary file
        self.temp_html = os.path.join(tempfile.gettempdir(), 'map.html')
        self.folium_map.save(self.temp_html)
        
        # Log the HTML content for debugging
        with open(self.temp_html, 'r') as f:
            logger.debug(f"Map HTML content: {f.read()[:500]}...")  # First 500 chars
        
        # Load the temporary file
        self.load(QUrl.fromLocalFile(self.temp_html))
    
    def on_load_finished(self, ok):
        """Handle page load completion."""
        if ok:
            logger.debug("Map loaded successfully")
        else:
            logger.error("Failed to load map")
    
    def update_timeline(self, dates, count):
        """Update the timeline with available image dates and count."""
        logger.debug(f"Updating timeline with dates: {dates}, count: {count}")
        self.page().runJavaScript(f"window.updateTimeline({json.dumps(dates)}, {count});")
    
    def set_aoi(self, geojson):
        """Display an AOI on the map."""
        logger.debug(f"Setting AOI: {geojson}")
        self.page().runJavaScript(f"""
            if (window.map) {{
                L.geoJSON({json.dumps(geojson)}).addTo(window.map);
            }}
        """)
    
    def clear_aoi(self):
        """Clear the AOI from the map."""
        logger.debug("Clearing AOI")
        self.page().runJavaScript("""
            if (window.map) {
                window.map.eachLayer(function(layer) {
                    if (layer instanceof L.GeoJSON) {
                        window.map.removeLayer(layer);
                    }
                });
            }
        """)
    
    def enable_drawing(self):
        """Enable AOI drawing mode."""
        logger.debug("Enabling drawing mode")
        self.page().runJavaScript("""
            if (window.drawControl) {
                window.drawControl.enable();
            }
        """)
    
    def disable_drawing(self):
        """Disable AOI drawing mode."""
        logger.debug("Disabling drawing mode")
        self.page().runJavaScript("""
            if (window.drawControl) {
                window.drawControl.disable();
            }
        """)
