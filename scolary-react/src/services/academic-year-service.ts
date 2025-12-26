import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  AcademicYear,
  AcademicYearListQuery,
  AcademicYearPayload
} from "@/models/academic-year";

const academicYearsKey = ["academicYears"] as const;

const queryKeys = {
  academicYears: (query?: AcademicYearListQuery): QueryKey =>
    query ? [...academicYearsKey, query] : academicYearsKey,
  academicYear: (id: number): QueryKey => ["academicYear", id]
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

export const fetchAcademicYears = async (
  query?: AcademicYearListQuery
): Promise<{ data: AcademicYear[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<AcademicYear> | AcademicYear[]>(
      "/academic_years/",
      { query }
    )
  );

export const fetchAcademicYear = (id: number): Promise<AcademicYear> =>
  apiRequest<AcademicYear>(`/academic_years/${id}/`);

export const createAcademicYear = (
  payload: AcademicYearPayload
): Promise<AcademicYear> =>
  apiRequest<AcademicYear>("/academic_years/", {
    method: "POST",
    json: payload
  });

export const updateAcademicYear = (
  id: number,
  payload: AcademicYearPayload
): Promise<AcademicYear> =>
  apiRequest<AcademicYear>(`/academic_years/${id}/`, {
    method: "PUT",
    json: payload
  });

export const deleteAcademicYear = (id: number): Promise<void> =>
  apiRequest<void>(`/academic_years/${id}/`, {
    method: "DELETE"
  });

export const useAcademicYears = (query?: AcademicYearListQuery) =>
  useQuery({
    queryKey: queryKeys.academicYears(query),
    queryFn: () => fetchAcademicYears(query)
  });

export const useAcademicYear = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.academicYear(id),
    queryFn: () => fetchAcademicYear(id),
    enabled
  });

export const useCreateAcademicYear = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAcademicYear,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: academicYearsKey });
    }
  });
};

export const useUpdateAcademicYear = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: AcademicYearPayload;
    }) => updateAcademicYear(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: academicYearsKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.academicYear(variables.id)
      });
    }
  });
};

export const useDeleteAcademicYear = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAcademicYear,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: academicYearsKey });
    }
  });
};

export const academicYearService = {
  fetchAcademicYears,
  fetchAcademicYear,
  createAcademicYear,
  updateAcademicYear,
  deleteAcademicYear,
  useAcademicYears,
  useAcademicYear,
  useCreateAcademicYear,
  useUpdateAcademicYear,
  useDeleteAcademicYear
};
