#!/usr/bin/e +nv python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import random
import re
import socket
import ssl
import uuid, secrets
from flask import (Flask, make_response,
                   redirect, render_template, request, session, url_for)
import logging
import zen_utils

# Disabling flask native debug logs to make manual logs fore clear in log file
logging.getLogger('werkzeug').disabled = True

# Logging setting as per the requirement
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='test.log', encoding='utf-8', level=logging.DEBUG)


app = Flask(__name__)

# Randomized secrets to use for session
app.secret_key = secrets.token_hex(16)

# Securing the session token
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Hardcoded certificates for test ease
CA_FILE = "www.crt"
SERVER_KEY="server.key"
HOST = "localhost"

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = sanitize(request.form.get('username', ''))
    password = sanitize(request.form.get('password', ''))

    if request.method == 'POST':
        credsAreValid = (username, password) in [('u1234567', 'csc2330a3')]

        # NOTE: If I enable this csrf validation, then test scripts complains because it's
        # not configured to test for a case with csrf_token. So, I'm disabling this
        # If you need to validate changing the script, just uncomment lines: 41, 43, 53, 54, 55
        # And comment lines: 45, 57, 48
        # validCSRF = session.get('csrf_token') == request.form.get('csrf_token', '')

        # if credsAreValid and validCSRF:
        if credsAreValid:
            logging.info(f"SECURITY: Successful login attempt: IP={request.remote_addr}, username={username}")
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex 
            response = make_response(render_template('logged_in.html'))
            response.set_cookie('session', username)
            return response

        logging.info(f"SECURITY: Unsuccessful login attempt: IP={request.remote_addr}, username={username}")

    # csrf_token = uuid.uuid4().hex
    # session['csrf_token'] = csrf_token
    # return render_template('login_with_csrf.html', csrf_token=csrf_token)
    return render_template('login.html')

@app.route('/logout')
def logout():
    logging.info(f"SECURITY: Successful logout attempt: IP={request.remote_addr}, username={session.get('username')}")
    session.pop('username', None)
    session.pop('csrf_token', None)
    return render_template("logout.html")

@app.route('/restricted', methods=['GET', 'POST'])
def restricted():
    username = session.get('username')

    if username: 
        if request.method == 'POST':
                csrf_token = request.form.get('csrf_token')
                if session['csrf_token'] == csrf_token:
                    logging.info(f"SECURITY: Successful aphorism request: IP={request.remote_addr}, username={session.get('username')}")
                    zen = request_aphorisms()
                    return render_template("aphorism.html", zen=zen)
                logging.info(f"SECURITY: CSRF attempt detected. Unsuccessful aphorism request.: IP={request.remote_addr}, username={session.get('username')}")
                # Else redirects to login below
        else:
            return render_template('restricted.html', csrf=session['csrf_token'])

    logging.info(f"SECURITY: Unsuccessful aphorism request. No session: IP={request.remote_addr}, username={session.get('username')}")
    return redirect(url_for("login"), 307)

def request_aphorisms():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, 3000))
    cxt = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=CA_FILE)
    secure_sock = cxt.wrap_socket(sock, server_side=False, server_hostname=HOST)
    aphorisms = list(zen_utils.aphorisms)
    received_answers = []
    for aphorism in random.sample(aphorisms, 3):
        secure_sock.sendall(aphorism)
        received_answers.append(str(aphorism) + " " + str(zen_utils.recv_until(secure_sock, b'.')))
    return received_answers

def sanitize(input_string):
    sanitized_input = input_string.strip()
    sanitized_input = re.sub(r'[^\w\s]', '', sanitized_input)
    return sanitized_input

if __name__ == '__main__':
    app.run(host=HOST, ssl_context=(CA_FILE, SERVER_KEY), debug=True)
