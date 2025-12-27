import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  Nationality,
  NationalityListQuery,
  NationalityPayload
} from "@/models/nationality";

const nationalityKey = ["nationalitys"] as const;

const queryKeys = {
  nationalitys: (query?: NationalityListQuery): QueryKey =>
    query ? [...nationalityKey, query] : nationalityKey,
  nationality: (id: number): QueryKey => ["nationality", id]
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

export const fetchNationalitys: any = async (
  query?: NationalityListQuery
): Promise<{ data: Nationality[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<Nationality> | Nationality[]>(
      "/nationalitys/",
      { query }
    )
  );

export const fetchNationality = (id: number): Promise<Nationality> =>
  apiRequest<Nationality>(`/nationalitys/${id}/`);

export const createNationality = (
  payload: NationalityPayload
): Promise<Nationality> =>
  apiRequest<Nationality>("/nationalitys/", {
    method: "POST",
    json: payload
  });

export const updateNationality = (
  id: number,
  payload: NationalityPayload
): Promise<Nationality> =>
  apiRequest<Nationality>(`/nationalitys/${id}/`, {
    method: "PUT",
    json: payload
  });

export const deleteNationality = (id: number): Promise<void> =>
  apiRequest<void>(`/nationalitys/${id}/`, {
    method: "DELETE"
  });

export const useNationalitys = (query?: NationalityListQuery) =>
  useQuery({
    queryKey: queryKeys.nationalitys(query),
    queryFn: () => fetchNationalitys(query)
  });

export const useNationality = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.nationality(id),
    queryFn: () => fetchNationality(id),
    enabled
  });

export const useCreateNationality = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createNationality,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nationalityKey });
    }
  });
};

export const useUpdateNationality = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: NationalityPayload;
    }) => updateNationality(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: nationalityKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.nationality(variables.id)
      });
    }
  });
};

export const useDeleteNationality = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteNationality,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nationalityKey });
    }
  });
};

export const nationalityService = {
  fetchNationalitys,
  fetchNationality,
  createNationality,
  updateNationality,
  deleteNationality,
  useNationalitys,
  useNationality,
  useCreateNationality,
  useUpdateNationality,
  useDeleteNationality
};
