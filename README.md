Complaint Management System (College Use)
A web-based application to manage student complaints in a college environment using Flask, MySQL, HTML/CSS.

🚀 Features
👨‍🎓 Student Portal

Register/Login

File a new complaint

View complaint status

🧑‍💼 Admin/Staff Portal

Login to view complaints

Monitor complaint status

View student details

🔒 Role-Based Access

💬 Flash messaging for success/error

🗃️ MySQL Database integration

🛠️ Tech Stack
Frontend: HTML, CSS (custom)

Backend: Flask (Python)

Database: MySQL

Security: Password hashing with Werkzeug

📁 Folder Structure

complaint_system/
│
├── app.py
├── config.py
├── schema.sql
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   └── file_complaint.html

⚙️ How to Run the Project


Install Flask: pip install flask mysql-connector-python

Create config.py

python
Copy code
host = "localhost"
user = "root"
password = "your_mysql_password"
database = "complaint_system"

Import schema.sql into MySQL to create the tables.

Run the project

python app.py
