import os
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import pandas as pd

app = Flask(__name__)

# Cấu hình MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'task_management'
mysql = MySQL(app)

# Đường dẫn lưu file tạm thời
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        cur.close()
        return jsonify(tasks)
    elif request.method == 'POST':
        data = request.json
        name = data['name']
        description = data['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (name, description))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task added successfully'}), 201

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

    # Lưu file Excel
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Đọc nội dung file Excel
    try:
        df = pd.read_excel(filepath)
        if 'Tên' not in df.columns or 'Mô tả' not in df.columns:
            return jsonify({'error': 'Invalid Excel format. Columns "Tên" and "Mô tả" are required.'}), 400

        # Insert dữ liệu vào database
        cur = mysql.connection.cursor()
        for _, row in df.iterrows():
            cur.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (row['Tên'], row['Mô tả']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Data imported successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)  # Xóa file sau khi xử lý

if __name__ == '__main__':
    app.run(debug=True)
