from flask import Blueprint, jsonify, request, send_from_directory
from app.models.db import create_aoi, get_aois, get_aoi, update_aoi, delete_aoi, get_db_connection
from app.api.gee_utils import initialize_gee, export_aoi_to_asset, check_task_status
import os
import json
from flask import current_app
import ee
from datetime import datetime
from functools import wraps

api_bp = Blueprint('api', __name__)

# Global state tracker for GEE initialization
gee_state = {
    'initialized': False,
    'last_init_time': None,
    'init_count': 0
}

def ensure_gee_initialized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not gee_state['initialized']:
            result = initialize_gee()
            if result['status'] != 'success':
                return jsonify(result), 500
            gee_state['initialized'] = True
            gee_state['last_init_time'] = datetime.now()
            gee_state['init_count'] += 1
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Comprehensive health check of all system components"""
    health_status = {
        'status': 'healthy',
        'components': {
            'api': 'healthy',
            'database': 'unknown',
            'gee': 'unknown'
        }
    }
    
    # Check database
    try:
        conn = get_db_connection()
        if conn is not None:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                conn.close()
                health_status['components']['database'] = 'healthy'
        else:
            health_status['components']['database'] = 'unhealthy'
    except Exception as e:
        health_status['components']['database'] = 'unhealthy'
    
    # Check GEE status
    try:
        if gee_state['initialized']:
            health_status['components']['gee'] = 'healthy'
        else:
            health_status['components']['gee'] = 'not initialized'
    except Exception as e:
        health_status['components']['gee'] = 'error'
    
    # Overall status is healthy only if all components are healthy
    if any(status != 'healthy' for status in health_status['components'].values()):
        health_status['status'] = 'degraded'
    
    return jsonify(health_status), 200

@api_bp.route('/health/api', methods=['GET'])
def api_health_check():
    """Check API health and basic functionality"""
    try:
        # Get basic system info
        api_info = {
            'status': 'healthy',
            'service': 'api',
            'version': '1.0.0',  # We should track this somewhere
            'uptime': datetime.now().isoformat(),
            'endpoints': {
                'total': len([rule for rule in current_app.url_map.iter_rules()]),
                'active': True
            }
        }
        return jsonify(api_info), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'api',
            'message': str(e)
        }), 500

@api_bp.route('/health/db', methods=['GET'])
def db_health_check():
    """Check database connection health"""
    try:
        conn = get_db_connection()
        if conn is not None:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                conn.close()
                return jsonify({
                    'status': 'healthy',
                    'service': 'database'
                }), 200
        return jsonify({
            'status': 'unhealthy',
            'service': 'database',
            'message': 'Could not establish connection'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'database',
            'message': str(e)
        }), 500

@api_bp.route('/health/gee', methods=['GET'])
def gee_health_check():
    """Check GEE service health"""
    try:
        if gee_state['initialized']:
            return jsonify({
                'status': 'healthy',
                'service': 'gee',
                'last_init': gee_state['last_init_time'].isoformat() if gee_state['last_init_time'] else None,
                'init_count': gee_state['init_count']
            }), 200
        return jsonify({
            'status': 'not initialized',
            'service': 'gee'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'service': 'gee',
            'message': str(e)
        }), 500

@api_bp.route('/test_create_aoi', methods=['POST'])
def test_create_aoi():
    test_name = 'Test AOI'
    test_geometry = 'SRID=4326;POLYGON((-74.0060 40.7128, -74.0065 40.7128, -74.0065 40.7123, -74.0060 40.7123, -74.0060 40.7128))'

    print(f"Attempting to create test AOI with name: {test_name} and geometry: {test_geometry}")

    try:
        new_aoi_id = create_aoi(test_name, test_geometry)
        if new_aoi_id:
            print(f"Test AOI created successfully with ID: {new_aoi_id}")
            return jsonify({'message': 'Test AOI created successfully', 'id': new_aoi_id}), 201
        else:
            print("Failed to create test AOI. Check logs for errors.")
            return jsonify({'message': 'Failed to create test AOI'}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': f'An error occurred: {e}'}), 500

@api_bp.route('/test_aois', methods=['GET'])
def test_aois():
    """Retrieves all AOIs for testing purposes."""
    try:
        aois = get_aois()
        return jsonify({'message': 'Successfully fetched AOIs', 'aois': aois}), 200
    except Exception as e:
        return jsonify({'message': f'An error occurred: {e}'}), 500

@api_bp.route('/aois', methods=['GET'])
def aois():
    try:
        aois = get_aois()
        print(f"Fetched AOIs: {aois}")  # Debug logging
        return jsonify({'message': 'Successfully fetched AOIs', 'aois': aois}), 200
    except Exception as e:
        print(f"Error in /aois route: {e}")  # Debug logging
        return jsonify({'message': f'An error occurred while fetching AOIs: {e}'}), 500

@api_bp.route('/aois', methods=['POST'])
def create_new_aoi():
    data = request.get_json()
    print(f"Received data: {data}")  # Debug log

    # Basic input validation
    if not data or 'name' not in data or 'geometry' not in data:
        return jsonify({'message': 'Bad Request: Missing name or geometry'}), 400
    if not data['name'] or not data['geometry']:
        return jsonify({'message': 'Bad Request: Name and geometry cannot be empty'}), 400

    try:
        # Convert geometry to WKT format if it's a GeoJSON
        geometry = data['geometry']
        print(f"Input geometry: {geometry}")  # Debug log
        
        # Ensure geometry is a string
        if isinstance(geometry, dict):
            geometry = json.dumps(geometry)
        print(f"Processed geometry: {geometry}")  # Debug log
        
        # Get optional description
        description = data.get('description')
        
        # Create AOI and get its ID
        new_aoi_id = create_aoi(data['name'], geometry, description)
        print(f"Result from create_aoi: {new_aoi_id}")  # Debug log
        
        if new_aoi_id:
            # Get the newly created AOI to return its full data
            new_aoi = get_aoi(new_aoi_id)
            return jsonify({
                'message': 'Successfully created AOI',
                'aoi': new_aoi
            }), 201
        else:
            return jsonify({'message': 'Failed to create AOI'}), 500
    except Exception as e:
        print(f"Error in create_new_aoi: {str(e)}")  # Debug log
        return jsonify({'message': f'Error creating AOI: {e}'}), 500

@api_bp.route('/aois/<int:aoi_id>', methods=['PUT'])
def update_existing_aoi(aoi_id):
    data = request.get_json()

    # Basic input validation
    if not data or 'name' not in data or 'geometry' not in data:
        return jsonify({'message': 'Bad Request: Missing name or geometry'}), 400
    if not data['name'] or not data['geometry']:
        return jsonify({'message': 'Bad Request: Name and geometry cannot be empty'}), 400

    try:
        success = update_aoi(aoi_id, data['name'], data['geometry'])
        if success:
            return jsonify({'message': 'AOI updated'}), 200
        else:
            return jsonify({'message': 'Error updating AOI'}), 500
    except Exception as e:
        return jsonify({'message': f'Error updating AOI: {e}'}), 500

@api_bp.route('/aois/<int:aoi_id>', methods=['DELETE'])
def delete_existing_aoi(aoi_id):
    try:
        success = delete_aoi(aoi_id)
        if success:
            return jsonify({'message': 'AOI deleted'}), 200
        else:
            return jsonify({'message': 'Error deleting AOI'}), 500
    except Exception as e:
        return jsonify({'message': f'Error deleting AOI: {e}'}), 500

@api_bp.route('/aois/<int:aoi_id>', methods=['GET'])
def get_single_aoi(aoi_id):
    try:
        aoi = get_aoi(aoi_id)
        if aoi:
            return jsonify({'message': 'AOI fetched successfully', 'aoi': aoi}), 200
        else:
            return jsonify({'message': 'AOI not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error fetching AOI: {e}'}), 500

@api_bp.route('/auth/gee', methods=['POST'])
def authenticate_gee():
    """Initialize GEE authentication and return detailed status"""
    try:
        result = initialize_gee()
        if result['status'] == 'success':
            gee_state['initialized'] = True
            gee_state['last_init_time'] = datetime.now()
            gee_state['init_count'] += 1
            
            # Add state information to response
            result.update({
                'initialized_at': gee_state['last_init_time'].isoformat(),
                'init_count': gee_state['init_count']
            })
        
        return jsonify(result), 200 if result['status'] == 'success' else 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/auth/gee/status', methods=['GET'])
def get_gee_status():
    """Get current GEE authentication status"""
    return jsonify({
        'status': 'success',
        'initialized': gee_state['initialized'],
        'last_init_time': gee_state['last_init_time'].isoformat() if gee_state['last_init_time'] else None,
        'init_count': gee_state['init_count']
    }), 200

@api_bp.route('/aois/<int:aoi_id>/export', methods=['POST'])
@ensure_gee_initialized
def export_aoi(aoi_id):
    """Start GEE export task for an AOI"""
    try:
        data = request.get_json() or {}
        params = {
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'polarization': data.get('polarization', ['VV', 'VH']),
            'orbit': data.get('orbit', 'ASCENDING')
        }
        
        result = export_aoi_to_asset(aoi_id, params)
        return jsonify(result), 200 if result['status'] == 'success' else 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/export/status/<task_id>', methods=['GET'])
@ensure_gee_initialized
def get_export_status(task_id):
    """Check status of an export task"""
    result = check_task_status(task_id)
    return jsonify(result), 200 if result['status'] == 'success' else 500

@api_bp.route('/auth/db/status', methods=['GET'])
def check_db_status():
    """Check database connection status"""
    try:
        conn = get_db_connection()
        if conn is not None:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")  # Simple query to test connection
                conn.close()
                return jsonify({'status': 'connected', 'message': 'Database connection successful'}), 200
        return jsonify({'status': 'error', 'message': 'Could not establish database connection'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500

@api_bp.route('/preferences', methods=['GET', 'POST'])
def handle_preferences():
    """Handle user preferences like default time ranges"""
    prefs_file = os.path.join(current_app.root_path, 'user_preferences.json')
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            with open(prefs_file, 'w') as f:
                json.dump(data, f)
            return jsonify({"status": "success", "message": "Preferences saved"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        try:
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    return jsonify(json.load(f)), 200
            return jsonify({}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/time-presets', methods=['GET'])
def list_time_presets():
    """List all time range presets"""
    try:
        presets_file = os.path.join(current_app.root_path, 'time_range_presets.json')
        if os.path.exists(presets_file):
            with open(presets_file, 'r') as f:
                data = json.load(f)
                return jsonify({"status": "success", "presets": data["presets"]}), 200
        return jsonify({"status": "error", "message": "No presets found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/time-presets', methods=['POST'])
def create_time_preset():
    """Create a new time range preset"""
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'days_back' not in data:
            return jsonify({"status": "error", "message": "Name and days_back required"}), 400

        presets_file = os.path.join(current_app.root_path, 'time_range_presets.json')
        
        # Load existing presets
        if os.path.exists(presets_file):
            with open(presets_file, 'r') as f:
                presets_data = json.load(f)
        else:
            presets_data = {"presets": {}, "next_id": 1}

        # Create new preset
        preset_id = f"preset_{presets_data['next_id']}"
        presets_data['next_id'] += 1
        
        presets_data['presets'][preset_id] = {
            "id": preset_id,
            "name": data['name'],
            "description": data.get('description', ''),
            "days_back": data['days_back']
        }

        # Save updated presets
        with open(presets_file, 'w') as f:
            json.dump(presets_data, f, indent=4)

        return jsonify({
            "status": "success",
            "message": "Preset created",
            "preset": presets_data['presets'][preset_id]
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/time-presets/<preset_id>', methods=['DELETE'])
def delete_time_preset(preset_id):
    """Delete a time range preset"""
    try:
        if preset_id == 'default':
            return jsonify({"status": "error", "message": "Cannot delete default preset"}), 400

        presets_file = os.path.join(current_app.root_path, 'time_range_presets.json')
        if not os.path.exists(presets_file):
            return jsonify({"status": "error", "message": "No presets found"}), 404

        with open(presets_file, 'r') as f:
            presets_data = json.load(f)

        if preset_id not in presets_data['presets']:
            return jsonify({"status": "error", "message": "Preset not found"}), 404

        del presets_data['presets'][preset_id]

        with open(presets_file, 'w') as f:
            json.dump(presets_data, f, indent=4)

        return jsonify({"status": "success", "message": "Preset deleted"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/dev', methods=['GET'])
def dev_dashboard():
    """Serve the development dashboard"""
    return send_from_directory('static', 'dev.html')

@api_bp.route('/test', methods=['GET'])
@ensure_gee_initialized
def test():
    """Legacy test endpoint - use /auth/gee for authentication and /auth/gee/status for status checks"""
    try:
        # Get basic GEE info without re-authenticating
        image = ee.Image('USGS/SRTMGL1_003')
        info = image.getInfo()
        return jsonify({
            "status": "success",
            "message": "GEE connection successful",
            "gee_status": {
                "initialized": gee_state['initialized'],
                "last_init_time": gee_state['last_init_time'].isoformat() if gee_state['last_init_time'] else None,
                "init_count": gee_state['init_count']
            },
            "test_image_info": info
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }), 500