import { Check, X } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

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
import { useAvailableModels } from "../../../services/available-model-service";
import {
  useCreatePermission,
  useDeletePermission,
  usePermissions,
  useUpdatePermission
} from "../../../services/permission-service";
import {
  createModelHasPermission,
  deleteModelHasPermission,
  updateModelHasPermission
} from "@/services/model-has-permission-service";
import { ActionButton } from "@/components/action-button";
import {
  ModelHasPermission,
  Permission,
  PermissionListQuery,
  PermissionPayload
} from "@/models/permission";
import { fetchPermission } from "@/services/permission-service";
import { useAuth } from "@/providers/auth-provider";

type ModelAccess = {
  id?: number;
  id_available_model: number;
  model_label: string;
  show_from_menu: boolean;
  method_post: boolean;
  method_get: boolean;
  method_put: boolean;
  method_delete: boolean;
};

type Feedback = { type: "success" | "error"; text: string };

type MethodKey = "method_get" | "method_post" | "method_put" | "method_delete";

const normalizeRouteKey = (value: string) =>
  value.trim().toLowerCase().replace(/^\/+/, "");

const METHOD_LABELS: { key: MethodKey; label: string }[] = [
  { key: "method_get", label: "Lire" },
  { key: "method_post", label: "Créer" },
  { key: "method_put", label: "Modifier" },
  { key: "method_delete", label: "Supprimer" }
];

const getPermissionEntry = (
  permissionMap: Record<
    string,
    { get?: boolean; post?: boolean; put?: boolean; delete?: boolean }
  > | null,
  key: string
) => {
  if (!permissionMap) {
    return null;
  }
  const normalized = normalizeRouteKey(key);
  return (
    permissionMap[normalized] ||
    permissionMap[`/${normalized}`] ||
    permissionMap[key]
  );
};

const resolvePermissionKey = (
  path: string,
  availableModels: { route_ui: string; route_api: string; name: string }[]
) => {
  const match = availableModels.find((model) => {
    const routeUi = model.route_ui?.trim();
    if (!routeUi) {
      return false;
    }
    const candidates = routeUi.startsWith("/admin/")
      ? [routeUi, routeUi.replace(/^\/admin/, "")]
      : [routeUi, `/admin${routeUi}`];
    return candidates.some(
      (candidate) => path === candidate || path.startsWith(`${candidate}/`)
    );
  });
  if (match) {
    return normalizeRouteKey(match.route_api || match.name || "");
  }
  const parts = path.split("/").filter(Boolean);
  if (!parts.length) {
    return null;
  }
  const scopeIndex = parts[0] === "admin" ? 1 : 0;
  const candidate = parts[scopeIndex] ?? "";
  return normalizeRouteKey(candidate.replace(/-/g, "_"));
};

