import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest } from './api-client';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface AvailableService {
  id: number;
  name: string;
  route_ui?: string | null;
}

export type AvailableServicePayload = Pick<AvailableService, 'name' | 'route_ui'>;
export type AvailableServiceListQuery = Record<string, string | number | boolean | undefined>;

const availableServicesKey = ['available-services'] as const;

const queryKeys = {
  availableServices: (query?: AvailableServiceListQuery): QueryKey =>
    query ? [...availableServicesKey, query] : availableServicesKey,
  availableService: (id: number): QueryKey => ['available-service', id]
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

export const fetchAvailableServices = async (
  query?: AvailableServiceListQuery
): Promise<{ data: AvailableService[]; count?: number }> =>
  normalizeList(await apiRequest<ApiListResponse<AvailableService> | AvailableService[]>('/available_services/', { query }));

export const fetchAvailableService = (id: number): Promise<AvailableService> =>
  apiRequest<AvailableService>(`/available_services/${id}/`);

export const createAvailableService = (payload: AvailableServicePayload): Promise<AvailableService> =>
  apiRequest<AvailableService>('/available_services/', {
    method: 'POST',
    json: payload
  });

export const updateAvailableService = (id: number, payload: AvailableServicePayload): Promise<AvailableService> =>
  apiRequest<AvailableService>(`/available_services/${id}/`, {
    method: 'PUT',
    json: payload
  });

export const deleteAvailableService = (id: number): Promise<void> =>
  apiRequest<void>(`/available_services/${id}/`, {
    method: 'DELETE'
  });

export const useAvailableServices = (query?: AvailableServiceListQuery) =>
  useQuery({
    queryKey: queryKeys.availableServices(query),
    queryFn: () => fetchAvailableServices(query)
  });

export const useAvailableService = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.availableService(id),
    queryFn: () => fetchAvailableService(id),
    enabled
  });

export const useCreateAvailableService = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAvailableService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: availableServicesKey });
    }
  });
};

export const useUpdateAvailableService = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: AvailableServicePayload }) =>
      updateAvailableService(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: availableServicesKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.availableService(variables.id) });
    }
  });
};

export const useDeleteAvailableService = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAvailableService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: availableServicesKey });
    }
  });
};

export const availableServiceService = {
  fetchAvailableServices,
  fetchAvailableService,
  createAvailableService,
  updateAvailableService,
  deleteAvailableService,
  useAvailableServices,
  useAvailableService,
  useCreateAvailableService,
  useUpdateAvailableService,
  useDeleteAvailableService
};
