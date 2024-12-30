import ee
import os
import json
from app.models.db import get_aoi
from flask import current_app
from datetime import datetime, timedelta

def initialize_gee():
    """Initialize Google Earth Engine using environment variables"""
    try:
        project_id = os.getenv('GEE_PROJECT')
        if not project_id:
            return {"status": "error", "message": "GEE_PROJECT environment variable not set"}

        ee.Initialize(project=project_id)
        return {"status": "success", "message": "Authentication successful"}
    except Exception as e:
        return {"status": "error", "message": f"Authentication failed: {str(e)}"}

def get_time_range(preset_id=None):
    """Get time range based on preset ID or default"""
    end_date = datetime.now()
    days_back = 30  # Default

    if preset_id:
        try:
            presets_file = os.path.join(current_app.root_path, 'time_range_presets.json')
            if os.path.exists(presets_file):
                with open(presets_file, 'r') as f:
                    presets_data = json.load(f)
                    if preset_id in presets_data['presets']:
                        days_back = presets_data['presets'][preset_id]['days_back']
        except Exception:
            pass  # Fall back to default if any error

    start_date = end_date - timedelta(days=days_back)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def export_aoi_to_drive(aoi_id, params=None):
    """
    Creates a GEE export task for a given AOI ID
    params can include:
    - preset_id: ID of time range preset to use
    - start_date: Override start date
    - end_date: Override end date
    - polarization: List of polarizations ['VV', 'VH']
    - orbit: Orbit direction ('ASCENDING' or 'DESCENDING')
    Returns task information including task ID
    """
    try:
        # Get AOI from database
        aoi_data = get_aoi(aoi_id)
        if not aoi_data:
            return {"status": "error", "message": "AOI not found"}

        # Set default parameters
        params = params or {}
        polarization = params.get('polarization', ['VV', 'VH'])
        orbit = params.get('orbit', 'ASCENDING')
        
        # Get time range from preset or parameters
        if params.get('start_date') and params.get('end_date'):
            start_date = params['start_date']
            end_date = params['end_date']
        else:
            start_date, end_date = get_time_range(params.get('preset_id'))

        # Convert PostGIS geometry to GEE geometry
        geom_dict = json.loads(aoi_data['geometry'])
        geometry = ee.Geometry(geom_dict)

        # Get Sentinel-1 collection
        collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(geometry) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.eq('orbitProperties_pass', orbit)) \
            .select(polarization)

        if collection.size().getInfo() == 0:
            return {"status": "error", "message": "No images found for this AOI with specified parameters"}

        # Get the first image and clip to AOI
        image = collection.first().clip(geometry)

        # Set up export task
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=f'AOI_{aoi_id}_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            scale=30,
            region=geometry,
            maxPixels=1e13
        )

        # Start the task
        task.start()

        return {
            "status": "success",
            "message": "Export task started",
            "task_id": task.id,
            "parameters": {
                "start_date": start_date,
                "end_date": end_date,
                "polarization": polarization,
                "orbit": orbit,
                "preset_id": params.get('preset_id')
            }
        }

    except Exception as e:
        return {"status": "error", "message": f"Export failed: {str(e)}"}

def check_task_status(task_id):
    """Check the status of a GEE export task"""
    try:
        task_list = ee.data.getTaskList()
        task = next((t for t in task_list if t['id'] == task_id), None)
        if task:
            return {"status": "success", "task_status": task['state']}
        return {"status": "error", "message": "Task not found"}
    except Exception as e:
        return {"status": "error", "message": f"Status check failed: {str(e)}"}
