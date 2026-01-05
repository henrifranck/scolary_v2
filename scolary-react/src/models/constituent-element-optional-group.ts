export interface ConstituentElementOptionalGroup {
  id: number;
  name?: string | null;
  description?: string | null;
}

export type ConstituentElementOptionalGroupListQuery = Record<
  string,
  string | number | boolean | undefined
>;
