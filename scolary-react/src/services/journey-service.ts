import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { Journey, JourneyListQuery, JourneyPayload } from "@/models/journey";
import { ApiListResponse } from "@/models/shared";

const journeysKey = ["journey"] as const;

const queryKeys = {
  journeys: (query?: JourneyListQuery): QueryKey =>
    query ? [...journeysKey, query] : journeysKey,
  journey: (id: number): QueryKey => ["journey", id]
} as const;

const isListResponse = <T>(payload: unknown): payload is ApiListResponse<T> =>
  Boolean(
    payload &&
      typeof payload === "object" &&
      "data" in (payload as Record<string, unknown>) &&
      Array.isArray((payload as ApiListResponse<T>).data)
  );

const normalizePaginatedList = <T>(
  payload: ApiListResponse<T> | T[]
): { data: T[]; count?: number } =>
  isListResponse(payload)
    ? { data: payload.data, count: payload.count }
    : {
        data: Array.isArray(payload) ? payload : [],
        count: Array.isArray(payload) ? payload.length : 0
      };

const defaultRelation = JSON.stringify([
  "mention{name,abbreviation,id_plugged}",
  "semester_list{id,semester}"
]);

const withDefaultRelation = (query?: JourneyListQuery): JourneyListQuery => {
  const nextQuery: JourneyListQuery = { ...(query ?? {}) };
  if (!nextQuery.relation) {
    nextQuery.relation = defaultRelation;
  }
  return nextQuery;
};

export const fetchJourneys = async (
  query?: JourneyListQuery
): Promise<{ data: Journey[]; count?: number }> =>
  normalizePaginatedList(
    await apiRequest<ApiListResponse<Journey> | Journey[]>("/journey/", {
      query: withDefaultRelation(query)
    })
  );

export const fetchJourney = (id: number): Promise<Journey> =>
  apiRequest<Journey>("/journey/by_id/", {
    query: { id_journey: id, relation: defaultRelation }
  });

export const createJourney = (payload: JourneyPayload): Promise<Journey> =>
  apiRequest<Journey>("/journey/", {
    method: "POST",
    json: payload
  });

export const updateJourney = (
  id: number,
  payload: JourneyPayload
): Promise<Journey> =>
  apiRequest<Journey>(`/journey/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteJourney = (id: number): Promise<void> =>
  apiRequest<void>(`/journey/${id}`, {
    method: "DELETE"
  });

export const useJourneys = (query?: JourneyListQuery) =>
  useQuery({
    queryKey: queryKeys.journeys(query),
    queryFn: () => fetchJourneys(query)
  });

export const useJourney = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.journey(id),
    queryFn: () => fetchJourney(id),
    enabled
  });

export const useCreateJourney = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createJourney,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: journeysKey });
    }
  });
};

export const useUpdateJourney = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: JourneyPayload }) =>
      updateJourney(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: journeysKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.journey(variables.id)
      });
    }
  });
};

export const useDeleteJourney = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteJourney,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: journeysKey });
    }
  });
};

export const journeyService = {
  fetchJourneys,
  fetchJourney,
  createJourney,
  updateJourney,
  deleteJourney,
  useJourneys,
  useJourney,
  useCreateJourney,
  useUpdateJourney,
  useDeleteJourney
};
