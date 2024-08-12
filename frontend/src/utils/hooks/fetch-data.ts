import { FetchResponse, OptionsFetch, OptionsFetchData } from "../domain/types/fetch.type";

export async function useGetFetch<E>(url: string, options?: OptionsFetch) {

    try {
        let myHeaders = new Headers()

        if (options?.tokenAuth) {
            myHeaders.append('Authorization', `bearer ${options?.tokenAuth}`)
        }
        const toURL = new URL(`${url}${options?.path ?? ""}`)
        if (options?.params) {
            const sizeParams = options.params.length
            for (let index = 0; index < sizeParams; index++) {
                const element = options.params[index];
                toURL.searchParams.append(element.name, element.value)
            }
        }
        console.log(`url --> ${toURL}`)
        const responseFetch = await fetch(toURL.toString(), {
            method: "GET",
            headers: myHeaders,
            credentials: 'include',
        })

        if (!responseFetch.ok) {
            const errorText = await responseFetch.text();
    throw new Error(`HTTP error! status: ${responseFetch.status}, message: ${errorText}`);
        }

        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        console.error(`Fetch error: ${error}`);
        return { detail: "Hubo problemas de conexión o aún no estas autenticado." }
    }
}

export async function useDeleteFetch<E, T extends BodyInit | null | undefined>(url: string, options?: OptionsFetchData<T>) {
    try {
        let myHeaders = new Headers()
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
            body: options?.data,
        })
        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        return { detail: "Hubo problemas de conexión." }
    }
}

export async function usePostFetch<E, T extends BodyInit | null | undefined>(url: string, options?: OptionsFetchData<T>) {
    try {
        let myHeaders = new Headers()
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
            method: "POST",
            headers: myHeaders,
            body: options?.data,
        })
        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        return { detail: "Hubo problemas de conexión." }
    }
}

export async function usePutFetch<E, T extends BodyInit | null | undefined>(url: string, options?: OptionsFetchData<T>) {
    try {
        let myHeaders = new Headers()
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
            body: options?.data,
        })
        return await responseFetch.json() as FetchResponse<E>
    } catch (error) {
        return { detail: "Hubo problemas de conexión." }
    }
}