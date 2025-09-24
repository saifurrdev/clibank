import requests

logo = """
Bank CLI Application
Developed by SaifurrDev"""
version = "1.0.0"

def print_logo():
    print(logo)
    print(f"Version: {version}\n")

def linex():
    print('-' * 40)

api_url = "http://localhost:5000"

session = 'session_token.txt'
try:
    with open(session, 'r') as f:
        session_token = f.read().strip()
except FileNotFoundError:
    session_token = None

def check_session():
    json_data = {'session': session_token}
    url = f"{api_url}/api/session"
    r = requests.post(url, json=json_data)
    if r['status'] == 0:
        return True
    return False  
    
if session_token:
    if check_session():
        print("Session valid. You are logged in.")
        linex()

def register():
    print_logo()
    print("Register New User")
    linex()
    username = input("Enter username: ")
    password = input("Enter password: ")
    json_data = {'user': username, 'pass': password}
    url = f"{api_url}/api/register"
    r = requests.post(url, json=json_data).json()
    if r['status'] == 0:
        with open(session, 'w') as f:
            f.write(r['session'])
        print("Registration successful. Session token saved.")
    else:
        print(f"Error: {r['message']}")