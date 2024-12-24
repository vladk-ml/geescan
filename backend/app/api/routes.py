from flask import Blueprint, jsonify, request
from app.models.db import create_aoi, get_aois, get_aoi, update_aoi, delete_aoi

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