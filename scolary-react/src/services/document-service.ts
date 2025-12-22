import { apiRequest } from "./api-client";

export type DocumentAsset = {
  id: number;
  id_annual_register?: number | null;
  name: string;
  description?: string | null;
  url: string;
};

export type DocumentPayload = {
  id_annual_register: number;
  name?: string;
  description?: string;
};

export type DocumentUpdatePayload = {
  name?: string;
  description?: string;
};

export type UploadDocumentInput = {
  file: File;
  payload: DocumentPayload;
};

export const uploadDocument = ({
  file,
  payload
}: UploadDocumentInput): Promise<DocumentAsset> => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("id_annual_register", String(payload.id_annual_register));
  if (payload.name) formData.append("name", payload.name);
  if (payload.description) formData.append("description", payload.description);

  return apiRequest<DocumentAsset>("/documents/upload/", {
    method: "POST",
    body: formData
  });
};

export const updateDocument = (
  id: number,
  payload: DocumentUpdatePayload
): Promise<DocumentAsset> =>
  apiRequest<DocumentAsset>(`/documents/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteDocument = (id: number): Promise<void> =>
  apiRequest<void>(`/documents/${id}`, {
    method: "DELETE"
  });

export const documentService = {
  uploadDocument,
  updateDocument,
  deleteDocument
};
