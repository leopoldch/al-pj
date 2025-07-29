import { useQuery, UseQueryResult } from "@tanstack/react-query";
import { useAuth } from "../hooks/useAuth";
import { IAlbum, AddAlbumInput } from "../types/album";
import { useMutation, UseMutationResult } from "@tanstack/react-query";
import { useQueryClient } from "@tanstack/react-query";

export const useAlbums = (): UseQueryResult<IAlbum[], unknown> => {
  const { axiosInstance } = useAuth();

  return useQuery<IAlbum[], unknown>({
    queryKey: ["albums"],
    queryFn: async () => {
      const response = await axiosInstance.get("/albums");
      return response.data;
    },
  });
};

export const useAddAlbumMutation = (): UseMutationResult<any, unknown, AddAlbumInput> => {
  const { axiosInstance } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ name, description, image }: AddAlbumInput) => {
      const formData = new FormData();
      formData.append("title", name);
      formData.append("description", description);
      if (image) {
        formData.append("image", image);
      }
      const response = await axiosInstance.post("/albums/", formData);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["albums"] });
    },
  });
};

export const useUpdateAlbumMutation = (): UseMutationResult<
  any,
  unknown,
  Partial<IAlbum> & { id: number; image?: File }
> => {
  const { axiosInstance } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (album) => {
      const { id, title, description, image } = album;

      if (!id) throw new Error("Album ID is required for update");

      const formData = new FormData();

      if (title !== undefined) {
        formData.append("title", title);
      }
      if (description !== undefined) {
        formData.append("description", description);
      }
      if (image instanceof File) {
        formData.append("image", image);
      }

      const response = await axiosInstance.put(`/albums/${id}/`, formData);

      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["albums"] });
    },
  });
};
