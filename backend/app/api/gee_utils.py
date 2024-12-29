import ee
import os
from app.models.db import get_aoi
from flask import current_app
import json

def initialize_gee(project_id=None):
    """
    Initialize Google Earth Engine with optional project ID
    Returns success status and message
    """
    try:
        # Try to initialize with existing credentials
        ee.Initialize()
        return {"status": "success", "message": "Already authenticated"}
    except Exception as e:
        try:
            # Trigger authentication flow
            ee.Authenticate()
            ee.Initialize(project=project_id)
            return {"status": "success", "message": "Authentication successful"}
        except Exception as auth_error:
            return {"status": "error", "message": f"Authentication failed: {str(auth_error)}"}

def export_aoi_to_drive(aoi_id, image_collection="LANDSAT/LC08/C02/T1_TOA"):
    """
    Creates a GEE export task for a given AOI ID
    Returns task information including task ID
    """
    try:
        # Get AOI from database
        aoi_data = get_aoi(aoi_id)
        if not aoi_data:
            return {"status": "error", "message": "AOI not found"}

        # Convert PostGIS geometry to GEE geometry
        # Assuming the geometry is in GeoJSON format
        geom_dict = json.loads(aoi_data['geometry'])
        geometry = ee.Geometry(geom_dict)

        # Get the image collection and filter
        collection = ee.ImageCollection(image_collection)\
            .filterBounds(geometry)\
            .sort('CLOUD_COVER')\
            .first()

        if not collection:
            return {"status": "error", "message": "No images found for this AOI"}

        # Set up export task
        task = ee.batch.Export.image.toDrive(
            image=collection,
            description=f'AOI_{aoi_id}_export',
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
            "description": f'AOI_{aoi_id}_export'
        }

    except Exception as e:
        return {"status": "error", "message": f"Export failed: {str(e)}"}

def check_task_status(task_id):
    """
    Check the status of a GEE export task
    """
    try:
        task_list = ee.data.getTaskList()
        task = next((t for t in task_list if t['id'] == task_id), None)
        if task:
            return {"status": "success", "task_status": task['state']}
        return {"status": "error", "message": "Task not found"}
    except Exception as e:
        return {"status": "error", "message": f"Status check failed: {str(e)}"}
