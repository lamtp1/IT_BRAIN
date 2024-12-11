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

# `Lộ trình học, bổ sung kiến thức trước khi code:`

## `I. Lộ trình học NextJS:`

### `1. Kiến thức cần chuẩn bị trước khi học Next.js`

#### `a. JavaScript (Cơ bản đến nâng cao)`

- Cơ bản:
  + Biến và kiểu dữ liệu: let, const, var, kiểu nguyên thủy.
  + Toán tử và câu điều kiện: if, else, switch, for, while.
  + Hàm và cách khai báo: function, arrow function.
  + DOM Manipulation: document.querySelector, addEventListener.
- Nâng cao:
  + ES6+:
    > Destructuring, Rest/Spread Operators.
    > Template literals.
    > Modules: import/export.
  + Asynchronous JavaScript:
    > Promise, async/await.
    > Fetch API (fetch, axios).
  + Array Methods: map, filter, reduce, forEach.

#### `b. React.js (Cơ bản đến nâng cao)`

- Cơ bản:
  + JSX: Viết HTML trong JavaScript.
  + Component: Functional Components, Props.
  + State và sự kiện: useState, quản lý sự kiện (onClick, onChange).
- Nâng cao:
  + React Router: Điều hướng giữa các trang.
  + Hooks nâng cao: useEffect, useContext.
  + Quản lý trạng thái:
    > Context API.
    > Redux (tuỳ chọn).
  + Tối ưu hiệu suất: React.memo, useCallback, useMemo.

#### `c. Kiến thức Web cơ bản`

- HTML và CSS: Semantic HTML, Flexbox, Grid, Responsive Design.
- HTTP/HTTPS, REST API:
  + Hiểu request (GET, POST, PUT, DELETE).
  + Cách kết nối Frontend và Backend.
- Kiến thức về SEO cơ bản: Meta tags, Sitemap.

#### `d. TypeScript (không bắt buộc nhưng nên học)`

- Kiểu dữ liệu: string, number, array, object.
- Interfaces, Types.
- Generics.
- Cách sử dụng TypeScript trong React.

### `2. Lộ trình học Next.js`

#### `Bước 1: Làm quen với Next.js`

`1. Cài đặt Next.js:`

  > Tạo ứng dụng:

    npx create-next-app@latest

  > Chạy dự án:

    npm run dev

`2. Hiểu cấu trúc thư mục:`

- pages/: Routing tự động.
- public/: Chứa các file tĩnh (hình ảnh, favicon).
- styles/: Chứa file CSS.

#### `Bước 2: Hiểu các khái niệm cốt lõi`

1. Routing:
- Tự động tạo route bằng cách thêm file trong pages/.
- Dynamic Routes: [id].js.
2. Rendering:
- CSR (Client-Side Rendering).
- SSR (Server-Side Rendering): getServerSideProps.
- SSG (Static Site Generation): getStaticProps và getStaticPaths.
- ISR (Incremental Static Regeneration).
3. API Routes:
- Tạo API trong thư mục pages/api/.

#### `Bước 3: Làm việc với dữ liệu`

1. Fetch API:
- Kết nối với Backend hoặc API bên thứ ba.
- Sử dụng getServerSideProps hoặc getStaticProps để fetch dữ liệu.
2. SEO và tối ưu hóa:
- Sử dụng next/head để thêm thẻ meta.
- Tối ưu tốc độ với Image Optimization (next/image).
3. Quản lý trạng thái:
- Sử dụng Context API hoặc Redux nếu dự án lớn.

#### `Bước 4: Các chủ đề nâng cao`

1. Authentication:
- Sử dụng next-auth hoặc JWT để quản lý người dùng.
2. Middleware:
- Sử dụng Middleware để xử lý request trước khi render.
3. Deploy ứng dụng:
- Sử dụng Vercel (miễn phí và dễ tích hợp).
- eploy trên VPS hoặc nền tảng khác (AWS, DigitalOcean).

## `II. Lộ trình học VueJS:`

### `1. Giai đoạn chuẩn bị kiến thức`

- HTML, CSS cơ bản và nâng cao:
  + Hiểu về cấu trúc HTML: Semantic HTML.
  + CSS nâng cao: Flexbox, Grid, Responsive Design, CSS Variables.
  + Công cụ CSS: SCSS, TailwindCSS (tuỳ chọn).

- JavaScript (Cơ bản đến nâng cao):
  + Biến, hàm, vòng lặp (let, const, function, for).
  + Array Methods: map, filter, reduce.
  + Promise, async/await, Fetch API.
  + ES6+ (Destructuring, Arrow Function, Template Literals).

- Hiểu về REST API:
  + Làm quen với các HTTP Methods: GET, POST, PUT, DELETE.
  + Hiểu về JSON và cách giao tiếp với API.

- Công cụ phát triển:
  + Sử dụng Git/GitHub để quản lý code.
  + IDE: Visual Studio Code (cài các extension cần thiết như Prettier, ESLint).

### `2. Lộ trình học Vue.js (Frontend)`

#### `A. Làm quen với Vue.js`

1. Cài đặt Vue.js:
  > Tạo ứng dụng Vue:

    npm init vue@latest

  > Khởi chạy dự án:

    npm run dev

2. Hiểu cấu trúc thư mục:
- src/: Chứa mã nguồn.
- components/: Chứa các Component.
- App.vue: Component gốc.

3. Cơ bản về Vue.js:
- Hiểu về Instance Vue và cách hoạt động.
- Data Binding: {{ }}, v-bind.
- Event Binding: @click, @input.

#### `B. Thành thạo Vue.js`

1. Làm việc với Components:
- Tạo và sử dụng Component.
- Truyền dữ liệu giữa Components: Props, Emit.

2. Vue Router:
- Cấu hình Router cho ứng dụng.
- Điều hướng giữa các trang (router-link, router-view).

3. State Management với Pinia hoặc Vuex:
- Hiểu cách quản lý trạng thái trong ứng dụng.
- Kết hợp Vue Router và Pinia để xử lý dữ liệu toàn cục.

4. Fetch API và tích hợp Backend:
- Sử dụng Fetch API hoặc axios để gọi API từ Backend (Next.js).

5. Vue Directives nâng cao:
- v-if, v-else, v-show.
- v-for, v-model.

6. Tối ưu hóa Vue.js:
- Dynamic Components.
- Slots.
- Composition API (Vue 3).

#### `C. Triển khai ứng dụng Frontend`

1. SEO và tối ưu hóa:
- Meta Tags.
- Lazy Loading cho Component.
2. Deploy:
- Deploy ứng dụng trên Netlify, Vercel, hoặc một VPS.

fdsfdsf
