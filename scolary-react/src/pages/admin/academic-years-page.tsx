import { Pencil, Trash2 } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';

import { Button } from '../../components/ui/button';
import { DataTable, type ColumnDef } from '../../components/data-table/data-table';
import { ConfirmDialog } from '../../components/confirm-dialog';
import { Input } from '../../components/ui/input';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '../../components/ui/dialog';
import { cn } from '../../lib/utils';
import {
  type AcademicYear,
  type AcademicYearPayload,
  useAcademicYears,
  useCreateAcademicYear,
  useUpdateAcademicYear,
  useDeleteAcademicYear
} from '../../services/academic-year-service';

type AcademicYearFormValues = {
  name: string;
  code: string;
};

const defaultFormValues: AcademicYearFormValues = {
  name: '',
  code: ''
};

const toFormValues = (year?: AcademicYear | null): AcademicYearFormValues => ({
  name: year?.name ?? '',
  code: year?.code ?? ''
});

const toPayload = (values: AcademicYearFormValues): AcademicYearPayload => ({
  name: values.name.trim(),
  code: values.code.trim()
});

interface AcademicYearFormProps {
  mode: 'create' | 'edit';
  initialValues?: AcademicYearFormValues;
  isSubmitting: boolean;
  onSubmit: (values: AcademicYearFormValues) => Promise<void>;
  onCancel: () => void;
}

const generateAcademicYearCode = () => {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_@#';
  return Array.from({ length: 8 })
    .map(() => characters[Math.floor(Math.random() * characters.length)])
    .join('');
};

const AcademicYearForm = ({ mode, initialValues, onSubmit, onCancel, isSubmitting }: AcademicYearFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm<AcademicYearFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  useEffect(() => {
    if (!initialValues?.code) {
      const generated = generateAcademicYearCode();
      setValue('code', generated, { shouldDirty: false, shouldValidate: true });
    }
  }, [initialValues, setValue]);

  const codeValue = watch('code');

  const handleRegenerate = useCallback(() => {
    const generated = generateAcademicYearCode();
    setValue('code', generated, { shouldDirty: true, shouldValidate: true });
  }, [setValue]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="year-name">
          Name
        </label>
        <Input
          id="year-name"
          placeholder="2024 / 2025"
          className={cn(errors.name && 'border-destructive text-destructive')}
          {...register('name', { required: 'Name is required' })}
        />
        {errors.name ? <p className="text-xs text-destructive">{errors.name.message}</p> : null}
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="year-code">
          Code
        </label>
        <div className="flex items-center gap-2">
          <Input
            id="year-code"
            placeholder="2024-2025"
            className={cn(errors.code && 'border-destructive text-destructive')}
            disabled
            value={codeValue || ''}
            {...register('code', { required: 'Code is required' })}
          />
          <Button type="button" variant="outline" size="sm" onClick={handleRegenerate} disabled={isSubmitting}>
            Regenerate
          </Button>
        </div>
        {errors.code ? <p className="text-xs text-destructive">{errors.code.message}</p> : null}
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'edit' ? 'Save changes' : 'Create academic year'}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: 'success' | 'error'; text: string };

export const AcademicYearsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingYear, setEditingYear] = useState<AcademicYear | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [yearToDelete, setYearToDelete] = useState<AcademicYear | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: academicYearsResponse,
    isPending,
    isError,
    error
  } = useAcademicYears({ offset, limit: pageSize });
  const academicYears = academicYearsResponse?.data ?? [];
  const totalAcademicYears = academicYearsResponse?.count ?? academicYears.length;
  const createAcademicYear = useCreateAcademicYear();
  const updateAcademicYear = useUpdateAcademicYear();
  const deleteAcademicYear = useDeleteAcademicYear();

  const openCreateForm = useCallback(() => {
    setEditingYear(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((year: AcademicYear) => {
    setEditingYear(year);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingYear(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: AcademicYearFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingYear) {
          await updateAcademicYear.mutateAsync({ id: editingYear.id, payload });
          setFeedback({ type: 'success', text: 'Academic year updated successfully.' });
        } else {
          await createAcademicYear.mutateAsync(payload);
          setFeedback({ type: 'success', text: 'Academic year created successfully.' });
        }
        closeForm();
      } catch (mutationError) {
        const message = mutationError instanceof Error ? mutationError.message : 'Unable to save academic year.';
        setFeedback({ type: 'error', text: message });
      }
    },
    [closeForm, createAcademicYear, editingYear, updateAcademicYear]
  );

  const handleDelete = useCallback(
    async () => {
      if (!yearToDelete) {
        return;
      }
      try {
        await deleteAcademicYear.mutateAsync(yearToDelete.id);
        setFeedback({ type: 'success', text: 'Academic year deleted successfully.' });
      } catch (mutationError) {
        const message = mutationError instanceof Error ? mutationError.message : 'Unable to delete academic year.';
        setFeedback({ type: 'error', text: message });
      } finally {
        setYearToDelete(null);
      }
    },
    [deleteAcademicYear, yearToDelete]
  );

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<AcademicYear>[]>(() => {
    return [
      {
        accessorKey: 'name',
        header: 'Academic year',
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
            <span className="text-xs text-muted-foreground">{row.original.code}</span>
          </div>
        )
      },
      {
        accessorKey: 'code',
        header: 'Code',
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{row.original.code}</span>
      },
      {
        id: 'actions',
        header: '',
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button
              size="icon"
              variant="ghost"
              onClick={() => handleEdit(row.original)}
              aria-label="Editer"
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              size="icon"
              variant="ghost"
              className="text-destructive hover:text-destructive"
              onClick={() => setYearToDelete(row.original)}
              aria-label="Supprimer"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createAcademicYear.isPending || updateAcademicYear.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Academic years</h1>
          <p className="text-sm text-muted-foreground">Manage academic years available across the platform.</p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add academic year
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
            setEditingYear(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingYear ? 'Edit academic year' : 'Create new academic year'}</DialogTitle>
            <DialogDescription>
              {editingYear
                ? 'Update the academic year to keep both panels aligned.'
                : 'Create an academic year that will be available across the platform.'}
            </DialogDescription>
          </DialogHeader>
          <AcademicYearForm
            mode={editingYear ? 'edit' : 'create'}
            initialValues={toFormValues(editingYear)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(yearToDelete)}
        title="Delete academic year"
        description={
          yearToDelete ? (
            <>
              Are you sure you want to delete <strong>{yearToDelete.name}</strong>? This action cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteAcademicYear.isPending}
        onCancel={() => setYearToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={academicYears}
        isLoading={isPending}
        searchPlaceholder="Search academic years"
        emptyText={isError ? error?.message ?? 'Unable to load academic years' : 'No academic years found'}
        totalItems={totalAcademicYears}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
