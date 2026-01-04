import { Journey } from "./journey";

export interface ConstituentElement {
  id: number;
  name: string;
  semester: string;
  color: string;
  id_journey: number;
  journey?: Journey | null;
}

export type ConstituentElementPayload = Pick<
  ConstituentElement,
  "name" | "semester" | "id_journey" | "color"
> & { id_journey: number | string };

export type ConstituentElementListQuery = Record<
  string,
  string | number | boolean | undefined
>;
