"""Main Flask application for Ngrok API."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from ngrok_app import NgrokManager, Config

app = Flask(__name__)
CORS(app)

config = Config()
manager = NgrokManager()


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "ngrok-api"}), 200


@app.route("/api/tunnels", methods=["GET"])
def get_tunnels():
    """Get all active tunnels."""
    tunnels = manager.list_tunnels()
    return jsonify({"tunnels": tunnels, "count": len(tunnels)}), 200


@app.route("/api/tunnels", methods=["POST"])
def create_tunnel():
    """Create a new tunnel."""
    data = request.get_json()

    if not data or "protocol" not in data or "local_port" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        tunnel_info = manager.create_tunnel(
            protocol=data.get("protocol", "http"),
            local_addr=data.get("local_addr", "localhost"),
            local_port=int(data.get("local_port")),
            name=data.get("name"),
        )
        return jsonify(tunnel_info), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tunnels/<name>", methods=["GET"])
def get_tunnel(name):
    """Get tunnel information."""
    tunnel = manager.get_tunnel(name)
    if tunnel:
        return jsonify(tunnel), 200
    return jsonify({"error": "Tunnel not found"}), 404


@app.route("/api/tunnels/<name>", methods=["DELETE"])
def delete_tunnel(name):
    """Delete a tunnel."""
    if manager.close_tunnel(name):
        return jsonify({"message": f"Tunnel {name} closed"}), 200
    return jsonify({"error": "Tunnel not found"}), 404


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    try:
        app.run(
            host="0.0.0.0",
            port=config.api_port,
            debug=config.debug,
        )
    except KeyboardInterrupt:
        manager.close_all()