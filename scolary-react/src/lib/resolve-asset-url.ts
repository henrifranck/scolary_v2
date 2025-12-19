const resolveApiBaseUrl = () => {
  const baseUrl = import.meta.env.VITE_SCOLARY_API_URL;
  if (!baseUrl) {
    return "";
  }

  const trimmed = baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl;
  if (trimmed.endsWith("/api/v1")) {
    return trimmed.slice(0, -7);
  }
  return trimmed;
};

export const resolveAssetUrl = (path?: string | null) => {
  if (!path) {
    return "";
  }

  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }

  const baseUrl = resolveApiBaseUrl();
  if (!baseUrl) {
    return path;
  }

  return path.startsWith("/") ? `${baseUrl}${path}` : `${baseUrl}/${path}`;
};
