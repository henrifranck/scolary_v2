import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest } from './api-client';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface RequiredDocument {
  id: number;
  name: string;
}

export type RequiredDocumentPayload = Pick<RequiredDocument, 'name'>;
export type RequiredDocumentListQuery = Record<string, string | number | boolean | undefined>;

const requiredDocumentsKey = ['required-documents'] as const;

const queryKeys = {
  requiredDocuments: (query?: RequiredDocumentListQuery): QueryKey =>
    query ? [...requiredDocumentsKey, query] : requiredDocumentsKey,
  requiredDocument: (id: number): QueryKey => ['required-document', id]
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

export const fetchRequiredDocuments = async (
  query?: RequiredDocumentListQuery
): Promise<{ data: RequiredDocument[]; count?: number }> =>
  normalizeList(await apiRequest<ApiListResponse<RequiredDocument> | RequiredDocument[]>('/required_documents/', { query }));

export const fetchRequiredDocument = (id: number): Promise<RequiredDocument> =>
  apiRequest<RequiredDocument>(`/required_documents/${id}/`);

export const createRequiredDocument = (payload: RequiredDocumentPayload): Promise<RequiredDocument> =>
  apiRequest<RequiredDocument>('/required_documents/', {
    method: 'POST',
    json: payload
  });

export const updateRequiredDocument = (id: number, payload: RequiredDocumentPayload): Promise<RequiredDocument> =>
  apiRequest<RequiredDocument>(`/required_documents/${id}/`, {
    method: 'PUT',
    json: payload
  });

export const deleteRequiredDocument = (id: number): Promise<void> =>
  apiRequest<void>(`/required_documents/${id}/`, {
    method: 'DELETE'
  });

export const useRequiredDocuments = (query?: RequiredDocumentListQuery) =>
  useQuery({
    queryKey: queryKeys.requiredDocuments(query),
    queryFn: () => fetchRequiredDocuments(query)
  });

export const useRequiredDocument = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.requiredDocument(id),
    queryFn: () => fetchRequiredDocument(id),
    enabled
  });

export const useCreateRequiredDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createRequiredDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: requiredDocumentsKey });
    }
  });
};

export const useUpdateRequiredDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: RequiredDocumentPayload }) =>
      updateRequiredDocument(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: requiredDocumentsKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.requiredDocument(variables.id) });
    }
  });
};

export const useDeleteRequiredDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteRequiredDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: requiredDocumentsKey });
    }
  });
};

export const requiredDocumentService = {
  fetchRequiredDocuments,
  fetchRequiredDocument,
  createRequiredDocument,
  updateRequiredDocument,
  deleteRequiredDocument,
  useRequiredDocuments,
  useRequiredDocument,
  useCreateRequiredDocument,
  useUpdateRequiredDocument,
  useDeleteRequiredDocument
};
