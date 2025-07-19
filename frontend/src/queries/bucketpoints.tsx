import { useMutation, UseMutationResult, useQuery, UseQueryResult } from "@tanstack/react-query";
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

  return useMutation<IBucketPoint, unknown, IBucketPoint>({
    mutationFn: async (newBucketPoint: IBucketPoint) => {
      const response = await axiosInstance.post("/bucketpoints/", newBucketPoint);
      return response.data;
    },
  });
};

const useUpdateBucketPointMutation = (): UseMutationResult<
  IBucketPoint,
  unknown,
  { id: number; data: Partial<IBucketPoint> }
> => {
  const { axiosInstance } = useAuth();

  return useMutation<IBucketPoint, unknown, { id: number; data: Partial<IBucketPoint> }>({
    mutationFn: async ({ id, data }) => {
      const response = await axiosInstance.put(`/bucketpoints/${id}/`, data);
      return response.data;
    },
  });
};

const useDeleteBucketPointMutation = (): UseMutationResult<void, unknown, number> => {
  const { axiosInstance } = useAuth();

  return useMutation<void, unknown, number>({
    mutationFn: async (id: number) => {
      await axiosInstance.delete(`/bucketpoints/${id}/`);
    },
  });
};

export {
  useBucketPointsQuery,
  useCreateBucketPointMutation,
  useUpdateBucketPointMutation,
  useDeleteBucketPointMutation,
};
