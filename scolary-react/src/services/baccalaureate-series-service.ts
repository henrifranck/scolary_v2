import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import {
  BaccalaureateSerie,
  BaccalaureateSerieListQuery,
  BaccalaureateSeriePayload
} from "@/models/baccalaureate-series";
import { ApiListResponse } from "@/models/shared";

const baccalaureateSerieKey = ["baccalaureateSeries"] as const;

const queryKeys = {
  baccalaureateSeries: (query?: BaccalaureateSerieListQuery): QueryKey =>
    query ? [...baccalaureateSerieKey, query] : baccalaureateSerieKey,
  baccalaureateSerie: (id: number): QueryKey => ["baccalaureateSerie", id]
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

export const fetchBaccalaureateSeries: any = async (
  query?: BaccalaureateSerieListQuery
): Promise<{ data: BaccalaureateSerie[]; count?: number }> =>
  normalizeList(
    await apiRequest<
      ApiListResponse<BaccalaureateSerie> | BaccalaureateSerie[]
    >("/baccalaureate_series/", { query })
  );

export const fetchBaccalaureateSerie = (
  id: number
): Promise<BaccalaureateSerie> =>
  apiRequest<BaccalaureateSerie>(`/baccalaureate_series/${id}/`);

export const createBaccalaureateSerie = (
  payload: BaccalaureateSeriePayload
): Promise<BaccalaureateSerie> =>
  apiRequest<BaccalaureateSerie>("/baccalaureate_series/", {
    method: "POST",
    json: payload
  });

export const updateBaccalaureateSerie = (
  id: number,
  payload: BaccalaureateSeriePayload
): Promise<BaccalaureateSerie> =>
  apiRequest<BaccalaureateSerie>(`/baccalaureate_series/${id}/`, {
    method: "PUT",
    json: payload
  });

export const deleteBaccalaureateSerie = (id: number): Promise<void> =>
  apiRequest<void>(`/baccalaureate_series/${id}/`, {
    method: "DELETE"
  });

export const useBaccalaureateSeries = (query?: BaccalaureateSerieListQuery) =>
  useQuery({
    queryKey: queryKeys.baccalaureateSeries(query),
    queryFn: () => fetchBaccalaureateSeries(query)
  });

export const useBaccalaureateSerie = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.baccalaureateSerie(id),
    queryFn: () => fetchBaccalaureateSerie(id),
    enabled
  });

export const useCreateBaccalaureateSerie = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createBaccalaureateSerie,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: baccalaureateSerieKey });
    }
  });
};

export const useUpdateBaccalaureateSerie = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: BaccalaureateSeriePayload;
    }) => updateBaccalaureateSerie(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: baccalaureateSerieKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.baccalaureateSerie(variables.id)
      });
    }
  });
};

export const useDeleteBaccalaureateSerie = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteBaccalaureateSerie,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: baccalaureateSerieKey });
    }
  });
};

export const baccalaureateSerieService = {
  fetchBaccalaureateSeries,
  fetchBaccalaureateSerie,
  createBaccalaureateSerie,
  updateBaccalaureateSerie,
  deleteBaccalaureateSerie,
  useBaccalaureateSeries,
  useBaccalaureateSerie,
  useCreateBaccalaureateSerie,
  useUpdateBaccalaureateSerie,
  useDeleteBaccalaureateSerie
};
