#!/usr/bin/env python3
"""
Google Earth Engine query functions for SAR data.
"""

import ee
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

def initialize_ee():
    """Initialize Earth Engine."""
    try:
        ee.Initialize()
        return True
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        return False

def get_sar_collection(
    geometry: Dict,
    start_date: str = None,
    end_date: str = None
) -> Tuple[ee.ImageCollection, List[str], int]:
    """
    Get SAR image collection for the given geometry and date range.
    
    Args:
        geometry: GeoJSON geometry of the AOI
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    
    Returns:
        Tuple of (ImageCollection, list of dates, image count)
    """
    # Convert geometry to EE format
    aoi = ee.Geometry(geometry)
    
    # Set default date range if not provided
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Get Sentinel-1 SAR collection
    collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
                 .filterBounds(aoi)
                 .filterDate(start_date, end_date)
                 .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                 .filter(ee.Filter.eq('instrumentMode', 'IW')))
    
    # Get dates
    dates = collection.aggregate_array('system:time_start').getInfo()
    dates = [datetime.fromtimestamp(d/1000).strftime('%Y-%m-%d') for d in dates]
    
    # Get count
    count = collection.size().getInfo()
    
    return collection, dates, count

def export_geotiff(
    collection: ee.ImageCollection,
    geometry: Dict,
    export_path: str
) -> ee.batch.Task:
    """
    Export a GeoTIFF for the given collection and geometry.
    
    Args:
        collection: EE ImageCollection to export
        geometry: GeoJSON geometry of the AOI
        export_path: Path to save the GeoTIFF
    
    Returns:
        EE export task
    """
    # Convert geometry to EE format
    aoi = ee.Geometry(geometry)
    
    # Create composite image
    image = collection.mean()
    
    # Start export task
    task = ee.batch.Export.image.toDrive({
        'image': image,
        'description': 'SAR_Export',
        'folder': 'SAR_Exports',
        'fileNamePrefix': export_path,
        'region': aoi,
        'scale': 10,
        'crs': 'EPSG:4326',
        'fileFormat': 'GeoTIFF'
    })
    
    task.start()
    return task
