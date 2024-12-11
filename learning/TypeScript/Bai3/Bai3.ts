class Human {
    protected firstName: string
    protected lastName: string
    tuoi: number

    constructor(firstName: string, lastName: string, tuoi: number) {
        this.firstName = firstName
        this.tuoi = tuoi
        this.lastName = lastName
    }

    get FullName() {
        return `${this.firstName} ${this.lastName}`
    }

    set TuoiNguoi(tuoi1: number){
        if (tuoi1 <= 1 || tuoi1 > 100){
            throw Error("Tuổi không hợp lệ")
        }
        this.tuoi = tuoi1
    }
}

class nhanVien extends Human {
    protected ma_NV: number
    protected chuc_danh: string

    constructor(firstName: string, lastName: string, tuoi: number, ma_NV: number, chuc_danh: string) {
        super(firstName, lastName, tuoi)
        this.ma_NV = ma_NV
        this.chuc_danh = chuc_danh
    }

    set MaNV(ma_NV1: number) {
        this.ma_NV = ma_NV1
    }
    
    set ChucDanh(chuc_danh1: string) {
        this.chuc_danh = chuc_danh1
    }

    
    get FullName(): string {
        return `${super.FullName} là tên của nhân viên này`
    }

}

let a = new nhanVien("Từ Phú", "Lâm", 25, 428118, "KS Thiết kế triển khai Công nghệ nền tảng")
a.TuoiNguoi = 15
a.ChucDanh = "Lao công"
console.log(a)