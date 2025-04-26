import {
  useMutation,
  UseMutationResult,
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "@tanstack/react-query";
import { useAuth } from "../hooks/useAuth";
import IBucketPoint from "../types/bucketspoints";

const BUCKET_POINTS_QUERY_KEY = ["bucketpoints"];

const useBucketPointsQuery = (): UseQueryResult<IBucketPoint[], unknown> => {
  const { axiosInstance } = useAuth();

  return useQuery<IBucketPoint[], unknown>({
    queryKey: BUCKET_POINTS_QUERY_KEY,
    queryFn: async () => {
      const response = await axiosInstance.get("/bucketpoints/");
      return response.data;
    },
  });
};

const useCreateBucketPointMutation = (): UseMutationResult<IBucketPoint, unknown, IBucketPoint> => {
  const { axiosInstance } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<IBucketPoint, unknown, IBucketPoint>({
    mutationFn: async (newBucketPoint: IBucketPoint) => {
      const response = await axiosInstance.post("/bucketpoints/", newBucketPoint);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: BUCKET_POINTS_QUERY_KEY });
    },
  });
};

const useUpdateBucketPointMutation = (): UseMutationResult<
  IBucketPoint,
  unknown,
  { id: number; data: Partial<IBucketPoint> }
> => {
  const { axiosInstance } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<IBucketPoint, unknown, { id: number; data: Partial<IBucketPoint> }>({
    mutationFn: async ({ id, data }) => {
      const response = await axiosInstance.put(`/bucketpoints/${id}/`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: BUCKET_POINTS_QUERY_KEY });
    },
  });
};

const useDeleteBucketPointMutation = (): UseMutationResult<void, unknown, number> => {
  const { axiosInstance } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<void, unknown, number>({
    mutationFn: async (id: number) => {
      await axiosInstance.delete(`/bucketpoints/${id}/`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: BUCKET_POINTS_QUERY_KEY });
    },
  });
};

export {
  useBucketPointsQuery,
  useCreateBucketPointMutation,
  useUpdateBucketPointMutation,
  useDeleteBucketPointMutation,
};
