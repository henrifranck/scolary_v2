import { useMutation, useQuery, useQueryClient, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  Group,
  GroupListQuery,
  CreateGroupPayload
} from "@/models/group";

const groupKey = ["groups"] as const;

const queryKeys = {
  groups: (query?: GroupListQuery): QueryKey =>
    query ? [...groupKey, query] : groupKey
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

export const fetchGroups = async (
  query?: GroupListQuery
): Promise<{ data: Group[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<Group> | Group[]>("/groups/", {
      query
    })
  );

export const useGroups = (query?: GroupListQuery) =>
  useQuery({
    queryKey: queryKeys.groups(query),
    queryFn: () => fetchGroups(query)
  });

export const createGroup = (payload: CreateGroupPayload): Promise<Group> =>
  apiRequest<Group>("/groups/", {
    method: "POST",
    json: payload
  });

export const updateGroup = (
  id: number,
  payload: Partial<CreateGroupPayload>
): Promise<Group> =>
  apiRequest<Group>(`/groups/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteGroup = (id: number): Promise<void> =>
  apiRequest<void>(`/groups/${id}`, {
    method: "DELETE"
  });

export const useCreateGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: groupKey });
    }
  });
};

export const useUpdateGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: Partial<CreateGroupPayload> }) =>
      updateGroup(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: groupKey });
    }
  });
};

export const useDeleteGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: groupKey });
    }
  });
};

export const groupService = {
  fetchGroups,
  useGroups,
  createGroup,
  useCreateGroup,
  updateGroup,
  useUpdateGroup,
  deleteGroup,
  useDeleteGroup
};
