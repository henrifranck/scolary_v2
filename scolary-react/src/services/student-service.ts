import { StudentProfile } from "@/components/student-form/student-form-types";
import { apiRequest } from "./api-client";
import { ReinscriptionFilters } from "./reinscription-service";

type OneStudentApiResponse =
  | StudentProfile
  | {
      data?: StudentProfile | null;
    };

export type StudentCreatePayload = Omit<StudentProfile, "id">;

const relations = JSON.stringify([
  "annual_register.register_semester",
  "annual_register.register_semester{id,id_annual_register,id_journey,semester,repeat_status}",
  "annual_register.register_semester.journey{id_mention,name}",
  "annual_register.register_semester.journey.mention{name}",
  "annual_register.payment{id,payed,num_receipt,date_receipt}",
  "annual_register.document{id,name,url,description,id_required_document}",
  "annual_register{max_semester_number,level_from_semester,total_payment,enrollment_fee_amount,payment_status}",
  "nationality{id,name}",
  "baccalaureate_serie{id,name}"
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
  "phone_number",
  "email",
  "num_of_cin",
  "date_of_cin",
  "place_of_cin",
  "sex",
  "martial_status",
  "num_of_baccalaureate",
  "center_of_baccalaureate",
  "job",
  "enrollment_status",
  "year_of_baccalaureate",
  "center_of_baccalaureate",
  "id_baccalaureate_series",
  "num_of_baccalaureate",
  "center_of_baccalaureate",
  "id_nationality",
  "mother_name",
  "mother_job",
  "father_name",
  "father_job",
  "parent_address"
]);

const buildWhereClause = (cardNumber: string) =>
  JSON.stringify([
    {
      key: "num_carte",
      operator: "==",
      value: cardNumber
    }
  ]);

const buildWhereCustomClause = (
  filter: ReinscriptionFilters,
  registerType: string,
  cardNumber: string
) =>
  JSON.stringify([
    {
      key: "id_academic_year",
      operator: "==",
      value: filter.id_year
    },
    {
      key: "register_type",
      operator: "==",
      value: registerType
    },
    {
      key: "num_carte",
      operator: "==",
      value: cardNumber
    }
  ]);

const buildWhereRelationClause = (
  filter: ReinscriptionFilters,
  registerType: string
) =>
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
    return payload.data ?? { id: null };
  }

  return payload as StudentProfile;
};

export const fetchStudentByCardNumber = async (
  filtes: ReinscriptionFilters,
  registerType: string,
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
        where_relation: buildWhereRelationClause(filtes, registerType),
        where_custom: buildWhereCustomClause(filtes, registerType, cardNumber),
        route_ui: "re-registration"
      }
    }
  );

  const student = extractStudent(response);
  if (!student || (!student.num_carte && !student.id)) {
    throw new Error("Aucun étudiant trouvé avec ce numéro de carte.");
  }

  return student;
};

export const fetchStudentByNumSelect = async (
  numSelect: string
): Promise<StudentProfile> => {
  const trimmed = numSelect.trim();
  if (!trimmed) {
    throw new Error("Le numéro de sélection est requis.");
  }

  const response = await apiRequest<OneStudentApiResponse>(
    "/students/one_student",
    {
      query: {
        relation: relations,
        base_column: baseColumn,
        where: JSON.stringify([
          { key: "num_select", operator: "==", value: trimmed }
        ]),
        route_ui: "re-registration"
      }
    }
  );

  const student = extractStudent(response);
  if (!student || (!student.num_select && !student.id)) {
    throw new Error("Aucun étudiant trouvé avec ce numéro de sélection.");
  }

  return student;
};

export const updateStudentProfile = async (
  studentId: string | number,
  payload: StudentProfile
): Promise<StudentProfile> => {
  if (!studentId) {
    throw new Error("Missing student identifier for update.");
  }

  return apiRequest<StudentProfile>(`/students/${studentId}`, {
    method: "PUT",
    json: payload
  });
};

export const createStudent = async (
  payload: StudentCreatePayload
): Promise<StudentProfile> => {
  return apiRequest<StudentProfile>("/students/", {
    method: "POST",
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

export const restoreStudent = async (
  studentId: string | number
): Promise<StudentProfile> => {
  if (!studentId) {
    throw new Error("Missing student identifier for restore.");
  }

  return apiRequest<StudentProfile>(`/students/${studentId}/restore`, {
    method: "POST"
  });
};

export const hardDeleteStudent = async (
  studentId: string | number
): Promise<void> => {
  if (!studentId) {
    throw new Error("Missing student identifier for delete.");
  }

  await apiRequest<void>(`/students/${studentId}/hard_delete`, {
    method: "DELETE"
  });
};

export const studentService = {
  fetchStudentByCardNumber,
  fetchStudentByNumSelect,
  updateStudentProfile,
  createStudent,
  uploadStudentPicture,
  softDeleteStudent,
  restoreStudent,
  hardDeleteStudent
};
