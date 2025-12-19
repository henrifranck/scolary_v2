import { apiRequest } from "./api-client";

type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

const isListResponse = <T>(payload: unknown): payload is ApiListResponse<T> =>
  Boolean(
    payload &&
      typeof payload === "object" &&
      "data" in (payload as Record<string, unknown>) &&
      Array.isArray((payload as ApiListResponse<T>).data)
  );

const normalizeList = <T>(payload: ApiListResponse<T> | T[]): T[] => {
  if (isListResponse<T>(payload)) {
    return payload.data;
  }

  return payload as T[];
};

export interface Nationality {
  id: number;
  name: string;
}

export interface Mention {
  id: number;
  name: string;
  abbreviation?: string;
}

export interface Journey {
  id: number;
  name: string;
  abbreviation: string;
  id_mention?: number;
  semester_list?:
    | string[]
    | {
        id?: number | null;
        semester?: string | null;
      }[];
}

export interface CollegeYear {
  id: number;
  name: string;
  is_active: boolean;
}

export interface SubscriptionType {
  id: number;
  name: string;
  description?: string;
  price: number;
}

export interface EnrollmentFee {
  id: number;
  level: string;
  price: number;
  id_year?: number;
  id_mention?: number;
}

export interface BaccSerie {
  id: number;
  title: string;
  value: string;
}

export interface ReceiptPayload {
  num: string;
  date: string;
  id_enrollment_fee: number;
  payed: number;
  year?: number | string;
}

export interface StudentYearPayload {
  active_semester: string;
  id_journey: number;
  status: string;
  id_year?: number;
}

export interface CreateInscriptionPayload {
  last_name: string;
  first_name?: string | null;
  date_birth: string;
  place_birth: string;
  address: string;
  sex: string;
  nationality_id: number;
  num_cin?: string | null;
  date_cin?: string | null;
  place_cin?: string | null;
  id_mention: number;
  num_select: string;
  receipt: ReceiptPayload;
  receipt_list?: unknown[];
  mean?: number | null;
  baccalaureate_years: string;
  type?: string;
  photo?: string | null;
  photo_url?: string | null;
  situation: string;
  telephone?: string | null;
  baccalaureate_num: string;
  baccalaureate_center: string;
  baccalaureate_series_id: number;
  work: string;
  father_name?: string | null;
  father_work?: string | null;
  mother_name?: string | null;
  mother_work?: string | null;
  parent_address?: string | null;
  student_years: StudentYearPayload[];
  subscription_type_id: number;
}

export const fetchNationalities = async () =>
  normalizeList(
    await apiRequest<ApiListResponse<Nationality> | Nationality[]>(
      "/nationality/"
    )
  );

export const fetchMentions = async () =>
  normalizeList(
    await apiRequest<ApiListResponse<Mention> | Mention[]>("/mentions/")
  );

export const fetchJourneys = async (mentionId?: number | string) => {
  const query: Record<string, string | number | boolean | undefined> = {};
  const relation = JSON.stringify(["semester_list{id,semester}"]);

  if (mentionId) {
    query.where = JSON.stringify([
      {
        key: "id_mention",
        operator: "==",
        value: mentionId
      }
    ]);
  }
  query.relation = relation;

  return normalizeList(
    await apiRequest<ApiListResponse<Journey> | Journey[]>("/journey/", {
      query
    })
  );
};

export const fetchCollegeYears = async () =>
  normalizeList(
    await apiRequest<ApiListResponse<CollegeYear> | CollegeYear[]>(
      "/academic_years/"
    )
  );

export const fetchSubscriptionTypes = async () =>
  normalizeList(
    await apiRequest<ApiListResponse<SubscriptionType> | SubscriptionType[]>(
      "/subscription_type/"
    )
  );

export const fetchEnrollmentFees = async (mentionId?: number) => {
  if (mentionId) {
    return await apiRequest<EnrollmentFee[]>("/enrollment_fee/by_mention", {
      query: { id_mention: mentionId }
    });
  }

  return normalizeList(
    await apiRequest<ApiListResponse<EnrollmentFee> | EnrollmentFee[]>(
      "/enrollment_fee/"
    )
  );
};

export const fetchBaccSeries = async () =>
  normalizeList(
    await apiRequest<ApiListResponse<BaccSerie> | BaccSerie[]>("/bacc_serie/")
  );

export const createInscription = async (payload: CreateInscriptionPayload) =>
  apiRequest("/student/new/", {
    method: "POST",
    json: payload
  });
