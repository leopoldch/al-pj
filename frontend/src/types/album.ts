export interface IAlbum {
    id: number
    title: string
    description: string
    cover_image: string
    created_at: string
    updated_at: string
    nb_photos: number
}

export interface AddAlbumInput {
    name: string
    description: string
    image?: File
}
export interface Album {
    id: number
    title: string
    description: string
    cover_image?: string
    created_at: string
    updated_at: string
    nb_photos: number
}
