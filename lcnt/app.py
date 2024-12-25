import os
import smtplib
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import pandas as pd
import math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
import threading
import time

app = Flask(__name__)

emails_sent_count = 0  # ★ Biến đếm tổng số mail đã gửi

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

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RESULTS_PER_PAGE = 10

sent_emails = set()  # Global variable to track sent emails

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', RESULTS_PER_PAGE, type=int)
    search = request.args.get('search', '').strip()  # <-- Lấy keyword tìm kiếm (mặc định là rỗng)

    offset = (page - 1) * page_size
    cur = mysql.connection.cursor()

    # Nếu search có nội dung, ta thêm điều kiện WHERE
    if search:
        # Đếm tổng số bản ghi phù hợp
        count_query = """
            SELECT COUNT(*) 
            FROM tasks 
            WHERE name LIKE %s OR email LIKE %s OR employee LIKE %s
        """
        like_str = f"%{search}%"
        cur.execute(count_query, (like_str, like_str, like_str))
        total_tasks = cur.fetchone()[0]
        
        # Tính total_pages
        total_pages = math.ceil(total_tasks / page_size) if page_size > 0 else 1
        
        # Lấy bản ghi phù hợp, có LIMIT + OFFSET
        data_query = """
            SELECT * 
            FROM tasks 
            WHERE name LIKE %s OR email LIKE %s OR employee LIKE %s
            LIMIT %s OFFSET %s
        """
        cur.execute(data_query, (like_str, like_str, like_str, page_size, offset))
        tasks = cur.fetchall()
    else:
        # Không có search => lấy tất cả như cũ
        cur.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = cur.fetchone()[0]
        total_pages = math.ceil(total_tasks / page_size) if page_size > 0 else 1

        cur.execute("SELECT * FROM tasks LIMIT %s OFFSET %s", (page_size, offset))
        tasks = cur.fetchall()

    cur.close()

    return jsonify({
        'tasks': tasks,
        'current_page': page,
        'total_pages': total_pages
    })

@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Khi thêm task:
    1) Thêm vào DB
    2) Quét các bản ghi (hoặc chỉ bản ghi vừa thêm)
    3) Gửi mail nếu deadline gần
    """
    global sent_emails
    data = request.json
    name = data['name']
    description = data['description']
    deadline = data['deadline']
    email = data.get('email', None)
    employee = data.get('employee', None)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO tasks (name, description, deadline, email, employee) 
        VALUES (%s, %s, %s, %s, %s)
    """, (name, description, deadline, email, employee))
    task_id = cur.lastrowid  # ★ MỚI: lấy ID của task vừa thêm
    mysql.connection.commit()
    cur.close()

    # Xoá "đã gửi" cũ nếu trùng email + deadline
    task_identifier = f"{email}_{deadline}"
    sent_emails.discard(task_identifier)

    # ★ MỚI: Sau khi thêm, chỉ quét email cho BẢN GHI VỪA THÊM này
    check_and_send_for_single_task(task_id)

    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    global sent_emails
    data = request.json
    name = data['name']
    description = data['description']
    deadline = data['deadline']
    email = data.get('email', None)
    employee = data.get('employee', None)

    cur = mysql.connection.cursor()
    cur.execute("SELECT email, deadline FROM tasks WHERE id = %s", (task_id,))
    old_task = cur.fetchone()
    cur.execute("""
        UPDATE tasks 
        SET name = %s, description = %s, deadline = %s, email = %s, employee = %s 
        WHERE id = %s
    """, (name, description, deadline, email, employee, task_id))
    mysql.connection.commit()
    cur.close()

    if old_task:
        old_task_identifier = f"{old_task[0]}_{old_task[1]}"
        sent_emails.discard(old_task_identifier)

    # ★ MỚI: Có thể muốn quét lại email cho task vừa update
    check_and_send_for_single_task(task_id)

    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/emails_sent_count', methods=['GET'])
def get_emails_sent_count():
    global emails_sent_count
    return jsonify({'count': emails_sent_count})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/import', methods=['POST'])
