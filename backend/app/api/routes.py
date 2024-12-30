from flask import Blueprint, jsonify, request
from app.models.db import create_aoi, get_aois, get_aoi, update_aoi, delete_aoi
from app.api.gee_utils import initialize_gee, export_aoi_to_drive, check_task_status, export_aoi_to_local
import os
import json
from flask import current_app

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

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
        return jsonify({'message': 'Successfully fetched AOIs', 'aois': aois}), 200
    except Exception as e:
        return jsonify({'message': f'An error occurred while fetching AOIs: {e}'}), 500

@api_bp.route('/aois', methods=['POST'])
def create_new_aoi():
    data = request.get_json()

    # Basic input validation
    if not data or 'name' not in data or 'geometry' not in data:
        return jsonify({'message': 'Bad Request: Missing name or geometry'}), 400
    if not data['name'] or not data['geometry']:
        return jsonify({'message': 'Bad Request: Name and geometry cannot be empty'}), 400

    try:
        new_aoi_id = create_aoi(data['name'], data['geometry'])
        return jsonify({'message': 'AOI created', 'id': new_aoi_id}), 201
    except Exception as e:
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
    """Initialize GEE authentication"""
    try:
        result = initialize_gee()
        return jsonify(result), 200 if result['status'] == 'success' else 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/aois/<int:aoi_id>/export', methods=['POST'])
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
        
        result = export_aoi_to_drive(aoi_id, params)
        return jsonify(result), 200 if result['status'] == 'success' else 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/export/status/<task_id>', methods=['GET'])
def get_export_status(task_id):
    """Check status of an export task"""
    result = check_task_status(task_id)
    return jsonify(result), 200 if result['status'] == 'success' else 500

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