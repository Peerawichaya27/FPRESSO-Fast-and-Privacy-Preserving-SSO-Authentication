from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    'app1': {'user1' : {"app1": {"role": "admin"},
                        "app2": {"role": "user"},
                        "app3": {"role": "user"}}
            },
    'app2': {'user2' : {"app1": {"role": "user"},
                        "app2": {"role": "admin"},
                        "app3": {"role": "user"}}
            },
    'app3': {'user3' : {"app1": {"role": "user"},
                        "app2": {"role": "user"},
                        "app3": {"role": "admin"}}
            }
    }
    
@app.route('/get_role', methods=['GET'])
def get_role():
    apps = request.headers.get('appNo')
    username = request.headers.get('username')
    role = users[apps][username]
    return jsonify({'role': role}), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)