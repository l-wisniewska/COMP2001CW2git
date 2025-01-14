from flask import Blueprint, jsonify, request
from app.models import User, Trail
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import logging

app_routes = Blueprint('routes', __name__)

@app_routes.route("/login", methods=["POST"])
def login():
    """Authenticate user and generate JWT token"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(Email_address=email).first()
    if not user or password != "insecurePassword":  # Replace with hash validation
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity={"user_id": user.UserID, "role": user.Role})
    return jsonify({"access_token": access_token}), 200



# get all users
@app_routes.route("/users", methods=["GET"])
def get_users():
    """Fetch all users"""
    users = User.query.all()
    return jsonify([{"UserID": u.UserID, "Email_address": u.Email_address, "Role": u.Role} for u in users])

# create a new user
@app_routes.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    data = request.get_json()
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201

# get all trails
@app_routes.route("/trails", methods=["GET"])
def get_trails():
    """Fetch all trails"""
    trails = Trail.query.all()
    return jsonify([{col.name: getattr(t, col.name) for col in Trail.__table__.columns} for t in trails])

# create a new trail (Admin only)
@app_routes.route("/trails", methods=["POST"])
@jwt_required()
def create_trail():
    """Create a new trail"""
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    if "Trail_ID" in data:
        data["TrailID"] = data.pop("Trail_ID")

    try:
        new_trail = Trail(**data)
        db.session.add(new_trail)
        db.session.commit()
        return jsonify({"message": "Trail created successfully."}), 201
    except Exception as e:
        logging.error(f"Error creating trail: {e}")
        return jsonify({"message": "An error occurred while creating the trail."}), 500

# get a trail by ID
@app_routes.route("/trails/<int:trail_id>", methods=["GET"])
def get_trail_by_id(trail_id):
    """Fetch a trail by ID"""
    trail = Trail.query.filter_by(TrailID=trail_id).first()
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    return jsonify({
        "TrailID": trail.TrailID,
        "TrailName": trail.TrailName,
        "TrailDescription": trail.TrailDescription,
        "Difficulty": trail.Difficulty,
        "Location": trail.Location,
        "Length": trail.Length,
        "ElevationGain": trail.ElevationGain,
        "RouteType": trail.RouteType,
        "OwnerID": trail.OwnerID
    }), 200

# Update a trail by ID
@app_routes.route("/trails/<int:trail_id>", methods=["PUT"])
@jwt_required()
def update_trail(trail_id):
    """Update a trail by ID"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    trail = Trail.query.filter_by(TrailID=trail_id).first()
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    for key, value in data.items():
        if hasattr(trail, key):
            setattr(trail, key, value)

    db.session.commit()
    return jsonify({"message": "Trail updated successfully."}), 200

# delete a trail by ID
@app_routes.route("/trails/<int:trail_id>", methods=["DELETE"])
@jwt_required()
def delete_trail(trail_id):
    """Delete a trail by ID"""
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    trail = Trail.query.filter_by(TrailID=trail_id).first()
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    try:
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully."}), 200
    except Exception as e:
        logging.error(f"Error deleting trail: {e}", exc_info=True)
        return jsonify({"message": "An error occurred while deleting the trail."}), 500
