import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest } from './api-client';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface Permission {
  id: number;
  name: string;
  model_name: string;
  method_post?: boolean;
  method_get?: boolean;
  method_put?: boolean;
  method_delete?: boolean;
}

export type PermissionPayload = Pick<
  Permission,
  'name' | 'model_name' | 'method_post' | 'method_get' | 'method_put' | 'method_delete'
>;
export type PermissionListQuery = Record<string, string | number | boolean | undefined>;

const permissionsKey = ['permissions'] as const;

const queryKeys = {
  permissions: (query?: PermissionListQuery): QueryKey => (query ? [...permissionsKey, query] : permissionsKey),
  permission: (id: number): QueryKey => ['permission', id]
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

export const fetchPermissions = async (query?: PermissionListQuery): Promise<{ data: Permission[]; count?: number }> =>
  normalizeList(await apiRequest<ApiListResponse<Permission> | Permission[]>('/permissions/', { query }));

export const fetchPermission = (id: number): Promise<Permission> => apiRequest<Permission>(`/permissions/${id}/`);

export const createPermission = (payload: PermissionPayload): Promise<Permission> =>
  apiRequest<Permission>('/permissions/', {
    method: 'POST',
    json: payload
  });

export const updatePermission = (id: number, payload: PermissionPayload): Promise<Permission> =>
  apiRequest<Permission>(`/permissions/${id}/`, {
    method: 'PUT',
    json: payload
  });

export const deletePermission = (id: number): Promise<void> =>
  apiRequest<void>(`/permissions/${id}/`, {
    method: 'DELETE'
  });

export const usePermissions = (query?: PermissionListQuery) =>
  useQuery({
    queryKey: queryKeys.permissions(query),
    queryFn: () => fetchPermissions(query)
  });

export const usePermission = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.permission(id),
    queryFn: () => fetchPermission(id),
    enabled
  });

export const useCreatePermission = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPermission,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: permissionsKey });
    }
  });
};

export const useUpdatePermission = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: PermissionPayload }) => updatePermission(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: permissionsKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.permission(variables.id) });
    }
  });
};

export const useDeletePermission = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deletePermission,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: permissionsKey });
    }
  });
};

export const permissionService = {
  fetchPermissions,
  fetchPermission,
  createPermission,
  updatePermission,
  deletePermission,
  usePermissions,
  usePermission,
  useCreatePermission,
  useUpdatePermission,
  useDeletePermission
};
