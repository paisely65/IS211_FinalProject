from flask import Flask, session, url_for, escape, render_template, render_template, request, redirect
app = Flask(__name__)


#http://opentechschool.github.io/python-flask/extras/sessions.html
@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    email_addresses.append(email)
    session['email'] = email
    print(email_addresses)
    return redirect('/')

@app.route('/unregister')
def unregister():
    # Make sure they've already registered an email address
    if 'email' not in session:
        return "You haven't submitted an email!"
    email = session['email']
    # Make sure it was already in our address list
    if email not in email_addresses:
        return "That address isn't on our list"
    email_addresses.remove(email)
    del session['email'] # Make sure to remove it from the session
    return 'We have removed ' + email + ' from the list!'



#http://flask.pocoo.org/docs/0.10/quickstart/#sessions
@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('index.html', message='You are not logged in')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
