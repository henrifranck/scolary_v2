import { AcademicYear } from "./academic-year";
import { TeachingUnit } from "./teaching-unit";

export interface TeachingUnitOffering {
  id: number;
  id_teaching_unit?: number | null;
  credit?: number | null;
  id_academic_year?: number | null;
  id_teaching_unit_optional_group?: number | null;
  teaching_unit?: TeachingUnit | null;
  academic_year?: AcademicYear | null;
}

export type TeachingUnitOfferingPayload = Partial<TeachingUnitOffering>;

export type TeachingUnitOfferingListQuery = Record<
  string,
  string | number | boolean | undefined
>;
