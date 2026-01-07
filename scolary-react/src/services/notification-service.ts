import { apiRequest } from "./api-client";

export type NotificationRecord = {
  _id: string;
  type?: string;
  message?: string;
  full_name?: string;
  created_at?: number;
  read?: boolean;
  [key: string]: any;
};

export const fetchNotifications = async (limit = 50): Promise<{ data: NotificationRecord[] }> =>
  apiRequest<{ data: NotificationRecord[] }>("/ws/notifications", {
    query: { limit }
  });

export const markNotificationRead = async (id: string): Promise<void> =>
  apiRequest<void>(`/ws/notifications/${id}/read`, {
    method: "POST"
  });
