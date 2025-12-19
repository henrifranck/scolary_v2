import { useCallback, useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";

import { Button } from "../../../components/ui/button";
import {
  DataTable,
  type ColumnDef
} from "../../../components/data-table/data-table";
import { ConfirmDialog } from "../../../components/confirm-dialog";
import { Input } from "../../../components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "../../../components/ui/dialog";
import { cn } from "../../../lib/utils";
import {
  type Role,
  type RolePayload,
  useCreateRole,
  useDeleteRole,
  useRoles,
  useUpdateRole
} from "../../../services/role-service";
import { usePermissions } from "../../../services/permission-service";

type RoleFormValues = {
  name: string;
  permissionIds: string[];
};

const defaultFormValues: RoleFormValues = {
  name: "",
  permissionIds: []
};

const toFormValues = (role?: Role | null): RoleFormValues => ({
  name: role?.name ?? "",
  permissionIds: (() => {
    if (!role) {
      return [];
    }

    const ids = new Set<number>();
    const addId = (value?: number | null) => {
      if (typeof value === "number" && Number.isFinite(value) && value > 0) {
        ids.add(value);
      }
    };

    role.permissions?.forEach((permission) => addId(permission?.id));
    role.role_permission?.forEach((assignment) => {
      addId(assignment.permission?.id);
      addId(assignment.id_permission);
    });
    role.permission_ids?.forEach(addId);

    return Array.from(ids).map((id) => String(id));
  })()
});

const toPayload = (values: RoleFormValues): RolePayload => {
  const permissionIds = (values.permissionIds ?? [])
    .map((permissionId) => Number(permissionId))
    .filter(
      (permissionId) => Number.isFinite(permissionId) && permissionId > 0
    );

  if (permissionIds.length === 0) {
    throw new Error("Select at least one permission");
  }

  return {
    name: values.name.trim(),
    permission_ids: Array.from(new Set(permissionIds))
  };
};

interface RoleFormProps {
  mode: "create" | "edit";
  initialValues?: RoleFormValues;
  isSubmitting: boolean;
  onSubmit: (values: RoleFormValues) => Promise<void>;
  onCancel: () => void;
  permissionOptions: { id: string; label: string }[];
  isPermissionsLoading: boolean;
}

const RoleForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  permissionOptions,
  isPermissionsLoading
}: RoleFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue
  } = useForm<RoleFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  useEffect(() => {
    register("permissionIds", {
      validate: (value) =>
        value?.length ? true : "Select at least one permission"
    });
  }, [register]);

  const selectedPermissionIds = watch("permissionIds") ?? [];
  const permissionSelectionError = (
    errors.permissionIds as { message?: string } | undefined
  )?.message;
  const handleCancel = () => {
    reset(initialValues ?? defaultFormValues);
    onCancel();
  };

  const togglePermissionSelection = (permissionId: string) => {
    setValue(
      "permissionIds",
      selectedPermissionIds.includes(permissionId)
        ? selectedPermissionIds.filter((id) => id !== permissionId)
        : [...selectedPermissionIds, permissionId],
      { shouldDirty: true, shouldValidate: true }
    );
  };
  const hasPermissionOptions = permissionOptions.length > 0;

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="role-name">
          Name
        </label>
        <Input
          id="role-name"
          placeholder="Administrator"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium">Permissions</label>
        <div className="rounded-md border border-input px-3 py-2">
          {isPermissionsLoading ? (
            <p className="text-sm text-muted-foreground">
              Loading permissions…
            </p>
          ) : hasPermissionOptions ? (
            <div className="space-y-2">
              {permissionOptions.map((permission) => {
                const checkboxId = `role-permission-${permission.id}`;
                const checked = selectedPermissionIds.includes(permission.id);
                return (
                  <label
                    key={permission.id}
                    className="flex items-center gap-2 text-sm"
                    htmlFor={checkboxId}
                  >
                    <input
                      id={checkboxId}
                      type="checkbox"
                      className="h-4 w-4 rounded border border-input text-primary"
                      checked={checked}
                      onChange={() => togglePermissionSelection(permission.id)}
                    />
                    <span
                      className={cn(
                        "flex-1",
                        !checked && "text-muted-foreground"
                      )}
                    >
                      {permission.label}
                    </span>
                  </label>
                );
              })}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              Create a permission first before assigning it to roles.
            </p>
          )}
        </div>
        {permissionSelectionError ? (
          <p className="text-xs text-destructive">{permissionSelectionError}</p>
        ) : null}
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button
          type="button"
          variant="ghost"
          onClick={handleCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? "Saving…"
            : mode === "edit"
              ? "Save changes"
              : "Create role"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const RolesPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingRole, setEditingRole] = useState<Role | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [roleToDelete, setRoleToDelete] = useState<Role | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: rolesResponse,
    isPending,
    isError,
    error
  } = useRoles({ offset, limit: pageSize });
  const {
    data: permissionsResponse,
    isPending: arePermissionsLoading,
    isError: isPermissionsError,
    error: permissionsError
  } = usePermissions();
  const roles = rolesResponse?.data ?? [];
  const totalRoles = rolesResponse?.count ?? roles.length;
  const permissionData = permissionsResponse?.data ?? [];
  const createRole = useCreateRole();
  const updateRole = useUpdateRole();
  const deleteRole = useDeleteRole();

  const openCreateForm = useCallback(() => {
    setEditingRole(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((role: Role) => {
    setEditingRole(role);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingRole(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: RoleFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingRole) {
          await updateRole.mutateAsync({ id: editingRole.id, payload });
          setFeedback({ type: "success", text: "Role updated successfully." });
        } else {
          await createRole.mutateAsync(payload);
          setFeedback({ type: "success", text: "Role created successfully." });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save role.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createRole, editingRole, updateRole]
  );

  const handleDelete = useCallback(
    async () => {
      if (!roleToDelete) {
        return;
      }
      try {
        await deleteRole.mutateAsync(roleToDelete.id);
        setFeedback({ type: "success", text: "Role deleted successfully." });
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to delete role.";
        setFeedback({ type: "error", text: message });
      } finally {
        setRoleToDelete(null);
      }
    },
    [deleteRole, roleToDelete]
  );

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const permissionOptions = useMemo(
    () =>
      permissionData.map((permission) => ({
        id: String(permission.id),
        label: permission.name
      })),
    [permissionData]
  );
  const permissionNameMap = useMemo(() => {
    const map = new Map<number, string>();
    permissionData.forEach((permission) => {
      if (typeof permission.id === "number" && permission.name) {
        map.set(permission.id, permission.name);
      }
    });
    return map;
  }, [permissionData]);
  const permissionsErrorMessage =
    isPermissionsError && permissionsError instanceof Error
      ? permissionsError.message
      : isPermissionsError
        ? "Unable to load permissions"
        : null;

  const resolvePermissionLabels = useCallback(
    (role: Role) => {
      const labels: string[] = [];
      const labelSet = new Set<string>();
      const addLabel = (label?: string | null) => {
        if (!label || labelSet.has(label)) {
          return;
        }
        labelSet.add(label);
        labels.push(label);
      };
      const idSet = new Set<number>();
      const addId = (id?: number | null) => {
        if (typeof id === "number" && Number.isFinite(id) && id > 0) {
          idSet.add(id);
        }
      };

      role.permissions?.forEach((permission) => {
        addLabel(permission?.name ?? null);
        addId(permission?.id);
      });
      role.role_permission?.forEach((assignment) => {
        const permissionId =
          assignment.permission?.id ?? assignment.id_permission;
        addId(permissionId);
        if (assignment.permission && "name" in assignment.permission) {
          addLabel(assignment.permission.name ?? null);
        }
      });
      role.permission_ids?.forEach(addId);

      if (labels.length === 0) {
        Array.from(idSet).forEach((id) =>
          addLabel(permissionNameMap.get(id) ?? `#${id}`)
        );
      } else {
        Array.from(idSet).forEach((id) => {
          const resolved = permissionNameMap.get(id);
          if (resolved && !labelSet.has(resolved)) {
            addLabel(resolved);
          }
        });
      }

      return labels;
    },
    [permissionNameMap]
  );

  const columns = useMemo<ColumnDef<Role>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Role",
        cell: ({ row }) => (
          <span className="font-medium">{row.original.name}</span>
        )
      },
      {
        accessorKey: "permission_names",
        header: "Permissions",
        cell: ({ row }) => {
          const labels = resolvePermissionLabels(row.original);
          return (
            <span className="text-sm text-muted-foreground">
              {labels.length ? labels.join(", ") : "—"}
            </span>
          );
        }
      },
      {
        id: "actions",
        header: "",
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleEdit(row.original)}
            >
              Edit
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="text-destructive hover:text-destructive"
              onClick={() => setRoleToDelete(row.original)}
            >
              Delete
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit, resolvePermissionLabels]);

  const isSubmitting = createRole.isPending || updateRole.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Roles</h1>
          <p className="text-sm text-muted-foreground">
            Manage Scolary roles and permissions labels.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Create role
        </Button>
      </div>

      {permissionsErrorMessage ? (
        <div className="rounded-md border border-destructive/30 bg-destructive/10 px-4 py-2 text-sm text-destructive">
          {permissionsErrorMessage}
        </div>
      ) : null}
      {!permissionsErrorMessage &&
      !arePermissionsLoading &&
      permissionOptions.length === 0 ? (
        <div className="rounded-md border border-amber-200 bg-amber-50 px-4 py-2 text-sm text-amber-800">
          Create at least one permission before editing roles.
        </div>
      ) : null}

      {feedback ? (
        <div
          className={cn(
            "flex items-start justify-between gap-4 rounded-md border px-4 py-3 text-sm",
            feedback.type === "success"
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-destructive/30 bg-destructive/10 text-destructive"
          )}
        >
          <span>{feedback.text}</span>
          <button
            className="text-xs font-medium underline"
            onClick={() => setFeedback(null)}
          >
            Dismiss
          </button>
        </div>
      ) : null}

      <Dialog
        open={isFormOpen}
        onOpenChange={(open) => {
          setIsFormOpen(open);
          if (!open) {
            setEditingRole(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingRole ? "Edit role" : "Create new role"}
            </DialogTitle>
            <DialogDescription>
              {editingRole
                ? "Update the role name to keep both panels aligned."
                : "Create a role that will be available to associate with users."}
            </DialogDescription>
          </DialogHeader>
          <RoleForm
            mode={editingRole ? "edit" : "create"}
            initialValues={toFormValues(editingRole)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            permissionOptions={permissionOptions}
            isPermissionsLoading={arePermissionsLoading}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(roleToDelete)}
        title="Delete role"
        description={
          roleToDelete ? (
            <>
              Are you sure you want to delete <strong>{roleToDelete.name}</strong>? This action cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteRole.isPending}
        onCancel={() => setRoleToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={roles}
        isLoading={isPending}
        searchPlaceholder="Search roles"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load roles")
            : "No roles found"
        }
        totalItems={totalRoles}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
