import { useQuery, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { ApiListResponse } from "@/pages/user/reinscription/reinscription-form-type";
import { isListResponse, normalizeList } from "./utils-common";

export type ReinscriptionStatus = "Pending" | "In progress" | "Validated";

export interface ReinscriptionStudent {
  id: string;
  recordId: string;
  fullName: string;
  firstName: string;
  lastName: string;
  semester: string;
  journeyId: string;
  journeyLabel: string;
  mentionId: string;
  mentionLabel: string;
  status: ReinscriptionStatus;
  lastUpdate: string;
  photoUrl: string;
  annualRegister?: any;
}

export interface ReinscriptionFilters {
  mentionId?: string;
  journeyId?: string;
  semester?: string;
  academicYearId?: string;
  id_mention?: string;
  id_journey?: string;
  id_year?: string;
  search?: string;
  limit?: number;
  offset?: number;
}

const queryKeys = {
  reinscriptions: (filters: ReinscriptionFilters): QueryKey => [
    "reinscriptions",
    filters
  ]
} as const;

type ApiRegisterSemester = {
  semester?: string | null;
  repeat_status?: string | null;
  id_journey?: number | string | null;
  journey?: {
    id: number;
    name?: string | null;
    abbreviation?: string | null;
    id_mention?: number | null;
    mention?: {
      id: number;
      name?: string | null;
      abbreviation?: string | null;
    };
  };
};

type ApiAnnualRegister = {
  register_semester?: ApiRegisterSemester[];
};

type ApiReinscriptionStudent = {
  id: number | string;
  num_carte?: string;
  first_name?: string | null;
  last_name?: string | null;
  status?: string | null;
  id_journey?: number | string | null;
  id_mention?: number | string | null;
  annual_register?: ApiAnnualRegister[];
  photo_url?: string | null;
  photo?: string | null;
  picture?: string | null;
  updated_at?: string | null;
  last_update?: string | null;
};

const pickSemester = (registerSemester?: ApiRegisterSemester) =>
  registerSemester?.semester ?? "";

const resolveStatus = (raw?: string | null): ReinscriptionStatus => {
  if (!raw) {
    return "Pending";
  }

  const normalized = raw.replace(/_/g, " ").toLowerCase();
  if (normalized.includes("progress")) {
    return "In progress";
  }
  if (normalized.includes("valid")) {
    return "Validated";
  }

  return "Pending";
};

const buildFullName = (student: ApiReinscriptionStudent) => {
  const parts = [student.first_name, student.last_name].filter(Boolean);
  if (parts.length) {
    return parts.join(" ");
  }

  return String(student.id);
};

const normalizeStudent = (
  student: ApiReinscriptionStudent
): ReinscriptionStudent => {
  const annualRegister = student.annual_register?.[0];
  const registerSemester = annualRegister?.register_semester?.[0];
  const journeyId =
    registerSemester?.id_journey ??
    registerSemester?.journey?.id ??
    student.id_journey ??
    "";
  const mentionId =
    student.id_mention ??
    registerSemester?.journey?.id_mention ??
    registerSemester?.journey?.mention?.id ??
    "";

  const journeyLabel =
    registerSemester?.journey?.name ??
    registerSemester?.journey?.abbreviation ??
    (journeyId ? `Journey ${journeyId}` : "");
  const mentionLabel =
    registerSemester?.journey?.mention?.name ??
    registerSemester?.journey?.mention?.abbreviation ??
    (mentionId ? `Mention ${mentionId}` : "");

  const firstName = student.first_name ?? "";
  const lastName = student.last_name ?? "";

  return {
    id: student.num_carte ?? String(student.id),
    recordId: String(student.id ?? student.num_carte ?? ""),
    fullName: buildFullName(student),
    firstName,
    lastName,
    semester: pickSemester(registerSemester),
    journeyId: String(journeyId ?? ""),
    journeyLabel,
    mentionId: String(mentionId ?? ""),
    mentionLabel,
    status: resolveStatus(student.status),
    lastUpdate: student.last_update ?? student.updated_at ?? "",
    photoUrl: resolveAssetUrl(
      student.photo_url ?? student.photo ?? student.picture ?? ""
    )
  };
};

const buildQueryParams = (filters: ReinscriptionFilters) => {
  const where: Array<Record<string, unknown>> = [];
  const academicYear = filters.id_year ?? filters.academicYearId;
  const journeyId = filters.id_journey ?? filters.journeyId;
  const semester = filters.semester;

  if (academicYear) {
    where.push({
      key: "annual_register.id_academic_year",
      operator: "==",
      value: academicYear
    });
  }

  if (journeyId) {
    where.push({
      key: "annual_register.register_semester.id_journey",
      operator: "==",
      value: journeyId
    });
  }

  if (semester) {
    where.push({
      key: "annual_register.register_semester.semester",
      operator: "==",
      value: semester
    });
  }
  where.push({
    key: "deleted_at",
    operator: "isNull",
    value: ""
  });

  const trimmedSearch = (filters.search ?? "").trim();
  if (trimmedSearch) {
    where.push({
      key: ["first_name", "last_name", "num_carte", "num_select"],
      operator: ["like", "like", "like", "like"],
      value: [trimmedSearch, trimmedSearch, trimmedSearch, trimmedSearch]
    });
  }

  return {
    limit: filters.limit,
    offset: filters.offset,
    where: JSON.stringify(where),
    relation: JSON.stringify([
      "annual_register",
      "annual_register.register_semester",
      "annual_register.register_semester.journey",
      "annual_register.register_semester.journey.mention"
    ])
  };
};

type ApiReinscriptionPayload =
  | ApiListResponse<ApiReinscriptionStudent>
  | ApiReinscriptionStudent[];

const toReinscriptionList = (
  payload: ApiReinscriptionPayload
): { data: ReinscriptionStudent[]; count: number } => {
  const list = normalizeList(payload).map(normalizeStudent);
  const count =
    (isListResponse(payload) && typeof payload.count === "number"
      ? payload.count
      : undefined) ?? list.length;

  return { data: list, count };
};

export async function fetchReinscriptionsWithMeta(
  filters: ReinscriptionFilters = {}
): Promise<{ data: ReinscriptionStudent[]; count: number }> {
  const payload = await apiRequest<ApiReinscriptionPayload>("/students/", {
    query: buildQueryParams(filters)
  });

  return toReinscriptionList(payload);
}

export async function fetchReinscriptions(
  filters: ReinscriptionFilters = {}
): Promise<ReinscriptionStudent[]> {
  const response = await fetchReinscriptionsWithMeta(filters);
  return response.data;
}

export function useReinscriptions(filters: ReinscriptionFilters) {
  const hasRequiredFilters = Boolean(
    (filters.id_mention ?? filters.mentionId) &&
      (filters.id_year ?? filters.academicYearId) &&
      (filters.id_journey ?? filters.journeyId)
  );

  return useQuery({
    queryKey: queryKeys.reinscriptions(filters),
    queryFn: () => fetchReinscriptions(filters),
    enabled: hasRequiredFilters
  });
}

export const reinscriptionService = {
  fetchReinscriptions,
  useReinscriptions
};
