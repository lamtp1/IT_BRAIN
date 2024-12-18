from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'  # Replace with your MariaDB password
app.config['MYSQL_DB'] = 'task_management'
app.config['MYSQL_PORT'] = 3306               # Cổng MariaDB (mặc định là 3306)
app.config['MYSQL_CONNECT_TIMEOUT'] = 10     # Thời gian chờ kết nối (giây)
mysql = MySQL(app)

# Initialize database
def init_db():
    with app.app_context():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            description TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS milestones (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            task_id INT,
                            milestone_time DATETIME,
                            assignee VARCHAR(255),
                            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                          )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return jsonify(tasks)
    elif request.method == 'POST':
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (data['name'], data['description']))
        mysql.connection.commit()
        return jsonify({'message': 'Task created successfully!'})

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task_operations(task_id):
    cursor = mysql.connection.cursor()
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE tasks SET name = %s, description = %s WHERE id = %s", (data['name'], data['description'], task_id))
        mysql.connection.commit()
        return jsonify({'message': 'Task updated successfully!'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        mysql.connection.commit()
        return jsonify({'message': 'Task deleted successfully!'})

@app.route('/milestones', methods=['POST'])
def add_milestone():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO milestones (task_id, milestone_time, assignee) VALUES (%s, %s, %s)", 
                   (data['task_id'], data['milestone_time'], data['assignee']))
    mysql.connection.commit()
    return jsonify({'message': 'Milestone added successfully!'})

def check_alerts():
    while True:
        cursor = mysql.connection.cursor()
        now = datetime.now()
        cursor.execute("SELECT milestone_time, assignee FROM milestones")
        milestones = cursor.fetchall()
        for milestone_time, assignee in milestones:
            if milestone_time - now <= timedelta(minutes=10):  # Configure alert threshold
                print(f"Alert: Milestone due soon for {assignee}!")
        cursor.close()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    threading.Thread(target=check_alerts, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
