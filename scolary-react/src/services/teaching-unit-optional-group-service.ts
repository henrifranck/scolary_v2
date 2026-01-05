import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";
import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  TeachingUnitOptionalGroup,
  TeachingUnitOptionalGroupListQuery
} from "@/models/teaching-unit-optional-group";

const tuOptionalGroupKey = ["tu-optional-groups"] as const;

const queryKeys = {
  groups: (query?: TeachingUnitOptionalGroupListQuery): QueryKey =>
    query ? [...tuOptionalGroupKey, query] : tuOptionalGroupKey
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

export const fetchTeachingUnitOptionalGroups = async (
  query?: TeachingUnitOptionalGroupListQuery
): Promise<{ data: TeachingUnitOptionalGroup[]; count?: number }> =>
  normalizeList(
    await apiRequest<
      | ApiListResponse<TeachingUnitOptionalGroup>
      | TeachingUnitOptionalGroup[]
    >("/teaching_unit_optional_groups/", { query })
  );

export const useTeachingUnitOptionalGroups = (
  query?: TeachingUnitOptionalGroupListQuery
) =>
  useQuery({
    queryKey: queryKeys.groups(query),
    queryFn: () => fetchTeachingUnitOptionalGroups(query)
  });

export const createTeachingUnitOptionalGroup = (
  payload: Partial<TeachingUnitOptionalGroup>
): Promise<TeachingUnitOptionalGroup> =>
  apiRequest<TeachingUnitOptionalGroup>("/teaching_unit_optional_groups/", {
    method: "POST",
    json: payload
  });

export const useCreateTeachingUnitOptionalGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createTeachingUnitOptionalGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: tuOptionalGroupKey });
    }
  });
};

export const updateTeachingUnitOptionalGroup = (
  id: number,
  payload: Partial<TeachingUnitOptionalGroup>
): Promise<TeachingUnitOptionalGroup> =>
  apiRequest<TeachingUnitOptionalGroup>(
    `/teaching_unit_optional_groups/${id}`,
    {
      method: "PUT",
      json: payload
    }
  );

export const deleteTeachingUnitOptionalGroup = (id: number): Promise<void> =>
  apiRequest<void>(`/teaching_unit_optional_groups/${id}`, {
    method: "DELETE"
  });

export const useUpdateTeachingUnitOptionalGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: Partial<TeachingUnitOptionalGroup>;
    }) => updateTeachingUnitOptionalGroup(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: tuOptionalGroupKey });
    }
  });
};

export const useDeleteTeachingUnitOptionalGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteTeachingUnitOptionalGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: tuOptionalGroupKey });
    }
  });
};

export const teachingUnitOptionalGroupService = {
  fetchTeachingUnitOptionalGroups,
  useTeachingUnitOptionalGroups,
  createTeachingUnitOptionalGroup,
  useCreateTeachingUnitOptionalGroup,
  updateTeachingUnitOptionalGroup,
  deleteTeachingUnitOptionalGroup,
  useUpdateTeachingUnitOptionalGroup,
  useDeleteTeachingUnitOptionalGroup
};
