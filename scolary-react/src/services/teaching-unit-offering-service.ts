import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  TeachingUnitOffering,
  TeachingUnitOfferingListQuery,
  TeachingUnitOfferingPayload
} from "@/models/teaching-unit-offering";

const teachingUnitOfferingKey = ["teaching-unit-offerings"] as const;

const queryKeys = {
  offerings: (query?: TeachingUnitOfferingListQuery): QueryKey =>
    query ? [...teachingUnitOfferingKey, query] : teachingUnitOfferingKey
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

export const fetchTeachingUnitOfferings = async (
  query?: TeachingUnitOfferingListQuery
): Promise<{ data: TeachingUnitOffering[]; count?: number }> =>
  normalizeList(
    await apiRequest<
      ApiListResponse<TeachingUnitOffering> | TeachingUnitOffering[]
    >("/teaching_unit_offerings/", { query })
  );

export const useTeachingUnitOfferings = (
  query?: TeachingUnitOfferingListQuery
) =>
  useQuery({
    queryKey: queryKeys.offerings(query),
    queryFn: () => fetchTeachingUnitOfferings(query)
  });

export const createTeachingUnitOffering = (
  payload: TeachingUnitOfferingPayload
): Promise<TeachingUnitOffering> =>
  apiRequest<TeachingUnitOffering>("/teaching_unit_offerings/", {
    method: "POST",
    json: payload
  });

export const updateTeachingUnitOffering = (
  id: number,
  payload: TeachingUnitOfferingPayload
): Promise<TeachingUnitOffering> =>
  apiRequest<TeachingUnitOffering>(`/teaching_unit_offerings/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteTeachingUnitOffering = (id: number): Promise<void> =>
  apiRequest<void>(`/teaching_unit_offerings/${id}`, { method: "DELETE" });

export const useCreateTeachingUnitOffering = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createTeachingUnitOffering,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teachingUnitOfferingKey });
    }
  });
};

export const useUpdateTeachingUnitOffering = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: TeachingUnitOfferingPayload;
    }) => updateTeachingUnitOffering(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teachingUnitOfferingKey });
    }
  });
};

export const useDeleteTeachingUnitOffering = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteTeachingUnitOffering,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teachingUnitOfferingKey });
    }
  });
};

export const teachingUnitOfferingService = {
  fetchTeachingUnitOfferings,
  useTeachingUnitOfferings,
  createTeachingUnitOffering,
  updateTeachingUnitOffering,
  deleteTeachingUnitOffering,
  useCreateTeachingUnitOffering,
  useUpdateTeachingUnitOffering,
  useDeleteTeachingUnitOffering
};
