export interface ConstituentElementOptionalGroup {
  id: number;
  name?: string | null;
  description?: string | null;
  id_teaching_unit_offering?: number | null;
  selection_regle?: string | null;
  teaching_unit?: {
    id: number;
    credit?: number | null;
    academic_year?: {
      id: number;
      name?: string | null;
    } | null;
  } | null;
  created_at?: string;
  updated_at?: string;
}

export type ConstituentElementOptionalGroupListQuery = Record<
  string,
  string | number | boolean | undefined
>;
