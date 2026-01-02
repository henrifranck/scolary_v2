import { useQuery, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { isListResponse, normalizeList } from "./utils-common";
import { Mention } from "@/models/mentions";
import { ApiListResponse } from "@/models/shared";

export type SelectionStatus =
  | "Pending"
  | "Rejected"
  | "Selected"
  | "Registered"
  | "Former";

export interface SelectionStudent {
  id: string;
  apiId?: string;
  numSelect: string;
  recordId: string;
  fullName: string;
  firstName: string;
  lastName: string;
  mentionId: string;
  mentionLabel: string;
  enrollment_status: SelectionStatus;
  lastUpdate: string;
  deletedAt?: string;
  phoneNumber?: string;
  annualRegister?: any;
}

export interface SelectionFilters {
  mentionId?: string;
  academicYearId?: string;
  id_enter_year?: string;
  id_mention?: string;
  level?: string;
  search?: string;
  deletedOnly?: boolean;
  limit?: number;
  offset?: number;
  enrollmentStatus?: SelectionStatus | string;
}

const queryKeys = {
  selections: (filters: SelectionFilters): QueryKey => ["selections", filters]
} as const;

type ApiRegisterSemester = {
  semester?: string | null;
  repeat_status?: string | null;
};

type ApiAnnualRegister = {
  register_semester?: ApiRegisterSemester[];
};

type ApiSelectionStudent = {
  id: number | string;
  num_select?: string;
  num_carte?: string;
  first_name?: string | null;
  last_name?: string | null;
  enrollment_status?: string | null;
  id_mention?: number | string | null;
  annual_register?: ApiAnnualRegister[];
  photo_url?: string | null;
  photo?: string | null;
  picture?: string | null;
  deleted_at?: string | null;
  updated_at?: string | null;
  last_update?: string | null;
  mention: Mention;
  phone_number?: string;
};

const resolveStatus = (raw?: string | null): SelectionStatus => {
  if (!raw) {
    return "Pending";
  }

  const normalized = raw.replace(/_/g, " ").toLowerCase();
  if (normalized.includes("selected")) {
    return "Selected";
  } else if (normalized.includes("rejected")) {
    return "Rejected";
  } else if (normalized.includes("registered")) {
    return "Registered";
  } else if (normalized.includes("former")) {
    return "Former";
  }

  return "Pending";
};

const buildFullName = (student: ApiSelectionStudent) => {
  const parts = [student.first_name, student.last_name].filter(Boolean);
  if (parts.length) {
    return parts.join(" ");
  }

  return String(student.id);
};

const normalizeStudent = (student: ApiSelectionStudent): SelectionStudent => {
  const firstName = student.first_name ?? "";
  const lastName = student.last_name ?? "";
  const mentionLabel = student.mention?.name;
  const phoneNumber = student.phone_number;
  return {
    id: student.num_carte ?? String(student.id),
    apiId: student.id ? String(student.id) : undefined,
    numSelect: student.num_select ?? String(student.id),
    recordId: String(student.id ?? student.num_carte ?? ""),
    fullName: buildFullName(student),
    phoneNumber: phoneNumber,
    firstName,
    lastName,
    mentionLabel,
    mentionId: String(student.id_mention ?? ""),
    enrollment_status: resolveStatus(student.enrollment_status),
    lastUpdate: student.last_update ?? student.updated_at ?? "",
    deletedAt: student.deleted_at ?? ""
  };
};

const buildQueryParams = (filters: SelectionFilters) => {
  const where: Array<Record<string, unknown>> = [];
  const mentionId = filters.mentionId ?? filters.id_mention;
  const academicYear = filters.academicYearId ?? filters.id_enter_year;
  const level = filters.level;
  const enrollmentStatus = filters.enrollmentStatus;
  if (mentionId) {
    where.push({
      key: "id_mention",
      operator: "==",
      value: mentionId
    });
  }

  if (academicYear) {
    where.push({
      key: "id_enter_year",
      operator: "==",
      value: academicYear
    });
  }
  if (level) {
    where.push({
      key: "level",
      operator: "==",
      value: level
    });
  }
  if (enrollmentStatus) {
    where.push({
      key: "enrollment_status",
      operator: "==",
      value: enrollmentStatus
    });
  }
  if (filters.deletedOnly) {
    where.push({
      key: "deleted_at",
      operator: "isNotNull",
      value: ""
    });
  } else {
    where.push({
      key: "deleted_at",
      operator: "isNull",
      value: ""
    });
  }

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
    include_deleted: filters.deletedOnly ? true : false,
    where: JSON.stringify(where)
  };
};

type ApiReinscriptionPayload =
  | ApiListResponse<ApiSelectionStudent>
  | ApiSelectionStudent[];

const toReinscriptionList = (
  payload: ApiReinscriptionPayload
): { data: SelectionStudent[]; count: number } => {
  const list = normalizeList(payload).map(normalizeStudent);
  const count =
    (isListResponse(payload) && typeof payload.count === "number"
      ? payload.count
      : undefined) ?? list.length;

  return { data: list, count };
};

export async function fetchReinscriptionsWithMeta(
  filters: SelectionFilters = {}
): Promise<{ data: SelectionStudent[]; count: number }> {
  const payload = await apiRequest<ApiReinscriptionPayload>("/students/", {
    query: buildQueryParams(filters)
  });

  return toReinscriptionList(payload);
}

export async function fetchNewStudent(
  filters: SelectionFilters = {}
): Promise<SelectionStudent[]> {
  const response = await fetchReinscriptionsWithMeta(filters);
  return response.data;
}

export function useSelectionStudents(filters: SelectionFilters) {
  const hasRequiredFilters = Boolean(
    (filters.id_mention ?? filters.mentionId) &&
      (filters.id_enter_year ?? filters.academicYearId)
  );

  return useQuery({
    queryKey: queryKeys.selections(filters),
    queryFn: () => fetchNewStudent(filters),
    enabled: hasRequiredFilters
  });
}

export const selectionService = {
  fetchNewStudent,
  useSelectionStudents
};
