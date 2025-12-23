import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest } from './api-client';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface AvailableServiceRequiredDocument {
  id: number;
  id_available_service: number;
  id_required_document: number;
  required_document?: { id: number; name: string };
}

export type AvailableServiceRequiredDocumentPayload = Pick<
  AvailableServiceRequiredDocument,
  'id_available_service' | 'id_required_document'
>;

export type AvailableServiceRequiredDocumentListQuery = Record<string, string | number | boolean | undefined>;

const serviceRequiredDocsKey = ['available-service-required-documents'] as const;

const queryKeys = {
  serviceRequiredDocs: (query?: AvailableServiceRequiredDocumentListQuery): QueryKey =>
    query ? [...serviceRequiredDocsKey, query] : serviceRequiredDocsKey,
  serviceRequiredDoc: (id: number): QueryKey => ['available-service-required-document', id]
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

export const fetchAvailableServiceRequiredDocuments = async (
  query?: AvailableServiceRequiredDocumentListQuery
): Promise<{ data: AvailableServiceRequiredDocument[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<AvailableServiceRequiredDocument> | AvailableServiceRequiredDocument[]>(
      '/available_service_required_documents/',
      { query }
    )
  );

export const createAvailableServiceRequiredDocument = (
  payload: AvailableServiceRequiredDocumentPayload
): Promise<AvailableServiceRequiredDocument> =>
  apiRequest('/available_service_required_documents/', {
    method: 'POST',
    json: payload
  });

export const deleteAvailableServiceRequiredDocument = (id: number): Promise<void> =>
  apiRequest(`/available_service_required_documents/${id}/`, {
    method: 'DELETE'
  });

export const useAvailableServiceRequiredDocuments = (
  query?: AvailableServiceRequiredDocumentListQuery,
  enabled = true
) =>
  useQuery({
    queryKey: queryKeys.serviceRequiredDocs(query),
    queryFn: () => fetchAvailableServiceRequiredDocuments(query),
    enabled
  });

export const useCreateAvailableServiceRequiredDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAvailableServiceRequiredDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: serviceRequiredDocsKey });
    }
  });
};

export const useDeleteAvailableServiceRequiredDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAvailableServiceRequiredDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: serviceRequiredDocsKey });
    }
  });
};

export const availableServiceRequiredDocumentService = {
  fetchAvailableServiceRequiredDocuments,
  createAvailableServiceRequiredDocument,
  deleteAvailableServiceRequiredDocument,
  useAvailableServiceRequiredDocuments,
  useCreateAvailableServiceRequiredDocument,
  useDeleteAvailableServiceRequiredDocument
};
