# I. Giới thiệu về GIT:

## 1. Khái niệm:

- Là hệ thống để kiểm soát phiên bản: version control system (vcs): dự án về website, ứng dụng, phần mềm...
- Lịch sử: thông tin thay đổi, có gì đã thực hiện, do ai, khi nào, tại sao lại làm vậy...
- Các nhóm có thể cộng tác trong dự án
- Có thể khôi phục lại phiên bản trước đó mà ta cần (rollback)

## 2. Nguyên tắc làm việc của git:

- Có 1 kho lưu trữ trung tâm (repository)
- Lấy dữ liệu về (pull), đẩy lên (push), lên repo
- Công cấp công cụ để giải quyết các xung đột

## 3. Lợi ích:

- Không lo làm hỏng bất cứ thứ gì vĩnh viễn (do rollback được).
- Merge code nhiều người làm với nhau, giúp dễ cộng tác với người khác.
- Giúp phát triển phiên bản mới mà không ảnh hưởng tới phiên bản cũ.

### Cách để chạy file .ts trên máy khi gặp lỗi "execution of scirpts is disabled on this system"

1.  Login bằng user Administrator
2.  Mở PowerShell, gõ lệnh Set-ExecutionPolicy Restricted

### Build frontend và backend modules để hết lỗi không tìm thấy module:

1. Backend: 

        npm run start:dev

2. Frontend:

        npm run dev

### Fix lỗi không thấy module tsc khi chạy code:

- Nguyên nhân: chưa khai báo module tsc trong biến môi trường, mặc định nodejs sẽ gọi đến `C:\Users\Admin\AppData\Roaming\npm\node_modules\bin\tsc` để tìm file tsc.
-> Phải bổ sung thêm đường dẫn khác cho tsc nếu có (Edit environment variables) và thoát VScode/cmd ra vào lại thì thay đổi mới áp dụng

- Có thể dùng `ts-node` để chạy thẳng file `.ts` mà  không cần gõ tsc để dịch sang file `.js` rồi dùng `node` để biên dịch file `js` thành ngôn ngữ máy tính.
- Browser không hiểu được typescript mà chỉ hiểu javascript nên mới cần phiên dịch sang `js`

### Tại sao dùng typescript:

- Typescript kế thừa và khắc phục các nhược điểm của javascript
- js là ngôn ngữ động (dynamic language) do không cần khai báo kiểu dữ liệu khi khai báo biến

### Các bước dựng môi trường chạy code hệ thống IT_BRAIN

1. Dùng user Admin trên máy bàn cài NodeJs bản 18.18.2
2. Cài redis-server để chạy backend (windows 10 thì dùng file `.msi`), dùng user admin để cài, để port dịch vụ mặc định (port 6379). Cài xong gõ redis-server vào command line để chạy. Nếu gặp lỗi ` Could not create server TCP listening socket *:6379: bind: An operation was attempted on something that is not a socket.` thì vào redis-cli.exe ở thư mục cài redis rồi gõ shutdown, sau đó chạy lại lệnh redis-server trên cmd
3. Copy node_modules của a DuongNT72 vào node_modules ở frontend và backend. Sau đó, thêm đường dẫn tới file `.bin` của thư mục frontend và backend vào biến môi trường (Edit the system environment variables). Nhớ add biến môi trường ở cả user admin và user LAMTP1
4. Run backend, dùng lệnh: `npm run start:dev` trên terminal của VSCode (nhớ trỏ tới thư mục backend để chạy lệnh). Nếu bị lỗi kết nối tới redis thì kiểm tra lại file `.env.local` ở thư mục backend đã sửa `REDIS_HOST=127.0.0.1` chưa.
5. Backend không báo lỗi thì chạy tiếp frontend, lệnh: `npm run dev` trên terminal. Check lại file `.env.development` nếu báo lỗi connection khi truy cập vào web, đảm bảo giống như dưới:

                # just a flag
                VUE_APP_ENV='development'
                # base url
                VUE_APP_BASE='http://10.211.202.5:8000/'
                # base api
                VUE_APP_BASE_API='http://localhost:8000/api/1.0/'
                VUE_APP_SSO_LOGIN='https://10.30.132.79:8225/sso/login'
                VUE_APP_PORT=9000
                VUE_APP_HOST=localhost
                VUE_APP_IS_MANUAL_LOGIN=true
                VUE_APP_SSO_LOGOUT='https://10.30.132.79:8225/sso/logout'

#### `Lưu ý:`

- File .env.local ở backend và .env.development ở frontend có thể không tồn tại từ đầu, phải tạo mới.
- user/password đăng nhập vào web it_brain là `id_nhân_viên/qwe123!@#`
- Đảm bảo đã cài `git` trước đấy để kéo code mới nhất về

## Frontend:

- Việc biên dịch sẽ được thực hiện tự động khi lưu code nhờ vào việc dùng lệnh `npm run dev` khi khởi tạo frontend, lệnh này sẽ kích hoạt lệnh `vue-cli-service serve --watch --mode development`, lệnh này tương tự với việc auto dịch file ts --> js khi dùng `tsc: watch` ở backend

### Cách sửa giao diện với Vue:

- Vào it_brain_frontend --> src --> view --> [tên module muốn fix giao diện, vd: lb-management] --> index.vue
trong lb-management có thể có module con: lb-data, lb-device, lb-link-planning, trong module con này cũng có index.vue

### Cách tìm và sửa api frontend:

- Vào it_brain_frontend --> src --> router --> modules --> [tên module]. Tại đây ta sẽ thấy thuộc tính `path` của mỗi object, path này là đuôi của api, VD:

const router = {
  path: '/it-services',
  component: Layout,
  redirect: '/it-services/services',
  alwaysShow: true, // will always show the root menu
  name: 'IT Services',
  meta: {
    title: 'IT Services',
    icon: '/svg-icons/Service.svg',
  },
  children: [
    {
      path: 'services',
      component: () => import('@/views/it-services/catalog/index'),
      name: 'CatalogList',
      meta: {
        title: 'Service catalog',
      }
    },

Ở VD trên, object router sẽ có thuộc tính: path, component, redirect, children,... trong property children, lại có các object khác, mỗi object này có các property của riêng nó như: path, component, name, meta... trong path của children có value là services, tương ứng với api `/it-services/services`. Property component của children sẽ trỏ đến phần giao diện ở `@/views/it-services/catalog/index`

`--> Router trỏ đến views`


## Backend:

- Sửa api (GET/POST/PUT/DELETE) ở it_brain_frontend --> src --> modules --> [tên module muốn sửa]. Đảm báo mỗi module có đủ các file .ts là: 
1. .dto.ts
2. file controller.ts
3. file module.ts
4. file repository.ts
5. file service.ts

### Cách xử lý khi gặp lỗi `your local changes would be overwritten by merge` khi dùng git pull để kéo code mới nhất:

chạy lệnh sau trước khi pull:

    git stash push --include-untracked

sau đó dùng git pull

- Lưu ý backup file `.env.development` ở frontend và `.env.local` ở backend trước khi chạy lệnh vì khi pull về sẽ ghi đè các file này.

### Cài module mới nếu thiếu:

    npm install  [tên_module]  --legacy-peer-deps