import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Pencil, Plus, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { DataTable, type ColumnDef } from "@/components/data-table/data-table";
import {
  createNotificationTemplate,
  fetchNotificationTemplates,
  deleteNotificationTemplate,
  updateNotificationTemplate,
  type NotificationTemplate
} from "@/services/notification-template-service";
import { ConfirmDialog } from "@/components/confirm-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { fetchRoles } from "@/services/role-service";

type TemplateForm = {
  key: string;
  title: string;
  template: string;
  target_roles: string[];
};

export const NotificationTemplatesPage = () => {
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState<NotificationTemplate | null>(null);
  const [formValues, setFormValues] = useState<TemplateForm>({
    key: "",
    title: "",
    template: "",
    target_roles: []
  });
  const [confirmDelete, setConfirmDelete] = useState<NotificationTemplate | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const templatesQuery = useQuery({
    queryKey: ["notification-templates"],
    queryFn: async () => {
      const res = await fetchNotificationTemplates();
      return res || [];
    }
  });
  const rolesQuery = useQuery({
    queryKey: ["roles", "notification-templates"],
    queryFn: () => fetchRoles({ limit: 200 }),
    staleTime: 5 * 60 * 1000
  });

  const createMutation = useMutation({
    mutationFn: createNotificationTemplate,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notification-templates"] })
  });
  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: TemplateForm }) =>
      updateNotificationTemplate(id, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notification-templates"] })
  });
  const deleteMutation = useMutation({
    mutationFn: (id: number) => deleteNotificationTemplate(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notification-templates"] })
  });

  const handleSubmit = async () => {
    if (!formValues.key.trim() || !formValues.template.trim() || !formValues.title.trim()) return;
    if (editing) {
      await updateMutation.mutateAsync({ id: editing.id, payload: formValues });
    } else {
      await createMutation.mutateAsync(formValues);
    }
    setFormValues({ key: "", title: "", template: "", target_roles: [] });
    setEditing(null);
    setIsDialogOpen(false);
  };

  const columns = useMemo<ColumnDef<NotificationTemplate>[]>(
    () => [
      {
        accessorKey: "title",
        header: "Titre",
        cell: ({ row }) => <span className="font-medium">{row.original.title}</span>
      },
      {
        accessorKey: "key",
        header: "Clé",
        cell: ({ row }) => <span className="font-medium">{row.original.key}</span>
      },
      {
        accessorKey: "template",
        header: "Modèle",
        cell: ({ row }) => (
          <div className="text-sm whitespace-pre-wrap text-muted-foreground max-w-xl">
            {row.original.template}
          </div>
        )
      },
      {
        accessorKey: "target_roles",
        header: "Rôles cibles",
        cell: ({ row }) => {
          const roles = row.original.target_roles ?? [];
          if (!roles.length) return <span className="text-muted-foreground">Tous</span>;
          return <span className="text-sm text-muted-foreground">{roles.join(", ")}</span>;
        }
      },
      {
        id: "actions",
        header: "",
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button
              size="icon"
              variant="ghost"
              onClick={() => {
                setEditing(row.original);
                setFormValues({
                  key: row.original.key,
                  title: row.original.title,
                  template: row.original.template,
                  target_roles: row.original.target_roles ?? []
                });
                setIsDialogOpen(true);
              }}
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              size="icon"
              variant="ghost"
              className="text-destructive"
              onClick={() => setConfirmDelete(row.original)}
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        )
      }
    ],
    []
  );

  const tableData = templatesQuery.data ?? [];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Modèles de notifications
          </h1>
          <p className="text-sm text-muted-foreground">
            Définissez des modèles textuels pour les notifications système. Utilisez des
            variables entre accolades, par ex. {"{num_carte}"} ou {"{year}"}.
          </p>
        </div>
        <Button
          size="sm"
          className="gap-2"
          onClick={() => {
            setEditing(null);
            setFormValues({ key: "", title: "", template: "" });
            setIsDialogOpen(true);
          }}
        >
          <Plus className="h-4 w-4" />
          Nouveau modèle
        </Button>
      </div>

      <DataTable
        columns={columns}
        data={tableData}
        isLoading={templatesQuery.isLoading}
        searchPlaceholder="Rechercher un modèle"
      />

      <ConfirmDialog
        open={Boolean(confirmDelete)}
        title="Supprimer le modèle"
        description={
          confirmDelete ? (
            <>
              Supprimer le modèle <strong>{confirmDelete.key}</strong> ?
            </>
          ) : null
        }
        destructive
        confirmLabel="Supprimer"
        isConfirming={deleteMutation.isPending}
        onCancel={() => setConfirmDelete(null)}
        onConfirm={async () => {
          if (!confirmDelete) return;
          try {
            await deleteMutation.mutateAsync(confirmDelete.id);
          } catch (error) {
            console.error(error);
          } finally {
            setConfirmDelete(null);
          }
        }}
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editing ? "Modifier le modèle" : "Nouveau modèle"}
            </DialogTitle>
            <DialogDescription>
              Utilisez des variables entre accolades, par ex. {"{num_carte}"} ou {"{year}"}.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3">
            <div className="space-y-2">
              <label className="text-sm font-medium">Clé</label>
              <Input
                placeholder="ex: annual_register_created"
                value={formValues.key}
                onChange={(e) =>
                  setFormValues((prev) => ({ ...prev, key: e.target.value }))
                }
                disabled={Boolean(editing)}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Titre</label>
              <Input
                placeholder="ex: Nouvelle inscription annuelle"
                value={formValues.title}
                onChange={(e) =>
                  setFormValues((prev) => ({ ...prev, title: e.target.value }))
                }
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Modèle</label>
              <Textarea
                rows={6}
                placeholder="Nouvelle inscription annuelle: carte {num_carte} pour l'année {year}"
                value={formValues.template}
                onChange={(e) =>
                  setFormValues((prev) => ({ ...prev, template: e.target.value }))
                }
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <label className="text-sm font-medium">Rôles ciblés</label>
                <span className="text-xs text-muted-foreground">
                  Vide = visible par tous
                </span>
              </div>
              <div className="grid gap-2 rounded-md border p-3 max-h-52 overflow-y-auto">
                {(rolesQuery.data?.data ?? []).map((role) => {
                  const checked = formValues.target_roles.includes(role.name);
                  return (
                    <label
                      key={role.id}
                      className="flex items-center gap-2 text-sm"
                    >
                      <input
                        type="checkbox"
                        className="h-4 w-4"
                        checked={checked}
                        onChange={(e) => {
                          const next = e.target.checked
                            ? [...formValues.target_roles, role.name]
                            : formValues.target_roles.filter((r) => r !== role.name);
                          setFormValues((prev) => ({ ...prev, target_roles: next }));
                        }}
                      />
                      <span>{role.name}</span>
                    </label>
                  );
                })}
                {!rolesQuery.data?.data?.length && (
                  <p className="text-sm text-muted-foreground">
                    Aucun rôle disponible.
                  </p>
                )}
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                Annuler
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={
                  createMutation.isPending ||
                  updateMutation.isPending ||
                  !formValues.key.trim() ||
                  !formValues.title.trim() ||
                  !formValues.template.trim()
                }
              >
                {editing
                  ? updateMutation.isPending
                    ? "Mise à jour..."
                    : "Mettre à jour"
                  : createMutation.isPending
                    ? "Création..."
                    : "Enregistrer"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};
