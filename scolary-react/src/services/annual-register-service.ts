import {
  ApiListResponse,
  StudentAnnualProps
} from "@/components/student-form/student-form-types";
import { apiRequest } from "./api-client";

const relations = JSON.stringify([
  "register_semester",
  "academic_year{id,name}",
  "register_semester{id,id_annual_register,id_journey,semester,repeat_status}",
  "register_semester.journey{id_mention,name}",
  "register_semester.journey.mention{name}",
  "payment{id,payed,num_receipt,date_receipt,description}",
  "document{id,id_annual_register,name,description,url,id_required_document,required_document_name}",
  "document.required_document{id,name}"
]);
const baseColumn = JSON.stringify(["last_name", "first_name"]);

const buildWhereClause = (
  cardNumber: string,
  academicYearId?: string | number
) =>
  JSON.stringify([
    {
      key: "num_carte",
      operator: "==",
      value: cardNumber
    },
    ...(academicYearId
      ? [
          {
            key: "id_academic_year",
            operator: "==",
            value: academicYearId
          }
        ]
      : [])
  ]);

type ApiAnnualRegisterPayload = ApiListResponse<StudentAnnualProps>;

export type AnnualRegisterPayload = {
  num_carte: string;
  id_academic_year: number;
  semester_count: number;
  id_enrollment_fee?: number;
};

export type RegisterSemesterPayload = {
  id_annual_register: number;
  semester: string;
  repeat_status: string;
  id_journey: number;
};

export type PaymentPayload = {
  id_annual_register: number;
  payed: number;
  num_receipt: string;
  date_receipt: string;
  description?: string;
};

export const fetchAnnualRegisterByCardNumber = async (
  cardNumber: string,
  academicYearId?: string | number
): Promise<ApiAnnualRegisterPayload> => {
  const trimmed = cardNumber.trim();
  if (!trimmed) {
    throw new Error("Le numéro de carte est requis.");
  }

  const response = await apiRequest<ApiAnnualRegisterPayload>(
    "/annual_registers/",
    {
      query: {
        relation: relations,
        base_column: baseColumn,
        where: buildWhereClause(trimmed, academicYearId)
      }
    }
  );

  return response;
};

export const createAnnualRegister = async (
  payload: AnnualRegisterPayload
): Promise<StudentAnnualProps> =>
  apiRequest<StudentAnnualProps>("/annual_registers/", {
    method: "POST",
    json: payload
  });

export const deleteAnnualRegister = async (
  id: number
): Promise<{ msg: string }> =>
  apiRequest<{ msg: string }>(`/annual_registers/${id}`, {
    method: "DELETE"
  });

export const deleteRegisterSemester = async (
  id: number
): Promise<{ msg: string }> =>
  apiRequest<{ msg: string }>(`/register_semesters/${id}`, {
    method: "DELETE"
  });

export const createRegisterSemester = async (
  payload: RegisterSemesterPayload
) =>
  apiRequest("/register_semesters/", {
    method: "POST",
    json: payload
  });

export const updateRegisterSemester = async (
  id: number,
  payload: Partial<RegisterSemesterPayload>
) =>
  apiRequest(`/register_semesters/${id}`, {
    method: "PUT",
    json: payload
  });

export const createPayment = async (payload: PaymentPayload) =>
  apiRequest("/payments/", {
    method: "POST",
    json: payload
  });

export const deletePayment = async (
  id: number
): Promise<{ msg: string }> =>
  apiRequest<{ msg: string }>(`/payments/${id}`, {
    method: "DELETE"
  });

export const updatePayment = async (
  id: number,
  payload: Partial<PaymentPayload>
) =>
  apiRequest(`/payments/${id}`, {
    method: "PUT",
    json: payload
  });
