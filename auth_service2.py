from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    encoded = request.json.get('credentials')
    username, password = base64.b64decode(encoded).decode('utf-8').split(':')
    # Implement actual user verification logic here
    if username == "user3" and password == "password3":  # Example validation
        return jsonify({'status': 'success', 'username': username, 'role': 'manager'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=5002,debug=True)
