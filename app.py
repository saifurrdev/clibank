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

def add_user(username, password):
    try:
        with open(database_path, 'a') as file:
            make_session = {'user': username, 'password': password, 'timec': int(time.time()), 'timee': int(time.time()) + 86400}
            session_token = encode(data=str(make_session), password=dbs_pass)
            file.write(f"{username}--=--{encode(data=password, password=dbs_pass)}--=--{session_token}\n")
        return {'msg': 0, 'session': session_token}
    except:
        return {'msg': 1, 'session': None}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('user')
    password = data.get('pass')
    if user_check(username) == True:
        return jsonify({'status': 'error', 'message': 'User already exists'}), 400
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
