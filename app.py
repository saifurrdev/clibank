from flask import Flask, request, jsonify
from utils.enc import encode, decode
import time

app = Flask(__name__)

# Credentials
database_path = 'dbs/dbs_enc.ecb'
dbs_pass = "Adaa1458FF@" # you can set a strong password here

@app.route('/')
def hello():
    return "v/0.1"

def user_check(username):
    try:
        with open(database_path, 'r') as file:
            for item in file.read().splitlines():
                if item.split(';')[0] == username:
                    return True
        return False
    except:
        return True

@app.route('/api/session', methods=['POST'])
def check_session():
    data = request.json
    session_token = data.get('session')
    try:
        session_data = decode(encoded=session_token, password=dbs_pass)
        session_dict = eval(session_data)
        if 'timee' in session_dict and int(time.time()) < session_dict['timee']:
            return jsonify({'status': 0, 'message': 'Session valid'}), 200
        else:
            return jsonify({'status': 1, 'message': 'Session expired'}), 401
    except Exception as e:
        return jsonify({'status': 1, 'message': 'Invalid session'}), 401

def add_user(username, password):
    try:
        with open(database_path, 'a') as file:
            make_session = {'user': username, 'password': password, 'timec': int(time.time()), 'timee': int(time.time()) + 86400}
            session_token = encode(data=str(make_session), password=dbs_pass)
            file.write(f"{username}--=--{encode(data=password, password=dbs_pass)}--=--{session_token}\n")
        return {'msg': 0, 'session': session_token}
    except:
        return {'msg': 1, 'session': None}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('user')
    password = data.get('pass')
    if user_check(username) == True:
        return jsonify({'status': 1, 'message': 'User already exists'}), 400
    result = add_user(username, password)
    if result['msg'] == 0:
        return jsonify({'status': 0, 'session': result['session']}), 200
    else:
        return jsonify({'status': 1, 'message': 'Registration failed'}), 500
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('user')
    password = data.get('pass')
    try:
        with open(database_path, 'r') as file:
            for item in file.read().splitlines():
                stored_user, stored_pass_enc, stored_session = item.split('--=--')
                if stored_user == username:
                    stored_pass = decode(encoded=stored_pass_enc, password=dbs_pass)
                    if stored_pass == password
                        new_session_data = {'user': username, 'password': password, 'timec': int(time.time()), 'timee': int(time.time()) + 86400}
                        new_session_token = encode(data=str(new_session_data), password=dbs_pass)
                        updated_lines = []
                        for line in file.read().splitlines():
                            if line.startswith(f"{username}--=--"):
                                updated_lines.append(f"{username}--=--{stored_pass_enc}--=--{new_session_token}\n")
                            else:
                                updated_lines.append(line + '\n')
                        with open(database_path, 'w') as f:
                            f.writelines(updated_lines)
                        return jsonify({'status': 0, 'session': new_session_token}), 200
                    else:
                        return jsonify({'status': 1, 'message': 'Incorrect password'}), 401
        return jsonify({'status': 1, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'status': 1, 'message': 'Login failed'}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
