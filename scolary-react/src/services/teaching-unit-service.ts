import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";
import { apiRequest } from "./api-client";
import { TeachingUnit, TeachingUnitListQuery } from "@/models/teaching-unit";
import { ApiListResponse } from "@/models/shared";

const teachingUnitKey = ["teaching-unit"] as const;

const queryKeys = {
  teachingUnits: (query?: TeachingUnitListQuery): QueryKey =>
    query ? [...teachingUnitKey, query] : teachingUnitKey
};

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

export const fetchTeachingUnits = async (
  query?: TeachingUnitListQuery
): Promise<{ data: TeachingUnit[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<TeachingUnit> | TeachingUnit[]>(
      "/teaching_units/",
      { query }
    )
  );

export const useTeachingUnits = (query?: TeachingUnitListQuery) =>
  useQuery({
    queryKey: queryKeys.teachingUnits(query),
    queryFn: () => fetchTeachingUnits(query)
  });

export const createTeachingUnit = (
  payload: Partial<TeachingUnit>
): Promise<TeachingUnit> =>
  apiRequest<TeachingUnit>("/teaching_units/", {
    method: "POST",
    json: payload
  });

export const updateTeachingUnit = (
  id: number,
  payload: Partial<TeachingUnit>
): Promise<TeachingUnit> =>
  apiRequest<TeachingUnit>(`/teaching_units/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteTeachingUnit = (id: number): Promise<void> =>
  apiRequest<void>(`/teaching_units/${id}`, { method: "DELETE" });

export const useCreateTeachingUnit = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createTeachingUnit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teachingUnitKey });
    }
  });
};

export const useUpdateTeachingUnit = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: Partial<TeachingUnit>;
    }) => updateTeachingUnit(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teachingUnitKey });
    }
  });
};

export const useDeleteTeachingUnit = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteTeachingUnit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: teachingUnitKey });
    }
  });
};

export const teachingUnitService = {
  fetchTeachingUnits,
  useTeachingUnits,
  createTeachingUnit,
  updateTeachingUnit,
  deleteTeachingUnit,
  useCreateTeachingUnit,
  useUpdateTeachingUnit,
  useDeleteTeachingUnit
};
