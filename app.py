from flask import Flask, render_template, request, redirect, session
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

#Database
def get_db():
    return sqlite3.connect('database.db')

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password text)'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount REAL,
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
    )

    conn.commit()
    conn.close()

init_db()

#Signup
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'])

        conn = get_db()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                     (request.form['username'], hashed))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('signup.html')

#Login
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?",
                    (request.form['username'],))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], request.form['password']):
            session['user'] = request.form['username']
            return redirect('/dashboard')
        else:
            error = "Account not found. Please Signup first"

    return render_template('login.html', error=error)

#Dashboard
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/')

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        if not request.form['category'] or not request.form['amount']:
            return "Invalid input"

        cur.execute("INSERT INTO expenses (category, amount, comments) VALUES (?, ?, ?)",
                    (request.form['category'],
                     request.form['amount'],
                     request.form['comments']))
        conn.commit()

    cur.execute("SELECT * FROM expenses ORDER BY id DESC")
    expenses = cur.fetchall()

    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    chart = cur.fetchall()

    cur.execute("SELECT DISTINCT category FROM expenses")
    categories = [x[0] for x in cur.fetchall()]

    conn.close()

    labels = [x[0] for x in chart]
    values = [x[1] for x in chart]

    return render_template('dashboard.html',
                           expenses=expenses,
                           labels=labels,
                           values=values,
                           categories=categories)

#Edit
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("""UPDATE expenses 
                        SET category=?, amount=?, comments=?, updated_at=CURRENT_TIMESTAMP 
                        WHERE id=?
                        """, (request.form['category'],
                            request.form['amount'],
                            request.form['comments'], id))
        conn.commit()
        conn.close()
        return redirect('/dashboard')

    cur.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = cur.fetchone()
    conn.close()

    return render_template('edit.html', e=expense)

#Delete
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


app.run(debug=True)