
export function useGetLocalStorage(key: string) {
    return localStorage.getItem(key)
}


export function useSetLocalStorage(key: string, value: string = "") {
    localStorage.setItem(key, value)
    return true
}

export function useRemoveLocalStorage(key: string) {
    localStorage.removeItem(key)
    return true
}