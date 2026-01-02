import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import type { Grade } from "./teacher-service";
import { Role } from "@/models/role";
import { Mention } from "@/models/mentions";

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface UserRoleAssignment {
  id: number;
  role_id?: number | null;
  role?: Pick<Role, "id" | "name"> | null;
}

export interface UserMentionAssignment {
  id: number;
  id_mention?: number | null;
  mention?: Pick<Mention, "id" | "name"> | null;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  password?: string | null;
  is_superuser?: boolean;
  picture?: string | null;
  is_active?: boolean;
  address?: string | null;
  phone_number?: string | null;
  teacher?: {
    id?: number | null;
    id_user?: number | null;
    grade?: Grade | null;
    max_hours_per_day?: number | null;
    max_days_per_week?: number | null;
  } | null;
  permissions?: Record<
    string,
    { get: boolean; post: boolean; put: boolean; delete: boolean }
  > | null;
  role_id?: number | null;
  role?: Role | null;
  role_ids?: number[] | null;
  roles?: Role[] | null;
  user_role?: UserRoleAssignment[] | null;
  mention_ids?: number[] | null;
  mentions?: Mention[] | null;
  user_mention?: UserMentionAssignment[] | null;
}

export type UserPayload = Pick<
  User,
  | "email"
  | "first_name"
  | "last_name"
  | "is_superuser"
  | "is_active"
  | "picture"
  | "address"
  | "phone_number"
> & {
  password?: string;
  role_ids: number[];
  mention_ids: number[];
};

export type UserListQuery = Record<
  string,
  string | number | boolean | undefined
>;

const usersKey = ["users"] as const;

const queryKeys = {
  users: (query?: UserListQuery): QueryKey =>
    query ? [...usersKey, query] : usersKey,
  user: (id: number, query?: UserListQuery): QueryKey =>
    query ? ["user", id, query] : ["user", id]
} as const;

const defaultRelation = JSON.stringify([
  "user_role.role",
  "user_mention.mention",
  "teacher{grade,max_hours_per_day,max_days_per_week}"
]);

const withDefaultRelation = (query?: UserListQuery): UserListQuery => {
  const nextQuery: UserListQuery = { ...(query ?? {}) };
  if (!nextQuery.relation) {
    nextQuery.relation = defaultRelation;
  }
  return nextQuery;
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

export const fetchUsers = async (
  query?: UserListQuery
): Promise<{ data: User[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<User> | User[]>("/users/", {
      query: withDefaultRelation(query)
    })
  );

export const fetchUser = (id: number, query?: UserListQuery): Promise<User> =>
  apiRequest<User>(`/users/${id}/`, { query: withDefaultRelation(query) });

export const fetchCurrentUser = (): Promise<User> =>
  apiRequest<User>("/users/me");

export const createUser = (payload: UserPayload): Promise<User> =>
  apiRequest<User>("/users/", {
    method: "POST",
    json: payload
  });

export const updateUser = (id: number, payload: UserPayload): Promise<User> =>
  apiRequest<User>(`/users/${id}/`, {
    method: "PUT",
    json: payload
  });

export const deleteUser = (id: number): Promise<void> =>
  apiRequest<void>(`/users/${id}/`, {
    method: "DELETE"
  });

export const uploadUserPicture = (id: number, file: File): Promise<void> => {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<void>(`/users/${id}/picture`, {
    method: "POST",
    body: formData
  });
};

export const useUsers = (query?: UserListQuery) =>
  useQuery({
    queryKey: queryKeys.users(query),
    queryFn: () => fetchUsers(query)
  });

export const useUser = (id: number, enabled = true, query?: UserListQuery) =>
  useQuery({
    queryKey: queryKeys.user(id, query),
    queryFn: () => fetchUser(id, query),
    enabled
  });

export const useCurrentUser = (enabled = true) =>
  useQuery({
    queryKey: ["users", "me"],
    queryFn: () => fetchCurrentUser(),
    enabled
  });

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: usersKey });
    }
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: UserPayload }) =>
      updateUser(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: usersKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.user(variables.id) });
    }
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: usersKey });
    }
  });
};

export const userService = {
  fetchUsers,
  fetchUser,
  fetchCurrentUser,
  createUser,
  updateUser,
  deleteUser,
  uploadUserPicture,
  useUsers,
  useUser,
  useCurrentUser,
  useCreateUser,
  useUpdateUser,
  useDeleteUser
};
