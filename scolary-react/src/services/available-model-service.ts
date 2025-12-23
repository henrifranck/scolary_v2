import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest } from './api-client';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface AvailableModel {
  id: number;
  name: string;
}

export type AvailableModelPayload = Pick<AvailableModel, 'name'>;
export type AvailableModelListQuery = Record<string, string | number | boolean | undefined>;

const availableModelsKey = ['available-models'] as const;

const queryKeys = {
  availableModels: (query?: AvailableModelListQuery): QueryKey =>
    query ? [...availableModelsKey, query] : availableModelsKey,
  availableModel: (id: number): QueryKey => ['available-model', id]
} as const;

const isListResponse = <T>(payload: unknown): payload is ApiListResponse<T> =>
  Boolean(
    payload &&
      typeof payload === 'object' &&
      'data' in (payload as Record<string, unknown>) &&
      Array.isArray((payload as ApiListResponse<T>).data)
  );

const normalizeList = <T>(payload: ApiListResponse<T> | T[]): { data: T[]; count?: number } =>
  isListResponse(payload)
    ? { data: payload.data, count: payload.count }
    : { data: Array.isArray(payload) ? payload : [], count: Array.isArray(payload) ? payload.length : 0 };

export const fetchAvailableModels = async (
  query?: AvailableModelListQuery
): Promise<{ data: AvailableModel[]; count?: number }> =>
  normalizeList(await apiRequest<ApiListResponse<AvailableModel> | AvailableModel[]>('/available_models/', { query }));

export const fetchAvailableModel = (id: number): Promise<AvailableModel> =>
  apiRequest<AvailableModel>(`/available_models/${id}/`);

export const createAvailableModel = (payload: AvailableModelPayload): Promise<AvailableModel> =>
  apiRequest<AvailableModel>('/available_models/', {
    method: 'POST',
    json: payload
  });

export const updateAvailableModel = (id: number, payload: AvailableModelPayload): Promise<AvailableModel> =>
  apiRequest<AvailableModel>(`/available_models/${id}/`, {
    method: 'PUT',
    json: payload
  });

export const deleteAvailableModel = (id: number): Promise<void> =>
  apiRequest<void>(`/available_models/${id}/`, {
    method: 'DELETE'
  });

export const useAvailableModels = (query?: AvailableModelListQuery) =>
  useQuery({
    queryKey: queryKeys.availableModels(query),
    queryFn: () => fetchAvailableModels(query)
  });

export const useAvailableModel = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.availableModel(id),
    queryFn: () => fetchAvailableModel(id),
    enabled
  });

export const useCreateAvailableModel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAvailableModel,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: availableModelsKey });
    }
  });
};

export const useUpdateAvailableModel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: AvailableModelPayload }) =>
      updateAvailableModel(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: availableModelsKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.availableModel(variables.id) });
    }
  });
};

export const useDeleteAvailableModel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAvailableModel,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: availableModelsKey });
    }
  });
};

export const availableModelService = {
  fetchAvailableModels,
  fetchAvailableModel,
  createAvailableModel,
  updateAvailableModel,
  deleteAvailableModel,
  useAvailableModels,
  useAvailableModel,
  useCreateAvailableModel,
  useUpdateAvailableModel,
  useDeleteAvailableModel
};
