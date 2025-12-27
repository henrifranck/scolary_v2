import { ApiListResponse } from "@/models/shared";

export const isListResponse = <T>(
  payload: unknown
): payload is ApiListResponse<T> =>
  Boolean(
    payload &&
      typeof payload === "object" &&
      "data" in (payload as Record<string, unknown>) &&
      Array.isArray((payload as ApiListResponse<T>).data)
  );

export const normalizeList = <T>(payload: ApiListResponse<T> | T[]): T[] => {
  if (isListResponse<T>(payload)) {
    return payload.data;
  }

  return payload as T[];
};
