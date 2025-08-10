from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "app2_secret_key"
DB_PATH = "database/app.db"

def get_db():
    return sqlite3.connect(DB_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mobile = request.form['mobile']
        category = request.form['category']
        selected_seq = request.form['password_seq']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password_seq FROM graphical_passwords WHERE mobile=? AND app_name='app2' AND category=?", (mobile, category))
        record = cursor.fetchone()
        conn.close()

        if record and record[0] == selected_seq:
            return render_template('welcome.html', app_name='App2', mobile=mobile)
        else:
            flash("Incorrect graphical password.")
            return redirect(url_for('index'))

    return render_template('app_password.html', app_name='App2')

if __name__ == "__main__":
    app.run(port=5002, debug=True)
