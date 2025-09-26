from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response
import subprocess
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()
#load the extension

def gen_pgp_challenge():
    _ = subprocess.run(["scripts/gen_challenge.sh"], capture_output=False)
    with open('scripts/encrypted.txt', 'r') as file:
        challenge = file.read()
    return challenge

def gen_index():
    # generates a pgp encrypted challenge that the user most solve to authenticate
    challenge = gen_pgp_challenge()
    return render_template("index.html", pgp=challenge)

def authenticate_user():
    user_solution = request.form.get('solution')
    with open('scripts/solution.txt', 'r') as file:
        correct_solution = file.read().strip()
    # if user solves the challenge, they are authenticated and go to admin page
    if user_solution == correct_solution:
        session['authenticated'] = True
        return redirect(url_for('admin'))
    else:
        flash('Invalid Solution')
        return redirect(url_for('index'))

def api_response(text):
    response = make_response(text)
    response.headers['Content-Type'] = 'text/plain'
    return response

def authenticate_api():
    api_solution = request.data.decode('utf-8')
    with open('scripts/solution.txt', 'r') as file:
        correct_solution = file.read().strip()
    if api_solution == correct_solution:
        session['authenticated'] = True
        return api_response("You have solved the challenge and have been authenticated!")
    else:
        return api_response("You have failed to solve the challenge, please try again!")

    
@app.route("/", methods=['GET', 'POST'])
def index():
    # authenticate request when answer is submitted
    if request.method == 'POST':
        return authenticate_user()
    else:
        return gen_index()
# /pgp directory is for headless requests for authenticaton, e.g a program wanting to access the /admin page
@app.route("/api", methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        return authenticate_api()
    else:
        return api_response(gen_pgp_challenge())

@app.route("/admin")
def admin():
    # only allow authenticated users to acces this page
    if not session.get('authenticated'):
        flash('Authentication required to enter!')
        return redirect(url_for('index'))
    else:
        return "You have been authenticated!"

@app.route("/admin_api")
def admin_api():
    if not session.get('authenticated'):
        return api_response("You can not access this page without first solving the pgp challenge!")
    else:
        return api_response("You have been authenticated!")



