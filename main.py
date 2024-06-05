
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

users = [
    User(1, 'John', 'john@example.com'),
    User(2, 'Jane', 'jane@example.com')
]

@app.route('/')
def index():
    return render_template('auth.html')

@app.route('/google')
def google_auth():
    return redirect(url_for('oauth2callback', provider='google'))

@app.route('/facebook')
def facebook_auth():
    return redirect(url_for('oauth2callback', provider='facebook'))

@app.route('/microsoft')
def microsoft_auth():
    return redirect(url_for('oauth2callback', provider='microsoft'))

@app.route('/oauth2callback')
def oauth2callback():
    provider = request.args.get('provider')
    user_info = get_user_info_from_provider(provider)

    user = next((user for user in users if user.email == user_info['email']), None)

    if not user:
        user = User(len(users) + 1, user_info['name'], user_info['email'])
        users.append(user)

    login_user(user)

    return redirect(url_for('account'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
