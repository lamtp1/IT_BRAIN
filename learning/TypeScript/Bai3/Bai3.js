"use strict";
class Human {
    constructor(firstName, lastName, tuoi) {
        this.firstName = firstName;
        this.tuoi = tuoi;
        this.lastName = lastName;
    }
    get FullName() {
        return `${this.firstName} ${this.lastName}`;
    }
    set TuoiNguoi(tuoi1) {
        if (tuoi1 <= 1 || tuoi1 > 100) {
            throw Error("Tuổi không hợp lệ");
        }
        this.tuoi = tuoi1;
    }
}
class nhanVien extends Human {
    constructor(firstName, lastName, tuoi, ma_NV, chuc_danh) {
        super(firstName, lastName, tuoi);
        this.ma_NV = ma_NV;
        this.chuc_danh = chuc_danh;
    }
    set MaNV(ma_NV1) {
        this.ma_NV = ma_NV1;
    }
    set ChucDanh(chuc_danh1) {
        this.chuc_danh = chuc_danh1;
    }
    get FullName() {
        return `${super.FullName} là tên của nhân viên này`;
    }
}
let a = new nhanVien("Từ Phú", "Lâm", 25, 428118, "KS Thiết kế triển khai Công nghệ nền tảng");
a.TuoiNguoi = 15;
a.ChucDanh = "Lao công";
console.log(a);
