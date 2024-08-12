
export type ResponseLogin = { detail?: string; token?: string; user?: UserContent }

export type ResponseRegister = {
    token?: string
    detail?: string
}

export type ResponseList<T> = {
    detail?: string
    count?: number
    next?: string | null
    previous?: string | null
    results?: T[]
}

export type ResponseAddProduct = {
    id?: number
    name?: string
    serial?: string
    price?: string
    count?: number
    updated_at?: Date
    created_at?: Date
    detail?: string
}

export type ProductContent = {
    id: number
    name: string
    serial: string
    price: string
    count: number
    updated_at: Date
    created_at: Date
}

export type UserContent = { id: number; username: string; email: string }