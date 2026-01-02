import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { fetchMentions } from "@/services/mention-service";
import { fetchBaccalaureateSeries } from "@/services/baccalaureate-series-service";
import { fetchAcademicYears } from "@/services/academic-year-service";
import { fetchAvailableServices } from "@/services/available-service";
import { fetchAvailableModels } from "@/services/available-model-service";
import { Mention, MentionOption } from "@/models/mentions";
import { BaccalaureateSerieOption } from "@/models/baccalaureate-series";
import { AcademicYearOption } from "@/components/filters/academic-filters";

const LOOKUP_STALE_TIME = 1000 * 60 * 30; // 30 minutes
const LOOKUP_GC_TIME = 1000 * 60 * 120; // 2 hours

type UseLookupOptionsArgs = {
  includeMentions?: boolean;
  includeBaccalaureateSeries?: boolean;
  includeAcademicYears?: boolean;
  includeAvailableServices?: boolean;
  includeAvailableModels?: boolean;
};

type AvailableServiceOption = {
  id: string;
  label: string;
  route_ui?: string | null;
};

type AvailableModelOption = {
  id: string;
  label: string;
  route_ui?: string;
  route_api?: string;
};

export const useLookupOptions = ({
  includeMentions = false,
  includeBaccalaureateSeries = false,
  includeAcademicYears = false,
  includeAvailableServices = false,
  includeAvailableModels = false
}: UseLookupOptionsArgs = {}) => {
  const mentionQuery = useQuery({
    queryKey: ["lookups", "mentions", "user-only"],
    queryFn: () => fetchMentions({ user_only: true }),
    enabled: includeMentions,
    staleTime: LOOKUP_STALE_TIME,
    gcTime: LOOKUP_GC_TIME,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false
  });

  const baccalaureateQuery = useQuery({
    queryKey: ["lookups", "baccalaureateSeries"],
    queryFn: () => fetchBaccalaureateSeries(),
    enabled: includeBaccalaureateSeries,
    staleTime: LOOKUP_STALE_TIME,
    gcTime: LOOKUP_GC_TIME,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false
  });

  const academicYearQuery = useQuery({
    queryKey: ["lookups", "academicYears"],
    queryFn: () => fetchAcademicYears(),
    enabled: includeAcademicYears,
    staleTime: LOOKUP_STALE_TIME,
    gcTime: LOOKUP_GC_TIME,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false
  });

  const availableServiceQuery = useQuery({
    queryKey: ["lookups", "availableServices"],
    queryFn: () => fetchAvailableServices(),
    enabled: includeAvailableServices,
    staleTime: LOOKUP_STALE_TIME,
    gcTime: LOOKUP_GC_TIME,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false
  });

  const availableModelQuery = useQuery({
    queryKey: ["lookups", "availableModels"],
    queryFn: () => fetchAvailableModels({ limit: 1000 }),
    enabled: includeAvailableModels,
    staleTime: LOOKUP_STALE_TIME,
    gcTime: LOOKUP_GC_TIME,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false
  });

  const mentionOptions: MentionOption[] = useMemo(() => {
    if (!includeMentions) {
      return [];
    }
    const mentions = mentionQuery.data?.data ?? [];
    return mentions.map((mention: Mention) => ({
      id: String(mention.id),
      label:
        mention.name?.trim() ||
        mention.abbreviation?.trim() ||
        `Mention ${mention.id}`
    }));
  }, [includeMentions, mentionQuery.data]);

  const baccalaureateSerieOptions: BaccalaureateSerieOption[] = useMemo(() => {
    if (!includeBaccalaureateSeries) {
      return [];
    }
    const series = baccalaureateQuery.data?.data ?? [];
    return series.map((serie: any) => ({
      id: String(serie.id),
      label: serie.name ?? serie.value ?? `Serie ${serie.id}`
    }));
  }, [includeBaccalaureateSeries, baccalaureateQuery.data]);

  const academicYearOptions: AcademicYearOption[] = useMemo(() => {
    if (!includeAcademicYears) {
      return [];
    }
    const years = academicYearQuery.data?.data ?? [];
    return years.map((year) => ({
      id: String(year.id),
      label: year.name ?? `Year ${year.id}`
    }));
  }, [includeAcademicYears, academicYearQuery.data]);

  const availableServiceOptions: AvailableServiceOption[] = useMemo(() => {
    if (!includeAvailableServices) {
      return [];
    }
    const services = availableServiceQuery.data?.data ?? [];
    return services.map((service) => ({
      id: String(service.id),
      label: service.name ?? `Service ${service.id}`,
      route_ui: service.route_ui
    }));
  }, [includeAvailableServices, availableServiceQuery.data]);

  const availableModelOptions: AvailableModelOption[] = useMemo(() => {
    if (!includeAvailableModels) {
      return [];
    }
    const models = availableModelQuery.data?.data ?? [];
    return models.map((model) => ({
      id: String(model.id),
      label: model.name ?? `Model ${model.id}`,
      route_ui: model.route_ui,
      route_api: model.route_api
    }));
  }, [availableModelQuery.data, includeAvailableModels]);

  return {
    mentionOptions,
    baccalaureateSerieOptions,
    academicYearOptions,
    availableServiceOptions,
    availableModelOptions,
    isLoadingMentions:
      includeMentions &&
      (mentionQuery.isPending ||
        mentionQuery.isFetching ||
        mentionQuery.isRefetching),
    isLoadingBaccalaureateSeries:
      includeBaccalaureateSeries &&
      (baccalaureateQuery.isPending ||
        baccalaureateQuery.isFetching ||
        baccalaureateQuery.isRefetching),
    isLoadingAcademicYears:
      includeAcademicYears &&
      (academicYearQuery.isPending ||
        academicYearQuery.isFetching ||
        academicYearQuery.isRefetching),
    isLoadingAvailableServices:
      includeAvailableServices &&
      (availableServiceQuery.isPending ||
        availableServiceQuery.isFetching ||
        availableServiceQuery.isRefetching),
    isLoadingAvailableModels:
      includeAvailableModels &&
      (availableModelQuery.isPending ||
        availableModelQuery.isFetching ||
        availableModelQuery.isRefetching)
  };
};
