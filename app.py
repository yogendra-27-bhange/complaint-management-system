# Import required modules
from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
from config import host, user, password, database
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'student')", (name, email, password))
        conn.commit()
        flash('Registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        if user_data and check_password_hash(user_data['password'], password_input):
            session['user_id'] = user_data['id']
            session['role'] = user_data['role']
            if user_data['role'] == 'student':
                return redirect('/student/dashboard')
            else:
                return redirect('/admin/dashboard')
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# Student Dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect('/login')
    cursor.execute("SELECT * FROM complaints WHERE student_id = %s", (session['user_id'],))
    complaints = cursor.fetchall()
    return render_template('student_dashboard.html', complaints=complaints)

# File complaint
@app.route('/file-complaint', methods=['GET', 'POST'])
def file_complaint():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect('/login')
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    if request.method == 'POST':
        category_id = request.form['category']
        description = request.form['description']
        cursor.execute("INSERT INTO complaints (student_id, category_id, description) VALUES (%s, %s, %s)", (session['user_id'], category_id, description))
        conn.commit()
        flash('Complaint submitted')
        return redirect('/student/dashboard')
    return render_template('file_complaint.html', categories=categories)

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        return redirect('/login')
    cursor.execute("SELECT complaints.*, users.name FROM complaints JOIN users ON complaints.student_id = users.id")
    all_complaints = cursor.fetchall()
    return render_template('admin_dashboard.html', complaints=all_complaints)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Run app
if __name__ == '__main__':
    app.run(debug=True)
