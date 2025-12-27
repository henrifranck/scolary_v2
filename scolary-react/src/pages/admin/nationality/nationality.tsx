import { Pencil, Trash2 } from "lucide-react";
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
import { ActionButton } from "@/components/action-button";
import {
  useCreateNationality,
  useDeleteNationality,
  useNationalitys,
  useUpdateNationality
} from "@/services/nationality-service";
import { Nationality, NationalityPayload } from "@/models/nationality";

type NationalityFormValues = {
  name: string;
};

const defaultFormValues: NationalityFormValues = {
  name: ""
};

const toFormValues = (
  nationality?: Nationality | null
): NationalityFormValues => ({
  name: nationality?.name ?? ""
});

const toPayload = (values: NationalityFormValues): NationalityPayload => ({
  name: values.name.trim()
});

interface NationalityFormProps {
  mode: "create" | "edit";
  initialValues?: NationalityFormValues;
  isSubmitting: boolean;
  onSubmit: (values: NationalityFormValues) => Promise<void>;
  onCancel: () => void;
}

const NationalityForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting
}: NationalityFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm<NationalityFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  const methodOptions = [
    { key: "method_get", label: "Lire" },
    { key: "method_post", label: "Créer" },
    { key: "method_put", label: "Modifier" },
    { key: "method_delete", label: "Supprimer" }
  ] as const;

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="nationality-name">
          Name
        </label>
        <Input
          id="nationality-name"
          placeholder="e.g. Manage Users"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button
          type="button"
          variant="ghost"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? "Saving…"
            : mode === "edit"
              ? "Save changes"
              : "Create nationality"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const NationalitysPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingNationality, setEditingNationality] =
    useState<Nationality | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [nationalityToDelete, setNationalityToDelete] =
    useState<Nationality | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: nationalitysResponse,
    isPending,
    isError,
    error
  } = useNationalitys({ offset, limit: pageSize });
  const nationalitys = nationalitysResponse?.data ?? [];
  const totalNationalitys = nationalitysResponse?.count ?? nationalitys.length;
  const createNationality = useCreateNationality();
  const updateNationality = useUpdateNationality();
  const deleteNationality = useDeleteNationality();
  const openCreateForm = useCallback(() => {
    setEditingNationality(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((nationality: Nationality) => {
    setEditingNationality(nationality);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingNationality(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: NationalityFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingNationality) {
          await updateNationality.mutateAsync({
            id: editingNationality.id,
            payload
          });
          setFeedback({
            type: "success",
            text: "Nationality updated successfully."
          });
        } else {
          await createNationality.mutateAsync(payload);
          setFeedback({
            type: "success",
            text: "Nationality created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save nationality.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createNationality, editingNationality, updateNationality]
  );

  const handleDelete = useCallback(async () => {
    if (!nationalityToDelete) {
      return;
    }
    try {
      await deleteNationality.mutateAsync(nationalityToDelete.id);
      setFeedback({
        type: "success",
        text: "Nationality deleted successfully."
      });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete nationality.";
      setFeedback({ type: "error", text: message });
    } finally {
      setNationalityToDelete(null);
    }
  }, [deleteNationality, nationalityToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<Nationality>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Nationality",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
          </div>
        )
      },

      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <ActionButton
            row={row}
            setConfirmDelete={setNationalityToDelete}
            handleEdit={handleEdit}
          />
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting =
    createNationality.isPending || updateNationality.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Nationalitys
          </h1>
          <p className="text-sm text-muted-foreground">
            Control which roles can access each API resource.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add nationality
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
            setEditingNationality(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingNationality
                ? "Edit nationality"
                : "Create new nationality"}
            </DialogTitle>
            <DialogDescription>
              {editingNationality
                ? "Update the nationality to align access rules."
                : "Define a nationality that can be associated with roles."}
            </DialogDescription>
          </DialogHeader>
          <NationalityForm
            mode={editingNationality ? "edit" : "create"}
            initialValues={toFormValues(editingNationality)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(nationalityToDelete)}
        title="Delete nationality"
        description={
          nationalityToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>{nationalityToDelete.name}</strong>? This action cannot be
              undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteNationality.isPending}
        onCancel={() => setNationalityToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={nationalitys}
        isLoading={isPending}
        searchPlaceholder="Search nationalitys"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load nationalitys")
            : "No nationalitys found"
        }
        totalItems={totalNationalitys}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
