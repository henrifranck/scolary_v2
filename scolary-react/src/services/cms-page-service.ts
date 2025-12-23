import { useMutation, useQuery, useQueryClient, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";

export interface CmsPage {
  id: number;
  slug: string;
  title?: string | null;
  content_json?: string | null;
  draft_content?: string | null;
  meta_json?: string | null;
  status?: string | null;
}

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export type CmsPagePayload = Pick<
  CmsPage,
  "slug" | "title" | "content_json" | "draft_content" | "meta_json" | "status"
>;
export type CmsPageListQuery = Record<string, string | number | boolean | undefined>;

const cmsPagesKey = ["cms-pages"] as const;

const queryKeys = {
  cmsPages: (query?: CmsPageListQuery): QueryKey => (query ? [...cmsPagesKey, query] : cmsPagesKey),
  cmsPage: (id: number): QueryKey => ["cms-page", id],
  cmsPageBySlug: (slug: string): QueryKey => ["cms-page", "slug", slug]
};

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

export const fetchCmsPages = async (
  query?: CmsPageListQuery
): Promise<{ data: CmsPage[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<CmsPage> | CmsPage[]>("/cms_pages/", {
      query
    })
  );

export const fetchPublicCmsPages = async (
  query?: CmsPageListQuery
): Promise<{ data: CmsPage[]; count?: number }> =>
  normalizeList(
    await apiRequest<ApiListResponse<CmsPage> | CmsPage[]>("/cms_pages/public", {
      query
    })
  );

export const fetchCmsPageBySlug = (slug: string): Promise<CmsPage> =>
  apiRequest<CmsPage>(`/cms_pages/by_slug/${slug}`);

export const fetchCmsPage = (id: number): Promise<CmsPage> =>
  apiRequest<CmsPage>(`/cms_pages/${id}`);

export const createCmsPage = (payload: CmsPagePayload): Promise<CmsPage> =>
  apiRequest<CmsPage>("/cms_pages/", {
    method: "POST",
    json: payload
  });

export const updateCmsPage = (id: number, payload: CmsPagePayload): Promise<CmsPage> =>
  apiRequest<CmsPage>(`/cms_pages/${id}`, {
    method: "PUT",
    json: payload
  });

export const deleteCmsPage = (id: number): Promise<void> =>
  apiRequest<void>(`/cms_pages/${id}`, {
    method: "DELETE"
  });

export const useCmsPages = (query?: CmsPageListQuery) =>
  useQuery({
    queryKey: queryKeys.cmsPages(query),
    queryFn: () => fetchCmsPages(query)
  });

export const usePublicCmsPages = (query?: CmsPageListQuery) =>
  useQuery({
    queryKey: ["cms-pages-public", query],
    queryFn: () => fetchPublicCmsPages(query)
  });

export const useCmsPageBySlug = (slug: string, enabled = true) =>
  useQuery({
    queryKey: queryKeys.cmsPageBySlug(slug),
    queryFn: () => fetchCmsPageBySlug(slug),
    enabled
  });

export const useCmsPage = (id: number, enabled = true) =>
  useQuery({
    queryKey: queryKeys.cmsPage(id),
    queryFn: () => fetchCmsPage(id),
    enabled
  });

export const useCreateCmsPage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createCmsPage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cmsPagesKey });
    }
  });
};

export const useUpdateCmsPage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: CmsPagePayload }) =>
      updateCmsPage(id, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: cmsPagesKey });
      queryClient.invalidateQueries({ queryKey: queryKeys.cmsPage(variables.id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.cmsPageBySlug(variables.payload.slug) });
    }
  });
};

export const useDeleteCmsPage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteCmsPage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cmsPagesKey });
    }
  });
};
