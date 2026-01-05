import { Teacher } from "@/services/teacher-service";
import { AcademicYear } from "./academic-year";
import { ConstituentElement } from "./constituent-element";
import { Journey } from "./journey";

export interface ConstituentElementOffering {
  id: number;
  id_constituent_element?: number | null;
  id_academic_year?: number | null;
  id_teacher?: number | null;
  id_constituent_element_optional_group?: number | null;
  id_teching_unit_offering?: number | null;
  weight?: number | null;
  constituent_element?:
    | (ConstituentElement & { journey?: Journey | null })
    | null;
  academic_year?: AcademicYear | null;
  teacher?: Teacher;
}

export type ConstituentElementOfferingListQuery = Record<
  string,
  string | number | boolean | undefined
>;
