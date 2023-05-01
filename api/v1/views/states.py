from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object based on its ID"""
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
    else:
        return None

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Removes a State object from the database"""
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    return None

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Endpoint to create a new State object"""

    # Check if request data is in JSON format
    if not request.is_json:
        abort(400, "Not a JSON")

    # Get JSON data from the request
    data = request.get_json()

    # Check if the 'name' key is in the JSON data
    if 'name' not in data:
        abort(400, "Missing name")

    # Create a new State object with the data from the request
    state = State(**data)

    # Add the new State object to the storage
    storage.new(state)

    # Save the changes to the storage
    storage.save()

    # Return a JSON response with the new State object and a 201 status code
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    if state_id:
        # get the State object with the given state_id from the storage
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        # If the request data is not in JSON format,
        # we return a 400 Bad Request error using Flask's abort function
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        # save updated state object
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
