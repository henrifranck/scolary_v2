import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  ConstituentElementOffering,
  ConstituentElementOfferingListQuery
} from "@/models/constituent-element-offering";

const offeringKey = ["constituent-element-offerings"] as const;

const queryKeys = {
  offerings: (query?: ConstituentElementOfferingListQuery): QueryKey =>
    query ? [...offeringKey, query] : offeringKey
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

export const fetchConstituentElementOfferings = async (
  query?: ConstituentElementOfferingListQuery
): Promise<{ data: ConstituentElementOffering[]; count?: number }> =>
  normalizeList(
    await apiRequest<
      ApiListResponse<ConstituentElementOffering> | ConstituentElementOffering[]
    >("/constituent_element_offerings/", {
      query
    })
  );

export const useConstituentElementOfferings = (
  query?: ConstituentElementOfferingListQuery
) =>
  useQuery({
    queryKey: queryKeys.offerings(query),
    queryFn: () => fetchConstituentElementOfferings(query),
    enabled: Boolean(query)
  });

export const createConstituentElementOffering = (
  payload: Partial<ConstituentElementOffering>
): Promise<ConstituentElementOffering> =>
  apiRequest<ConstituentElementOffering>("/constituent_element_offerings/", {
    method: "POST",
    json: payload
  });

export const updateConstituentElementOffering = (
  id: number,
  payload: Partial<ConstituentElementOffering>
): Promise<ConstituentElementOffering> =>
  apiRequest<ConstituentElementOffering>(
    `/constituent_element_offerings/${id}`,
    {
      method: "PUT",
      json: payload
    }
  );

export const deleteConstituentElementOffering = (id: number): Promise<void> =>
  apiRequest<void>(`/constituent_element_offerings/${id}`, {
    method: "DELETE"
  });

export const useCreateConstituentElementOffering = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createConstituentElementOffering,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: offeringKey });
    }
  });
};

export const useUpdateConstituentElementOffering = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: Partial<ConstituentElementOffering>;
    }) => updateConstituentElementOffering(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: offeringKey });
    }
  });
};

export const useDeleteConstituentElementOffering = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteConstituentElementOffering,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: offeringKey });
    }
  });
};

export const constituentElementOfferingService = {
  fetchConstituentElementOfferings,
  useConstituentElementOfferings,
  createConstituentElementOffering,
  updateConstituentElementOffering,
  deleteConstituentElementOffering,
  useCreateConstituentElementOffering,
  useUpdateConstituentElementOffering,
  useDeleteConstituentElementOffering
};
