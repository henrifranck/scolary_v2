import { Permission } from "./permission";

export interface RolePermissionAssignment {
  id: number;
  id_permission?: number | null;
  permission?: Pick<Permission, "id" | "name"> | null;
}

export interface Role {
  id: number;
  name: string;
  use_for_card?: boolean | null;
  permission_ids?: number[] | null;
  permissions?: Permission[] | null;
  role_permission?: RolePermissionAssignment[] | null;
}

export type RolePayload = Pick<Role, "name" | "use_for_card"> & {
  permission_ids: number[];
};
export type RoleListQuery = Record<
  string,
  string | number | boolean | undefined
>;
