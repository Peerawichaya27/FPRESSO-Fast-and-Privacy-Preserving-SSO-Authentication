from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jwt_secret_key1'

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.json['username'] # Simulated validation
    role = request.json['role']
    # Normally here you would validate the password. We simulate it.
    token = jwt.encode({'username': username, 'role': role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'status': 'success', 'jwt_token': token}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
