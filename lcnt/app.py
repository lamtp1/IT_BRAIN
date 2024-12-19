import os
import smtplib
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import pandas as pd
import math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import threading
import time
import logging

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
SMTP_PASSWORD = "kbkzbbvnsjldnmdg"

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
    email = data.get('email', None)  # New field
    employee = data.get('employee', None)  # New field

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (name, description, deadline, email, employee) VALUES (%s, %s, %s, %s, %s)", 
                (name, description, deadline, email, employee))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data['name']
    description = data['description']
    deadline = data['deadline']
    email = data.get('email', None)  # New field
    employee = data.get('employee', None)  # New field

    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET name = %s, description = %s, deadline = %s, email = %s, employee = %s WHERE id = %s", 
                (name, description, deadline, email, employee, task_id))
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
        required_columns = ['Tên', 'Mô tả', 'Deadline', 'Email', 'Nhân viên']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'error': f'Missing column: {col}'}), 400

        cur = mysql.connection.cursor()
        for _, row in df.iterrows():
            cur.execute("INSERT INTO tasks (name, description, deadline, email, employee) VALUES (%s, %s, %s, %s, %s)", 
                        (row['Tên'], row['Mô tả'], row['Deadline'], row['Email'], row['Nhân viên']))
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
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
    finally:
        server.quit()

logging.basicConfig(level=logging.INFO)

def notify_due_tasks():
    logging.info("Chạy notify_due_tasks...")
    # Tạo kết nối mới mỗi lần chạy
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT name, deadline, email, employee 
            FROM tasks 
            WHERE TIMESTAMPDIFF(DAY, NOW(), deadline) BETWEEN 0 AND 3
        """)
        tasks = cur.fetchall()
        cur.close()

        processed_tasks = set()  # Lưu trữ các công việc đã xử lý

        for task in tasks:
            name, deadline, email, employee = task
            task_identifier = f"{email}_{deadline}"  # Định danh duy nhất cho công việc
            if email and task_identifier not in processed_tasks:  # Kiểm tra trùng lặp
                processed_tasks.add(task_identifier)
                logging.info(f"Gửi email tới {email} cho công việc '{name}' (Deadline: {deadline})")
                subject = f"Reminder: Task '{name}' is approaching"
                content = f"""
                <p>Dear {employee},</p>
                <p>Đây là mail thông báo để nhắc rằng đầu việc <b>'{name}'</b> sẽ đến hạn vào ngày <b>{deadline}</b>.</p>
                <p>Vậy nên hãy đảm bảo hoàn thành đầu việc đúng hạn.</p>
                """
                send_email(email, subject, content)


notification_thread_started = False  # Global flag to ensure a single thread

def start_notification_thread():
    global notification_thread_started
    if notification_thread_started:
        logging.info("Notification thread already running. Skipping...")
        return
    notification_thread_started = True

    def notify():
        with app.app_context():  # Push the app context here
            while True:
                logging.info("Notification thread running...")
                notify_due_tasks()
                time.sleep(24*60*60)  # Run daily

    logging.info("Starting notification thread...")
    threading.Thread(target=notify, daemon=True).start()

# Start the notification thread
start_notification_thread()

if __name__ == '__main__':
    app.run(debug=True)