from flask import Flask, request, redirect, render_template
import cgi
import os
 
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('index.html', title="User Signup")


def is_valid_email(address):
    if len(address) < 3 or len(address) > 20:
        return False

    at = "@"
    at_count = address.count(at)
    if at_count != 1:
        return False

    period = "."
    period_count = address.count(period)
    if period_count != 1:
        return False

    space = " "
    space_count = address.count(space)
    if space_count != 0:
        return False

    else:
        return True

@app.route("/register", methods=['POST'])
def register():

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']
    
    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''
    space = ' ' 

    #validate username
    if len(username) < 3 or len(username) > 20:
        username_error = 'Username must be between 3 and 20 characters.'
        password = ''
        verify = ''
    if username.count(space) != 0:
        username_error = "Username cannot contain spaces."
        password = ''
        verify = ''

    #validate passwords and make sure they match
    if password == '':
        password_error = "Please enter a valid password."
    elif len(password) < 3 or len(password) > 20:
        password_error = "Password must be between 3 and 20 characters."
    elif ' ' in password:
        password_error = "Your password cannot contain spaces."

    if verify == '' or verify != password:
        verify_error = "Passwords do not match. Please try again."
        verify = ''

    
    
    #if email field isn't empty, validate the email
    if len(email) != 0:
        if is_valid_email(email) == False:
            email_error = "Please enter a valid email (3-20 characters, no spaces, one @ symbol, one period)."
            password = ''
            verify = ''

    if not username_error and not password_error and not verify_error and not email_error:
        username = request.form['username']
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('index.html', title="User Signup",
            username=username, username_error=username_error,
            password=password, password_error=password_error,
            verify=verify, verify_error=verify_error,
            email=email, email_error=email_error)

@app.route("/welcome")
def welcome():
    user = request.args.get('username')
    return render_template('welcome.html', title="Signup Successful", user=user)

app.run()