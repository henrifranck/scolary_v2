const resolveBaseUrl = () => {
  const baseUrl = import.meta.env.VITE_SCOLARY_API_URL;
  if (!baseUrl) {
    throw new Error(
      "Missing VITE_SCOLARY_API_URL in your environment configuration."
    );
  }

  return baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl;
};

const buildUrl = (
  path: string,
  query?: Record<string, string | number | boolean | undefined>
) => {
  const baseUrl = new URL(resolveBaseUrl());
  const normalizedPath = path.replace(/^\//, "");
  const basePath = baseUrl.pathname.replace(/\/$/, "");
  baseUrl.pathname = [basePath, normalizedPath].filter(Boolean).join("/") || "/";

  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value === undefined || value === null || value === "") {
        return;
      }

      baseUrl.searchParams.set(key, String(value));
    });
  }

  return baseUrl.toString();
};

const readStoredToken = () => {
  if (typeof window === "undefined") {
    return null;
  }

  const sessionToken = window.sessionStorage?.getItem("token");
  if (sessionToken) {
    return sessionToken;
  }

  const localToken = window.localStorage?.getItem("token");
  if (localToken) {
    return localToken;
  }

  const legacyToken = window.localStorage?.getItem("scolary_token_value");
  if (legacyToken) {
    try {
      const parsed = JSON.parse(legacyToken) as { access_token?: string };
      if (parsed?.access_token) {
        return parsed.access_token;
      }
    } catch {
      return legacyToken;
    }
  }

  return null;
};

const getAuthHeaders = () => {
  if (typeof window === "undefined") {
    return {};
  }

  const token = readStoredToken();

  return token ? { Authorization: `Bearer ${token}` } : {};
};

type RequestOptions = {
  body?: BodyInit;
  json?: unknown;
  query?: Record<string, string | number | boolean | undefined>;
  headers?: HeadersInit;
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
};

const extractErrorMessage = (
  detail: unknown,
  fallbackStatus: number
): string => {
  if (!detail) {
    return `Request failed with status ${fallbackStatus}`;
  }
  if (typeof detail === "string") {
    return detail;
  }
  if (
    Array.isArray(detail) &&
    detail.length > 0 &&
    typeof detail[0] === "object"
  ) {
    const messages = detail
      .map((item: any) => item?.msg || item?.message || item?.detail)
      .filter(Boolean);
    if (messages.length) {
      return messages.join("; ");
    }
  }
  if (typeof detail === "object") {
    const asObj = detail as Record<string, unknown>;
    if (asObj.message) return String(asObj.message);
    if (Array.isArray(asObj.detail)) {
      const messages = (asObj.detail as any[])
        .map((item) => item?.msg || item?.message || item?.detail)
        .filter(Boolean);
      if (messages.length) {
        return messages.join("; ");
      }
    }
    if (asObj.detail) return String(asObj.detail);
  }
  return `Request failed with status ${fallbackStatus}`;
};

const redirectToForbidden = () => {
  if (typeof window === "undefined") {
    return;
  }
  if (window.location.pathname === "/403") {
    return;
  }
  window.location.replace("/403");
};

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const { body, json, query, headers, method = "GET" } = options;
  const payload = json !== undefined ? JSON.stringify(json) : body;
  const defaultHeaders: Record<string, string> = {
    Accept: "application/json",
    ...(getAuthHeaders() as Record<string, string>)
  };

  if (json !== undefined) {
    defaultHeaders["Content-Type"] = "application/json";
  }

  const response = await fetch(buildUrl(path, query), {
    method,
    headers: {
      ...defaultHeaders,
      ...headers
    },
    body: payload
  });

  if (!response.ok) {
    const detail = await safeReadJson(response);
    const message =
      response.status === 403
        ? "Vous n'avez pas les permissions nécessaires pour effectuer cette action."
        : extractErrorMessage(detail, response.status);
    if (response.status === 403) {
      redirectToForbidden();
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null as T;
  }

  return (await response.json()) as T;
}

const safeReadJson = async (response: Response) => {
  try {
    return await response.json();
  } catch {
    return null;
  }
};

export async function apiRequestBlob(
  path: string,
  options: RequestOptions = {}
): Promise<Blob> {
  const { body, json, query, headers, method = "GET" } = options;
  const payload = json !== undefined ? JSON.stringify(json) : body;
  const defaultHeaders: Record<string, string> = {
    Accept: "application/pdf",
    ...(getAuthHeaders() as Record<string, string>)
  };

  if (json !== undefined) {
    defaultHeaders["Content-Type"] = "application/json";
  }

  const response = await fetch(buildUrl(path, query), {
    method,
    headers: {
      ...defaultHeaders,
      ...headers
    },
    body: payload
  });

  if (!response.ok) {
    const detail = await safeReadJson(response);
    const message =
      response.status === 403
        ? "Vous n'avez pas les permissions nécessaires pour effectuer cette action."
        : extractErrorMessage(detail, response.status);
    if (response.status === 403) {
      redirectToForbidden();
    }
    throw new Error(message);
  }

  return await response.blob();
}
