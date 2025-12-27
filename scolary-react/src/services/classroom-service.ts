import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import {
  Classroom,
  ClassroomListQuery,
  ClassroomPayload
} from "@/models/classroom";

const classroomKey = ["classrooms"] as const;

const queryKeys = {
  classrooms: (query?: ClassroomListQuery): QueryKey =>
    query ? [...classroomKey, query] : classroomKey,
  classroom: (id: number): QueryKey => ["classroom", id]
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

export const fetchClassrooms: any = async (
  query?: ClassroomListQuery
): Promise<{ data: Classroom[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<Classroom> | Classroom[]>("/classrooms/", {
      query
    })
  );

export const fetchClassroom = (id: number): Promise<Classroom> =>
  apiRequest<Classroom>(`/classrooms/${id}/`);

export const createClassroom = (
  payload: ClassroomPayload
): Promise<Classroom> =>
  apiRequest<Classroom>("/classrooms/", {
    method: "POST",
    json: payload
  });

export const updateClassroom = (
  id: number,
  payload: ClassroomPayload
): Promise<Classroom> =>
  apiRequest<Classroom>(`/classrooms/${id}/`, {
    method: "PUT",
    json: payload
  });

export const deleteClassroom = (id: number): Promise<void> =>
  apiRequest<void>(`/classrooms/${id}/`, {
    method: "DELETE"
  });

export const useClassrooms = (query?: ClassroomListQuery) =>
  useQuery({
    queryKey: queryKeys.classrooms(query),
    queryFn: () => fetchClassrooms(query)
  });

export const useClassroom = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.classroom(id),
    queryFn: () => fetchClassroom(id),
    enabled
  });

export const useCreateClassroom = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createClassroom,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: classroomKey });
    }
  });
};

export const useUpdateClassroom = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: ClassroomPayload }) =>
      updateClassroom(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: classroomKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.classroom(variables.id)
      });
    }
  });
};

export const useDeleteClassroom = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteClassroom,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: classroomKey });
    }
  });
};

export const classroomService = {
  fetchClassrooms,
  fetchClassroom,
  createClassroom,
  updateClassroom,
  deleteClassroom,
  useClassrooms,
  useClassroom,
  useCreateClassroom,
  useUpdateClassroom,
  useDeleteClassroom
};
