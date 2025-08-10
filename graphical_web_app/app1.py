from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_PATH = "database/app.db"

def get_db():
    return sqlite3.connect(DB_PATH)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']

        # Get category and password_seq from DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT category, password_seq FROM graphical_passwords WHERE mobile=? AND app_name='app1'", (mobile,))
        row = cursor.fetchone()
        conn.close()

        if row:
            session['mobile'] = mobile
            session['category'] = row[0]
            session['password_seq'] = row[1]
            return redirect(url_for('unlock'))
        else:
            flash("No password set for this mobile on app1.")
            return redirect(url_for('login'))

    return render_template('app_login.html', app_name='app1')

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    if 'mobile' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_seq = request.form['password_seq']
        if entered_seq == session['password_seq']:
            return render_template('app_unlock.html', app_name='app1', success=True)
        else:
            flash("Incorrect password sequence.")
            return redirect(url_for('unlock'))

    return render_template('unlock_graphical.html', app_name='app1', category=session['category'])

if __name__ == '__main__':
    app.run(port=5001, debug=True)
