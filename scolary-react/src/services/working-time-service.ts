import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  WorkingTime,
  WorkingTimeListQuery,
  WorkingTimePayload
} from "@/models/working-time";

const workingTimeKey = ["working-times"] as const;

const queryKeys = {
  workingTimes: (query?: WorkingTimeListQuery): QueryKey =>
    query ? [...workingTimeKey, query] : workingTimeKey
} as const;

const isListResponse = <T>(payload: unknown): payload is ApiListResponse<T> =>
  Boolean(
    payload &&
      typeof payload === "object" &&
      "data" in (payload as Record<string, unknown>) &&
      Array.isArray((payload as ApiListResponse<T>).data)
  );

const normalizeList = <T>(
  payload: ApiListResponse<T> | T[]
): { data: T[]; count?: number } =>
  isListResponse(payload)
    ? { data: payload.data, count: payload.count }
    : {
        data: Array.isArray(payload) ? payload : [],
        count: Array.isArray(payload) ? payload.length : 0
      };

export const fetchWorkingTimes = async (
  query?: WorkingTimeListQuery
): Promise<{ data: WorkingTime[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<WorkingTime> | WorkingTime[]>(
      "/working_times/",
      { query }
    )
  );

export const useWorkingTimes = (query?: WorkingTimeListQuery) =>
  useQuery({
    queryKey: queryKeys.workingTimes(query),
    queryFn: () => fetchWorkingTimes(query)
  });

export const createWorkingTime = (
  payload: WorkingTimePayload
): Promise<WorkingTime> =>
  apiRequest<WorkingTime>("/working_times/", {
    method: "POST",
    json: payload
  });

export const updateWorkingTime = (
  id: number,
  payload: WorkingTimePayload
): Promise<WorkingTime> =>
  apiRequest<WorkingTime>(`/working_times/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteWorkingTime = (id: number): Promise<void> =>
  apiRequest<void>(`/working_times/${id}`, { method: "DELETE" });

export const useCreateWorkingTime = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createWorkingTime,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: workingTimeKey });
    }
  });
};

export const useUpdateWorkingTime = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: WorkingTimePayload }) =>
      updateWorkingTime(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: workingTimeKey });
    }
  });
};

export const useDeleteWorkingTime = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteWorkingTime,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: workingTimeKey });
    }
  });
};

export const workingTimeService = {
  fetchWorkingTimes,
  useWorkingTimes,
  createWorkingTime,
  updateWorkingTime,
  deleteWorkingTime,
  useCreateWorkingTime,
  useUpdateWorkingTime,
  useDeleteWorkingTime
};
