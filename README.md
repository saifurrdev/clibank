Workspace: Collecting workspace information# EchoBank

EchoBank is a simple bank CLI and API application for secure user registration and session management. It uses encrypted storage for credentials and session tokens.

## Features

- User registration via REST API
- Session token generation and validation
- Credentials and sessions encrypted using password-based key derivation
- CLI client for interacting with the API

## Project Structure

```
app.py                # Flask API server
public/cliapp.py      # CLI client application
utils/enc.py          # Encryption utilities
dbs/dbs_enc.ecb       # Encrypted database file
requerments.txt       # Python dependencies
README.md             # Project documentation
```

## Installation

1. **Clone the repository**
2. **Install dependencies**

```sh
pip install -r requerments.txt
```

## Usage

### Start the API Server

```sh
python app.py
```

The server will run at `http://localhost:5000`.

### Register a User

Send a POST request to `/api/register`:

```sh
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"user": "your_username", "pass": "your_password"}'
```

### Validate Session

Send a POST request to `/api/session` with your session token:

```sh
curl -X POST http://localhost:5000/api/session \
  -H "Content-Type: application/json" \
  -d '{"session": "your_session_token"}'
```

### CLI Client

Run the CLI client:

```sh
python public/cliapp.py
```

## Encryption

All credentials and session tokens are encrypted using the `encode` and `decode` functions in enc.py.

## Configuration

- Change the database password in `dbs_pass` in app.py for stronger security.
- The encrypted database is stored in dbs_enc.ecb.

## License

MIT License

---

Developed by SaifurrDev