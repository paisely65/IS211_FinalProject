from flask import Flask, session, url_for, escape, render_template, request, redirect
app = Flask(__name__)

import sqlite3, datetime as dt

db = sqlite3.connect("final.db")
c = db.cursor()

setup = open('schema.sql', 'r').read()
c.executescript(setup)
db.commit()

#http://flask.pocoo.org/docs/0.10/quickstart/#sessions
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
          session['username'] = request.form['username']
          return redirect(url_for('dashboard'))
    if 'username' in session:
	    return redirect('/dashboard')
    else:
        return render_template('login.html', message='You are not logged in')

@app.route('/')
def index():
    QUERY = "SELECT * FROM posts ORDER BY timestamp DESC"
    c.execute(QUERY)
    posts = c.fetchall()
    return render_template('index.html', posts = posts)


### HERE
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
	    QUERY = "SELECT * FROM posts WHERE author = ?"
	    c.execute(QUERY, [session['username']] )
	    posts = c.fetchall()
	    return render_template('dashboard.html', posts = posts)
    else:
	    return render_template('login.html', message='You are not logged in')


@app.route('/add-story', methods=['POST'])
def add_story():
    content = request.form['content']
    title = request.form['title']
    QUERY = "INSERT INTO posts (author, heading, content, timestamp) VALUES (?, ?, ?, ?)"
    c.execute(QUERY, [session['username'], title, content, dt.datetime.now()])
    return redirect(url_for('dashboard'))

@app.route('/edit-story', methods=['POST'])
def edit_story():
    content = request.form['content']
    title = request.form['title']
    id = request.form['id']
    QUERY = "UPDATE posts SET heading=?, content=? WHERE id=?"
    c.execute(QUERY, [title, content, id])
    return redirect(url_for('dashboard'))

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    QUERY = "DELETE FROM posts WHERE id=?"
    c.execute(QUERY, [id])
    return redirect(url_for('dashboard'))



@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    if 'username' in session:
	    QUERY = "SELECT * FROM posts WHERE id = ?"
	    c.execute(QUERY, [id] )
	    post = c.fetchone()
	    return render_template('edit.html', post = post)
    else:
	    return render_template('login.html', message='You are not logged in')

###
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run()
