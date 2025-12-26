export interface RequiredDocument {
  id: number;
  name: string;
  description: string;
}

export type RequiredDocumentPayload = Pick<
  RequiredDocument,
  "name" | "description"
>;
export type RequiredDocumentListQuery = Record<
  string,
  string | number | boolean | undefined
>;
