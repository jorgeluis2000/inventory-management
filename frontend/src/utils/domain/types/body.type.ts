
export type BodyLogin = { username: string; password: string }

export type BodyRegister = {
    username: string
    email: string
    password: string
}


export type BodyAddProduct = {
    name: string
    serial: string
    price?: string
}