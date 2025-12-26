import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import {
  Mention,
  MentionListQuery,
  MentionPayload,
  MentionUser
} from "@/models/mentions";
import { ApiListResponse } from "@/models/shared";

const mentionsKey = ["mentions"] as const;

const queryKeys = {
  mentions: (query?: MentionListQuery): QueryKey =>
    query ? [...mentionsKey, query] : mentionsKey,
  mention: (id: number): QueryKey => ["mention", id],
  mentionUsers: (userId: number): QueryKey => ["mention-users", userId]
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

// export const fetchMentions = async (
//   query?: MentionListQuery
// ): Promise<{ data: Mention[]; count?: number }> =>
//   normalizeList(
//     await apiRequest<ApiListResponse<Mention> | Mention[]>("/mentions/", {
//       query
//     })
//   );

export const fetchMentions: any = async (
  query?: Record<string, string | number | boolean | undefined>
) =>
  normalizeList(
    await apiRequest<ApiListResponse<Mention> | Mention[]>("/mentions/", {
      query
    })
  );

export const fetchMention = (id: number): Promise<Mention> =>
  apiRequest<Mention>("/mentions/by_id/", { query: { id_mention: id } });

export const createMention = (payload: MentionPayload): Promise<Mention> =>
  apiRequest<Mention>("/mentions/", {
    method: "POST",
    json: payload
  });

export const updateMention = (
  id: number,
  payload: MentionPayload
): Promise<Mention> =>
  apiRequest<Mention>(`/mentions/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteMention = (id: number): Promise<void> =>
  apiRequest<void>(`/mentions/${id}`, {
    method: "DELETE"
  });

export const fetchMentionUsers = async (
  userId: number
): Promise<MentionUser[] | any> =>
  normalizeList(
    await apiRequest<ApiListResponse<MentionUser> | MentionUser[]>(
      "/user_mention/by_user/",
      {
        query: { id_user: userId }
      }
    )
  );

export const useMentions = (query?: MentionListQuery) =>
  useQuery({
    queryKey: queryKeys.mentions(query),
    queryFn: () => fetchMentions(query)
  });

export const useMention = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.mention(id),
    queryFn: () => fetchMention(id),
    enabled
  });

export const useCreateMention = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createMention,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: mentionsKey });
    }
  });
};

export const useUpdateMention = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: MentionPayload }) =>
      updateMention(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: mentionsKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.mention(variables.id)
      });
    }
  });
};

export const useDeleteMention = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteMention,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: mentionsKey });
    }
  });
};

export const mentionService = {
  fetchMentions,
  fetchMention,
  fetchMentionUsers,
  createMention,
  updateMention,
  deleteMention,
  useMentions,
  useMention,
  useCreateMention,
  useUpdateMention,
  useDeleteMention
};
