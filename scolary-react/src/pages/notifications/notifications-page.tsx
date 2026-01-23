import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  fetchNotifications,
  markNotificationRead,
  type NotificationRecord
} from "@/services/notification-service";

export const NotificationsPage = () => {
  const [notifications, setNotifications] = useState<NotificationRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchNotifications(200);
      setNotifications(res.data || []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Impossible de charger les notifications."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const markAllRead = async () => {
    const unread = notifications.filter((n) => !n.read);
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
    for (const n of unread) {
      markNotificationRead(n._id).catch(() => {});
    }
  };

  const toggleRead = async (id: string, next: boolean) => {
    setNotifications((prev) =>
      prev.map((n) => (n._id === id ? { ...n, read: next } : n))
    );
    if (next) {
      markNotificationRead(id).catch(() => {});
    }
  };

  return (
    <div className="space-y-4 p-4 sm:p-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Notifications</h1>
          <p className="text-sm text-muted-foreground">
            Dernières notifications reçues (max 200).
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={load}
            disabled={loading}
            className="w-full sm:w-auto"
          >
            Rafraîchir
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={markAllRead}
            disabled={!notifications.some((n) => !n.read)}
            className="w-full sm:w-auto"
          >
            Tout marquer comme lu
          </Button>
        </div>
      </div>

      {error ? <p className="text-sm text-destructive">{error}</p> : null}

      <div className="rounded-lg border divide-y">
        {loading ? (
          <p className="p-4 text-sm text-muted-foreground">Chargement…</p>
        ) : notifications.length ? (
          notifications.map((notif) => (
            <div
              key={notif._id}
              className="flex items-start gap-3 p-4 hover:bg-muted/50"
            >
              <span
                className={cn(
                  "mt-1 inline-block h-2.5 w-2.5 rounded-full",
                  notif.read ? "bg-muted-foreground/50" : "bg-green-500"
                )}
              />
              <div className="flex-1 space-y-1">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-medium line-clamp-2">
                    {notif.title || notif.type || "Notification"}
                  </p>
                  {!notif.read ? (
                    <Button
                      size="xs"
                      variant="ghost"
                      onClick={() => toggleRead(notif._id, true)}
                    >
                      Marquer lu
                    </Button>
                  ) : null}
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {notif.message || notif.full_name || notif._id}
                </p>
              </div>
            </div>
          ))
        ) : (
          <p className="p-4 text-sm text-muted-foreground">
            Aucune notification disponible.
          </p>
        )}
      </div>
    </div>
  );
};
