import { useCallback, useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';

import { Button } from '../../../components/ui/button';
import { DataTable, type ColumnDef } from '../../../components/data-table/data-table';
import { ConfirmDialog } from '../../../components/confirm-dialog';
import { Input } from '../../../components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '../../../components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '../../../components/ui/dialog';
import { cn } from '../../../lib/utils';
import { useAvailableModels } from '../../../services/available-model-service';
import {
  type Permission,
  type PermissionPayload,
  useCreatePermission,
  useDeletePermission,
  usePermissions,
  useUpdatePermission
} from '../../../services/permission-service';

type PermissionFormValues = {
  name: string;
  model_name: string;
  method_post: boolean;
  method_get: boolean;
  method_put: boolean;
  method_delete: boolean;
};

const defaultFormValues: PermissionFormValues = {
  name: '',
  model_name: '',
  method_post: false,
  method_get: false,
  method_put: false,
  method_delete: false
};

const toFormValues = (permission?: Permission | null): PermissionFormValues => ({
  name: permission?.name ?? '',
  model_name: permission?.model_name ?? '',
  method_post: Boolean(permission?.method_post),
  method_get: Boolean(permission?.method_get),
  method_put: Boolean(permission?.method_put),
  method_delete: Boolean(permission?.method_delete)
});

const toPayload = (values: PermissionFormValues): PermissionPayload => ({
  name: values.name.trim(),
  model_name: values.model_name.trim(),
  method_post: values.method_post,
  method_get: values.method_get,
  method_put: values.method_put,
  method_delete: values.method_delete
});

interface PermissionFormProps {
  mode: 'create' | 'edit';
  initialValues?: PermissionFormValues;
  availableModels: Array<{ id: string; name: string }>;
  isModelsLoading: boolean;
  isSubmitting: boolean;
  onSubmit: (values: PermissionFormValues) => Promise<void>;
  onCancel: () => void;
}

const PermissionForm = ({
  mode,
  initialValues,
  availableModels,
  isModelsLoading,
  onSubmit,
  onCancel,
  isSubmitting
}: PermissionFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm<PermissionFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  const selectedModel = watch('model_name');

  const methodOptions = [
    { key: 'method_get', label: 'Lire' },
    { key: 'method_post', label: 'Créer' },
    { key: 'method_put', label: 'Modifier' },
    { key: 'method_delete', label: 'Supprimer' }
  ] as const;

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="permission-name">
          Name
        </label>
        <Input
          id="permission-name"
          placeholder="e.g. Manage Users"
          className={cn(errors.name && 'border-destructive text-destructive')}
          {...register('name', { required: 'Name is required' })}
        />
        {errors.name ? <p className="text-xs text-destructive">{errors.name.message}</p> : null}
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="permission-model">
          Model name
        </label>
        <input type="hidden" {...register('model_name', { required: 'Model name is required' })} />
        <Select
          value={selectedModel}
          onValueChange={(value) => setValue('model_name', value, { shouldDirty: true })}
          disabled={isModelsLoading || availableModels.length === 0}
        >
          <SelectTrigger id="permission-model">
            <SelectValue placeholder={isModelsLoading ? 'Loading models…' : 'Select a model'} />
          </SelectTrigger>
          <SelectContent>
            {availableModels.map((model) => (
              <SelectItem key={model.id} value={model.name}>
                {model.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {errors.model_name ? <p className="text-xs text-destructive">{errors.model_name.message}</p> : null}
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium">Methods</label>
        <div className="grid gap-2 sm:grid-cols-2">
          {methodOptions.map((option) => {
            const inputId = `permission-${option.key}`;
            return (
              <label key={option.key} className="flex items-center gap-2 text-sm">
                <input id={inputId} type="checkbox" {...register(option.key)} />
                {option.label}
              </label>
            );
          })}
        </div>
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'edit' ? 'Save changes' : 'Create permission'}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: 'success' | 'error'; text: string };

export const PermissionsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingPermission, setEditingPermission] = useState<Permission | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [permissionToDelete, setPermissionToDelete] = useState<Permission | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: permissionsResponse,
    isPending,
    isError,
    error
  } = usePermissions({ offset, limit: pageSize });
  const permissions = permissionsResponse?.data ?? [];
  const totalPermissions = permissionsResponse?.count ?? permissions.length;
  const createPermission = useCreatePermission();
  const updatePermission = useUpdatePermission();
  const deletePermission = useDeletePermission();
  const { data: availableModelsResponse, isPending: areModelsLoading } = useAvailableModels({ limit: 1000 });
  const availableModels = useMemo(
    () =>
      (availableModelsResponse?.data ?? []).map((model) => ({
        id: String(model.id),
        name: model.name
      })),
    [availableModelsResponse]
  );

  const openCreateForm = useCallback(() => {
    setEditingPermission(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((permission: Permission) => {
    setEditingPermission(permission);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingPermission(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: PermissionFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingPermission) {
          await updatePermission.mutateAsync({ id: editingPermission.id, payload });
          setFeedback({ type: 'success', text: 'Permission updated successfully.' });
        } else {
          await createPermission.mutateAsync(payload);
          setFeedback({ type: 'success', text: 'Permission created successfully.' });
        }
        closeForm();
      } catch (mutationError) {
        const message = mutationError instanceof Error ? mutationError.message : 'Unable to save permission.';
        setFeedback({ type: 'error', text: message });
      }
    },
    [closeForm, createPermission, editingPermission, updatePermission]
  );

  const handleDelete = useCallback(
    async () => {
      if (!permissionToDelete) {
        return;
      }
      try {
        await deletePermission.mutateAsync(permissionToDelete.id);
        setFeedback({ type: 'success', text: 'Permission deleted successfully.' });
      } catch (mutationError) {
        const message = mutationError instanceof Error ? mutationError.message : 'Unable to delete permission.';
        setFeedback({ type: 'error', text: message });
      } finally {
        setPermissionToDelete(null);
      }
    },
    [deletePermission, permissionToDelete]
  );

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
        accessorKey: 'name',
        header: 'Permission',
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
            <span className="text-xs text-muted-foreground">{row.original.model_name}</span>
          </div>
        )
      },
      {
        accessorKey: 'model_name',
        header: 'Model',
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{row.original.model_name}</span>
      },
      {
        id: 'methods',
        header: 'Methods',
        cell: ({ row }) => (
          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-muted-foreground">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={Boolean(row.original.method_get)} readOnly />
              Lire
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={Boolean(row.original.method_post)} readOnly />
              Créer
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={Boolean(row.original.method_put)} readOnly />
              Modifier
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={Boolean(row.original.method_delete)} readOnly />
              Supprimer
            </label>
          </div>
        )
      },
      {
        id: 'actions',
        header: '',
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button size="sm" variant="outline" onClick={() => handleEdit(row.original)}>
              Edit
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="text-destructive hover:text-destructive"
              onClick={() => setPermissionToDelete(row.original)}
            >
              Delete
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createPermission.isPending || updatePermission.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Permissions</h1>
          <p className="text-sm text-muted-foreground">Control which roles can access each API resource.</p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add permission
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
            setEditingPermission(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingPermission ? 'Edit permission' : 'Create new permission'}</DialogTitle>
            <DialogDescription>
              {editingPermission
                ? 'Update the permission to align access rules.'
                : 'Define a permission that can be associated with roles.'}
            </DialogDescription>
          </DialogHeader>
          <PermissionForm
            mode={editingPermission ? 'edit' : 'create'}
            initialValues={toFormValues(editingPermission)}
            availableModels={availableModels}
            isModelsLoading={areModelsLoading}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(permissionToDelete)}
        title="Delete permission"
        description={
          permissionToDelete ? (
            <>
              Are you sure you want to delete <strong>{permissionToDelete.name}</strong>? This action cannot be undone.
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
        emptyText={isError ? error?.message ?? 'Unable to load permissions' : 'No permissions found'}
        totalItems={totalPermissions}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
