from flask import Blueprint, request, jsonify
from .video import process_video

main_bp = Blueprint("main", __name__)

@main_bp.route
