export interface BaccalaureateSerie {
  id: number;
  name: string;
  value: string;
}

export type BaccalaureateSeriePayload = Pick<
  BaccalaureateSerie,
  "name" | "value"
>;
export type BaccalaureateSerieListQuery = Record<
  string,
  string | number | boolean | undefined
>;
