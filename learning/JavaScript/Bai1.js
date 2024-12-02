 class XeMay {
    LopXe
    DongCo
    NhienLieu

    constructor(LopXe, DongCo, NhienLieu) {
        this.DongCo = DongCo
        this.LopXe = LopXe
        this.NhienLieu = NhienLieu
    }

    getLopXe() {
        return `Lốp xe của hãng này là ${this.LopXe}`
    }

    setLopXe(LopXe1) {
        this.LopXe = LopXe1
    }
}
let a = new XeMay("Michelin", "Động cơ V8", "Động cơ xăng")
a.LopXe = "Dunlop"
console.log(a)


