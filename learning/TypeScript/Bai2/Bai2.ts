// Khởi tạo class xe hơi 

enum dongCo {
    v8 = "Động cơ v8",
    v16 = "Động cơ v16",
    v32 = "Động cơ v32"
}

enum nhienLieu {
    xang = "Động cơ xăng",
    dien = "Động cơ điện",
    khi = "Động cơ khí"
}

enum model {
    c300 = "Mercedes C300",
    s450 = "Mercedes S450 - Maybach",
    glk = "Mercedes GLK 400",
    glc300 = "Mercedes GLC 300 "
}

enum chatLieu {
    carbon = "Sợi Carbon tinh chất",
    steel = "Hợp kim siêu thép kháng gỉ",
    alu = "Nhôm chế tạo máy bay chiến đấu"
}

abstract class xeOto {
    trongLuong: number // bao nhieu kg
    dongCo: dongCo // v8, v16, hay v32
    nhienLieu: nhienLieu // xang, dien, hay khi
    giaThanh: number 

    constructor(trongLuong: number, dongCo: dongCo, nhienLieu: nhienLieu, giaThanh: number) {
        this.trongLuong = trongLuong
        this.dongCo = dongCo
        this.nhienLieu = nhienLieu
        this.giaThanh = giaThanh
    }

    abstract get TrongLuong (): number
    
    abstract set giaThanh1 (giaThanh1: number)
}

class otoTai extends xeOto {
    carryWeight: number

    constructor (trongLuong: number, dongCo: dongCo, nhienLieu: nhienLieu, giaThanh: number, carryWeight: number) {
        super(trongLuong, dongCo, nhienLieu, giaThanh)
        this.carryWeight = carryWeight
    }

    get TrongLuong(): number {
        return this.trongLuong
    }

    set giaThanh1 (giaThanh1: number) {
        this.giaThanh = giaThanh1
    }

    get carryWeight1 () {
        return this.carryWeight
    }
}

abstract class xeDua extends xeOto {
    tocDo: number

    constructor (trongLuong: number, dongCo: dongCo, nhienLieu: nhienLieu, giaThanh: number, tocDo: number) {
        super(trongLuong, dongCo, nhienLieu, giaThanh)
        this.tocDo = tocDo
    }

    get TrongLuong(): number {
        return this.trongLuong
    }

    set giaThanh1 (giaThanh1: number) {
        this.giaThanh = giaThanh1
    }

    abstract get tocDo1(): number
}

class Mercedes extends xeDua {
    model: model

    constructor(trongLuong: number, dongCo: dongCo, nhienLieu: nhienLieu, giaThanh: number, carryWeight: number, tocDo: number, model: model) {
        super(trongLuong, dongCo, nhienLieu, giaThanh, tocDo)
        this.model = model
    }

    get tocDo1() {
        return this.tocDo
    }

    set model1 (model1: model) {
        this.model = model1
    }

    get model1 (): string {
        return this.model
    }
}

class RedBull extends xeDua {
    chatLieu: string
     
    constructor(trongLuong: number, dongCo: dongCo, nhienLieu: nhienLieu, giaThanh: number, tocDo: number, chatLieu: string) {
        super(trongLuong, dongCo, nhienLieu, giaThanh, tocDo)
        this.chatLieu = chatLieu
    }

    get tocDo1 (){
        return this.tocDo
    }

    set chatLieu1 (chatLieu1: string) {
        this.chatLieu = chatLieu1
    }

    get chatLieu1 () {
        return this.chatLieu
    }
}

let xedua1 = new Mercedes (1200, dongCo.v32, nhienLieu.xang, 12000000, 333, 4444, model.s450)
console.log(xedua1)

let xedua2 = new RedBull (1260, dongCo.v16, nhienLieu.xang, 2000000, 290, chatLieu.carbon)

let xedua3 = new Mercedes (1100, dongCo.v8, nhienLieu.xang, 12000000, 333, 4444, model.s450)
console.log(xedua1)

let xedua4 = new RedBull (900, dongCo.v8, nhienLieu.xang, 2000000, 290, chatLieu.carbon)

let xedua = [xedua1, xedua2, xedua3, xedua4]

for (let i = 0; i < 4; i++) {
    if (xedua[i].trongLuong > xedua[i+1].trongLuong) {
        
    }
}
