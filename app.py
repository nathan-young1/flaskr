from datetime import timedelta
from flask import *
from auth.authentication import AuthenticationHandler

# from auth.authentication import AuthenticationHandler
from db.db_connector import MYSQL_DB
from auth.user_model import User

app = Flask(__name__)
# App secret for encryption purposes.
app.secret_key = "1234"
# Set session lifetime
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def register():
    return render_template('signup.html')

@app.route('/forgotPassword')
def forgotPassword():
    return render_template('forgot_password.html')


@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]

        if AuthenticationHandler.get_instance().validate_login_credientials(username, password):
            session['user'] = username
            return jsonify({"auth_result": True})

    return jsonify({"auth_result": False})

@app.route('/signup', methods=['POST'])
def register_post():
    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]

        if AuthenticationHandler.get_instance().register(username, password):
            session['user'] = username
            return jsonify({"auth_result": True})

    return jsonify({"auth_result": False})

@app.route('/forgotPassword', methods=['POST'])
def forgotPassword_post():
    if request.method == 'POST':
        username = request.json["username"]
        newPassword = request.json["password"]

        if AuthenticationHandler.get_instance().forgot_password(username, newPassword):
            session['user'] = username
            return jsonify({"auth_result": True})

    return jsonify({"auth_result": False})

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        data = {
            'username': session['user']
        }
        return render_template('dashboard.html', **data)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/error')
@app.errorhandler(404)
def error(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)