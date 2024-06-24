from flask import Flask, request, jsonify
import jwt
import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

app = Flask(__name__)

# Function to generate SSO token
def generate_sso_token(user_identity_data):
    # Step 1: Create JWT token
    jwt_token = create_jwt(user_identity_data)
    authorization_policy = get_authorization_policy(user_identity_data)
    
    # Step 2: Bind authorization policy (hash values)
    role_hash = hash_data(authorization_policy['roles'])
    permission_hash = hash_data(authorization_policy['permissions'])
    jwt_token['roleHash'] = role_hash
    jwt_token['permissionHash'] = permission_hash
    
    # Step 3: Sign the token with HSM
    token_string = jwt.encode(jwt_token, 'your_secret_key', algorithm='HS256')
    signed_token = sign_token(token_string)
    
    # Step 4: Perturb the token
    perturbed_token = perturb_token(signed_token)
    
    # Step 5: Padding
    padded_token = pad_token(perturbed_token)
    return padded_token

# Function to create JWT token
def create_jwt(user_identity_data):
    jwt_token = {
        "userID": user_identity_data['userID'],
        "roles": user_identity_data['roles'],
        "permissions": user_identity_data['permissions']
    }
    return jwt_token

# Function to hash data
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to sign token
def sign_token(token):
    private_key = RSA.import_key(open('private.pem').read())
    h = SHA256.new(token.encode())
    signature = pkcs1_15.new(private_key).sign(h)
    return signature.hex()

# Function to perturb token
def perturb_token(token):
    R = os.urandom(256)
    perturbed_token = bytes(a ^ b for a, b in zip(token.encode(), R))
    return perturbed_token.hex()

# Function to pad token
def pad_token(token):
    R1 = os.urandom(32)
    R2 = os.urandom(32)
    padded_token = R1 + token + R2
    return padded_token.hex()

# Dummy function to get authorization policy
def get_authorization_policy(user_identity_data):
    return {
        "roles": "admin",
        "permissions": "read,write"
    }

@app.route('/generate-token', methods=['POST'])
def generate_token():
    user_identity_data = request.json
    sso_token = generate_sso_token(user_identity_data)
    return jsonify({"sso_token": sso_token})

if __name__ == '__main__':
    app.run(port=5000)
