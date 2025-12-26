export interface Permission {
  id: number;
  name: string;
  model_name: string;
  method_post?: boolean;
  method_get?: boolean;
  method_put?: boolean;
  method_delete?: boolean;
}

export type PermissionPayload = Pick<
  Permission,
  | "name"
  | "model_name"
  | "method_post"
  | "method_get"
  | "method_put"
  | "method_delete"
>;
export type PermissionListQuery = Record<
  string,
  string | number | boolean | undefined
>;
