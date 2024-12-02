## Demo dự án fullstack sử dụng NextJS và NestJS.

- Cả 2 framework này đều sử dụng TypeScript
- NextJS sử dụng để code Frontend 
- NestJS thì Backend

### Công nghệ sử dụng:

1. Frontend: Next.JS v14 (typescript), auth.js v5 (next-auth) - dùng để đăng nhập (khi vào 1 link bất kỳ mà chưa đăng nhập sẽ tự động quay lại màn đăng nhập, auth.js sẽ hỗ trợ việc này)
2. Backend: Nest.JS v10 (typescript), xác thực endpoint với JWT (jason web token)
3. Database: MongoDB sử dụng miễn phí với MongoDB Atlas (dùng docker)

### Các tính năng chính:

1. CRUD users (next.js + nestjs)
    - Thêm sửa xóa user trong phần danh sách user.
2. Tích hợp JWT cho nestjs
3. Gửi mail (theo tempalte) với nestjs
4. Login/register/forgot password
    - Khi register thì thông tin account sẽ được lưu vào mongoDB dưới dạng json
    - Một khi account đã ở trong DB thì chỉ cần login là truy cập được trang chủ
    - Cơ chế resend email nếu người dùng đăng ký tài khoản xong mà không nhập mã xác thực gửi tới mail (do mail vào mục spam, mất điện, etc..) tuy nhiên vẫn login bằng account vừa tạo.
5. Khi register (new account) cần xác thực tài khoản qua mail
6. Khi login (nếu tài khoản chưa được xác thực) cần xác thực qua mail.
7. Khi forgot password cần xác thực qua mail.

> Khi demo ở chế độ develop sẽ chậm hơn demo ở chế độ production do mất thời gian biên dịch code.