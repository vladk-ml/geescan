#!/usr/bin/env python3
"""
AOI Manager module for handling GeoJSON operations.
"""

import os
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AOIManager:
    """Manages AOI operations including saving, loading, and validation."""
    
    def __init__(self, base_dir: str = None):
        """Initialize the AOI manager.
        
        Args:
            base_dir: Base directory for AOI storage. If None, uses default location.
        """
        if base_dir is None:
            # Use the 'aois' directory within the application directory
            self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'aois')
        else:
            self.base_dir = base_dir
            
        # Ensure the directory exists
        os.makedirs(self.base_dir, exist_ok=True)
        logger.debug(f"AOI storage directory: {self.base_dir}")
        
        # Dictionary to store loaded AOIs
        self.aois: Dict[str, dict] = {}
        
    def save_aoi(self, name: str, geometry: dict) -> bool:
        """Save an AOI to a GeoJSON file.
        
        Args:
            name: Name of the AOI (will be used as filename)
            geometry: GeoJSON geometry object
            
        Returns:
            bool: True if save was successful
        """
        try:
            # Create a proper GeoJSON feature
            feature = {
                "type": "Feature",
                "properties": {"name": name},
                "geometry": geometry
            }
            
            # Save to file
            filepath = os.path.join(self.base_dir, f"{name}.geojson")
            with open(filepath, 'w') as f:
                json.dump(feature, f, indent=2)
            
            # Update internal dictionary
            self.aois[name] = feature
            logger.debug(f"Saved AOI: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving AOI {name}: {str(e)}")
            return False
    
    def load_all_aois(self) -> Dict[str, dict]:
        """Load all AOIs from the storage directory.
        
        Returns:
            Dict[str, dict]: Dictionary of AOI name to GeoJSON feature
        """
        self.aois.clear()
        try:
            for file in os.listdir(self.base_dir):
                if file.endswith('.geojson'):
                    name = os.path.splitext(file)[0]
                    filepath = os.path.join(self.base_dir, file)
                    with open(filepath, 'r') as f:
                        feature = json.load(f)
                        self.aois[name] = feature
            
            logger.debug(f"Loaded {len(self.aois)} AOIs")
            return self.aois
            
        except Exception as e:
            logger.error(f"Error loading AOIs: {str(e)}")
            return {}
    
    def delete_aoi(self, name: str) -> bool:
        """Delete an AOI.
        
        Args:
            name: Name of the AOI to delete
            
        Returns:
            bool: True if deletion was successful
        """
        try:
            filepath = os.path.join(self.base_dir, f"{name}.geojson")
            if os.path.exists(filepath):
                os.remove(filepath)
                self.aois.pop(name, None)
                logger.debug(f"Deleted AOI: {name}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting AOI {name}: {str(e)}")
            return False
    
    def import_geojson(self, filepath: str) -> Optional[str]:
        """Import an AOI from a GeoJSON file.
        
        Args:
            filepath: Path to the GeoJSON file
            
        Returns:
            str: Name of the imported AOI if successful, None otherwise
        """
        try:
            with open(filepath, 'r') as f:
                feature = json.load(f)
            
            # Generate a name from the file or properties
            name = feature.get("properties", {}).get("name")
            if not name:
                name = os.path.splitext(os.path.basename(filepath))[0]
            
            # Save the imported AOI
            if self.save_aoi(name, feature["geometry"]):
                return name
            return None
            
        except Exception as e:
            logger.error(f"Error importing GeoJSON {filepath}: {str(e)}")
            return None
    
    def export_aoi(self, name: str, filepath: str) -> bool:
        """Export an AOI to a GeoJSON file.
        
        Args:
            name: Name of the AOI to export
            filepath: Destination path for the GeoJSON file
            
        Returns:
            bool: True if export was successful
        """
        try:
            if name in self.aois:
                with open(filepath, 'w') as f:
                    json.dump(self.aois[name], f, indent=2)
                logger.debug(f"Exported AOI {name} to {filepath}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error exporting AOI {name}: {str(e)}")
            return False
