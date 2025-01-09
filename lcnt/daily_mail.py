import MySQLdb
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# Thông tin SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "tuphulam@gmail.com"
SMTP_PASSWORD = "kbkzbbvnsjldnmdg"

def send_email(recipient, subject, content):
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
        server.quit()
        print(f"Sent to {recipient}")
    except Exception as e:
        print(f"Failed to send to {recipient}: {e}")

def send_daily_mails():
    # Kết nối DB (sửa host, user, pass, db)
    conn = MySQLdb.connect(host="171.229.20.248", user="root", password="Cdvdstyvds@1412", port=4406, db="task_management", charset="utf8")
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    # Lấy tất cả các bản ghi
    sql = """
    SELECT 
      id, du_an, ten_goi_thau, email, nhan_su_to_chuyen_gia,
      step1_trang_thai, step2_trang_thai, step3_trang_thai, step4_trang_thai, step5_trang_thai, step6_trang_thai, step7_trang_thai, step8_trang_thai, step9_trang_thai, step10_trang_thai, step11_trang_thai, step12_trang_thai, step13_trang_thai, step14_trang_thai, step15_trang_thai, step16_trang_thai, step17_trang_thai, step18_trang_thai, step19_trang_thai
    FROM khlcnt_test
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

if __name__ == "__main__":
    send_daily_mails()
