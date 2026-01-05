import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";
import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  ConstituentElementOptionalGroup,
  ConstituentElementOptionalGroupListQuery
} from "@/models/constituent-element-optional-group";

const ceOptionalGroupKey = ["ce-optional-groups"] as const;

const queryKeys = {
  groups: (query?: ConstituentElementOptionalGroupListQuery): QueryKey =>
    query ? [...ceOptionalGroupKey, query] : ceOptionalGroupKey
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

export const fetchConstituentElementOptionalGroups = async (
  query?: ConstituentElementOptionalGroupListQuery
): Promise<{ data: ConstituentElementOptionalGroup[]; count?: number }> =>
  normalizeList(
    await apiRequest<
      | ApiListResponse<ConstituentElementOptionalGroup>
      | ConstituentElementOptionalGroup[]
    >("/constituent_element_optional_groups/", { query })
  );

export const useConstituentElementOptionalGroups = (
  query?: ConstituentElementOptionalGroupListQuery
) =>
  useQuery({
    queryKey: queryKeys.groups(query),
    queryFn: () => fetchConstituentElementOptionalGroups(query)
  });

export const createConstituentElementOptionalGroup = (
  payload: Partial<ConstituentElementOptionalGroup>
): Promise<ConstituentElementOptionalGroup> =>
  apiRequest<ConstituentElementOptionalGroup>(
    "/constituent_element_optional_groups/",
    {
      method: "POST",
      json: payload
    }
  );

export const useCreateConstituentElementOptionalGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createConstituentElementOptionalGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ceOptionalGroupKey });
    }
  });
};

export const updateConstituentElementOptionalGroup = (
  id: number,
  payload: Partial<ConstituentElementOptionalGroup>
): Promise<ConstituentElementOptionalGroup> =>
  apiRequest<ConstituentElementOptionalGroup>(
    `/constituent_element_optional_groups/${id}`,
    {
      method: "PUT",
      json: payload
    }
  );

export const deleteConstituentElementOptionalGroup = (
  id: number
): Promise<void> =>
  apiRequest<void>(`/constituent_element_optional_groups/${id}`, {
    method: "DELETE"
  });

export const useUpdateConstituentElementOptionalGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: Partial<ConstituentElementOptionalGroup>;
    }) => updateConstituentElementOptionalGroup(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ceOptionalGroupKey });
    }
  });
};

export const useDeleteConstituentElementOptionalGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteConstituentElementOptionalGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ceOptionalGroupKey });
    }
  });
};

export const constituentElementOptionalGroupService = {
  fetchConstituentElementOptionalGroups,
  useConstituentElementOptionalGroups,
  createConstituentElementOptionalGroup,
  useCreateConstituentElementOptionalGroup,
  updateConstituentElementOptionalGroup,
  deleteConstituentElementOptionalGroup,
  useUpdateConstituentElementOptionalGroup,
  useDeleteConstituentElementOptionalGroup
};
