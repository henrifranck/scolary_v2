import { useQuery, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";
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
  limit?: number;
  offset?: number;
}

const queryKeys = {
  reinscriptions: (filters: ReinscriptionFilters): QueryKey => [
    "reinscriptions",
    filters
  ]
} as const;

type ApiStudentYear = {
  id_year?: number;
  id_journey?: number;
  status?: string | null;
  active_semester?: string | null;
  another_semester?: string | null;
  sup_semester?: string | null;
  journey?: {
    id: number;
    title?: string;
    abbreviation?: string;
    id_mention?: number;
    mention?: {
      id: number;
      title?: string;
      abbreviation?: string;
    };
  };
  mention?: {
    id: number;
    title?: string;
    abbreviation?: string;
  };
};

type ApiReinscriptionStudent = {
  id: number | string;
  num_carte?: string;
  first_name?: string | null;
  last_name?: string | null;
  status?: string | null;
  id_journey?: number | string | null;
  id_mention?: number | string | null;
  student_year?: ApiStudentYear[];
  photo_url?: string | null;
  photo?: string | null;
  updated_at?: string | null;
  last_update?: string | null;
};

const pickSemester = (studentYear?: ApiStudentYear) =>
  studentYear?.active_semester ??
  studentYear?.another_semester ??
  studentYear?.sup_semester ??
  "";

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
  const studentYear = student.student_year?.[0];
  const journeyId = studentYear?.id_journey ?? student.id_journey ?? "";
  const mentionId =
    student.id_mention ??
    studentYear?.journey?.id_mention ??
    studentYear?.journey?.mention?.id ??
    studentYear?.mention?.id ??
    "";

  const journeyLabel =
    studentYear?.journey?.title ??
    studentYear?.journey?.abbreviation ??
    (journeyId ? `Journey ${journeyId}` : "");
  const mentionLabel =
    studentYear?.journey?.mention?.title ??
    studentYear?.mention?.title ??
    (mentionId ? `Mention ${mentionId}` : "");

  const firstName = student.first_name ?? "";
  const lastName = student.last_name ?? "";

  return {
    id: student.num_carte ?? String(student.id),
    recordId: String(student.id ?? student.num_carte ?? ""),
    fullName: buildFullName(student),
    firstName,
    lastName,
    semester: pickSemester(studentYear),
    journeyId: String(journeyId ?? ""),
    journeyLabel,
    mentionId: String(mentionId ?? ""),
    mentionLabel,
    status: resolveStatus(studentYear?.status ?? student.status),
    lastUpdate: student.last_update ?? student.updated_at ?? "",
    photoUrl: student.photo_url ?? ""
  };
};

const buildQueryParams = (filters: ReinscriptionFilters) => ({
  limit: filters.limit,
  offset: filters.offset,
  where: JSON.stringify([
    {
      key: "annual_register.id_academic_year",
      operator: "==",
      value: filters.id_year ?? filters.academicYearId ?? ""
    },
    {
      key: "annual_register.register_semester.id_journey",
      operator: "==",
      value: filters.id_journey ?? filters.journeyId
    },
    {
      key: "annual_register.register_semester.semester",
      operator: "==",
      value: filters.semester
    }
  ]),
  relations: JSON.stringify(["student_year.journey.mention", "student_year"])
});

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
