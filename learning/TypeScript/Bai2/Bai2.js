"use strict";
// Khởi tạo class xe hơi 
var dongCo;
(function (dongCo) {
    dongCo["v8"] = "\u0110\u1ED9ng c\u01A1 v8";
    dongCo["v16"] = "\u0110\u1ED9ng c\u01A1 v16";
    dongCo["v32"] = "\u0110\u1ED9ng c\u01A1 v32";
})(dongCo || (dongCo = {}));
var nhienLieu;
(function (nhienLieu) {
    nhienLieu["xang"] = "\u0110\u1ED9ng c\u01A1 x\u0103ng";
    nhienLieu["dien"] = "\u0110\u1ED9ng c\u01A1 \u0111i\u1EC7n";
    nhienLieu["khi"] = "\u0110\u1ED9ng c\u01A1 kh\u00ED";
})(nhienLieu || (nhienLieu = {}));
var model;
(function (model) {
    model["c300"] = "Mercedes C300";
    model["s450"] = "Mercedes S450 - Maybach";
    model["glk"] = "Mercedes GLK 400";
    model["glc300"] = "Mercedes GLC 300 ";
})(model || (model = {}));
var chatLieu;
(function (chatLieu) {
    chatLieu["carbon"] = "S\u1EE3i Carbon tinh ch\u1EA5t";
    chatLieu["steel"] = "H\u1EE3p kim si\u00EAu th\u00E9p kh\u00E1ng g\u1EC9";
    chatLieu["alu"] = "Nh\u00F4m ch\u1EBF t\u1EA1o m\u00E1y bay chi\u1EBFn \u0111\u1EA5u";
})(chatLieu || (chatLieu = {}));
class xeOto {
    constructor(trongLuong, dongCo, nhienLieu, giaThanh) {
        this.trongLuong = trongLuong;
        this.dongCo = dongCo;
        this.nhienLieu = nhienLieu;
        this.giaThanh = giaThanh;
    }
}
class otoTai extends xeOto {
    constructor(trongLuong, dongCo, nhienLieu, giaThanh, carryWeight) {
        super(trongLuong, dongCo, nhienLieu, giaThanh);
        this.carryWeight = carryWeight;
    }
    get TrongLuong() {
        return this.trongLuong;
    }
    set giaThanh1(giaThanh1) {
        this.giaThanh = giaThanh1;
    }
    get carryWeight1() {
        return this.carryWeight;
    }
}
class xeDua extends xeOto {
    constructor(trongLuong, dongCo, nhienLieu, giaThanh, tocDo) {
        super(trongLuong, dongCo, nhienLieu, giaThanh);
        this.tocDo = tocDo;
    }
    get TrongLuong() {
        return this.trongLuong;
    }
    set giaThanh1(giaThanh1) {
        this.giaThanh = giaThanh1;
    }
}
class Mercedes extends xeDua {
    constructor(trongLuong, dongCo, nhienLieu, giaThanh, carryWeight, tocDo, model) {
        super(trongLuong, dongCo, nhienLieu, giaThanh, tocDo);
        this.model = model;
    }
    get tocDo1() {
        return this.tocDo;
    }
    set model1(model1) {
        this.model = model1;
    }
    get model1() {
        return this.model;
    }
}
class RedBull extends xeDua {
    constructor(trongLuong, dongCo, nhienLieu, giaThanh, tocDo, chatLieu) {
        super(trongLuong, dongCo, nhienLieu, giaThanh, tocDo);
        this.chatLieu = chatLieu;
    }
    get tocDo1() {
        return this.tocDo;
    }
    set chatLieu1(chatLieu1) {
        this.chatLieu = chatLieu1;
    }
    get chatLieu1() {
        return this.chatLieu;
    }
}
let xedua1 = new Mercedes(4344, dongCo.v32, nhienLieu.xang, 12000000, 333, 4444, model.s450);
console.log(xedua1);
