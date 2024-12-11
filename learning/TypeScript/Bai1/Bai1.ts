interface IPerson {
    firstName: string
    lastName: string
    address: string
}

let nguoi1: IPerson = {firstName: "Tu", lastName: "Lam", address: "11 ngõ 87 Tam Trinh"}
console.log(nguoi1)

interface nguoiLaoDong extends IPerson {
    chieuCao: number
    canNang: number
}

let nguoi3: nguoiLaoDong = {firstName: "James", lastName: "Harden", address: "LA", chieuCao: 196, canNang: 189}