export const PermissionsPage = () => {
  const {
    state: { user }
  } = useAuth();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingPermission, setEditingPermission] = useState<Permission | null>(
    null
  );
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [permissionToDelete, setPermissionToDelete] =
    useState<Permission | null>(null);
  const [bulkName, setBulkName] = useState("");
  const [modelAccessList, setModelAccessList] = useState<ModelAccess[]>([]);
  const [formError, setFormError] = useState<string | null>(null);
  const [loadingPermission, setLoadingPermission] = useState(false);

  const offset = (page - 1) * pageSize;
  const {
    data: permissionsResponse,
    isPending,
    isError,
    error
  } = usePermissions({
    offset,
    limit: pageSize,
    relation: JSON.stringify([
      "model_has_permission{id,id_permission,id_available_model,method_get,method_post,method_put,method_delete,show_from_menu}",
      "model_has_permission.available_model{id,name,route_ui,route_api}"
    ])
  });
  const permissions = permissionsResponse?.data ?? [];
  const totalPermissions = permissionsResponse?.count ?? permissions.length;
  const createPermission = useCreatePermission();
  const updatePermission = useUpdatePermission();
  const deletePermission = useDeletePermission();
  const { data: availableModelsResponse, isPending: areModelsLoading } =
    useAvailableModels({ limit: 1000 });
  const availableModels = useMemo(
    () => availableModelsResponse?.data ?? [],
    [availableModelsResponse]
  );
  const availableModelMap = useMemo(() => {
    const map = new Map<number, string>();
    availableModels.forEach((model) => map.set(model.id, model.name));
    return map;
  }, [availableModels]);
  const getModelLabel = useCallback(
    (id: number, fallback?: string) =>
      availableModelMap.get(id) || fallback || `Modèle #${id}`,
    [availableModelMap]
  );
  const isSuperuser = Boolean(
    user?.is_superuser || user?.role === "superuser"
  );
  const permissionKey = useMemo(() => {
    const pathname =
      typeof window !== "undefined" ? window.location.pathname : "";
    return (
      resolvePermissionKey(pathname, availableModels) ??
      normalizeRouteKey("permissions")
    );
  }, [availableModels]);
  const currentPermissionEntry = useMemo(() => {
    const baseEntry = getPermissionEntry(user?.permissions ?? null, permissionKey);
    if (baseEntry || permissionKey === "permissions") {
      return baseEntry;
    }
    return getPermissionEntry(user?.permissions ?? null, "permissions");
  }, [permissionKey, user?.permissions]);
  const canEditPermission = isSuperuser || Boolean(currentPermissionEntry?.put);
  const canDeletePermission =
    isSuperuser || Boolean(currentPermissionEntry?.delete);
  const resetBulkForm = useCallback(() => {
    setBulkName(editingPermission?.name ?? "");
    setFormError(null);
    const baseAccess = availableModels.map((model) => {
      const existing = editingPermission?.model_has_permission?.find(
        (rel) => rel.id_available_model === model.id
      );
      const isEditingModel = Boolean(existing);
      return {
        id: existing?.id,
        id_available_model: model.id,
        model_label: model.name,
        show_from_menu:
          isEditingModel && existing?.show_from_menu !== undefined
            ? Boolean(existing.show_from_menu)
            : true,
        method_get: isEditingModel ? Boolean(existing?.method_get) : false,
        method_post: isEditingModel ? Boolean(existing?.method_post) : false,
        method_put: isEditingModel ? Boolean(existing?.method_put) : false,
        method_delete: isEditingModel ? Boolean(existing?.method_delete) : false
      };
    });

    const extraExisting =
      editingPermission?.model_has_permission
        ?.filter(
          (rel) =>
            rel.id_available_model &&
            !availableModels.some(
              (model) => model.id === rel.id_available_model
            )
        )
        .map((rel) => ({
          id: rel.id,
          id_available_model: rel.id_available_model,
          model_label:
            rel.available_model?.name ||
            availableModelMap.get(rel.id_available_model) ||
            `Modèle #${rel.id_available_model}`,
          show_from_menu:
            rel.show_from_menu === undefined
              ? true
              : Boolean(rel.show_from_menu),
          method_get: Boolean(rel.method_get),
          method_post: Boolean(rel.method_post),
          method_put: Boolean(rel.method_put),
          method_delete: Boolean(rel.method_delete)
        })) ?? [];

    setModelAccessList([...baseAccess, ...extraExisting]);
  }, [availableModelMap, availableModels, editingPermission]);

  const openCreateForm = useCallback(() => {
    setEditingPermission(null);
    resetBulkForm();
    setIsFormOpen(true);
  }, [resetBulkForm]);

  const handleEdit = useCallback(async (permission: Permission) => {
    setLoadingPermission(true);
    try {
      const full = await fetchPermission(permission.id);
      setEditingPermission(full);
    } catch {
      setEditingPermission(permission);
    } finally {
      setLoadingPermission(false);
      setIsFormOpen(true);
    }
  }, []);

  const closeForm = useCallback(() => {
    setEditingPermission(null);
    setIsFormOpen(false);
  }, []);

  useEffect(() => {
    if (isFormOpen) {
      resetBulkForm();
    }
  }, [availableModels, editingPermission, isFormOpen, resetBulkForm]);

  const handleSubmit = useCallback(async () => {
    setFormError(null);
    const trimmedName = bulkName.trim();
    if (!trimmedName) {
      setFormError("Le nom de la permission est requis.");
      return;
    }

    const selectedModels = modelAccessList.filter(
      (entry) =>
        entry.method_get ||
        entry.method_post ||
        entry.method_put ||
        entry.method_delete
    );

    if (!selectedModels.length) {
      setFormError("Sélectionnez au moins un modèle et une méthode.");
      return;
    }

    try {
      if (editingPermission) {
        await updatePermission.mutateAsync({
          id: editingPermission.id,
          payload: { name: trimmedName }
        });
        const operations = selectedModels.map(async (entry) => {
          if (entry.id) {
            if (
              !entry.method_get &&
              !entry.method_post &&
              !entry.method_put &&
              !entry.method_delete
            ) {
              await deleteModelHasPermission(entry.id);
              return;
            }
            await updateModelHasPermission(entry.id, {
              id_available_model: entry.id_available_model,
              show_from_menu: entry.show_from_menu,
              method_get: entry.method_get,
              method_post: entry.method_post,
              method_put: entry.method_put,
              method_delete: entry.method_delete
            });
            return;
          }
          await createModelHasPermission({
            id_permission: editingPermission.id,
            id_available_model: entry.id_available_model,
            show_from_menu: entry.show_from_menu,
            method_get: entry.method_get,
            method_post: entry.method_post,
            method_put: entry.method_put,
            method_delete: entry.method_delete
          });
        });
        await Promise.all(operations);
        setFeedback({
          type: "success",
          text: "Permission mise à jour."
        });
        closeForm();
      } else {
        const created = await createPermission.mutateAsync({
          name: trimmedName
        } as PermissionPayload);
        await Promise.all(
          selectedModels.map((entry) =>
            createModelHasPermission({
              id_permission: created.id,
              id_available_model: entry.id_available_model,
              show_from_menu: entry.show_from_menu,
              method_get: entry.method_get,
              method_post: entry.method_post,
              method_put: entry.method_put,
              method_delete: entry.method_delete
            })
          )
        );
        setFeedback({
          type: "success",
          text: "Permissions créées avec succès."
        });
        closeForm();
      }
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : editingPermission
            ? "Impossible de mettre à jour la permission."
            : "Impossible de créer les permissions.";
      setFeedback({ type: "error", text: message });
    }
  }, [
    bulkName,
    closeForm,
    createPermission,
    deleteModelHasPermission,
    editingPermission,
    modelAccessList,
    updateModelHasPermission,
    updatePermission
  ]);

  const handleDelete = useCallback(async () => {
    if (!permissionToDelete) {
      return;
    }
    try {
      await deletePermission.mutateAsync(permissionToDelete.id);
      setFeedback({
        type: "success",
        text: "Permission deleted successfully."
      });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete permission.";
      setFeedback({ type: "error", text: message });
    } finally {
      setPermissionToDelete(null);
    }
  }, [deletePermission, permissionToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<Permission>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Permission",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
          </div>
        )
      },
      {
        id: "methods",
        header: "Modèles & méthodes",
        cell: ({ row }) => {
          const entries = row.original.model_has_permission ?? [];
          const items =
            availableModels.length > 0
              ? [
                  ...availableModels.map((model) => ({
                    id: model.id,
                    label: model.name,
                    entry: entries.find(
                      (rel) => rel.id_available_model === model.id
                    )
                  })),
                  ...entries
                    .filter(
                      (rel) =>
                        rel.id_available_model &&
                        !availableModels.some(
                          (model) => model.id === rel.id_available_model
                        )
                    )
                    .map((rel) => ({
                      id: rel.id_available_model,
                      label: getModelLabel(
                        rel.id_available_model,
                        rel.available_model?.name
                      ),
                      entry: rel
                    }))
                ]
              : entries.map((rel) => ({
                  id: rel.id_available_model,
                  label: getModelLabel(
                    rel.id_available_model,
                    rel.available_model?.name
                  ),
                  entry: rel
                }));

          if (!items.length) {
            return (
              <span className="text-xs text-muted-foreground">
                Aucun modèle
              </span>
            );
          }
          return (
            <div className="grid grid-cols-1 gap-1.5 text-xs text-muted-foreground md:grid-cols-2">
              {items.map(({ id, label, entry }) => (
                <div
                  key={id}
                  className="flex flex-wrap items-start gap-2 rounded-lg border border-border/60 bg-muted/30 p-2"
                >
                  <span className="min-w-[120px] font-semibold text-foreground">
                    {label}
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {METHOD_LABELS.map(({ key, label }) => {
                      const isAllowed = Boolean(entry?.[key]);
                      return (
                        <span
                          key={key}
                          className={cn(
                            "inline-flex items-center gap-1 rounded border px-1.5 py-0.5 text-[11px] leading-tight",
                            isAllowed
                              ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                              : "border-destructive/30 bg-destructive/10 text-destructive"
                          )}
                        >
                          {isAllowed ? (
                            <Check className="h-3 w-3" />
                          ) : (
                            <X className="h-3 w-3" />
                          )}
                          {label}
                        </span>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          );
        }
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <ActionButton
            row={row}
            setConfirmDelete={setPermissionToDelete}
            handleEdit={handleEdit}
            allowEdit={canEditPermission}
            allowDelete={canDeletePermission}
          />
        )
      }
    ];
  }, [
    availableModels,
    canDeletePermission,
    canEditPermission,
    getModelLabel,
    handleEdit
  ]);

  const isSubmitting = createPermission.isPending || updatePermission.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Permissions</h1>
          <p className="text-sm text-muted-foreground">
            Control which roles can access each API resource.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add permissions
        </Button>
      </div>

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
            setEditingPermission(null);
          }
        }}
      >
        <DialogContent className="w-[95vw] max-w-6xl">
          <DialogHeader>
            <DialogTitle>
              {editingPermission
                ? "Edit permission"
                : "Create permissions in bulk"}
            </DialogTitle>
            <DialogDescription>
              {editingPermission
                ? "Update the permission to align access rules."
                : "Define a permission name and select access per model."}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Permission name</label>
              <Input
                placeholder="ex: Manage students"
                value={bulkName}
                onChange={(e) => setBulkName(e.target.value)}
                disabled={loadingPermission}
              />
            </div>
            <div className="rounded-xl border">
              <div className="grid grid-cols-[1fr_repeat(5,120px)] items-center gap-2 border-b px-4 py-3 text-sm font-medium">
                <span>Modèle</span>
                <span className="text-center">Lire</span>
                <span className="text-center">Créer</span>
                <span className="text-center">Modifier</span>
                <span className="text-center">Supprimer</span>
                <span className="text-center">Afficher menu</span>
              </div>
              <div className="max-h-[60vh] overflow-y-auto divide-y">
                {modelAccessList.map((entry, idx) => (
                  <div
                    key={entry.id_available_model}
                    className="grid grid-cols-[1fr_repeat(5,120px)] items-center gap-2 px-4 py-3 text-sm"
                  >
                    <span className="font-medium text-muted-foreground">
                      {getModelLabel(
                        entry.id_available_model,
                        entry.model_label
                      )}
                    </span>
                    {(
                      [
                        "method_get",
                        "method_post",
                        "method_put",
                        "method_delete"
                      ] as const
                    ).map((key) => (
                      <label
                        key={key}
                        className="flex items-center justify-center gap-2"
                      >
                        <input
                          type="checkbox"
                          checked={Boolean((modelAccessList[idx] as any)[key])}
                          onChange={(e) => {
                            const next = [...modelAccessList];
                            next[idx] = {
                              ...next[idx],
                              [key]: e.target.checked
                            };
                            setModelAccessList(next);
                          }}
                        />
                      </label>
                    ))}
                    <label className="flex items-center justify-center gap-2">
                      <input
                        type="checkbox"
                        checked={Boolean(entry.show_from_menu)}
                        onChange={(e) => {
                          const next = [...modelAccessList];
                          next[idx] = {
                            ...next[idx],
                            show_from_menu: e.target.checked
                          };
                          setModelAccessList(next);
                        }}
                      />
                    </label>
                  </div>
                ))}
              </div>
            </div>
            {formError ? (
              <p className="text-sm text-destructive">{formError}</p>
            ) : null}
            <div className="flex justify-end gap-2">
              <Button
                variant="ghost"
                onClick={closeForm}
                disabled={isSubmitting}
              >
                Cancel
              </Button>
              <Button onClick={handleSubmit} disabled={isSubmitting}>
                {isSubmitting
                  ? "Saving…"
                  : editingPermission
                    ? "Save changes"
                    : "Create"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(permissionToDelete)}
        title="Delete permission"
        description={
          permissionToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>{permissionToDelete.name}</strong>? This action cannot be
              undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deletePermission.isPending}
        onCancel={() => setPermissionToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={permissions}
        isLoading={isPending}
        searchPlaceholder="Search permissions"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load permissions")
            : "No permissions found"
        }
        totalItems={totalPermissions}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
