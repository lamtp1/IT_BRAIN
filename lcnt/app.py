import os
import smtplib
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import pandas as pd
import math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

app = Flask(__name__)

# Cấu hình MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'task_management'
mysql = MySQL(app)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "tuphulam@gmail.com"
SMTP_PASSWORD = "kbkzbbvnsjldnmdg "

# Đường dẫn lưu file tạm thời
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Số lượng bản ghi trên mỗi trang
RESULTS_PER_PAGE = 10

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int)  # Trang hiện tại (mặc định là trang 1)
    offset = (page - 1) * RESULTS_PER_PAGE

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cur.fetchone()[0]  # Tổng số bản ghi
    total_pages = math.ceil(total_tasks / RESULTS_PER_PAGE)

    cur.execute("SELECT * FROM tasks LIMIT %s OFFSET %s", (RESULTS_PER_PAGE, offset))
    tasks = cur.fetchall()
    cur.close()

    return jsonify({
        'tasks': tasks,
        'current_page': page,
        'total_pages': total_pages
    })

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    name = data['name']
    description = data['description']
    deadline = data['deadline']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (name, description, deadline) VALUES (%s, %s, %s)", (name, description, deadline))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data['name']
    description = data['description']
    deadline = data['deadline']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET name = %s, description = %s, deadline = %s WHERE id = %s", (name, description, deadline, task_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/import', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)
        if 'Tên' not in df.columns or 'Mô tả' not in df.columns or 'Deadline' not in df.columns:
            return jsonify({'error': 'Invalid Excel format. Columns "Tên", "Mô tả", and "Deadline" are required.'}), 400

        cur = mysql.connection.cursor()
        for _, row in df.iterrows():
            cur.execute("INSERT INTO tasks (name, description, deadline) VALUES (%s, %s, %s)", (row['Tên'], row['Mô tả'], row['Deadline']))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Data imported successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

def send_email(recipient, subject, content):
    # Tạo email
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "html"))

    # Kết nối đến SMTP server và gửi email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Bắt đầu kết nối an toàn
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, recipient, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Gửi email
send_email("tuphulam@gmail.com", "Test Email", "<h1>This is a test email for lamtp1</h1>")

if __name__ == '__main__':
    app.run(debug=True)