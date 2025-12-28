import { useQuery, type QueryKey } from "@tanstack/react-query";

import { apiRequest } from "./api-client";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { isListResponse, normalizeList } from "./utils-common";
import {
  ApiListResponse,
  StudentFormState,
  StudentProfile,
  StudentSemesterState
} from "@/components/student-form/student-form-types";

export type ReinscriptionStatus = "Pending" | "In progress" | "Validated";

export interface ReinscriptionFilters {
  mentionId?: string;
  journeyId?: string;
  semester?: string;
  academicYearId?: string;
  annualRegisterId?: string | number;
  id_mention?: string;
  id_journey?: string;
  id_annual_register?: string | number;
  id_year?: string;
  id_enter_year?: string;
  search?: string;
  deletedOnly?: boolean;
  registerType?: string;
  limit?: number;
  offset?: number;
}

const queryKeys = {
  reinscriptions: (filters: ReinscriptionFilters): QueryKey => [
    "reinscriptions",
    filters
  ]
} as const;

const pickSemester = (registerSemester?: StudentSemesterState) =>
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

const buildFullName = (student: StudentProfile) => {
  const parts = [student.first_name, student.last_name].filter(Boolean);
  if (parts.length) {
    return parts.join(" ");
  }

  return String(student.id);
};

const normalizeStudent = (student: StudentProfile): StudentFormState => {
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
    studentRecordId: student.num_carte ?? String(student.id),
    studentId: String(student.id ?? student.num_carte ?? ""),
    fullName: buildFullName(student),
    email: student.email,
    cardNumber: student.num_carte,
    firstName,
    lastName,
    semester: pickSemester(registerSemester),
    journeyId: String(journeyId ?? ""),
    journeyLabel,
    mentionId: String(mentionId ?? ""),
    mentionLabel,
    sex: student.sex,
    address: student.address,
    maritalStatus: student.martial_status,
    phoneNumber: student.phone_number,
    cinNumber: student.num_cin,
    status: resolveStatus(student.enrollment_status),
    lastUpdate: student.updated_at ?? "",
    picture: resolveAssetUrl(student.photo_url ?? student.picture ?? ""),
    deletedAt: student.deleted_at ?? "",
    cinIssueDate: student.date_of_cin,
    cinIssuePlace: student.place_of_cin,
    birthDate: student.date_of_birth,
    birthPlace: student.place_of_birth,
    baccalaureateCenter: student.center_of_baccalaureate,
    baccalaureateSerieId: student.id_baccalaureate_series,
    baccalaureateYear: student.year_of_baccalaureate,
    job: student.job,
    enrollmentStatus: student.enrollment_status,
    mean: student.mean
  };
};

const buildQueryParams = (filters: ReinscriptionFilters) => {
  const where: Array<Record<string, unknown>> = [];
  const whereRelation: Array<Record<string, unknown>> = [];
  const academicYear = filters.id_year ?? filters.academicYearId;
  const journeyId = filters.id_journey ?? filters.journeyId;
  const annualRegisterId =
    filters.id_annual_register ?? filters.annualRegisterId;
  const semester = filters.semester;

  // Build nested filter: annual_register.[id_academic_year,register_semester.[id_journey,semester]]
  const nestedKeys: string[] = ["register_type"];
  const nestedOperators: string[] = ["=="];
  const nestedValues: Array<string | number> = ["REGISTRATION"];

  if (academicYear) {
    nestedKeys.push("id_academic_year");
    nestedOperators.push("==");
    nestedValues.push(Number(academicYear));
  }

  const registerParts: string[] = [];
  const registerOperators: string[] = [];
  const registerValues: Array<string | number> = [];

  if (journeyId) {
    registerParts.push("id_journey");
    registerOperators.push("==");
    registerValues.push(Number(journeyId));
  }

  if (semester) {
    registerParts.push("semester");
    registerOperators.push("==");
    registerValues.push(semester);
  }

  if (registerParts.length) {
    nestedKeys.push(`register_semester.[${registerParts.join(",")}]`);
    nestedOperators.push(registerOperators.join(","));
    nestedValues.push(registerValues.join(","));
  }

  if (nestedKeys.length) {
    where.push({
      key: `annual_register.[${nestedKeys.join(",")}]`,
      operator: nestedOperators.join(","),
      value: nestedValues.join(",")
    });
  }

  if (annualRegisterId) {
    whereRelation.push({
      key: "annual_register.id",
      operator: "==",
      value: Number(annualRegisterId)
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
    where: JSON.stringify(where),
    where_relation: JSON.stringify(whereRelation),
    relation: JSON.stringify([
      "annual_register",
      "annual_register.register_semester",
      "annual_register.register_semester.journey",
      "annual_register.register_semester.journey.mention"
    ])
  };
};

type ApiReinscriptionPayload =
  | ApiListResponse<StudentProfile>
  | StudentProfile[];

const toReinscriptionList = (
  payload: ApiReinscriptionPayload
): { data: StudentFormState[]; count: number } => {
  const list = normalizeList(payload).map(normalizeStudent);
  const count =
    (isListResponse(payload) && typeof payload.count === "number"
      ? payload.count
      : undefined) ?? list.length;

  return { data: list, count };
};

export async function fetchReinscriptionsWithMeta(
  filters: ReinscriptionFilters = {}
): Promise<{ data: StudentFormState[]; count: number }> {
  const payload = await apiRequest<ApiReinscriptionPayload>("/students/", {
    query: buildQueryParams(filters)
  });

  return toReinscriptionList(payload);
}

export async function fetchReinscriptions(
  filters: ReinscriptionFilters = {}
): Promise<StudentFormState[]> {
  const response = await fetchReinscriptionsWithMeta(filters);
  return response.data;
}

export function useReinscriptions(filters: ReinscriptionFilters) {
  const hasRequiredFilters = Boolean(
    (filters.id_mention ?? filters.mentionId) &&
      (filters.id_year ?? filters.academicYearId)
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
