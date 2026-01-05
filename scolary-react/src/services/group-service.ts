import { useQuery, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import { Group, GroupListQuery } from "@/models/group";

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

export const groupService = {
  fetchGroups,
  useGroups
};
