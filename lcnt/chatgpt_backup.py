import os
import smtplib
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import pandas as pd
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import MySQLdb.cursors
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = 'cntt@123'  # cần cho session
emails_sent_count = 0  # ★ Biến đếm tổng số mail đã gửi

# ==================  CẤU HÌNH MÀN LOGIN  ==================
@app.route('/')
def index():
    # Trang chủ, nếu chưa login -> chuyển sang /login
    if 'loggedin' in session:
        return redirect(url_for('view_khlcnt'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Nếu GET: hiển thị form đăng nhập
    Nếu POST: lấy username/password, check DB -> nếu đúng -> session -> redirect
    """
    if request.method == 'POST':
        # Lấy data
        username = request.form.get('username')
        password = request.form.get('password')

        # Kết nối DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Tìm user
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        account = cursor.fetchone()

        if account:
            # Tạo session
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            flash('Đăng nhập thành công!')
            return redirect(url_for('index'))
        else:
            flash('Sai tài khoản hoặc mật khẩu!')
            return redirect(url_for('login'))
    else:
        # GET -> hiển thị form
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Xóa session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('Đã đăng xuất!')
    return redirect(url_for('login'))

# ==================  CẤU HÌNH MYSQL  ==================
app.config['MYSQL_HOST'] = '171.229.20.248'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Cdvdstyvds@1412'
app.config['MYSQL_PORT'] = 4406
app.config['MYSQL_DB'] = 'task_management'  # Tên DB chứa bảng khlcnt, status_lcnt
mysql = MySQL(app)

# ==================  THƯ MỤC UPLOAD  ==================
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==================  HÀM GỬI MAIL  ==================
def send_email(recipient, subject, content):
    global emails_sent_count
    
    """
    Gửi mail với SMTP Gmail. Thay SMTP_EMAIL & SMTP_PASSWORD
    bằng tài khoản thật của bạn hoặc config server SMTP nội bộ.
    """
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_EMAIL = "tuphulam@gmail.com"
    SMTP_PASSWORD = "kbkzbbvnsjldnmdg"

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
        
        emails_sent_count += 1
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
    finally:
        server.quit()

# ================== HÀM GỬI MAIL HÀNG NGÀY =========================

def daily_send_mail_job():
    # Kết nối DB (sửa host, user, pass, db)
    conn = MySQLdb.connect(host="171.229.20.248", user="root", password="Cdvdstyvds@1412", port=4406, db="task_management", charset="utf8")
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    # Lấy tất cả các bản ghi
    sql = """
    SELECT 
      id, du_an, ten_goi_thau, email, nhan_su_to_chuyen_gia,
      step1_trang_thai, step2_trang_thai, step3_trang_thai, step4_trang_thai, step5_trang_thai, step6_trang_thai, step7_trang_thai, step8_trang_thai, step9_trang_thai, step10_trang_thai, step11_trang_thai, step12_trang_thai, step13_trang_thai, step14_trang_thai, step15_trang_thai, step16_trang_thai, step17_trang_thai, step18_trang_thai, step19_trang_thai
    FROM khlcnt
    """
    cur.execute(sql)
    rows = cur.fetchall()

    for r in rows:
        # Tập hợp tất cả stepX_trang_thai
        statuses = [
            r['step1_trang_thai'], r['step2_trang_thai'], r['step3_trang_thai'], r['step4_trang_thai'] , r['step5_trang_thai'] , r['step6_trang_thai'], r['step7_trang_thai'] , r['step8_trang_thai'] , r['step9_trang_thai'] , r['step10_trang_thai'] , r['step11_trang_thai'] , r['step12_trang_thai'] , r['step13_trang_thai'] , r['step14_trang_thai'] , r['step15_trang_thai'] , r['step16_trang_thai'] , r['step17_trang_thai'] , r['step18_trang_thai'],r['step19_trang_thai']
        ]
        # Kiểm tra có step nào = “Chưa HT_TH” hoặc “Chưa HT_QH”
        need_send = any(s in ("Chưa HT_TH", "Chưa HT_QH") for s in statuses)

        if need_send and r['email']:
            subject = f"[Nhắc tiến độ] {r['ten_goi_thau']}"
            greet_name = r['nhan_su_to_chuyen_gia'] or "Bạn"
            content = f"""
            <p>Chào đ/c {greet_name},</p>
            <p>Gói thầu <b>{r['ten_goi_thau']}</b> (thuộc Dự án: <b>{r['du_an']}</b>) vẫn còn ít nhất 1 bước <b>chưa hoàn thành</b>.</p>
            <p>Vui lòng kiểm tra tiến độ!</p>
            """
            send_email(r['email'], subject, content)

    conn.close()

# ================== HÀM TÍNH TRẠNG THÁI CHO TASKS  ==================
def get_status(ngay_htthucte, kh_date):
    """
    Rule:
      - HT_TH:  nếu ngay_htthucte < kh_date
      - HT_QH:  nếu ngay_htthucte > kh_date
      - Chưa HT_TH: nếu ngay_htthucte rỗng & hôm nay < kh_date
      - Chưa HT_QH: nếu ngay_htthucte rỗng & hôm nay > kh_date
    """
    if kh_date is None:
        return None  # Hoặc logic tùy ý, vì ko có KH => ko biết so sánh

    today = date.today()
    if ngay_htthucte:  # Đã có ngày hoàn thành thực tế
        if ngay_htthucte < kh_date:
            return "HT_TH"
        else:
            return "HT_QH"
    else:
        # Chưa có ngày hoàn thành thực tế
        if today < kh_date:
            return "Chưa HT_TH"
        else:
            return "Chưa HT_QH"

#============ HÀM ĐẾM MAIL ĐÃ GỬI ==========================
@app.route('/emails_sent_count', methods=['GET'])
def get_emails_sent_count():
    global emails_sent_count
    return jsonify({'count': emails_sent_count})

# @app.route('/')
# def index():
#     return render_template('chatgpt_backup.html')

# ==================  Kiểm tra session để đảm bảo chỉ người đã login mới xem được dashboard  ==================
# @app.route('/dashboard')
# def dashboard():
#     if 'loggedin' not in session:
#         return redirect(url_for('login'))
#     # Nếu đã login:
#     # Lấy dữ liệu DB, render template
#     return render_template('chatgpt_backup.html')

# ================== HÀM HIỂN THỊ CHI TIẾT DỮ LIỆU ========================
@app.route('/khlcnt_detail/<int:record_id>')
def khlcnt_detail(record_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM khlcnt WHERE id=%s", (record_id,))
    row = cur.fetchone()
    cur.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row)


# ==================  Hàm hiển thị dữ liệu  ================================

@app.route('/dashboard', methods=['GET'])
def view_khlcnt():
    if 'loggedin' not in session:
        return redirect(url_for('login'))    
    """
    Lấy dữ liệu từ bảng 'khlcnt' và hiển thị lên giao diện.
    """
        # Lấy page, page_size
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    if page_size not in [5, 10, 20, 50]:
        page_size = 10
    
    # Lấy từ khóa
    q = request.args.get('search', '').strip()
    
    import math
    cur = mysql.connection.cursor()

    # Lấy từ khoá search từ query params
    q = request.args.get('search', '').strip()
    try:
        # Kết nối và thực hiện truy vấn
        cur = mysql.connection.cursor()
        if q:
            like_pattern = f"%{q}%"

            # Bước 1) Đếm
            count_sql = """
                SELECT COUNT(*) 
                FROM khlcnt
                WHERE (mang LIKE %s
                OR du_an LIKE %s
                OR ten_goi_thau LIKE %s
                OR nhan_su_to_chuyen_gia LIKE %s)
            """
            cur.execute(count_sql, (like_pattern, like_pattern, like_pattern, like_pattern))
            total_rows = cur.fetchone()[0]  # tuple[0] => số đếm
            
            # Tính total_pages, clamp page, offset
            total_pages = math.ceil(total_rows / page_size) if total_rows else 1
            if page < 1:
                page = 1
            if page > total_pages:
                page = total_pages

            offset = (page - 1) * page_size

            # Bước 2) SELECT có LIMIT
            query = """
                SELECT 
                        id,mang, du_an, ten_goi_thau, thoi_gian_bat_dau_lcnt, muc_uu_tien,
           
                        hang_ve_kho, nhan_su_to_chuyen_gia, email, step1_ngay_htthucte, step2_ngay_htthucte,
                        step3_ngay_htthucte, step4_ngay_htthucte, step5_ngay_htthucte, step6_ngay_htthucte,
                        step7_ngay_htthucte, step8_ngay_htthucte, step9_ngay_htthucte, step10_ngay_htthucte,
                        step11_ngay_htthucte, step12_ngay_htthucte, step13_ngay_htthucte, step14_ngay_htthucte, 
                        step15_ngay_htthucte, step16_ngay_htthucte, step17_ngay_htthucte, step18_ngay_htthucte,
                        step19_ngay_htthucte
                    FROM khlcnt
                    WHERE 
                        (mang LIKE %s
                        OR du_an LIKE %s
                        OR ten_goi_thau LIKE %s
                        OR nhan_su_to_chuyen_gia LIKE %s)
                    LIMIT %s OFFSET %s                 
                    """
            cur.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern, page_size, offset))

            rows = cur.fetchall()
        else:

            # Bước 1) Đếm
            count_sql = """
                SELECT COUNT(*) 
                FROM khlcnt
            """
            cur.execute(count_sql)
            total_rows = cur.fetchone()[0]  # tuple[0] => số đếm
            
            # Tính total_pages, clamp page, offset
            total_pages = math.ceil(total_rows / page_size) if total_rows else 1
            if page < 1:
                page = 1
            if page > total_pages:
                page = total_pages

            offset = (page - 1) * page_size

            # Bước 2) SELECT có LIMIT
            query = """
                SELECT 
                        id,mang, du_an, ten_goi_thau, thoi_gian_bat_dau_lcnt, muc_uu_tien,
              
                        hang_ve_kho, nhan_su_to_chuyen_gia, email, step1_ngay_htthucte, step2_ngay_htthucte,
                        step3_ngay_htthucte, step4_ngay_htthucte, step5_ngay_htthucte, step6_ngay_htthucte,
                        step7_ngay_htthucte, step8_ngay_htthucte, step9_ngay_htthucte, step10_ngay_htthucte,
                        step11_ngay_htthucte, step12_ngay_htthucte, step13_ngay_htthucte, step14_ngay_htthucte, 
                        step15_ngay_htthucte, step16_ngay_htthucte, step17_ngay_htthucte, step18_ngay_htthucte,
                        step19_ngay_htthucte
                    FROM khlcnt
                    LIMIT %s OFFSET %s                 
                    """
            cur.execute(query,  (page_size, offset))

            rows = cur.fetchall()

        # Truyền dữ liệu tới template
        return render_template(
            'chatgpt_backup.html',
            rows=rows,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            total_rows=total_rows,
            q=q
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#================ HÀM XÓA BẢN GHI ===========================================
@app.route('/delete_record', methods=['POST'])
def delete_record():
    """
    Xóa một bản ghi dựa trên id từ bảng khlcnt.
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    # Lấy id từ form
    id = request.form.get('id')  # Lấy giá trị ID từ dữ liệu POST
    if not id:
        flash("ID không hợp lệ!")
        return redirect(url_for('view_khlcnt'))

    try:
        cur = mysql.connection.cursor()
        query = "DELETE FROM khlcnt WHERE id = %s"
        cur.execute(query, (id,))
        mysql.connection.commit()
        cur.close()

        flash("Xóa thành công!")
    except Exception as e:
        flash(f"Lỗi: {str(e)}")
    return redirect(url_for('view_khlcnt'))

#=================== HÀM XÓA NHIỀU BẢN GHI =============================
@app.route('/delete_multiple', methods=['POST'])
def delete_multiple():
    """
    Xóa nhiều record trong khlcnt dựa vào list id.
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'error': 'Không có id nào'}), 400

    try:
        cur = mysql.connection.cursor()
        # Tạo chuỗi in cho WHERE id in (...)
        placeholders = ', '.join(['%s'] * len(ids))
        query = f"DELETE FROM khlcnt WHERE id IN ({placeholders})"
        cur.execute(query, tuple(ids))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': f'Đã xóa {len(ids)} dòng'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#=================== HÀM UPDATE BẢN GHI =================================
@app.route('/khlcnt/<int:record_id>', methods=['PUT'])
def update_khlcnt(record_id):
    """
    Cập nhật 8 trường:
      - mang
      - du_an
      - ten_goi_thau
      - thoi_gian_bat_dau_lcnt
      - muc_uu_tien
      - hang_ve_kho (date)
      - nhan_su_to_chuyen_gia
      - email
    """
    data = request.json

    # print("DEBUG step1_ngay_htthucte =", data.get('step1_ngay_htthucte'))
        # Parse date
    import datetime
    def parse_date(strdate):
        if not strdate: 
            return None
        return datetime.datetime.strptime(strdate, '%Y-%m-%d').date()

    # print(step1_ngay)
        # Lấy cột KH cũ (step1_kh, step2_kh, ...) từ DB để so sánh
        
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM khlcnt WHERE id=%s", (record_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Record not found"}), 404
    
    # Tính lại stepX_trang_thai
    # (giả sử row['step1_kh'] là cột date KH)
    mang = data.get('mang')
    du_an = data.get('du_an')
    ten_goi_thau = data.get('ten_goi_thau')
    thoi_gian_bat_dau_lcnt = data.get('thoi_gian_bat_dau_lcnt')
    muc_uu_tien = data.get('muc_uu_tien')
    hang_ve_kho = parse_date(data.get('hang_ve_kho'))
    nhan_su_to_chuyen_gia = data.get('nhan_su_to_chuyen_gia')
    email = data.get('email')

    step1_ngay = parse_date(data.get('step1_ngay_htthucte'))
    step1_kh = row['step1_kh']  # type date or None
    s1_status = get_status(step1_ngay, step1_kh)  # => "HT_TH", ...

    step2_ngay = parse_date(data.get('step2_ngay_htthucte'))
    step2_kh = row['step2_kh']  # type date or None
    s2_status = get_status(step2_ngay, step2_kh)  # => "HT_TH", ...

    step3_ngay = parse_date(data.get('step3_ngay_htthucte'))
    step3_kh = row['step3_kh']  # type date or None
    s3_status = get_status(step3_ngay, step3_kh)  # => "HT_TH", ...

    step4_ngay = parse_date(data.get('step4_ngay_htthucte'))
    step4_kh = row['step4_kh']  # type date or None
    s4_status = get_status(step4_ngay, step4_kh)  # => "HT_TH", ...

    step5_ngay = parse_date(data.get('step5_ngay_htthucte'))
    step5_kh = row['step5_kh']  # type date or None
    s5_status = get_status(step5_ngay, step5_kh)  # => "HT_TH", ...

    step6_ngay = parse_date(data.get('step6_ngay_htthucte'))
    step6_kh = row['step6_kh']  # type date or None
    s6_status = get_status(step6_ngay, step6_kh)  # => "HT_TH", ...

    step7_ngay = parse_date(data.get('step7_ngay_htthucte'))
    step7_kh = row['step7_kh']  # type date or None
    s7_status = get_status(step7_ngay, step7_kh)  # => "HT_TH", ...

    step8_ngay = parse_date(data.get('step8_ngay_htthucte'))
    step8_kh = row['step8_kh']  # type date or None
    s8_status = get_status(step8_ngay, step8_kh)  # => "HT_TH", ...

    step9_ngay = parse_date(data.get('step9_ngay_htthucte'))
    step9_kh = row['step9_kh']  # type date or None
    s9_status = get_status(step9_ngay, step9_kh)  # => "HT_TH", ...

    step10_ngay = parse_date(data.get('step10_ngay_htthucte'))
    step10_kh = row['step10_kh']  # type date or None
    s10_status = get_status(step10_ngay, step10_kh)  # => "HT_TH", ...

    step11_ngay = parse_date(data.get('step11_ngay_htthucte'))
    step11_kh = row['step11_kh']  # type date or None
    s11_status = get_status(step11_ngay, step11_kh)  # => "HT_TH", ...

    step12_ngay = parse_date(data.get('step12_ngay_htthucte'))
    step12_kh = row['step12_kh']  # type date or None
    s12_status = get_status(step12_ngay, step12_kh)  # => "HT_TH", ...

    step13_ngay = parse_date(data.get('step13_ngay_htthucte'))
    step13_kh = row['step13_kh']  # type date or None
    s13_status = get_status(step13_ngay, step13_kh)  # => "HT_TH", ...

    step14_ngay = parse_date(data.get('step14_ngay_htthucte'))
    step14_kh = row['step14_kh']  # type date or None
    s14_status = get_status(step14_ngay, step14_kh)  # => "HT_TH", ...

    step15_ngay = parse_date(data.get('step15_ngay_htthucte'))
    step15_kh = row['step15_kh']  # type date or None
    s15_status = get_status(step15_ngay, step15_kh)  # => "HT_TH", ...

    step16_ngay = parse_date(data.get('step16_ngay_htthucte'))
    step16_kh = row['step16_kh']  # type date or None
    s16_status = get_status(step16_ngay, step16_kh)  # => "HT_TH", ...

    step17_ngay = parse_date(data.get('step17_ngay_htthucte'))
    step17_kh = row['step17_kh']  # type date or None
    s17_status = get_status(step17_ngay, step17_kh)  # => "HT_TH", ...

    step18_ngay = parse_date(data.get('step18_ngay_htthucte'))
    step18_kh = row['step18_kh']  # type date or None
    s18_status = get_status(step18_ngay, step18_kh)  # => "HT_TH", ...

    step19_ngay = parse_date(data.get('step19_ngay_htthucte'))
    step19_kh = row['step19_kh']  # type date or None
    s19_status = get_status(step19_ngay, step19_kh)  # => "HT_TH", ...
    # Update DB
    try:
        cur = mysql.connection.cursor()
        sql = """
          UPDATE khlcnt 
          SET 
            mang=%s,
            du_an=%s,
            ten_goi_thau=%s,
            thoi_gian_bat_dau_lcnt=%s,
            muc_uu_tien=%s,
            hang_ve_kho=%s,
            nhan_su_to_chuyen_gia=%s,
            email=%s,
            step1_ngay_htthucte=%s, step1_trang_thai=%s,
            step2_ngay_htthucte=%s, step2_trang_thai=%s,
            step3_ngay_htthucte=%s, step3_trang_thai=%s,
            step4_ngay_htthucte=%s, step4_trang_thai=%s,
            step5_ngay_htthucte=%s, step5_trang_thai=%s,
            step6_ngay_htthucte=%s, step6_trang_thai=%s,
            step7_ngay_htthucte=%s, step7_trang_thai=%s,
            step8_ngay_htthucte=%s, step8_trang_thai=%s,
            step9_ngay_htthucte=%s, step9_trang_thai=%s,
            step10_ngay_htthucte=%s, step10_trang_thai=%s,
            step11_ngay_htthucte=%s, step11_trang_thai=%s,
            step12_ngay_htthucte=%s, step12_trang_thai=%s,
            step13_ngay_htthucte=%s, step13_trang_thai=%s,
            step14_ngay_htthucte=%s, step14_trang_thai=%s,
            step15_ngay_htthucte=%s, step15_trang_thai=%s,
            step16_ngay_htthucte=%s, step16_trang_thai=%s,
            step17_ngay_htthucte=%s, step17_trang_thai=%s,
            step18_ngay_htthucte=%s, step18_trang_thai=%s,
            step19_ngay_htthucte=%s, step19_trang_thai=%s
          WHERE id=%s
        """
        cur.execute(sql, (mang, du_an, ten_goi_thau, thoi_gian_bat_dau_lcnt, 
                          muc_uu_tien, hang_ve_kho, nhan_su_to_chuyen_gia, 
                          email, step1_ngay, s1_status, 
                                step2_ngay, s2_status,
                                step3_ngay, s3_status,
                                step4_ngay, s4_status,
                                step5_ngay, s5_status,
                                step6_ngay, s6_status,
                                step7_ngay, s7_status,
                                step8_ngay, s8_status,
                                step9_ngay, s9_status,
                                step10_ngay, s10_status,
                                step11_ngay, s11_status,
                                step12_ngay, s12_status,
                                step13_ngay, s13_status,
                                step14_ngay, s14_status,
                                step15_ngay, s15_status,
                                step16_ngay, s16_status,
                                step17_ngay, s17_status,
                                step18_ngay, s18_status,
                                step19_ngay, s19_status, record_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#====================== HÀM TÌM KIẾM =========================================
@app.route('/search', methods=['GET'])
def search():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    # Lấy keyword
    q_mang = request.args.get('mang', '').strip()
    q_du_an = request.args.get('du_an', '').strip()
    q_ten_goi_thau = request.args.get('ten_goi_thau', '').strip()
    q_nhan_su = request.args.get('nhan_su_to_chuyen_gia', '').strip()
    
    # Tạo SQL động
    sql = """
    SELECT 
      id,mang,du_an,ten_goi_thau,thoi_gian_bat_dau_lcnt,muc_uu_tien,
      step1_kh, step1_ngay_htthucte, step1_trang_thai,
      ...
      step19_kh, step19_ngay_htthucte, step19_trang_thai,
      hang_ve_kho, nhan_su_to_chuyen_gia, email
    FROM khlcnt
    WHERE 1=1
    """
    params = []
    
    if q_mang:
        sql += " AND mang LIKE %s"
        params.append(f"%{q_mang}%")
    if q_du_an:
        sql += " AND du_an LIKE %s"
        params.append(f"%{q_du_an}%")
    if q_ten_goi_thau:
        sql += " AND ten_goi_thau LIKE %s"
        params.append(f"%{q_ten_goi_thau}%")
    if q_nhan_su:
        sql += " AND nhan_su_to_chuyen_gia LIKE %s"
        params.append(f"%{q_nhan_su}%")
    
    try:
        cur = mysql.connection.cursor()
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        
        # Render cùng template hiển thị danh sách
        return render_template('chatgpt_backup.html', rows=rows,
                               q_mang=q_mang, q_du_an=q_du_an, 
                               q_ten_goi_thau=q_ten_goi_thau, 
                               q_nhan_su=q_nhan_su)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================  ROUTE IMPORT EXCEL  ==================
@app.route('/import_khlcnt', methods=['POST'])
def import_khlcnt():
    """
    1) Nhận file Excel (có cột cha/cột con) -> đọc 2 hàng tiêu đề
    2) Map cột -> cột DB
    3) Tính step1_trang_thai ... step19_trang_thai
    4) Insert vào bảng khlcnt
    5) Gửi mail cho các bản ghi có step nào đó = 'Chưa HT_TH' hoặc 'Chưa HT_QH'
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        # --- Đọc 2 hàng tiêu đề trong Excel ---
        df = pd.read_excel(filepath, header=[0,1])
        # Lúc này, df.columns là MultiIndex kiểu: (('MẠNG',''), ('(1)_Xây...','KH'), ...)

        # === Map cột trong Excel -> cột DB ===
        # Bạn phải tùy biến EXACT theo tên cột thật trong file Excel:
        col_map = {
            ("MẢNG", "MẢNG"): "mang",
            ("Dự án", "Dự án"): "du_an",
            ("Tên gói thầu", "Tên gói thầu"): "ten_goi_thau",
            ("Thời gian bắt đầu tổ chức LCNT", "Thời gian bắt đầu tổ chức LCNT"): "thoi_gian_bat_dau_lcnt",
            ("Mức ƯT", "Mức ƯT"): "muc_uu_tien",

            # Step1
            ("(1)_Xây dựng HSMT/HSYC","KH"): "step1_kh",
            ("(1)_Xây dựng HSMT/HSYC","Ngày hoàn thành thực tế"): "step1_ngay_htthucte",
            # step1_trang_thai ko import, vì ta TỰ TÍNH

            # Step2
            ("(2)_Hoàn thiện_HSMT/HSYC","KH"): "step2_kh",
            ("(2)_Hoàn thiện_HSMT/HSYC","Ngày hoàn thành thực tế"): "step2_ngay_htthucte",

            ("(3)_Phê duyệt_HSMT/HSYC","KH"): "step3_kh",
            ("(3)_Phê duyệt_HSMT/HSYC","Ngày hoàn thành thực tế"): "step3_ngay_htthucte",

            ("(4)_Phát_thầu","KH"): "step4_kh",
            ("(4)_Phát_thầu","Ngày hoàn thành thực tế"): "step4_ngay_htthucte",

            ("(5)_Đóng, mở_thầu","KH"): "step5_kh",
            ("(5)_Đóng, mở_thầu","Ngày hoàn thành thực tế"): "step5_ngay_htthucte",

            ("(6)_Hoàn thành_chấm kỹ thuật, tài chính, pháp lý","KH"): "step6_kh",
            ("(6)_Hoàn thành_chấm kỹ thuật, tài chính, pháp lý","Ngày hoàn thành thực tế"): "step6_ngay_htthucte",

            ("(7)_Báo cáo quả_Đánh giá PL-KT-TC","KH"): "step7_kh",
            ("(7)_Báo cáo quả_Đánh giá PL-KT-TC","Ngày hoàn thành thực tế"): "step7_ngay_htthucte",
            
            ("(8)_Ký xong Báo cáo đánh giá của TCG","KH"): "step8_kh",
            ("(8)_Ký xong Báo cáo đánh giá của TCG","Ngày hoàn thành thực tế"): "step8_ngay_htthucte",

            ("(9)_Thư mời thương thảo","KH"): "step9_kh",
            ("(9)_Thư mời thương thảo","Ngày hoàn thành thực tế"): "step9_ngay_htthucte",

            ("(10)_Hoàn thiện ký biên bản thương thảo hợp đồng","KH"): "step10_kh",
            ("(10)_Hoàn thiện ký biên bản thương thảo hợp đồng","Ngày hoàn thành thực tế"): "step10_ngay_htthucte",

            ("(11)_Tờ trình phê duyệt Kết quả LCNT","KH"): "step11_kh",
            ("(11)_Tờ trình phê duyệt Kết quả LCNT","Ngày hoàn thành thực tế"): "step11_ngay_htthucte",

            ("(12)_Lấy nhận xét của Pháp chế","KH"): "step12_kh",
            ("(12)_Lấy nhận xét của Pháp chế","Ngày hoàn thành thực tế"): "step12_ngay_htthucte",

            ("(13)_Trình Hội đồng đầu tư báo cáo thẩm định kết quả LCNT","KH"): "step13_kh",
            ("(13)_Trình Hội đồng đầu tư báo cáo thẩm định kết quả LCNT","Ngày hoàn thành thực tế"): "step13_ngay_htthucte",

            ("(14)_Hội đồng ĐT phê duyệt  Kết quả LCNT","KH"): "step14_kh",
            ("(14)_Hội đồng ĐT phê duyệt  Kết quả LCNT","Ngày hoàn thành thực tế"): "step14_ngay_htthucte",

            ("(15)_TGĐ phê duyệt_KQLCNT","KH"): "step15_kh",
            ("(15)_TGĐ phê duyệt_KQLCNT","Ngày hoàn thành thực tế"): "step15_ngay_htthucte",

            ("(16)_Thông báo KQLCNT và thư trao HĐ","KH"): "step16_kh",
            ("(16)_Thông báo KQLCNT và thư trao HĐ","Ngày hoàn thành thực tế"): "step16_ngay_htthucte",

            ("(17)_Báo cáo kết quả đàm phán HĐ","KH"): "step17_kh",
            ("(17)_Báo cáo kết quả đàm phán HĐ","Ngày hoàn thành thực tế"): "step17_ngay_htthucte",

            ("(18)_Biên bản hoàn thiện hđ (nếu có)","KH"): "step18_kh",
            ("(18)_Biên bản hoàn thiện hđ (nếu có)","Ngày hoàn thành thực tế"): "step18_ngay_htthucte",

            # ... Tương tự step3.. step19 ...
            ("(19)_Hoàn thành ký hợp đồng","KH"): "step19_kh",
            ("(19)_Hoàn thành ký hợp đồng","Ngày hoàn thành thực tế"): "step19_ngay_htthucte",

            # (20)_Hàng về kho -> cột hang_ve_kho DATE
            ("(20)_Hàng về kho","(20)_Hàng về kho"): "hang_ve_kho",

            # Nhân sự Tổ chuyên gia
            ("Nhân sự Tổ Chuyên gia","Nhân sự Tổ Chuyên gia"): "nhan_su_to_chuyen_gia",

            # email
            ("email","email"): "email"
        }
        
        # Lấy danh sách cột thực có trong Excel
        actual_cols = df.columns
        inserted_ids = []
        cur = mysql.connection.cursor()

        for idx, row in df.iterrows():
            # Tạo dict tạm => row_data
            row_data = {}
            for col_pair, db_col in col_map.items():
                if col_pair in actual_cols:
                    val = row[col_pair]

                    # Nếu cột DB là kiểu DATE, ta parse
                    if (db_col.endswith('_kh') or 
                        db_col.endswith('_ngay_htthucte') or 
                        db_col == "hang_ve_kho"):
                        # db_col == "thoi_gian_bat_dau_lcnt"):
                        if pd.isna(val):
                            row_data[db_col] = None
                        else:
                            if isinstance(val, datetime):
                                row_data[db_col] = val.date()
                            else:
                                # thử parse
                                try:
                                    row_data[db_col] = pd.to_datetime(str(val)).date()
                                except:
                                    row_data[db_col] = None
                    else:
                        # text
                        if pd.isna(val):
                            row_data[db_col] = None
                        else:
                            row_data[db_col] = str(val)
                else:
                    row_data[db_col] = None

            # === Tính trạng thái cho 19 step ===
            # Ta lần lượt step1..step19
            for i in range(1, 20):  # 1..19
                kh_col   = f"step{i}_kh"
                ht_col   = f"step{i}_ngay_htthucte"
                st_col   = f"step{i}_trang_thai"  # cột mà DB có
                kh_date  = row_data.get(kh_col, None)
                ht_date  = row_data.get(ht_col, None)
                row_data[st_col] = get_status(ht_date, kh_date)

            # Insert row_data vào DB
            db_cols = list(row_data.keys())  # Tất cả cột ta có
            placeholders = ", ".join(["%s"] * len(db_cols))
            columns_joined = ", ".join(db_cols)
                        # Check trùng bản ghi
            # Hứng tạm 4 cột chính để check trùng:
            mang_val = row_data.get('mang')
            du_an_val = row_data.get('du_an')
            ten_goi_thau_val = row_data.get('ten_goi_thau')
            thoi_gian_bat_dau_lcnt_val = row_data.get('thoi_gian_bat_dau_lcnt')

            # Kiểm tra DB
            check_sql = """
            SELECT id FROM khlcnt
            WHERE mang=%s
            AND du_an=%s
            AND ten_goi_thau=%s
            AND thoi_gian_bat_dau_lcnt=%s
            LIMIT 1
            """
            cur.execute(check_sql, (mang_val, du_an_val, ten_goi_thau_val, thoi_gian_bat_dau_lcnt_val))
            duplicate = cur.fetchone()

            if duplicate:
                # Tồn tại rồi => bỏ qua, không insert
                print(f"Bỏ qua dòng vì trùng: {mang_val}, {du_an_val}, {ten_goi_thau_val}, {thoi_gian_bat_dau_lcnt_val}")
                continue
            else:
                insert_sql = f"INSERT INTO khlcnt ({columns_joined}) VALUES ({placeholders})"
                values_tuple = tuple(row_data[col] for col in db_cols)
                cur.execute(insert_sql, values_tuple)

                inserted_ids.append(cur.lastrowid)

        mysql.connection.commit()
        cur.close()

        # === Gửi mail cho các bản ghi có bất kỳ step_trang_thai = 'Chưa HT_TH' hoặc 'Chưa HT_QH' ===
        if inserted_ids:
            # SELECT cột email, nhan_su_to_chuyen_gia, step1_trang_thai,... step19_trang_thai
            cur2 = mysql.connection.cursor()
            select_sql = f"""
            SELECT
              id,
              email,
              nhan_su_to_chuyen_gia,
              step1_trang_thai,
              step2_trang_thai,
              step3_trang_thai,
              step4_trang_thai,
              step5_trang_thai,
              step6_trang_thai,
              step7_trang_thai,
              step8_trang_thai,
              step9_trang_thai,
              step10_trang_thai,
              step11_trang_thai,
              step12_trang_thai,
              step13_trang_thai,
              step14_trang_thai,
              step15_trang_thai,
              step16_trang_thai,
              step17_trang_thai,
              step18_trang_thai,
              step19_trang_thai,
              du_an,
              ten_goi_thau
            FROM khlcnt
            WHERE id IN ({",".join(str(i) for i in inserted_ids)})
            """
            cur2.execute(select_sql)
            rows = cur2.fetchall()
            cur2.close()

            for r in rows:
                ten_goi_thau = r[23]
                rec_id = r[22]
                to_email = r[1]
                to_name  = r[2]  # cột nhan_su_to_chuyen_gia

                # Lấy stepX_trang_thai
                all_steps = list(r[3:3+19])  # r[3] -> step1_trang_thai, ... r[21] -> step19_trang_thai

                # Kiểm tra xem có step nào = 'Chưa HT_TH' hoặc 'Chưa HT_QH'
                need_send = any(s in ("Chưa HT_TH", "Chưa HT_QH") for s in all_steps)

                if need_send and to_email:
                    greet = to_name if to_name else "Anh/Chị"
                    subject = f"[Thông báo] {rec_id}"
                    content = f"""
                    <p>Xin chào đ/c {greet},</p>
                    <p>Gói thầu <b>{ten_goi_thau}</b> thuộc Dự án: <b>{rec_id}</b> có ít nhất 1 bước ở trạng thái <b>Chưa hoàn thành</b>.</p>
                    <p>Vui lòng kiểm tra tiến độ!</p>
                    """
                    send_email(to_email, subject, content)

        return jsonify({
            "message": "Import thành công",
            "count": len(inserted_ids)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
   # Thêm job vào scheduler
    scheduler.add_job(daily_send_mail_job, 'cron', hour=9, minute=25, id='daily_mail_job', replace_existing=True)
    # Nếu muốn truy cập từ ngoài container, hãy thêm host='0.0.0.0'
    app.run(host="0.0.0.0", port=5200,debug=True, use_reloader=False)