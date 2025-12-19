import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest } from './api-client';
import type { Permission } from './permission-service';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface RolePermissionAssignment {
  id: number;
  id_permission?: number | null;
  permission?: Pick<Permission, 'id' | 'name'> | null;
}

export interface Role {
  id: number;
  name: string;
  permission_ids?: number[] | null;
  permissions?: Permission[] | null;
  role_permission?: RolePermissionAssignment[] | null;
}

export type RolePayload = Pick<Role, 'name'> & {
  permission_ids: number[];
};
export type RoleListQuery = Record<string, string | number | boolean | undefined>;

const rolesKey = ['roles'] as const;

const queryKeys = {
  roles: (query?: RoleListQuery): QueryKey => (query ? [...rolesKey, query] : rolesKey),
  role: (id: number): QueryKey => ['role', id]
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

const defaultRelation = JSON.stringify(['role_permission.permission']);

const withDefaultRelation = (query?: RoleListQuery): RoleListQuery => {
  const nextQuery: RoleListQuery = { ...(query ?? {}) };
  if (!nextQuery.relation) {
    nextQuery.relation = defaultRelation;
  }
  return nextQuery;
};

export const fetchRoles = async (query?: RoleListQuery): Promise<{ data: Role[]; count?: number }> =>
  normalizeList(await apiRequest<ApiListResponse<Role> | Role[]>('/roles/', { query: withDefaultRelation(query) }));

export const fetchRole = (id: number): Promise<Role> => apiRequest<Role>(`/roles/${id}/`, { query: withDefaultRelation() });

export const createRole = (payload: RolePayload): Promise<Role> =>
  apiRequest<Role>('/roles/', {
    method: 'POST',
    json: payload
  });

export const updateRole = (id: number, payload: RolePayload): Promise<Role> =>
  apiRequest<Role>(`/roles/${id}/`, {
    method: 'PUT',
    json: payload
  });

export const deleteRole = (id: number): Promise<void> =>
  apiRequest<void>(`/roles/${id}/`, {
    method: 'DELETE'
  });

export const useRoles = (query?: RoleListQuery) =>
  useQuery({
    queryKey: queryKeys.roles(query),
    queryFn: () => fetchRoles(query)
  });

export const useRole = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.role(id),
    queryFn: () => fetchRole(id),
    enabled
  });

export const useCreateRole = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createRole,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: rolesKey });
    }
  });
};

export const useUpdateRole = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: RolePayload }) => updateRole(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: rolesKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.role(variables.id) });
    }
  });
};

export const useDeleteRole = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteRole,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: rolesKey });
    }
  });
};

export const roleService = {
  fetchRoles,
  fetchRole,
  createRole,
  updateRole,
  deleteRole,
  useRoles,
  useRole,
  useCreateRole,
  useUpdateRole,
  useDeleteRole
};
