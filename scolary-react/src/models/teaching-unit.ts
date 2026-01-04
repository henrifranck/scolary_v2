import { Journey } from "./journey";

export interface TeachingUnit {
  id: number;
  name: string;
  semester: string;
  id_journey: number;
  journey?: Journey | null;
}

export type TeachingUnitPayload = Pick<
  TeachingUnit,
  "name" | "semester" | "id_journey"
> & { id_journey: number | string };

export type TeachingUnitListQuery = Record<
  string,
  string | number | boolean | undefined
>;
