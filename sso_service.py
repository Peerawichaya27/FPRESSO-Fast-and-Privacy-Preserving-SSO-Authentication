from flask import Flask, request, jsonify, make_response
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    role = request.json.get('role')
    
    # Create SSO token with user details
    sso_token = jwt.encode({
        'sub': username,
        'role': role,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm=ALGORITHM)
    
    resp = make_response(jsonify({'sso_token': sso_token}))
    resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax', path='/')
    return resp

@app.route('/verify', methods=['GET'])
def verify():
    sso_token = request.cookies.get('sso_token')
    try:
        decoded = jwt.decode(sso_token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        return jsonify({'status': 'verified', 'username': decoded['sub'], 'role': decoded['role']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