def import_excel():
    """
    Khi import nhiều bản ghi cùng lúc:
    1) Thêm tất cả vào DB
    2) Gửi mail cho những bản ghi mới thêm (deadline gần)
    """
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
        new_ids = []
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO tasks (name, description, deadline, email, employee) 
                VALUES (%s, %s, %s, %s, %s)
            """, (row['Tên'], row['Mô tả'], row['Deadline'], row['Email'], row['Nhân viên']))
            new_ids.append(cur.lastrowid)  # ★ MỚI: lưu lại ID cho từng task mới
        mysql.connection.commit()
        cur.close()

        # ★ MỚI: Quét email CHỈ cho các bản ghi vừa thêm
        for tid in new_ids:
            check_and_send_for_single_task(tid)

        return jsonify({'message': 'Data imported successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)


# --- HÀM GỬI MAIL ---

def send_email(recipient, subject, content):
    global emails_sent_count
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, recipient, msg.as_string())
        print(f"Email sent to {recipient}")
        
        # Mỗi lần gửi thành công, tăng biến đếm 1
        emails_sent_count += 1

    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
    finally:
        server.quit()

# ★ MỚI: Hàm quét & gửi email CHO 1 TASK (vừa thêm hoặc vừa update)
def check_and_send_for_single_task(task_id):
    """
    Đọc 1 task từ DB.
    Nếu deadline còn 0-3 ngày => gửi mail (nếu chưa gửi).
    """
    global sent_emails
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, deadline, email, employee FROM tasks WHERE id = %s", (task_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return
        name, deadline, email, employee = row
        
        # Kiểm tra deadline
        if not deadline or not email:
            return
        
        # Tính số ngày còn lại
        days_left = (deadline - date.today()).days
        
        # Nếu deadline còn trong vòng 3 ngày => gửi
        if 0 <= days_left <= 3:
            task_identifier = f"{task_id}_{deadline}"
            if task_identifier not in sent_emails:
                # Gửi mail
                sent_emails.add(task_identifier)
                subject = f"Reminder: Task '{name}' is approaching"
                content = f"""
                <p>Dear đ/c {employee},</p>
                <p>Đầu việc <b>{name}</b> sẽ đến hạn vào ngày <b>{deadline}</b>.</p>
                <p>Vui lòng hoàn thành đúng hạn.</p>
                """
                send_email(email, subject, content)


# --- HÀM QUÉT TOÀN BỘ (1 LẦN/NGÀY) ---

def notify_due_tasks_full():
    global sent_emails
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, name, deadline, email, employee
            FROM tasks
            WHERE deadline IS NOT NULL
        """)
        tasks = cur.fetchall()
        cur.close()

        for row in tasks:
            task_id, name, deadline, email, employee = row
            
            if not email:
                continue
            
            # Nếu deadline là chuỗi => parse
            if isinstance(deadline, str):
                # Giả sử deadline có format "YYYY-MM-DD" 
                try:
                    deadline = datetime.strptime(deadline, '%Y-%m-%d')
                except ValueError:
                    # Trường hợp parse không được, ta bỏ qua
                    continue

            days_left = (deadline - date.today()).days
            if 0 <= days_left <= 3:
                task_identifier = f"{email}_{deadline}"
                if task_identifier not in sent_emails:
                    sent_emails.add(task_identifier)
                    subject = f"Reminder: Task '{name}' is approaching"
                    content = f"""
                    <p>Dear {employee},</p>
                    <p>Đầu việc <b>{name}</b> sẽ đến hạn vào ngày <b>{deadline}</b>.</p>
                    <p>Vui lòng hoàn thành đúng hạn.</p>
                    """
                    send_email(email, subject, content)


def start_notification_thread():
    """
    1 thread chạy vòng lặp vô hạn:
    - Mỗi 24 giờ => quét toàn bộ DB 1 lần
    """
    def notify():
        while True:
            notify_due_tasks_full()
            time.sleep(86400)  # 1 ngày
            
    threading.Thread(target=notify, daemon=True).start()

# Bật thread (nếu muốn chạy quét toàn bộ hằng ngày)
start_notification_thread()

if __name__ == '__main__':
    # Nếu muốn server lắng nghe ngoài container, đặt host='0.0.0.0'
    app.run(debug=True)
