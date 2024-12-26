import os
import smtplib
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import pandas as pd
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

emails_sent_count = 0  # ★ Biến đếm tổng số mail đã gửi

# ==================  CẤU HÌNH MYSQL  ==================
app.config['MYSQL_HOST'] = '171.229.20.248'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
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

# ==================  TÍNH TRẠNG THÁI CHO MỖI STEP  ==================
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

@app.route('/emails_sent_count', methods=['GET'])
def get_emails_sent_count():
    global emails_sent_count
    return jsonify({'count': emails_sent_count})

# @app.route('/')
# def index():
#     return render_template('chatgpt_backup.html')

@app.route('/', methods=['GET'])
def view_khlcnt():
    """
    Lấy dữ liệu từ bảng 'khlcnt' và hiển thị lên giao diện.
    """
    try:
        # Kết nối và thực hiện truy vấn
        cur = mysql.connection.cursor()
        query = """
        SELECT 
            mang, du_an, ten_goi_thau, thoi_gian_bat_dau_lcnt, muc_uu_tien,
            step1_kh, step1_ngay_htthucte, step1_trang_thai,
            step2_kh, step2_ngay_htthucte, step2_trang_thai,
            step3_kh, step3_ngay_htthucte, step3_trang_thai,
            step4_kh, step4_ngay_htthucte, step4_trang_thai,
            step5_kh, step5_ngay_htthucte, step5_trang_thai,
            step6_kh, step6_ngay_htthucte, step6_trang_thai,
            step7_kh, step7_ngay_htthucte, step7_trang_thai,
            step8_kh, step8_ngay_htthucte, step8_trang_thai,
            step9_kh, step9_ngay_htthucte, step9_trang_thai,
            step10_kh, step10_ngay_htthucte, step10_trang_thai,
            step11_kh, step11_ngay_htthucte, step11_trang_thai,
            step12_kh, step12_ngay_htthucte, step12_trang_thai,
            step13_kh, step13_ngay_htthucte, step13_trang_thai,
            step14_kh, step14_ngay_htthucte, step14_trang_thai,
            step15_kh, step15_ngay_htthucte, step15_trang_thai,
            step16_kh, step16_ngay_htthucte, step16_trang_thai,
            step17_kh, step17_ngay_htthucte, step17_trang_thai,
            step18_kh, step18_ngay_htthucte, step18_trang_thai,
            step19_kh, step19_ngay_htthucte, step19_trang_thai,
            hang_ve_kho, nhan_su_to_chuyen_gia, email
        FROM khlcnt
        """
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

        # Tên cột hiển thị
        columns = [
            "Mạng", "Dự án", "Tên gói thầu", "Thời gian bắt đầu LCNT", "Mức ưu tiên",
            "Step 1 KH", "Step 1 Ngày HT TT", "Step 1 Trạng thái",
            "Step 2 KH", "Step 2 Ngày HT TT", "Step 2 Trạng thái",
            "Step 3 KH", "Step 3 Ngày HT TT", "Step 3 Trạng thái",
            "Step 4 KH", "Step 4 Ngày HT TT", "Step 4 Trạng thái",
            "Step 5 KH", "Step 5 Ngày HT TT", "Step 5 Trạng thái",
            "Step 6 KH", "Step 6 Ngày HT TT", "Step 6 Trạng thái",
            "Step 7 KH", "Step 7 Ngày HT TT", "Step 7 Trạng thái",
            "Step 8 KH", "Step 8 Ngày HT TT", "Step 8 Trạng thái",
            "Step 9 KH", "Step 9 Ngày HT TT", "Step 9 Trạng thái",
            "Step 10 KH", "Step 10 Ngày HT TT", "Step 10 Trạng thái",
            "Step 11 KH", "Step 11 Ngày HT TT", "Step 11 Trạng thái",
            "Step 12 KH", "Step 12 Ngày HT TT", "Step 12 Trạng thái",
            "Step 13 KH", "Step 13 Ngày HT TT", "Step 13 Trạng thái",
            "Step 14 KH", "Step 14 Ngày HT TT", "Step 14 Trạng thái",
            "Step 15 KH", "Step 15 Ngày HT TT", "Step 15 Trạng thái",
            "Step 16 KH", "Step 16 Ngày HT TT", "Step 16 Trạng thái",
            "Step 17 KH", "Step 17 Ngày HT TT", "Step 17 Trạng thái",
            "Step 18 KH", "Step 18 Ngày HT TT", "Step 18 Trạng thái",
            "Step 19 KH", "Step 19 Ngày HT TT", "Step 19 Trạng thái",
            "Hàng về kho", "Nhân sự tổ chuyên gia", "Email"
        ]

        # Truyền dữ liệu tới template
        return render_template('chatgpt_backup.html', columns=columns, rows=rows)
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
            
            ("(8)_Ký xong Báo cáo đánh","KH"): "step8_kh",
            ("(8)_Ký xong Báo cáo đánh","Ngày hoàn thành thực tế"): "step8_ngay_htthucte",

            ("(9)_Thư mời thương thảo","KH"): "step9_kh",
            ("(9)_Thư mời thương thảo","Ngày hoàn thành thực tế"): "step9_ngay_htthucte",

            ("(10)_Hoàn thiện ký biên bản thương thảo","KH"): "step10_kh",
            ("(10)_Hoàn thiện ký biên bản thương thảo","Ngày hoàn thành thực tế"): "step10_ngay_htthucte",

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
                        db_col == "hang_ve_kho" or 
                        db_col == "thoi_gian_bat_dau_lcnt"):
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
              du_an
            FROM khlcnt
            WHERE id IN ({",".join(str(i) for i in inserted_ids)})
            """
            cur2.execute(select_sql)
            rows = cur2.fetchall()
            cur2.close()

            for r in rows:
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
                    <p>Dự án {rec_id} có ít nhất 1 bước ở trạng thái Chưa hoàn thành.</p>
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
    # Nếu muốn truy cập từ ngoài container, hãy thêm host='0.0.0.0'
    app.run(debug=True)
