export interface Permission {
  id: number;
  name: string;
  model_has_permission?: ModelHasPermission[];
}

export type PermissionPayload = {
  name: string;
};

export interface ModelHasPermission {
  id: number;
  id_permission: number;
  id_available_model: number;
  available_model?: {
    id: number;
    name: string;
    route_api?: string;
    route_ui?: string;
  };
  show_from_menu?: boolean;
  method_post?: boolean;
  method_get?: boolean;
  method_put?: boolean;
  method_delete?: boolean;
}

export type ModelHasPermissionPayload = Omit<
  ModelHasPermission,
  "id" | "model_has_permission" | "id_permission" | "available_model"
> & { id_permission: number };
export type PermissionListQuery = Record<
  string,
  string | number | boolean | undefined
>;
