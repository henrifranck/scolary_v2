export interface Mention {
  id: number | string;
  name: string;
  slug: string;
  abbreviation: string;
  id_plugged?: number | string | null;
  plugged?: string;
  background: string;
}

export interface MentionOption {
  id: string;
  label: string;
}

export interface MentionUser {
  id: number;
  id_mention: number;
  id_user: number;
  full_name?: string | null;
  email?: string | null;
  role?: string | null;
}

export type MentionPayload = Pick<
  Mention,
  "name" | "slug" | "abbreviation" | "background"
> & { id_plugged: number | string };

export type MentionListQuery = Record<
  string,
  string | number | boolean | undefined
>;
