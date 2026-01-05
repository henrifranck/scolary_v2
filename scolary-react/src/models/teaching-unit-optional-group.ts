export interface TeachingUnitOptionalGroup {
  id: number;
  name?: string | null;
  description?: string | null;
}

export type TeachingUnitOptionalGroupListQuery = Record<
  string,
  string | number | boolean | undefined
>;
