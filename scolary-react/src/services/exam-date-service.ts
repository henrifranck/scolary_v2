import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";
import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";
import { ExamDate, ExamDateListQuery } from "@/models/exam-date";

const examDateKey = ["exam-dates"] as const;

const queryKeys = {
  dates: (query?: ExamDateListQuery): QueryKey =>
    query ? [...examDateKey, query] : examDateKey
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

export const fetchExamDates = async (
  query?: ExamDateListQuery
): Promise<{ data: ExamDate[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<ExamDate> | ExamDate[]>("/exam_dates/", {
      query
    })
  );

export const createExamDate = (
  payload: Partial<ExamDate>
): Promise<ExamDate> =>
  apiRequest<ExamDate>("/exam_dates/", {
    method: "POST",
    json: payload
  });

export const updateExamDate = (
  id: number,
  payload: Partial<ExamDate>
): Promise<ExamDate> =>
  apiRequest<ExamDate>(`/exam_dates/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteExamDate = (id: number): Promise<void> =>
  apiRequest<void>(`/exam_dates/${id}`, {
    method: "DELETE"
  });

export const useExamDates = (query?: ExamDateListQuery) =>
  useQuery({
    queryKey: queryKeys.dates(query),
    queryFn: () => fetchExamDates(query)
  });

export const useCreateExamDate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createExamDate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examDateKey });
    }
  });
};

export const useUpdateExamDate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: Partial<ExamDate>;
    }) => updateExamDate(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examDateKey });
    }
  });
};

export const useDeleteExamDate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteExamDate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: examDateKey });
    }
  });
};

export const examDateService = {
  fetchExamDates,
  useExamDates,
  createExamDate,
  useCreateExamDate,
  updateExamDate,
  useUpdateExamDate,
  deleteExamDate,
  useDeleteExamDate
};
