export interface AcademicYear {
  id: number;
  name: string;
  code: string;
}

export type AcademicYearPayload = Pick<AcademicYear, "name" | "code">;
export type AcademicYearListQuery = Record<
  string,
  string | number | boolean | undefined
>;
