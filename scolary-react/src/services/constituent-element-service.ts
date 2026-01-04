import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";
import { apiRequest } from "./api-client";
import {
  ConstituentElement,
  ConstituentElementListQuery
} from "@/models/constituent-element";
import { ApiListResponse } from "@/models/shared";

const constituentElementKey = ["constituent-element"] as const;

const queryKeys = {
  constituentElements: (query?: ConstituentElementListQuery): QueryKey =>
    query ? [...constituentElementKey, query] : constituentElementKey
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

export const fetchConstituentElements = async (
  query?: ConstituentElementListQuery
): Promise<{ data: ConstituentElement[]; count?: number }> =>
  normalizeList(
    await apiRequest<
      ApiListResponse<ConstituentElement> | ConstituentElement[]
    >("/constituent_elements/", { query })
  );

export const useConstituentElements = (query?: ConstituentElementListQuery) =>
  useQuery({
    queryKey: queryKeys.constituentElements(query),
    queryFn: () => fetchConstituentElements(query)
  });

export const createConstituentElement = (
  payload: Partial<ConstituentElement>
): Promise<ConstituentElement> =>
  apiRequest<ConstituentElement>("/constituent_elements/", {
    method: "POST",
    json: payload
  });

export const updateConstituentElement = (
  id: number,
  payload: Partial<ConstituentElement>
): Promise<ConstituentElement> =>
  apiRequest<ConstituentElement>(`/constituent_elements/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteConstituentElement = (id: number): Promise<void> =>
  apiRequest<void>(`/constituent_elements/${id}`, { method: "DELETE" });

export const useCreateConstituentElement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createConstituentElement,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: constituentElementKey });
    }
  });
};

export const useUpdateConstituentElement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: Partial<ConstituentElement>;
    }) => updateConstituentElement(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: constituentElementKey });
    }
  });
};

export const useDeleteConstituentElement = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteConstituentElement,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: constituentElementKey });
    }
  });
};

export const constituentElementService = {
  fetchConstituentElements,
  useConstituentElements,
  createConstituentElement,
  updateConstituentElement,
  deleteConstituentElement,
  useCreateConstituentElement,
  useUpdateConstituentElement,
  useDeleteConstituentElement
};
