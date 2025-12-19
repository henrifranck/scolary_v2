import { StudentProfile } from "@/pages/user/reinscription/reinscription-form-type";
import { apiRequest } from "./api-client";
import { ReinscriptionFilters } from "./reinscription-service";

type OneStudentApiResponse =
  | StudentProfile
  | {
      data?: StudentProfile | null;
    };

export interface StudentUpdatePayload {
  id?: number | string | null;
  num_select?: string;
  num_carte?: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  address?: string;
  num_of_cin?: string;
  date_of_cin?: string;
  place_of_cin?: string;
  date_of_birth?: string;
  place_of_birth?: string;
  picture?: string | null;
  id_mention?: string | number;
  id_journey?: string | number;
  active_semester?: string;
  enrollment_status?: string;
  notes?: string;
}

const relations = JSON.stringify([
  "annual_register.register_semester",
  "annual_register.register_semester{id,id_annual_register,id_journey,semester,repeat_status}",
  "annual_register.register_semester.journey{id_mention,name}",
  "annual_register.register_semester.journey.mention{name}",
  "annual_register.payment{id,payed,num_receipt,date_receipt}"
]);
const baseColumn = JSON.stringify([
  "last_name",
  "first_name",
  "num_carte",
  "id",
  "num_select",
  "picture",
  "id_mention",
  "date_of_birth",
  "place_of_birth",
  "address",
  "email",
  "num_of_cin",
  "date_of_cin",
  "place_of_cin"
]);

const buildWhereClause = (cardNumber: string) =>
  JSON.stringify([
    {
      key: "num_carte",
      operator: "==",
      value: cardNumber
    }
  ]);

const buildWhereRelationClause = (filter: ReinscriptionFilters) =>
  JSON.stringify([
    {
      key: "annual_register.id_academic_year",
      operator: "==",
      value: filter.id_year
    },
    {
      key: "annual_register.register_semester.semester",
      operator: "==",
      value: filter.semester
    }
  ]);

const extractStudent = (payload: OneStudentApiResponse): StudentProfile => {
  if (payload && typeof payload === "object" && "data" in payload) {
    return payload.data ?? {};
  }

  return payload as StudentProfile;
};

export const fetchStudentByCardNumber = async (
  filtes: ReinscriptionFilters,
  cardNumber: string
): Promise<StudentProfile> => {
  const trimmed = cardNumber.trim();
  if (!trimmed) {
    throw new Error("Le numéro de carte est requis.");
  }

  const response = await apiRequest<OneStudentApiResponse>(
    "/students/one_student",
    {
      query: {
        relation: relations,
        base_column: baseColumn,
        where: buildWhereClause(trimmed),
        where_relation: buildWhereRelationClause(filtes)
      }
    }
  );

  const student = extractStudent(response);
  if (!student || (!student.num_carte && !student.id)) {
    throw new Error("Aucun étudiant trouvé avec ce numéro de carte.");
  }

  return student;
};

export const updateStudentProfile = async (
  studentId: string | number,
  payload: StudentUpdatePayload
): Promise<StudentProfile> => {
  if (!studentId) {
    throw new Error("Missing student identifier for update.");
  }

  return apiRequest<StudentProfile>(`/students/${studentId}`, {
    method: "PUT",
    json: payload
  });
};

export const uploadStudentPicture = async (
  studentId: string | number,
  file: File
): Promise<StudentProfile> => {
  if (!studentId) {
    throw new Error("Missing student identifier for picture upload.");
  }

  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<StudentProfile>(`/students/${studentId}/picture`, {
    method: "POST",
    body: formData
  });
};

export const softDeleteStudent = async (
  studentId: string | number
): Promise<StudentProfile> => {
  if (!studentId) {
    throw new Error("Missing student identifier for delete.");
  }

  return apiRequest<StudentProfile>(`/students/${studentId}/soft_delete`, {
    method: "POST"
  });
};

export const studentService = {
  fetchStudentByCardNumber,
  updateStudentProfile,
  uploadStudentPicture,
  softDeleteStudent
};
