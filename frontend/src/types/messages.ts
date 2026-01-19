export interface PaginatedResponse<T> {
    count: number
    next: string | null
    previous: string | null
    results: T[]
}

export default interface Imessage {
    id: number
    name: string
    email: string
    message: string
    created_at: string
    user: number
    status: boolean
}
