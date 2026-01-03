import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import {
  Plugged,
  PluggedListQuery,
  PluggedPayload
} from "@/models/plugged";
import { ApiListResponse } from "@/models/shared";

const pluggedKey = ["plugged"] as const;

const queryKeys = {
  plugged: (query?: PluggedListQuery): QueryKey =>
    query ? [...pluggedKey, query] : pluggedKey,
  pluggedById: (id: number): QueryKey => ["plugged", id]
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

export const fetchPluggeds = async (
  query?: PluggedListQuery
): Promise<{ data: Plugged[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<Plugged> | Plugged[]>("/plugged/", {
      query
    })
  );

export const fetchPlugged = (id: number): Promise<Plugged> =>
  apiRequest<Plugged>(`/plugged/${id}`, { method: "GET" });

export const createPlugged = (payload: PluggedPayload): Promise<Plugged> =>
  apiRequest<Plugged>("/plugged/", { method: "POST", json: payload });

export const updatePlugged = (
  id: number,
  payload: PluggedPayload
): Promise<Plugged> =>
  apiRequest<Plugged>(`/plugged/${id}`, { method: "PUT", json: payload });

export const deletePlugged = (id: number): Promise<void> =>
  apiRequest<void>(`/plugged/${id}`, { method: "DELETE" });

export const usePluggeds = (query?: PluggedListQuery) =>
  useQuery({
    queryKey: queryKeys.plugged(query),
    queryFn: () => fetchPluggeds(query)
  });

export const useCreatePlugged = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createPlugged,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: pluggedKey });
    }
  });
};

export const useUpdatePlugged = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: PluggedPayload }) =>
      updatePlugged(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: pluggedKey });
    }
  });
};

export const useDeletePlugged = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deletePlugged,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: pluggedKey });
    }
  });
};

export const pluggedService = {
  fetchPluggeds,
  fetchPlugged,
  createPlugged,
  updatePlugged,
  deletePlugged,
  usePluggeds,
  useCreatePlugged,
  useUpdatePlugged,
  useDeletePlugged
};
