import { useCallback, useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';

import { Button } from '../../../components/ui/button';
import { DataTable, type ColumnDef } from '../../../components/data-table/data-table';
import { ConfirmDialog } from '../../../components/confirm-dialog';
import { Input } from '../../../components/ui/input';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '../../../components/ui/dialog';
import { cn } from '../../../lib/utils';
import {
  type AvailableModel,
  type AvailableModelPayload,
  useAvailableModels,
  useCreateAvailableModel,
  useUpdateAvailableModel,
  useDeleteAvailableModel
} from '../../../services/available-model-service';

type AvailableModelFormValues = {
  name: string;
};

const defaultFormValues: AvailableModelFormValues = {
  name: ''
};

const toFormValues = (model?: AvailableModel | null): AvailableModelFormValues => ({
  name: model?.name ?? ''
});

const toPayload = (values: AvailableModelFormValues): AvailableModelPayload => ({
  name: values.name.trim()
});

interface AvailableModelFormProps {
  mode: 'create' | 'edit';
  initialValues?: AvailableModelFormValues;
  isSubmitting: boolean;
  onSubmit: (values: AvailableModelFormValues) => Promise<void>;
  onCancel: () => void;
}

const AvailableModelForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting
}: AvailableModelFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<AvailableModelFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="available-model-name">
          Name
        </label>
        <Input
          id="available-model-name"
          placeholder="Student, Payment, Role..."
          className={cn(errors.name && 'border-destructive text-destructive')}
          {...register('name', { required: 'Name is required' })}
        />
        {errors.name ? <p className="text-xs text-destructive">{errors.name.message}</p> : null}
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'edit' ? 'Save changes' : 'Create model'}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: 'success' | 'error'; text: string };

export const AvailableModelsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingModel, setEditingModel] = useState<AvailableModel | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [modelToDelete, setModelToDelete] = useState<AvailableModel | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: modelsResponse,
    isPending,
    isError,
    error
  } = useAvailableModels({ offset, limit: pageSize });
  const models = modelsResponse?.data ?? [];
  const totalModels = modelsResponse?.count ?? models.length;

  const createModel = useCreateAvailableModel();
  const updateModel = useUpdateAvailableModel();
  const deleteModel = useDeleteAvailableModel();

  const openCreateForm = useCallback(() => {
    setEditingModel(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((model: AvailableModel) => {
    setEditingModel(model);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingModel(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: AvailableModelFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingModel) {
          await updateModel.mutateAsync({ id: editingModel.id, payload });
          setFeedback({ type: 'success', text: 'Model updated successfully.' });
        } else {
          await createModel.mutateAsync(payload);
          setFeedback({ type: 'success', text: 'Model created successfully.' });
        }
        closeForm();
      } catch (mutationError) {
        const message = mutationError instanceof Error ? mutationError.message : 'Unable to save model.';
        setFeedback({ type: 'error', text: message });
      }
    },
    [closeForm, createModel, editingModel, updateModel]
  );

  const handleDelete = useCallback(async () => {
    if (!modelToDelete) {
      return;
    }
    try {
      await deleteModel.mutateAsync(modelToDelete.id);
      setFeedback({ type: 'success', text: 'Model deleted successfully.' });
    } catch (mutationError) {
      const message = mutationError instanceof Error ? mutationError.message : 'Unable to delete model.';
      setFeedback({ type: 'error', text: message });
    } finally {
      setModelToDelete(null);
    }
  }, [deleteModel, modelToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextPageSize: number) => {
    setPageSize(nextPageSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<AvailableModel>[]>(() => {
    return [
      {
        accessorKey: 'name',
        header: 'Model'
      },
      {
        id: 'actions',
        header: 'Actions',
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={() => handleEdit(row.original)}>
              Edit
            </Button>
            <Button
              variant="ghost"
              className="text-destructive hover:text-destructive"
              onClick={() => setModelToDelete(row.original)}
            >
              Delete
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createModel.isPending || updateModel.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Available models</h1>
          <p className="text-sm text-muted-foreground">Manage model names for permission scoping.</p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add model
        </Button>
      </div>

      {feedback ? (
        <div
          className={cn(
            'flex items-start justify-between gap-4 rounded-md border px-4 py-3 text-sm',
            feedback.type === 'success'
              ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
              : 'border-destructive/30 bg-destructive/10 text-destructive'
          )}
        >
          <span>{feedback.text}</span>
          <button className="text-xs font-medium underline" onClick={() => setFeedback(null)}>
            Dismiss
          </button>
        </div>
      ) : null}

      <Dialog
        open={isFormOpen}
        onOpenChange={(open) => {
          setIsFormOpen(open);
          if (!open) {
            setEditingModel(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingModel ? 'Edit model' : 'Create new model'}</DialogTitle>
            <DialogDescription>
              {editingModel ? 'Update the available model.' : 'Add a model that can be used in permissions.'}
            </DialogDescription>
          </DialogHeader>
          <AvailableModelForm
            mode={editingModel ? 'edit' : 'create'}
            initialValues={toFormValues(editingModel)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(modelToDelete)}
        title="Delete model"
        description={
          modelToDelete ? (
            <>
              Are you sure you want to delete <strong>{modelToDelete.name}</strong>? This action cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteModel.isPending}
        onCancel={() => setModelToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={models}
        isLoading={isPending}
        searchPlaceholder="Search models"
        emptyText={isError ? error?.message ?? 'Unable to load models' : 'No models found'}
        totalItems={totalModels}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
