export interface Photo {
  id: number;
  album: string;
  image_url: string;
  caption: string;
  created_at: string;
  updated_at: string;
  location: string;
}

export interface AddPhotoInput {
  albumId: string;
  image: File | null;
  caption?: string;
  location?: string;
}
