import os
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import pandas as pd
import math

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

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (name, description))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data['name']
    description = data['description']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET name = %s, description = %s WHERE id = %s", (name, description, task_id))
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
        if 'Tên' not in df.columns or 'Mô tả' not in df.columns:
            return jsonify({'error': 'Invalid Excel format. Columns "Tên" and "Mô tả" are required.'}), 400

        cur = mysql.connection.cursor()
        for _, row in df.iterrows():
            cur.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (row['Tên'], row['Mô tả']))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Data imported successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
