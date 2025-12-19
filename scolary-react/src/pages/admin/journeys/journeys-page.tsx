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
import {
  Journey,
  JourneyPayload,
  useCreateJourney,
  useDeleteJourney,
  useJourneys,
  useUpdateJourney
} from "@/services/journey-service";
import { Mention, useMentions } from "@/services/mention-service";

type JourneyFormValues = {
  name: string;
  abbreviation: string;
  mentionId: string;
  semesterList: string[];
};

const defaultFormValues: JourneyFormValues = {
  name: "",
  abbreviation: "",
  mentionId: "",
  semesterList: []
};

const toFormValues = (journey?: Journey | null): JourneyFormValues => {
  const semesterList = Array.isArray(journey?.semester_list)
    ? journey.semester_list
        .map((entry) =>
          typeof entry === "string" ? entry : entry?.semester ?? null
        )
        .filter((value): value is string => Boolean(value))
    : [];

  return {
    name: journey?.name ?? "",
    abbreviation: journey?.abbreviation ?? "",
    mentionId: journey?.id_mention ? String(journey.id_mention) : "",
    semesterList
  };
};

const semesterOptions = Array.from({ length: 10 }, (_, index) => `S${index + 1}`);

const toPayload = (values: JourneyFormValues): JourneyPayload => {
  const mentionId = Number(values.mentionId);
  if (!Number.isFinite(mentionId) || mentionId <= 0) {
    throw new Error("Mention is required");
  }

  const semesters = (values.semesterList ?? []).filter((semester) =>
    semesterOptions.includes(semester)
  );
  if (semesters.length === 0) {
    throw new Error("Select at least one semester");
  }

  return {
    name: values.name.trim(),
    abbreviation: values.abbreviation.trim(),
    id_mention: mentionId,
    semester_list: Array.from(new Set(semesters))
  };
};

interface JourneyFormProps {
  mode: "create" | "edit";
  initialValues?: JourneyFormValues;
  isSubmitting: boolean;
  onSubmit: (values: JourneyFormValues) => Promise<void>;
  onCancel: () => void;
  mentionOptions: Mention[];
  isMentionsLoading: boolean;
}

const JourneyForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  mentionOptions,
  isMentionsLoading
}: JourneyFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue
  } = useForm<JourneyFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  useEffect(() => {
    register("mentionId", { required: "Mention is required" });
    register("semesterList", {
      validate: (value) =>
        value?.length ? true : "Select at least one semester"
    });
  }, [register]);

  const mentionValue = watch("mentionId");
  const selectedSemesters = watch("semesterList") ?? [];
  const hasMentionOptions = mentionOptions.length > 0;
  const isMentionSelectDisabled = isMentionsLoading || !hasMentionOptions;
  const semesterSelectionError = (
    errors.semesterList as { message?: string } | undefined
  )?.message;

  const toggleSemesterSelection = (semester: string) => {
    setValue(
      "semesterList",
      selectedSemesters.includes(semester)
        ? selectedSemesters.filter((item) => item !== semester)
        : [...selectedSemesters, semester],
      { shouldDirty: true, shouldValidate: true }
    );
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="journey-name">
          Name
        </label>
        <Input
          id="journey-name"
          placeholder="e.g. Génie logiciel"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="journey-abbreviation">
            Abbreviation
          </label>
          <Input
            id="journey-abbreviation"
            placeholder="GL"
            className={cn(errors.abbreviation && "border-destructive text-destructive")}
            {...register("abbreviation", { required: "Abbreviation is required" })}
          />
          {errors.abbreviation ? (
            <p className="text-xs text-destructive">{errors.abbreviation.message}</p>
          ) : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="journey-mention">
            Mention
          </label>
          <Select
            value={mentionValue || undefined}
            onValueChange={(value) =>
              setValue("mentionId", value, {
                shouldDirty: true,
                shouldValidate: true
              })
            }
            disabled={isMentionSelectDisabled}
          >
            <SelectTrigger id="journey-mention">
              <SelectValue
                placeholder={
                  isMentionsLoading
                    ? "Loading mentions…"
                    : hasMentionOptions
                      ? "Select mention"
                      : "Create a mention first"
                }
              />
            </SelectTrigger>
            <SelectContent>
              {mentionOptions.map((mention) => (
                <SelectItem key={mention.id} value={String(mention.id)}>
                  {mention.name}
                  {mention.abbreviation ? ` — ${mention.abbreviation}` : ""}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.mentionId ? (
            <p className="text-xs text-destructive">
              {errors.mentionId.message}
            </p>
          ) : null}
          {!isMentionsLoading && !hasMentionOptions ? (
            <p className="text-xs text-muted-foreground">
              No mentions available. Create a mention before adding a journey.
            </p>
          ) : null}
        </div>
      </div>
      <div className="space-y-2">
        <p className="text-sm font-medium">Semesters</p>
        <div className="rounded-md border border-input px-3 py-2">
          <div className="grid gap-2 sm:grid-cols-2">
            {semesterOptions.map((semester) => {
              const checkboxId = `journey-semester-${semester}`;
              const checked = selectedSemesters.includes(semester);
              return (
                <label
                  key={semester}
                  className="flex items-center gap-2 text-sm"
                  htmlFor={checkboxId}
                >
                  <input
                    id={checkboxId}
                    type="checkbox"
                    className="h-4 w-4 rounded border border-input text-primary"
                    checked={checked}
                    onChange={() => toggleSemesterSelection(semester)}
                    disabled={isSubmitting}
                  />
                  <span
                    className={cn(
                      "flex-1",
                      !checked && "text-muted-foreground"
                    )}
                  >
                    {semester}
                  </span>
                </label>
              );
            })}
          </div>
        </div>
        {semesterSelectionError ? (
          <p className="text-xs text-destructive">{semesterSelectionError}</p>
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
          {isSubmitting ? "Saving…" : mode === "edit" ? "Save changes" : "Create journey"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const JourneysPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingJourney, setEditingJourney] = useState<Journey | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [journeyToArchive, setJourneyToArchive] = useState<Journey | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: journeysResponse,
    isPending,
    isError,
    error
  } = useJourneys({ offset, limit: pageSize });
  const {
    data: mentionsResponse,
    isPending: isMentionsPending
  } = useMentions();
  const mentions = mentionsResponse?.data ?? [];
  const createJourney = useCreateJourney();
  const updateJourney = useUpdateJourney();
  const deleteJourney = useDeleteJourney();
  const journeys = journeysResponse?.data ?? [];
  const totalJourneys = journeysResponse?.count ?? 0;

  const openCreateForm = useCallback(() => {
    setEditingJourney(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((journey: Journey) => {
    setEditingJourney(journey);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingJourney(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: JourneyFormValues) => {
      try {
        if (editingJourney) {
          await updateJourney.mutateAsync({
            id: editingJourney.id,
            payload: toPayload(values)
          });
          setFeedback({
            type: "success",
            text: "Journey updated successfully."
          });
        } else {
          await createJourney.mutateAsync(toPayload(values));
          setFeedback({
            type: "success",
            text: "Journey created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save journey.";
        setFeedback({ type: "error", text: message });
      }
    },
    [createJourney, updateJourney, editingJourney, closeForm]
  );

  const handleDelete = useCallback(
    async () => {
      if (!journeyToArchive) {
        return;
      }
      try {
        await deleteJourney.mutateAsync(journeyToArchive.id);
        setFeedback({
          type: "success",
          text: "Journey archived successfully."
        });
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to archive journey.";
        setFeedback({ type: "error", text: message });
      } finally {
        setJourneyToArchive(null);
      }
    },
    [deleteJourney, journeyToArchive]
  );

  const handlePageChange = (nextPage: number) => {
    setPage(Math.max(1, nextPage));
  };

  const handlePageSizeChange = (nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  };

  const columns = useMemo<ColumnDef<Journey>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Journey",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
            <span className="text-xs text-muted-foreground">
              {row.original.abbreviation}
            </span>
          </div>
        )
      },
      {
        accessorKey: "mention",
        header: "Mention",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.mention?.name ?? "—"}
          </span>
        )
      },
      {
        id: "actions",
        header: "",
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleEdit(row.original)}
            >
              Edit
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="text-destructive hover:text-destructive"
              onClick={() => setJourneyToArchive(row.original)}
            >
              Archive
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createJourney.isPending || updateJourney.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Journeys</h1>
          <p className="text-sm text-muted-foreground">
            Manage academic journeys and keep them aligned with their mentions.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add journey
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
            setEditingJourney(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingJourney ? "Edit journey" : "Create new journey"}
            </DialogTitle>
            <DialogDescription>
              {editingJourney
                ? "Update the journey to keep the Angular and React panels aligned."
                : "Create a journey that will be available across the platform."}
            </DialogDescription>
          </DialogHeader>
          <JourneyForm
            mode={editingJourney ? "edit" : "create"}
            initialValues={toFormValues(editingJourney)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            mentionOptions={mentions}
            isMentionsLoading={isMentionsPending}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(journeyToArchive)}
        title="Archive journey"
        description={
          journeyToArchive ? (
            <>
              Are you sure you want to archive <strong>{journeyToArchive.name}</strong>? This action cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Archive"
        destructive
        isConfirming={deleteJourney.isPending}
        onCancel={() => setJourneyToArchive(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={journeys}
        isLoading={isPending}
        searchPlaceholder="Search journeys"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load journeys")
            : "No journeys found"
        }
        totalItems={totalJourneys}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
