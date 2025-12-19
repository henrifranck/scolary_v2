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
  type Mention,
  type MentionPayload,
  useCreateMention,
  useDeleteMention,
  useMentions,
  useUpdateMention
} from '../../../services/mention-service';

type MentionFormValues = {
  name: string;
  slug: string;
  abbreviation: string;
  plugged: string;
  background: string;
};

const defaultFormValues: MentionFormValues = {
  name: '',
  slug: '',
  abbreviation: '',
  plugged: '',
  background: ''
};

const toFormValues = (mention?: Mention | null): MentionFormValues => ({
  name: mention?.name ?? '',
  slug: mention?.slug ?? '',
  abbreviation: mention?.abbreviation ?? '',
  plugged: mention?.plugged ?? '',
  background: mention?.background ?? ''
});

const toPayload = (values: MentionFormValues): MentionPayload => ({
  name: values.name.trim(),
  slug: values.slug.trim(),
  abbreviation: values.abbreviation.trim(),
  plugged: values.plugged.trim(),
  background: values.background.trim()
});

interface MentionFormProps {
  mode: 'create' | 'edit';
  initialValues?: MentionFormValues;
  isSubmitting: boolean;
  onSubmit: (values: MentionFormValues) => Promise<void>;
  onCancel: () => void;
}

const MentionForm = ({ mode, initialValues, onSubmit, onCancel, isSubmitting }: MentionFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<MentionFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="mention-name">
          Name
        </label>
        <Input
          id="mention-name"
          placeholder="e.g. Génie logiciel"
          className={cn(errors.name && 'border-destructive text-destructive')}
          {...register('name', { required: 'Name is required' })}
        />
        {errors.name ? <p className="text-xs text-destructive">{errors.name.message}</p> : null}
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="mention-slug">
            Slug
          </label>
          <Input
            id="mention-slug"
            placeholder="genie-logiciel"
            className={cn(errors.slug && 'border-destructive text-destructive')}
            {...register('slug', { required: 'Slug is required' })}
          />
          {errors.slug ? <p className="text-xs text-destructive">{errors.slug.message}</p> : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="mention-abbreviation">
            Abbreviation
          </label>
          <Input
            id="mention-abbreviation"
            placeholder="GL"
            className={cn(errors.abbreviation && 'border-destructive text-destructive')}
            {...register('abbreviation', { required: 'Abbreviation is required' })}
          />
          {errors.abbreviation ? (
            <p className="text-xs text-destructive">{errors.abbreviation.message}</p>
          ) : null}
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="mention-plugged">
            Plugged
          </label>
          <Input
            id="mention-plugged"
            placeholder="e.g. Computer science"
            className={cn(errors.plugged && 'border-destructive text-destructive')}
            {...register('plugged', { required: 'Plugged value is required' })}
          />
          {errors.plugged ? <p className="text-xs text-destructive">{errors.plugged.message}</p> : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="mention-background">
            Background
          </label>
          <Input
            id="mention-background"
            placeholder="#1f2937"
            className={cn(errors.background && 'border-destructive text-destructive')}
            {...register('background', { required: 'Background is required' })}
          />
          {errors.background ? <p className="text-xs text-destructive">{errors.background.message}</p> : null}
        </div>
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'edit' ? 'Save changes' : 'Create mention'}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: 'success' | 'error'; text: string };

export const MentionsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingMention, setEditingMention] = useState<Mention | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [mentionToArchive, setMentionToArchive] = useState<Mention | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: mentionsResponse,
    isPending,
    isError,
    error
  } = useMentions({ offset, limit: pageSize });
  const mentions = mentionsResponse?.data ?? [];
  const totalMentions = mentionsResponse?.count ?? mentions.length;
  const createMention = useCreateMention();
  const updateMention = useUpdateMention();
  const deleteMention = useDeleteMention();

  const openCreateForm = useCallback(() => {
    setEditingMention(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((mention: Mention) => {
    setEditingMention(mention);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingMention(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: MentionFormValues) => {
      try {
        if (editingMention) {
          await updateMention.mutateAsync({ id: editingMention.id, payload: toPayload(values) });
          setFeedback({ type: 'success', text: 'Mention updated successfully.' });
        } else {
          await createMention.mutateAsync(toPayload(values));
          setFeedback({ type: 'success', text: 'Mention created successfully.' });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error ? mutationError.message : 'Unable to save mention.';
        setFeedback({ type: 'error', text: message });
      }
    },
    [createMention, updateMention, editingMention, closeForm]
  );

  const handleDelete = useCallback(
    async () => {
      if (!mentionToArchive) {
        return;
      }
      try {
        await deleteMention.mutateAsync(mentionToArchive.id);
        setFeedback({ type: 'success', text: 'Mention archived successfully.' });
      } catch (mutationError) {
        const message =
          mutationError instanceof Error ? mutationError.message : 'Unable to archive mention.';
        setFeedback({ type: 'error', text: message });
      } finally {
        setMentionToArchive(null);
      }
    },
    [deleteMention, mentionToArchive]
  );

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<Mention>[]>(() => {
    return [
      {
        accessorKey: 'name',
        header: 'Mention',
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
            <span className="text-xs text-muted-foreground">/{row.original.slug}</span>
          </div>
        )
      },
      {
        accessorKey: 'abbreviation',
        header: 'Abbreviation',
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{row.original.abbreviation}</span>
      },
      {
        accessorKey: 'plugged',
        header: 'Plugged',
        cell: ({ row }) => <span className="text-sm text-muted-foreground">{row.original.plugged}</span>
      },
      {
        id: 'background',
        header: 'Background',
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <span className="h-4 w-4 rounded-full border" style={{ background: row.original.background }} />
            <span className="text-sm text-muted-foreground">{row.original.background}</span>
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
              onClick={() => setMentionToArchive(row.original)}
            >
              Archive
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createMention.isPending || updateMention.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Mentions</h1>
          <p className="text-sm text-muted-foreground">
            Manage academic mentions and keep them aligned with their departments.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add mention
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
            setEditingMention(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingMention ? 'Edit mention' : 'Create new mention'}</DialogTitle>
            <DialogDescription>
              {editingMention
                ? 'Update the mention to keep the Angular and React panels aligned.'
                : 'Create a mention that will be available across the platform.'}
            </DialogDescription>
          </DialogHeader>
          <MentionForm
            mode={editingMention ? 'edit' : 'create'}
            initialValues={toFormValues(editingMention)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(mentionToArchive)}
        title="Archive mention"
        description={
          mentionToArchive ? (
            <>
              Are you sure you want to archive <strong>{mentionToArchive.name}</strong>? This action cannot be
              undone.
            </>
          ) : null
        }
        confirmLabel="Archive"
        destructive
        isConfirming={deleteMention.isPending}
        onCancel={() => setMentionToArchive(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={mentions}
        isLoading={isPending}
        searchPlaceholder="Search mentions"
        emptyText={isError ? error?.message ?? 'Unable to load mentions' : 'No mentions found'}
        totalItems={totalMentions}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
