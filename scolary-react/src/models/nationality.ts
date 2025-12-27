export interface Nationality {
  id: number;
  name: string;
}

export interface NationalityOption {
  id: string;
  label: string;
}

export type NationalityPayload = Pick<Nationality, "name">;
export type NationalityListQuery = Record<
  string,
  string | number | boolean | undefined
>;
