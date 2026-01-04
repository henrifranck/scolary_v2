import { Pencil, Trash2 } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { DataTable, type ColumnDef } from "@/components/data-table/data-table";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import {
  usePluggeds,
  useCreatePlugged,
  useUpdatePlugged,
  useDeletePlugged
} from "@/services/plugged-service";
import { Plugged, PluggedPayload } from "@/models/plugged";
import { ActionButton } from "@/components/action-button";

type PluggedFormValues = {
  name: string;
};

const defaultFormValues: PluggedFormValues = { name: "" };

const toFormValues = (plugged?: Plugged | null): PluggedFormValues => ({
  name: plugged?.name ?? ""
});

const toPayload = (values: PluggedFormValues): PluggedPayload => ({
  name: values.name.trim()
});

type Feedback = { type: "success" | "error"; text: string };

export const PluggedPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingPlugged, setEditingPlugged] = useState<Plugged | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [pluggedToDelete, setPluggedToDelete] = useState<Plugged | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: pluggedResponse,
    isPending,
    isError,
    error
  } = usePluggeds({
    offset,
    limit: pageSize
  });
  const pluggedList = pluggedResponse?.data ?? [];
  const totalPlugged = pluggedResponse?.count ?? pluggedList.length;
  const createPlugged = useCreatePlugged();
  const updatePlugged = useUpdatePlugged();
  const deletePlugged = useDeletePlugged();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<PluggedFormValues>({ defaultValues: defaultFormValues });

  useEffect(() => {
    reset(toFormValues(editingPlugged));
  }, [editingPlugged, reset]);

  const openCreateForm = useCallback(() => {
    setEditingPlugged(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((plugged: Plugged) => {
    setEditingPlugged(plugged);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingPlugged(null);
    setIsFormOpen(false);
  }, []);

  const onSubmit = useCallback(
    async (values: PluggedFormValues) => {
      try {
        if (editingPlugged) {
          await updatePlugged.mutateAsync({
            id: editingPlugged.id,
            payload: toPayload(values)
          });
          setFeedback({
            type: "success",
            text: "Plugged updated successfully."
          });
        } else {
          await createPlugged.mutateAsync(toPayload(values));
          setFeedback({
            type: "success",
            text: "Plugged created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save plugged.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createPlugged, editingPlugged, updatePlugged]
  );

  const handleDelete = useCallback(async () => {
    if (!pluggedToDelete) return;
    try {
      await deletePlugged.mutateAsync(pluggedToDelete.id);
      setFeedback({ type: "success", text: "Plugged deleted successfully." });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete plugged.";
      setFeedback({ type: "error", text: message });
    } finally {
      setPluggedToDelete(null);
    }
  }, [deletePlugged, pluggedToDelete]);

  const handlePageChange = useCallback((next: number) => setPage(next), []);
  const handlePageSizeChange = useCallback((next: number) => {
    setPageSize(next);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<Plugged>[]>(
    () => [
      {
        accessorKey: "name",
        header: "Name",
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <span className="font-medium">{row.original.name}</span>
          </div>
        )
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          // <div className="flex items-center gap-2">
          //   <Button
          //     variant="ghost"
          //     size="icon"
          //     onClick={() => handleEdit(row.original)}
          //   >
          //     <Pencil className="h-4 w-4" />
          //   </Button>
          //   <Button
          //     variant="ghost"
          //     size="icon"
          //     onClick={() => setPluggedToDelete(row.original)}
          //   >
          //     <Trash2 className="h-4 w-4 text-destructive" />
          //   </Button>
          // </div>
          <ActionButton
            row={row}
            handleEdit={handleEdit}
            setConfirmDelete={setPluggedToDelete}
          />
        )
      }
    ],
    [handleEdit]
  );

  const isSubmitting =
    createPlugged.isPending ||
    updatePlugged.isPending ||
    deletePlugged.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Plugged</h1>
          <p className="text-sm text-muted-foreground">
            Manage plugged values to reuse across mentions.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add plugged
        </Button>
      </div>

      {feedback ? (
        <div
          className={cn(
            "rounded-md border px-3 py-2 text-sm",
            feedback.type === "success"
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-destructive/40 bg-destructive/10 text-destructive"
          )}
        >
          {feedback.text}
        </div>
      ) : null}

      <div className="rounded-lg border bg-background p-5 shadow-sm">
        <DataTable
          data={pluggedList}
          columns={columns}
          isLoading={isPending}
          totalItems={totalPlugged}
          page={page}
          pageSize={pageSize}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
        />
      </div>

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>
              {editingPlugged ? "Edit plugged" : "Create plugged"}
            </DialogTitle>
            <DialogDescription>
              {editingPlugged
                ? "Update the plugged entry."
                : "Create a plugged entry for mentions."}
            </DialogDescription>
          </DialogHeader>
          <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="plugged-name">
                Name
              </label>
              <Input
                id="plugged-name"
                placeholder="e.g. Computer science"
                className={cn(
                  errors.name && "border-destructive text-destructive"
                )}
                {...register("name", { required: "Name is required" })}
              />
              {errors.name ? (
                <p className="text-xs text-destructive">
                  {errors.name.message}
                </p>
              ) : null}
            </div>
            <div className="flex items-center justify-end gap-2">
              <Button type="button" variant="ghost" onClick={closeForm}>
                Cancel
              </Button>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting
                  ? "Saving…"
                  : editingPlugged
                    ? "Save changes"
                    : "Create plugged"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(pluggedToDelete)}
        title="Delete plugged"
        description={
          pluggedToDelete ? (
            <>
              Delete <strong>{pluggedToDelete.name}</strong>? This action cannot
              be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        onCancel={() => setPluggedToDelete(null)}
        onConfirm={handleDelete}
        isConfirming={deletePlugged.isPending}
      />
    </div>
  );
};
