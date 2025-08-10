from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_PATH = "database/app.db"

def get_db():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def index():
    if 'mobile' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']
        hint = request.form['hint']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (mobile, password, hint) VALUES (?, ?, ?)", (mobile, password, hint))
        conn.commit()
        conn.close()
        flash("Registration successful. Please log in.")
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    mobile = request.form['mobile']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE mobile=? AND password=?", (mobile, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['mobile'] = mobile
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid login credentials.")
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'mobile' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', mobile=session['mobile'])

@app.route('/set_password/<app_name>', methods=['GET', 'POST'])
def set_password(app_name):
    if 'mobile' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        category = request.form['category']
        password_seq = request.form['password_seq']  # Example: "3,1,5"

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO graphical_passwords (mobile, app_name, category, password_seq)
            VALUES (?, ?, ?, ?)
        ''', (session['mobile'], app_name, category, password_seq))
        conn.commit()
        conn.close()
        flash(f"Graphical password set for {app_name} using {category} category.")
        return redirect(url_for('dashboard'))

    return render_template('set_password.html', app_name=app_name)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        mobile = request.form['mobile']
        hint = request.form['hint']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE mobile=? AND hint=?", (mobile, hint))
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Your password is: {user[0]}"
        else:
            flash("Invalid hint or mobile number.")
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
