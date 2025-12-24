import { useMutation, useQuery, useQueryClient, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface EnrollmentFee {
  id: number;
  level: string;
  price: number;
  id_mention?: number | null;
  id_academic_year?: number | null;
  mention?: { id: number; name?: string; abbreviation?: string } | null;
  academinc_year?: { id: number; name?: string } | null;
}

export type EnrollmentFeePayload = {
  level: string;
  price: number;
  id_mention?: number | null;
  id_academic_year?: number | null;
};

export type EnrollmentFeeListQuery = Record<string, string | number | boolean | undefined>;

const enrollmentFeesKey = ["enrollment-fees"] as const;

const queryKeys = {
  enrollmentFees: (query?: EnrollmentFeeListQuery): QueryKey =>
    query ? [...enrollmentFeesKey, query] : enrollmentFeesKey,
  enrollmentFee: (id: number): QueryKey => ["enrollment-fee", id]
} as const;

const isListResponse = <T>(payload: unknown): payload is ApiListResponse<T> =>
  Boolean(
    payload &&
      typeof payload === "object" &&
      "data" in (payload as Record<string, unknown>) &&
      Array.isArray((payload as ApiListResponse<T>).data)
  );

const normalizeList = <T>(payload: ApiListResponse<T> | T[]): { data: T[]; count?: number } =>
  isListResponse(payload)
    ? { data: payload.data, count: payload.count }
    : { data: Array.isArray(payload) ? payload : [], count: Array.isArray(payload) ? payload.length : 0 };

export const fetchEnrollmentFees = async (
  query?: EnrollmentFeeListQuery
): Promise<{ data: EnrollmentFee[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<EnrollmentFee> | EnrollmentFee[]>("/enrollment_fees/", {
      query
    })
  );

export const fetchEnrollmentFee = (id: number): Promise<EnrollmentFee> =>
  apiRequest<EnrollmentFee>(`/enrollment_fees/${id}/`);

export const createEnrollmentFee = (payload: EnrollmentFeePayload): Promise<EnrollmentFee> =>
  apiRequest<EnrollmentFee>("/enrollment_fees/", {
    method: "POST",
    json: payload
  });

export const updateEnrollmentFee = (id: number, payload: EnrollmentFeePayload): Promise<EnrollmentFee> =>
  apiRequest<EnrollmentFee>(`/enrollment_fees/${id}/`, {
    method: "PUT",
    json: payload
  });

export const deleteEnrollmentFee = (id: number): Promise<void> =>
  apiRequest<void>(`/enrollment_fees/${id}/`, {
    method: "DELETE"
  });

export const useEnrollmentFees = (query?: EnrollmentFeeListQuery) =>
  useQuery({
    queryKey: queryKeys.enrollmentFees(query),
    queryFn: () => fetchEnrollmentFees(query)
  });

export const useCreateEnrollmentFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createEnrollmentFee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: enrollmentFeesKey });
    }
  });
};

export const useUpdateEnrollmentFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: EnrollmentFeePayload }) =>
      updateEnrollmentFee(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: enrollmentFeesKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.enrollmentFee(variables.id) });
    }
  });
};

export const useDeleteEnrollmentFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteEnrollmentFee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: enrollmentFeesKey });
    }
  });
};

export const enrollmentFeeService = {
  fetchEnrollmentFees,
  fetchEnrollmentFee,
  createEnrollmentFee,
  updateEnrollmentFee,
  deleteEnrollmentFee,
  useEnrollmentFees,
  useCreateEnrollmentFee,
  useUpdateEnrollmentFee,
  useDeleteEnrollmentFee
};
