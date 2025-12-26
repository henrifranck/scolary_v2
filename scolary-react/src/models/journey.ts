import { Mention } from "./mentions";

export type JourneySemester =
  | string
  | {
      id?: number | null;
      semester?: string | null;
    };

export interface Journey {
  id: number;
  name: string;
  abbreviation: string;
  id_mention: number | string;
  mention?: Mention;
  semester_list?: JourneySemester[] | null;
}

export interface JourneyUser {
  id: number;
  id_journey: number;
  id_user: number;
  full_name?: string | null;
  email?: string | null;
  role?: string | null;
}

export type JourneyPayload = {
  name: string;
  abbreviation: string;
  id_mention: number;
  semester_list: string[];
};

export type JourneyListQuery = Record<
  string,
  string | number | boolean | undefined
>;
