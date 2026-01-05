export interface TeachingUnitOptionalGroup {
  id: number;
  name?: string | null;
  description?: string | null;
  id_journey?: number | null;
  semester?: string | null;
  selection_regle?: string | null;
  journey?: {
    id: number;
    name?: string | null;
    abbreviation?: string | null;
    id_mention?: number | null;
  } | null;
  created_at?: string;
  updated_at?: string;
}

export type TeachingUnitOptionalGroupListQuery = Record<
  string,
  string | number | boolean | undefined
>;
