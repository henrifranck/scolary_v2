import { apiRequest } from "./api-client";
import {
  ModelHasPermission,
  ModelHasPermissionPayload
} from "@/models/permission";

export const fetchModelHasPermissions = async (query?: Record<string, any>) =>
  apiRequest<{ data: ModelHasPermission[]; count?: number }>(
    "/model_has_permissions/",
    { query }
  );

export const createModelHasPermission = async (
  payload: ModelHasPermissionPayload
): Promise<ModelHasPermission> =>
  apiRequest<ModelHasPermission>("/model_has_permissions/", {
    method: "POST",
    json: payload
  });

export const updateModelHasPermission = async (
  id: number,
  payload: Partial<ModelHasPermissionPayload>
): Promise<ModelHasPermission> =>
  apiRequest<ModelHasPermission>(`/model_has_permissions/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteModelHasPermission = async (id: number): Promise<void> =>
  apiRequest<void>(`/model_has_permissions/${id}`, {
    method: "DELETE"
  });
