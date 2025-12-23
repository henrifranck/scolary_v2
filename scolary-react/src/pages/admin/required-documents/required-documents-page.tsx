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
  type RequiredDocument,
  type RequiredDocumentPayload,
  useRequiredDocuments,
  useCreateRequiredDocument,
  useUpdateRequiredDocument,
  useDeleteRequiredDocument
} from '../../../services/required-document-service';

type RequiredDocumentFormValues = {
  name: string;
};

const defaultFormValues: RequiredDocumentFormValues = {
  name: ''
};

const toFormValues = (document?: RequiredDocument | null): RequiredDocumentFormValues => ({
  name: document?.name ?? ''
});

const toPayload = (values: RequiredDocumentFormValues): RequiredDocumentPayload => ({
  name: values.name.trim()
});

interface RequiredDocumentFormProps {
  mode: 'create' | 'edit';
  initialValues?: RequiredDocumentFormValues;
  isSubmitting: boolean;
  onSubmit: (values: RequiredDocumentFormValues) => Promise<void>;
  onCancel: () => void;
}

const RequiredDocumentForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting
}: RequiredDocumentFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<RequiredDocumentFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="required-document-name">
          Name
        </label>
        <Input
          id="required-document-name"
          placeholder="Proof of payment, ID, transcript..."
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
          {isSubmitting ? 'Saving…' : mode === 'edit' ? 'Save changes' : 'Create document'}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: 'success' | 'error'; text: string };

export const RequiredDocumentsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingDocument, setEditingDocument] = useState<RequiredDocument | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [documentToDelete, setDocumentToDelete] = useState<RequiredDocument | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: documentsResponse,
    isPending,
    isError,
    error
  } = useRequiredDocuments({ offset, limit: pageSize });
  const documents = documentsResponse?.data ?? [];
  const totalDocuments = documentsResponse?.count ?? documents.length;

  const createDocument = useCreateRequiredDocument();
  const updateDocument = useUpdateRequiredDocument();
  const deleteDocument = useDeleteRequiredDocument();

  const openCreateForm = useCallback(() => {
    setEditingDocument(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((document: RequiredDocument) => {
    setEditingDocument(document);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingDocument(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: RequiredDocumentFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingDocument) {
          await updateDocument.mutateAsync({ id: editingDocument.id, payload });
          setFeedback({ type: 'success', text: 'Document updated successfully.' });
        } else {
          await createDocument.mutateAsync(payload);
          setFeedback({ type: 'success', text: 'Document created successfully.' });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error ? mutationError.message : 'Unable to save the required document.';
        setFeedback({ type: 'error', text: message });
      }
    },
    [closeForm, createDocument, editingDocument, updateDocument]
  );

  const handleDelete = useCallback(async () => {
    if (!documentToDelete) {
      return;
    }
    try {
      await deleteDocument.mutateAsync(documentToDelete.id);
      setFeedback({ type: 'success', text: 'Document deleted successfully.' });
    } catch (mutationError) {
      const message = mutationError instanceof Error ? mutationError.message : 'Unable to delete the document.';
      setFeedback({ type: 'error', text: message });
    } finally {
      setDocumentToDelete(null);
    }
  }, [deleteDocument, documentToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextPageSize: number) => {
    setPageSize(nextPageSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<RequiredDocument>[]>(() => {
    return [
      {
        accessorKey: 'name',
        header: 'Name'
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
              onClick={() => setDocumentToDelete(row.original)}
            >
              Delete
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createDocument.isPending || updateDocument.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Required documents</h1>
          <p className="text-sm text-muted-foreground">Define the documents students must provide for services.</p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add document
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
            setEditingDocument(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingDocument ? 'Edit document' : 'Create new document'}</DialogTitle>
            <DialogDescription>
              {editingDocument
                ? 'Update the required document.'
                : 'Add a required document that can be linked to available services.'}
            </DialogDescription>
          </DialogHeader>
          <RequiredDocumentForm
            mode={editingDocument ? 'edit' : 'create'}
            initialValues={toFormValues(editingDocument)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(documentToDelete)}
        title="Delete document"
        description={
          documentToDelete ? (
            <>
              Are you sure you want to delete <strong>{documentToDelete.name}</strong>? This action cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteDocument.isPending}
        onCancel={() => setDocumentToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={documents}
        isLoading={isPending}
        searchPlaceholder="Search documents"
        emptyText={isError ? error?.message ?? 'Unable to load documents' : 'No documents found'}
        totalItems={totalDocuments}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
