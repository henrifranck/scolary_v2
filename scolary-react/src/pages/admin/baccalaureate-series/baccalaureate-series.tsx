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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "../../../components/ui/select";
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
  useCreateBaccalaureateSerie,
  useDeleteBaccalaureateSerie,
  useBaccalaureateSeries,
  useUpdateBaccalaureateSerie
} from "../../../services/baccalaureate-series-service";
import { ActionButton } from "@/components/action-button";
import {
  BaccalaureateSerie,
  BaccalaureateSeriePayload
} from "@/models/baccalaureate-series";

type BaccalaureateSerieFormValues = {
  name: string;
  value: string;
};

const defaultFormValues: BaccalaureateSerieFormValues = {
  name: "",
  value: ""
};

const toFormValues = (
  baccalaureateSerie?: BaccalaureateSerie | null
): BaccalaureateSerieFormValues => ({
  name: baccalaureateSerie?.name ?? "",
  value: baccalaureateSerie?.value ?? ""
});

const toPayload = (
  values: BaccalaureateSerieFormValues
): BaccalaureateSeriePayload => ({
  name: values.name.trim(),
  value: values.value.trim()
});

interface BaccalaureateSerieFormProps {
  mode: "create" | "edit";
  initialValues?: BaccalaureateSerieFormValues;
  availableModels: Array<{ id: string; name: string }>;
  isModelsLoading: boolean;
  isSubmitting: boolean;
  onSubmit: (values: BaccalaureateSerieFormValues) => Promise<void>;
  onCancel: () => void;
}

const BaccalaureateSerieForm = ({
  mode,
  initialValues,
  availableModels,
  isModelsLoading,
  onSubmit,
  onCancel,
  isSubmitting
}: BaccalaureateSerieFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm<BaccalaureateSerieFormValues>({
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
        <label
          className="text-sm font-medium"
          htmlFor="baccalaureate-serie-name"
        >
          Name
        </label>
        <Input
          id="baccalaureate-serie-name"
          placeholder="e.g. Manage Users"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>

      <div className="space-y-2">
        <label
          className="text-sm font-medium"
          htmlFor="baccalaureate-serie-name"
        >
          Value
        </label>
        <Input
          id="baccalaureate-serie-name"
          placeholder="Serie A"
          className={cn(errors.value && "border-destructive text-destructive")}
          {...register("value", { required: "Value is required" })}
        />
        {errors.value ? (
          <p className="text-xs text-destructive">{errors.value.message}</p>
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
              : "Create baccalaureate-serie"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const BaccalaureateSeriesPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingBaccalaureateSerie, setEditingBaccalaureateSerie] =
    useState<BaccalaureateSerie | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [baccalaureateSerieToDelete, setBaccalaureateSerieToDelete] =
    useState<BaccalaureateSerie | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: baccalaureateSeriesResponse,
    isPending,
    isError,
    error
  } = useBaccalaureateSeries({ offset, limit: pageSize });
  const baccalaureateSeries = baccalaureateSeriesResponse?.data ?? [];
  const totalBaccalaureateSeries =
    baccalaureateSeriesResponse?.count ?? baccalaureateSeries.length;
  const createBaccalaureateSerie = useCreateBaccalaureateSerie();
  const updateBaccalaureateSerie = useUpdateBaccalaureateSerie();
  const deleteBaccalaureateSerie = useDeleteBaccalaureateSerie();
  const { data: availableModelsResponse, isPending: areModelsLoading } =
    useAvailableModels({ limit: 1000 });
  const availableModels = useMemo(
    () =>
      (availableModelsResponse?.data ?? []).map((model) => ({
        id: String(model.id),
        name: model.name
      })),
    [availableModelsResponse]
  );

  const openCreateForm = useCallback(() => {
    setEditingBaccalaureateSerie(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((baccalaureateSerie: BaccalaureateSerie) => {
    setEditingBaccalaureateSerie(baccalaureateSerie);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingBaccalaureateSerie(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: BaccalaureateSerieFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingBaccalaureateSerie) {
          await updateBaccalaureateSerie.mutateAsync({
            id: editingBaccalaureateSerie.id,
            payload
          });
          setFeedback({
            type: "success",
            text: "BaccalaureateSerie updated successfully."
          });
        } else {
          await createBaccalaureateSerie.mutateAsync(payload);
          setFeedback({
            type: "success",
            text: "BaccalaureateSerie created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save baccalaureate-serie.";
        setFeedback({ type: "error", text: message });
      }
    },
    [
      closeForm,
      createBaccalaureateSerie,
      editingBaccalaureateSerie,
      updateBaccalaureateSerie
    ]
  );

  const handleDelete = useCallback(async () => {
    if (!baccalaureateSerieToDelete) {
      return;
    }
    try {
      await deleteBaccalaureateSerie.mutateAsync(baccalaureateSerieToDelete.id);
      setFeedback({
        type: "success",
        text: "BaccalaureateSerie deleted successfully."
      });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete baccalaureate-serie.";
      setFeedback({ type: "error", text: message });
    } finally {
      setBaccalaureateSerieToDelete(null);
    }
  }, [deleteBaccalaureateSerie, baccalaureateSerieToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<BaccalaureateSerie>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "BaccalaureateSerie",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
          </div>
        )
      },
      {
        accessorKey: "value",
        header: "Value",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.value}
          </span>
        )
      },

      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <ActionButton
            row={row}
            setConfirmDelete={setBaccalaureateSerieToDelete}
            handleEdit={handleEdit}
          />
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting =
    createBaccalaureateSerie.isPending || updateBaccalaureateSerie.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            BaccalaureateSeries
          </h1>
          <p className="text-sm text-muted-foreground">
            Control which roles can access each API resource.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add baccalaureate-serie
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
            setEditingBaccalaureateSerie(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingBaccalaureateSerie
                ? "Edit baccalaureate-serie"
                : "Create new baccalaureate-serie"}
            </DialogTitle>
            <DialogDescription>
              {editingBaccalaureateSerie
                ? "Update the baccalaureate-serie to align access rules."
                : "Define a baccalaureate-serie that can be associated with roles."}
            </DialogDescription>
          </DialogHeader>
          <BaccalaureateSerieForm
            mode={editingBaccalaureateSerie ? "edit" : "create"}
            initialValues={toFormValues(editingBaccalaureateSerie)}
            availableModels={availableModels}
            isModelsLoading={areModelsLoading}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(baccalaureateSerieToDelete)}
        title="Delete baccalaureate-serie"
        description={
          baccalaureateSerieToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>{baccalaureateSerieToDelete.name}</strong>? This action
              cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteBaccalaureateSerie.isPending}
        onCancel={() => setBaccalaureateSerieToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={baccalaureateSeries}
        isLoading={isPending}
        searchPlaceholder="Search baccalaureate-series"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load baccalaureate-series")
            : "No baccalaureate-series found"
        }
        totalItems={totalBaccalaureateSeries}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
