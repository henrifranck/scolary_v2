import { Journey } from "./journey";

export interface Group {
  id: number;
  id_journey?: number;
  semester?: string | null;
  group_number?: number | null;
  student_count?: number | null;
  journey?: Journey | null;
}

export type GroupListQuery = Record<
  string,
  string | number | boolean | undefined
>;
