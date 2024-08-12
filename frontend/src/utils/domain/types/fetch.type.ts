export type FetchResponse<T> = DataResponse & T 

export type DataResponse = {
    detail?: string
    token?: string
}

export type OptionsFetch = {
    path?: string
    params?: ParamURL[]
    timeout?: number,
    tokenAuth?: string
}

export type OptionsFetchData<D> = {
    path?: string
    data?: D
    params?: ParamURL[]
    timeout?: number,
    tokenAuth?: string
}

type ParamURL = {
    name: string
    value: string
}