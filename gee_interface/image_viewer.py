#!/usr/bin/env python3
"""
Map viewer component using Folium.
Handles map display, AOI drawing, and image visualization.
"""

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal, QFile, QObject, pyqtSlot
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
    point_added = pyqtSignal(dict)     # Emitted when a point is added
    drawing_complete = pyqtSignal(dict) # Emitted when drawing is complete
    geometry_edited = pyqtSignal(dict)  # Emitted when existing geometry is edited
    
    def __init__(self, parent=None):
        """Initialize the map viewer."""
        super().__init__(parent)
        
        # Initialize variables
        self.folium_map = None
        self.geojson_layers = {}
        
        # Create the map
        self.create_map()
        
        # Create a QWebChannel to handle JavaScript callbacks
        self.channel = QWebChannel()
        self.callback_handler = CallbackHandler()
        self.channel.registerObject('callback', self.callback_handler)
        self.page().setWebChannel(self.channel)
        
        # Connect callback signals
        self.callback_handler.messageReceived.connect(self.handle_message)
        
        # Enable local file access and debugging
        self.settings().setAttribute(
            self.settings().WebAttribute.LocalContentCanAccessRemoteUrls, 
            True
        )
        self.page().setDevToolsPage(self.page())
        
        # Load the map
        self.load_map()
        
        # Connect JavaScript
        self.page().loadFinished.connect(self.on_load_finished)
    
    def handle_message(self, message_type, data):
        """Handle messages from JavaScript.
        
        Args:
            message_type (str): Type of message
            data (dict): Message data
        """
        if message_type == 'point':
            self.point_added.emit(data)
        elif message_type == 'drawing_complete':
            self.drawing_complete.emit(data)
        elif message_type == 'geometry_edited':
            self.geometry_edited.emit(data)
        elif message_type == 'bounds':
            self.bounds_changed.emit(data)
    
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
        
        # Create a feature group for drawn items
        self.folium_map.get_root().html.add_child(folium.Element("""
            <script>
                var drawnItems = new L.FeatureGroup();
            </script>
        """))
        
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
                'featureGroup': 'drawnItems',
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
                    
                    // Wait for map to be initialized
                    var checkMap = setInterval(function() {
                        var mapDiv = document.getElementById('map');
                        if (mapDiv && mapDiv._leaflet_map) {
                            clearInterval(checkMap);
                            window.map = mapDiv._leaflet_map;
                            
                            // Add drawnItems layer to map
                            window.map.addLayer(drawnItems);
                            
                            // Add event listeners after map is initialized
                            window.map.on('draw:created', function(e) {
                                var layer = e.layer;
                                drawnItems.addLayer(layer);
                                var geojson = layer.toGeoJSON();
                                if (window.callback) {
                                    window.callback.handleMessage('drawing_complete', geojson.geometry);
                                }
                            });
                            
                            window.map.on('draw:drawvertex', function(e) {
                                var latLng = e.vertex;
                                if (window.callback) {
                                    window.callback.handleMessage('point', {
                                        lat: latLng.lat,
                                        lng: latLng.lng
                                    });
                                }
                            });
                            
                            window.map.on('draw:edited', function(e) {
                                var layers = e.layers;
                                layers.eachLayer(function(layer) {
                                    var geojson = layer.toGeoJSON();
                                    var name = layer.feature.properties.name;
                                    if (window.callback) {
                                        window.callback.handleMessage('geometry_edited', {
                                            name: name,
                                            geometry: geojson.geometry
                                        });
                                    }
                                });
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
                        }
                    }, 100);  // Check every 100ms
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
    
    def clear_drawing(self):
        """Clear all drawings from the map."""
        self.page().runJavaScript("""
            if (typeof L !== 'undefined' && window.map) {
                drawnItems.clearLayers();
            }
        """)
    
    def add_geojson(self, feature: dict, style: dict = None) -> bool:
        """Add a GeoJSON feature to the map.
        
        Args:
            feature: GeoJSON feature to add
            style: Optional style dictionary for the feature
            
        Returns:
            bool: True if successful
        """
        try:
            name = feature["properties"]["name"]
            if not style:
                style = {
                    "color": "#ff7800",
                    "weight": 2,
                    "fillOpacity": 0.35
                }
            
            # Store feature for later use
            self.geojson_layers[name] = feature
            
            # Add to map using JavaScript
            js_command = f"""
                var feature = {json.dumps(feature)};
                var style = {json.dumps(style)};
                if (typeof L !== 'undefined') {{
                    var layer = L.geoJSON(feature, {{style: function(feature) {{ return style; }}}});
                    drawnItems.addLayer(layer);
                    // Store reference to layer for editing
                    window.activeLayers['{name}'] = layer;
                    map.fitBounds(layer.getBounds());
                }}
            """
            self.page().runJavaScript(js_command)
            return True
            
        except Exception as e:
            logger.error(f"Error adding GeoJSON: {str(e)}")
            return False
    
    def remove_geojson(self, name: str) -> bool:
        """Remove a GeoJSON feature from the map.
        
        Args:
            name: Name of the feature to remove
            
        Returns:
            bool: True if successful
        """
        try:
            if name in self.geojson_layers:
                # Remove from map using JavaScript
                js_command = f"""
                    if (typeof L !== 'undefined') {{
                        drawnItems.eachLayer(function(layer) {{
                            if (layer.feature && layer.feature.properties.name === '{name}') {{
                                drawnItems.removeLayer(layer);
                            }}
                        }});
                    }}
                """
                self.page().runJavaScript(js_command)
                del self.geojson_layers[name]
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error removing GeoJSON: {str(e)}")
            return False
    
    def enable_editing(self, name: str):
        """Enable editing for a specific AOI.
        
        Args:
            name: Name of the AOI to edit
        """
        js_command = f"""
            if (typeof L !== 'undefined' && window.activeLayers['{name}']) {{
                var layer = window.activeLayers['{name}'];
                layer.editing.enable();
            }}
        """
        self.page().runJavaScript(js_command)
    
    def disable_editing(self, name: str):
        """Disable editing for a specific AOI.
        
        Args:
            name: Name of the AOI to stop editing
        """
        js_command = f"""
            if (typeof L !== 'undefined' && window.activeLayers['{name}']) {{
                var layer = window.activeLayers['{name}'];
                layer.editing.disable();
            }}
        """
        self.page().runJavaScript(js_command)

class CallbackHandler(QObject):
    messageReceived = pyqtSignal(str, dict)
    
    @pyqtSlot(str, dict)
    def handleMessage(self, message_type, data):
        self.messageReceived.emit(message_type, data)
