import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey
} from "@tanstack/react-query";

import { apiRequest } from "./api-client";

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export type FileType = "image" | "video" | "audio" | "document" | "other";

export interface FileAsset {
  id: number;
  name: string;
  url: string;
  type: FileType;
  size_bytes?: number | null;
  mime_type?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export type FileAssetPayload = {
  name?: string;
  type?: FileType;
};

export type UploadFileInput = {
  file: File;
  payload?: FileAssetPayload;
};

export type FileListQuery = Record<
  string,
  string | number | boolean | undefined
>;

const filesKey = ["file-manager"] as const;

const queryKeys = {
  files: (query?: FileListQuery): QueryKey =>
    query ? [...filesKey, query] : filesKey,
  file: (id: number): QueryKey => ["file-manager", id]
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

export const fetchFiles = async (
  query?: FileListQuery
): Promise<{ data: FileAsset[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<FileAsset> | FileAsset[]>("/files/", {
      query
    })
  );

export const fetchFile = (id: number): Promise<FileAsset> =>
  apiRequest<FileAsset>(`/files/${id}/`);

export const uploadFile = ({ file, payload }: UploadFileInput): Promise<FileAsset> => {
  const formData = new FormData();
  formData.append("file", file);
  if (payload?.name) formData.append("name", payload.name);
  if (payload?.type) formData.append("type", payload.type);

  return apiRequest<FileAsset>("/files/upload/", {
    method: "POST",
    body: formData
  });
};

export const updateFileMetadata = (
  id: number,
  payload: FileAssetPayload
): Promise<FileAsset> =>
  apiRequest<FileAsset>(`/files/${id}/`, {
    method: "PATCH",
    json: payload
  });

export const deleteFile = (id: number): Promise<void> =>
  apiRequest<void>(`/files/${id}/`, {
    method: "DELETE"
  });

export const useFiles = (query?: FileListQuery) =>
  useQuery({
    queryKey: queryKeys.files(query),
    queryFn: () => fetchFiles(query)
  });

export const useFile = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.file(id),
    queryFn: () => fetchFile(id),
    enabled
  });

export const useUploadFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: uploadFile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: filesKey });
    }
  });
};

export const useUpdateFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload
    }: {
      id: number;
      payload: FileAssetPayload;
    }) => updateFileMetadata(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: filesKey });
      queryClient.invalidateQueries({
        queryKey: queryKeys.file(variables.id)
      });
    }
  });
};

export const useDeleteFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteFile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: filesKey });
    }
  });
};

export const fileManagerService = {
  fetchFiles,
  fetchFile,
  uploadFile,
  updateFileMetadata,
  deleteFile,
  useFiles,
  useFile,
  useUploadFile,
  useUpdateFile,
  useDeleteFile
};
