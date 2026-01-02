import { Mention } from "@/models/mentions";
import { apiRequest } from "./api-client";
import { normalizeList, isListResponse } from "./utils-common";
import { ApiListResponse } from "@/models/shared";

export type TrashStudent = {
  recordId: string;
  fullName: string;
  numSelect?: string;
  cardNumber?: string;
  deletedAt?: string;
  mention: string;
  level?: string;
};

type ApiStudent = {
  id?: string | number;
  first_name?: string | null;
  last_name?: string | null;
  num_select?: string | null;
  num_carte?: string | null;
  deleted_at?: string | null;
  mention?: Mention;
  level?: string | null;
  generated_level?: string | null;
};

type TrashListResponse = ApiListResponse<ApiStudent> | ApiStudent[];

const mapStudent = (student: ApiStudent): TrashStudent => {
  const fullName = [student.first_name, student.last_name]
    .filter(Boolean)
    .join(" ")
    .trim();
  return {
    recordId: student.id ? String(student.id) : "",
    fullName: fullName || "",
    numSelect: student.num_select ?? undefined,
    cardNumber: student.num_carte ?? undefined,
    deletedAt: student.deleted_at ?? undefined,
    mention: student.mention?.name || "",
    level: student.generated_level || student.level || ""
  };
};

export const fetchTrashedStudents = async (query?: {
  limit?: number;
  offset?: number;
}): Promise<{ data: TrashStudent[]; count?: number }> => {
  const response = await apiRequest<TrashListResponse>("/students/", {
    query: {
      ...(query ?? {}),
      include_deleted: true,
      where: JSON.stringify([
        {
          key: "deleted_at",
          operator: "isNotNull",
          value: ""
        }
      ]),
      relation: JSON.stringify(["mention{name}"])
    }
  });

  const data = normalizeList(response);
  const count = isListResponse(response) ? response.count : data.length;
  return {
    data: data.map(mapStudent),
    count
  };
};

export const restoreStudentById = (id: string | number) =>
  apiRequest(`/students/${id}/restore`, {
    method: "POST"
  });

export const hardDeleteStudentById = (id: string | number) =>
  apiRequest(`/students/${id}/hard_delete`, {
    method: "DELETE"
  });

export const trashService = {
  fetchTrashedStudents,
  restoreStudentById,
  hardDeleteStudentById
};
