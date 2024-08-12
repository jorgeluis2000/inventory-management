import { FetchResponse, OptionsFetch, OptionsFetchData } from "../domain/types/fetch.type";

export async function useGetFetch<E>(url: string = import.meta.env.VITE_API_URL, options?: OptionsFetch) {

    try {
        let myHeaders = new Headers()
        myHeaders.append("Accept", "application/json")
        myHeaders.append("Content-Type", "application/json")
        myHeaders.append("Access-Control-Allow-Origin", "*")
        if (options?.tokenAuth) {
            myHeaders.append('Authorization', `Token ${options?.tokenAuth}`)
        }

        const toURL = new URL(`${url}${options?.path ?? ""}`)
        if (options?.params) {
            const sizeParams = options.params.length
            for (let index = 0; index < sizeParams; index++) {
                const element = options.params[index];
                toURL.searchParams.append(element.name, element.value)
            }
        }
        const responseFetch = await fetch(toURL.toString(), {
            method: "GET",
            headers: myHeaders,
        })

        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        console.error(`Fetch error: ${error}`);
        return { detail: "Hubo problemas de conexión o aún no estas autenticado." }
    }
}

export async function useDeleteFetch<E, T extends BodyInit | null | undefined | any>(url: string, options?: OptionsFetchData<T>) {
    try {
        let myHeaders = new Headers()
        myHeaders.append("Accept", "application/json")
        myHeaders.append("Content-Type", "application/json")
        myHeaders.append("Access-Control-Allow-Origin", "*")
        if (options?.tokenAuth) {
            myHeaders.append('Authorization', `Token ${options?.tokenAuth}`)
        }
        const toURL = new URL(`${url}${options?.path ?? ""}`)
        if (options?.params) {
            const sizeParams = options.params.length
            for (let index = 0; index < sizeParams; index++) {
                const element = options.params[index];
                toURL.searchParams.append(element.name, element.value)
            }
        }
        const responseFetch = await fetch(toURL, {
            method: "DELETE",
            headers: myHeaders,
            body: JSON.stringify(options?.data),
        })
        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        console.log("🚀 ~ error:", error)
        return { detail: "Hubo problemas de conexión." }
    }
}

export async function usePostFetch<E, T extends BodyInit | null | undefined | any>(url: string, options?: OptionsFetchData<T>) {
    try {
        let myHeaders = new Headers()
        myHeaders.append("Accept", "application/json")
        myHeaders.append("Content-Type", "application/json")
        myHeaders.append("Access-Control-Allow-Origin", "*")
        if (options?.tokenAuth) {
            myHeaders.append('Authorization', `Token ${options?.tokenAuth}`)
        }
        const toURL = new URL(`${url}${options?.path ?? ""}`)
        console.log("🚀 ~ toURL:", toURL.toString())
        if (options?.params) {
            const sizeParams = options.params.length
            for (let index = 0; index < sizeParams; index++) {
                const element = options.params[index];
                toURL.searchParams.append(element.name, element.value)
            }
        }
        const responseFetch = await fetch(toURL, {
            method: "POST",
            headers: myHeaders,
            body: JSON.stringify(options?.data),
        })

        if (!responseFetch.ok) {
            return { detail: `Upps, hubo un error al momento de tomar los datos, intenta de nuevo.` }
        }

        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        console.log("🚀 ~ error:", error)
        return { detail: "Hubo problemas de conexión." }
    }
}

export async function usePutFetch<E, T extends BodyInit | null | undefined | any>(url: string, options?: OptionsFetchData<T>) {
    try {
        let myHeaders = new Headers()
        myHeaders.append("Accept", "application/json")
        myHeaders.append("Content-Type", "application/json")
        myHeaders.append("Access-Control-Allow-Origin", "*")
        if (options?.tokenAuth) {
            myHeaders.append('Authorization', `Token ${options?.tokenAuth}`)
        }
        const toURL = new URL(`${url}${options?.path ?? ""}`)
        if (options?.params) {
            const sizeParams = options.params.length
            for (let index = 0; index < sizeParams; index++) {
                const element = options.params[index];
                toURL.searchParams.append(element.name, element.value)
            }
        }
        const responseFetch = await fetch(toURL, {
            method: "PUT",
            headers: myHeaders,
            body: JSON.stringify(options?.data),
        })
        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        console.log("🚀 ~ error:", error)
        return { detail: "Hubo problemas de conexión." }
    }
}