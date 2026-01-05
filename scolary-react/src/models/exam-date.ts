export interface ExamDate {
  id: number;
  id_academic_year: number;
  date_from: string;
  date_to: string;
  session?: string | null;
  year?: {
    id: number;
    name?: string | null;
  } | null;
  created_at?: string;
  updated_at?: string;
}

export type ExamDateListQuery = Record<
  string,
  string | number | boolean | undefined
>;
