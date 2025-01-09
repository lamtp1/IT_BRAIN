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
            LIMIT %s OFFSET %s                 
            """
    cur.execute(query,  (page_size, offset))

    rows = cur.fetchall()