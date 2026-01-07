import { apiRequest } from "./api-client";
import { ApiListResponse } from "@/models/shared";

export type NotificationTemplate = {
  id: number;
  key: string;
  title: string;
  template: string;
};

export type NotificationTemplatePayload = {
  key: string;
  title: string;
  template: string;
};

export const fetchNotificationTemplates = (): Promise<NotificationTemplate[]> =>
  apiRequest<NotificationTemplate[]>("/notification_templates/", {
    method: "GET"
  });

export const createNotificationTemplate = (
  payload: NotificationTemplatePayload
): Promise<NotificationTemplate> =>
  apiRequest<NotificationTemplate>("/notification_templates/", {
    method: "POST",
    json: payload
  });

export const updateNotificationTemplate = (
  id: number,
  payload: NotificationTemplatePayload
): Promise<NotificationTemplate> =>
  apiRequest<NotificationTemplate>(`/notification_templates/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteNotificationTemplate = (id: number): Promise<void> =>
  apiRequest<void>(`/notification_templates/${id}`, {
    method: "DELETE"
  });
