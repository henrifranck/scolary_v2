import { useMutation, useQuery, useQueryClient, type QueryKey } from '@tanstack/react-query';

import { apiRequest, apiRequestBlob } from './api-client';
import type { Mention } from './mention-service';
import type { Journey } from './journey-service';

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export interface Card {
  id: number;
  name: string;
  description?: string | null;
  card_type: string;
  html_template: string;
  css_styles: string;
  id_mention?: number | null;
  id_journey?: number | null;
  mention?: Mention | null;
  journey?: Journey | null;
}

export type CardPayload = Pick<Card, 'name' | 'description' | 'card_type' | 'html_template' | 'css_styles'> & {
  id_mention?: number | null;
  id_journey?: number | null;
};

export type RenderCardPdfPayload = {
  html_template: string;
  css_styles: string;
  data: Record<string, unknown>;
  page_size?: string;
  copies?: number;
};

export type CardListQuery = Record<string, string | number | boolean | undefined>;

const cardsKey = ['cards'] as const;

const queryKeys = {
  cards: (query?: CardListQuery): QueryKey => (query ? [...cardsKey, query] : cardsKey),
  card: (id: number): QueryKey => ['card', id]
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

const defaultRelation = JSON.stringify(['mention', 'journey']);

const withDefaultRelation = (query?: CardListQuery): CardListQuery => {
  const nextQuery: CardListQuery = { ...(query ?? {}) };
  if (!nextQuery.relation) {
    nextQuery.relation = defaultRelation;
  }
  return nextQuery;
};

export const fetchCards = async (query?: CardListQuery): Promise<{ data: Card[]; count?: number }> =>
  normalizeList(await apiRequest<ApiListResponse<Card> | Card[]>('/cards/', { query: withDefaultRelation(query) }));

export const fetchCard = (id: number): Promise<Card> =>
  apiRequest<Card>(`/cards/${id}/`, { query: { relation: defaultRelation } });

export const createCard = (payload: CardPayload): Promise<Card> =>
  apiRequest<Card>('/cards/', {
    method: 'POST',
    json: payload
  });

export const updateCard = (id: number, payload: CardPayload): Promise<Card> =>
  apiRequest<Card>(`/cards/${id}/`, {
    method: 'PUT',
    json: payload
  });

export const deleteCard = (id: number): Promise<void> =>
  apiRequest<void>(`/cards/${id}/`, {
    method: 'DELETE'
  });

export const renderCardPdf = (payload: RenderCardPdfPayload): Promise<Blob> =>
  apiRequestBlob('/cards/render-pdf/', {
    method: 'POST',
    json: payload
  });

export const uploadCardImage = (file: File): Promise<{ filename?: string; path: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  return apiRequest('/cards/upload-image', {
    method: 'POST',
    body: formData
  });
};

export const useCards = (query?: CardListQuery) =>
  useQuery({
    queryKey: queryKeys.cards(query),
    queryFn: () => fetchCards(query)
  });

export const useCard = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.card(id),
    queryFn: () => fetchCard(id),
    enabled
  });

export const useCreateCard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createCard,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cardsKey });
    }
  });
};

export const useUpdateCard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: CardPayload }) => updateCard(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: cardsKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.card(variables.id) });
    }
  });
};

export const useRenderCardPdf = () =>
  useMutation({
    mutationFn: renderCardPdf
  });

export const useUploadCardImage = () =>
  useMutation({
    mutationFn: uploadCardImage
  });

export const useDeleteCard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteCard,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cardsKey });
    }
  });
};

export const cardService = {
  fetchCards,
  fetchCard,
  createCard,
  updateCard,
  deleteCard,
  renderCardPdf,
  uploadCardImage,
  useCards,
  useCard,
  useCreateCard,
  useUpdateCard,
  useDeleteCard,
  useRenderCardPdf,
  useUploadCardImage
};
