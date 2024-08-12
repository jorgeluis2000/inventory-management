
export type ResponseLogin = { detail?: string; token?: string; user?: UserContent }

export type ResponseRegister = {
    token?: string
    detail?: string
}

export type UserContent = { id: number; username: string; email: string }