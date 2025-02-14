from flask import Flask, request, jsonify
import jwt
import os

app = Flask(__name__)
SECRET_KEY = "robot"  # Weak key

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "admin":
        return jsonify({"error": "Admins can only log in with a secure token!"}), 403

    token = jwt.encode({"user": data["username"], "role": "common"}, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

@app.route("/admin", methods=["GET"])
def admin():
    token = request.headers.get("Authorization").split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded["role"] == "admin":
            return "Flag : NoCable321"
        else:
            return "Access denied."
    except jwt.InvalidTokenError:
        return "Invalid token."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
