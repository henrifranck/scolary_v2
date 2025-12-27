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
  useCreateClassroom,
  useDeleteClassroom,
  useClassrooms,
  useUpdateClassroom
} from "@/services/classroom-service";
import { Classroom, ClassroomPayload } from "@/models/classroom";

type ClassroomFormValues = {
  name: string;
  capacity?: Number;
};

const defaultFormValues: ClassroomFormValues = {
  name: "",
  capacity: 0
};

const toFormValues = (classroom?: Classroom | null): ClassroomFormValues => ({
  name: classroom?.name ?? "",
  capacity: classroom?.capacity
});

const toPayload = (values: ClassroomFormValues): ClassroomPayload => ({
  name: values.name.trim(),
  capacity: values.capacity
});

interface ClassroomFormProps {
  mode: "create" | "edit";
  initialValues?: ClassroomFormValues;
  isSubmitting: boolean;
  onSubmit: (values: ClassroomFormValues) => Promise<void>;
  onCancel: () => void;
}

const ClassroomForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting
}: ClassroomFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm<ClassroomFormValues>({
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
        <label className="text-sm font-medium" htmlFor="classroom-name">
          Name
        </label>
        <Input
          id="classroom-name"
          placeholder="e.g. Enter name"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="classroom-name">
          Capacité
        </label>
        <Input
          id="classroom-name"
          placeholder="e.g. Enter capacity"
          type="number"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("capacity", { required: "Capacity is required" })}
        />
        {errors.capacity ? (
          <p className="text-xs text-destructive">{errors.capacity.message}</p>
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
              : "Create classroom"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const ClassroomsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingClassroom, setEditingClassroom] = useState<Classroom | null>(
    null
  );
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [classroomToDelete, setClassroomToDelete] = useState<Classroom | null>(
    null
  );

  const offset = (page - 1) * pageSize;
  const {
    data: classroomsResponse,
    isPending,
    isError,
    error
  } = useClassrooms({ offset, limit: pageSize });
  const classrooms = classroomsResponse?.data ?? [];
  const totalClassrooms = classroomsResponse?.count ?? classrooms.length;
  const createClassroom = useCreateClassroom();
  const updateClassroom = useUpdateClassroom();
  const deleteClassroom = useDeleteClassroom();
  const openCreateForm = useCallback(() => {
    setEditingClassroom(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((classroom: Classroom) => {
    setEditingClassroom(classroom);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingClassroom(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: ClassroomFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingClassroom) {
          await updateClassroom.mutateAsync({
            id: editingClassroom.id,
            payload
          });
          setFeedback({
            type: "success",
            text: "Classroom updated successfully."
          });
        } else {
          await createClassroom.mutateAsync(payload);
          setFeedback({
            type: "success",
            text: "Classroom created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save classroom.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createClassroom, editingClassroom, updateClassroom]
  );

  const handleDelete = useCallback(async () => {
    if (!classroomToDelete) {
      return;
    }
    try {
      await deleteClassroom.mutateAsync(classroomToDelete.id);
      setFeedback({
        type: "success",
        text: "Classroom deleted successfully."
      });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete classroom.";
      setFeedback({ type: "error", text: message });
    } finally {
      setClassroomToDelete(null);
    }
  }, [deleteClassroom, classroomToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<Classroom>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Classroom",
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
            setConfirmDelete={setClassroomToDelete}
            handleEdit={handleEdit}
          />
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createClassroom.isPending || updateClassroom.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Classrooms</h1>
          <p className="text-sm text-muted-foreground">
            Control which roles can access each API resource.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add classroom
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
            setEditingClassroom(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingClassroom ? "Edit classroom" : "Create new classroom"}
            </DialogTitle>
            <DialogDescription>
              {editingClassroom
                ? "Update the classroom to align access rules."
                : "Define a classroom that can be associated with roles."}
            </DialogDescription>
          </DialogHeader>
          <ClassroomForm
            mode={editingClassroom ? "edit" : "create"}
            initialValues={toFormValues(editingClassroom)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(classroomToDelete)}
        title="Delete classroom"
        description={
          classroomToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>{classroomToDelete.name}</strong>? This action cannot be
              undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteClassroom.isPending}
        onCancel={() => setClassroomToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={classrooms}
        isLoading={isPending}
        searchPlaceholder="Search classrooms"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load classrooms")
            : "No classrooms found"
        }
        totalItems={totalClassrooms}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
