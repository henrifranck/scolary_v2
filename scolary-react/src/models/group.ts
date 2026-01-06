import { Journey } from "./journey";

export interface Group {
  id: number;
  id_journey?: number;
  id_academic_year?: number | null;
  semester?: string | null;
  group_number?: number | null;
  student_count?: number | null;
  start_number?: number | null;
  end_number?: number | null;
  journey?: Journey | null;
  academic_year?: { id: number; name?: string | null } | null;
}

export type GroupListQuery = Record<
  string,
  string | number | boolean | undefined
>;

export type CreateGroupPayload = {
  id_journey: number;
  semester: string;
  group_number?: number | null;
  student_count?: number | null;
  id_academic_year?: number | null;
  start_number?: number | null;
  end_number?: number | null;
};
