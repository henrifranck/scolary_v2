export interface Plugged {
  id: number;
  name: string;
}

export type PluggedPayload = Pick<Plugged, "name">;

export type PluggedListQuery = Record<
  string,
  string | number | boolean | undefined
>;
