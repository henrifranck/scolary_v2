import { useEffect, useMemo, useRef, useState } from "react";

type NotificationEvent = Record<string, any> & {
  type?: string;
  message?: string;
  receivedAt?: string;
};

type Listener = (event: NotificationEvent | null) => void;

const readStoredToken = () => {
  if (typeof window === "undefined") return null;
  const sessionToken = window.sessionStorage?.getItem("token");
  if (sessionToken) return sessionToken;
  const localToken = window.localStorage?.getItem("token");
  if (localToken) return localToken;
  const legacyToken = window.localStorage?.getItem("scolary_token_value");
  if (legacyToken) {
    try {
      const parsed = JSON.parse(legacyToken) as { access_token?: string };
      if (parsed?.access_token) return parsed.access_token;
    } catch {
      return legacyToken;
    }
  }
  return null;
};

const buildWsUrl = () => {
  const apiBase = import.meta.env.VITE_SCOLARY_API_URL;
  if (!apiBase) return null;
  try {
    const url = new URL(apiBase);
    url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
    const basePath = url.pathname.replace(/\/$/, "");
    url.pathname = `${basePath}/ws/notifications`;
    url.search = "";
    return url.toString();
  } catch {
    return null;
  }
};

type SharedState = {
  ws: WebSocket | null;
  retryId: number | null;
  listeners: Set<Listener>;
};

const shared: SharedState = {
  ws: null,
  retryId: null,
  listeners: new Set()
};

const ensureConnection = (wsUrl: string, enabled: boolean) => {
  if (!enabled) return;
  if (
    shared.ws &&
    (shared.ws.readyState === WebSocket.OPEN ||
      shared.ws.readyState === WebSocket.CONNECTING)
  ) {
    return;
  }
  const token = readStoredToken();
  const urlWithToken =
    token && !wsUrl.includes("token=")
      ? `${wsUrl}?token=${encodeURIComponent(token)}`
      : wsUrl;
  const ws = new WebSocket(urlWithToken);
  shared.ws = ws;
  ws.onmessage = (messageEvent) => {
    let payload: NotificationEvent | null = null;
    try {
      const data = JSON.parse(messageEvent.data);
      payload = { ...data, receivedAt: new Date().toISOString() };
    } catch {
      payload = {
        message: String(messageEvent.data || "Notification"),
        receivedAt: new Date().toISOString()
      };
    }
    shared.listeners.forEach((listener) => listener(payload));
  };
  ws.onclose = () => {
    shared.ws = null;
    if (shared.retryId) {
      clearTimeout(shared.retryId);
      shared.retryId = null;
    }
    if (enabled) {
      shared.retryId = window.setTimeout(() => ensureConnection(wsUrl, enabled), 5000);
    }
  };
};

export const useNotifications = (enabled: boolean) => {
  const [event, setEvent] = useState<NotificationEvent | null>(null);
  const wsUrl = useMemo(() => buildWsUrl(), []);

  useEffect(() => {
    if (!enabled || !wsUrl) return;
    const listener: Listener = (payload) => setEvent(payload);
    shared.listeners.add(listener);
    ensureConnection(wsUrl, enabled);
    return () => {
      shared.listeners.delete(listener);
      if (shared.listeners.size === 0) {
        if (shared.retryId) {
          clearTimeout(shared.retryId);
          shared.retryId = null;
        }
        if (shared.ws) {
          shared.ws.close();
          shared.ws = null;
        }
      }
    };
  }, [enabled, wsUrl]);

  return event;
};
