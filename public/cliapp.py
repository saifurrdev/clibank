import requests
import os

logo = """
Bank CLI Application
Developed by SaifurrDev"""
version = "1.0.0"

def clear_sc():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    clear_sc()
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
    else:
        print("Session expired or invalid. Please log in again.")
        linex()
        session_token = None


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

def reglog():
    print_logo()
    print("Login")
    linex()
    username = input("Enter username: ")
    password = input("Enter password: ")
    json_data = {'user': username, 'pass': password}
    url = f"{api_url}/api/login"
    r = requests.post(url, json=json_data).json()
    if r['status'] == 0:
        with open(session, 'w') as f:
            f.write(r['session'])
        print("Login successful. Session token saved.")
    else:
        print(f"Error: {r['message']}")

def main():
    print_logo()
    if session_token:
        print("You are already logged in.")
        dashboard()
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option (1 or 2): ")
    if choice == '1':
        register()
    elif choice == '2':
        reglog()
    else:
        print("Invalid choice. Please select 1 or 2.")

def dashboard():
    print_logo()
    print("Welcome to your dashboard!")
    linex()
    print("1. View Profile")
    print("2. Logout")
    choice = input("Choose an option (1 or 2): ")
    if choice == '1':
        print("Profile details would be shown here.")
    elif choice == '2':
        try:
            os.remove(session)
            print("Logged out successfully.")
        except FileNotFoundError:
            print("No active session found.")
    else:
        print("Invalid choice. Please select 1 or 2.")