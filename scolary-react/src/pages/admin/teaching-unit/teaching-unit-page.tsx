import { useCallback, useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ColumnDef } from "@tanstack/react-table";
import { BookOpen, Layers, Plus, Trash2 } from "lucide-react";

import {
  AcademicFilters,
  JourneyOption
} from "@/components/filters/academic-filters";
import { DataTable } from "@/components/data-table/data-table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { TeachingUnit, TeachingUnitPayload } from "@/models/teaching-unit";
import { useLookupOptions } from "@/hooks/use-lookup-options";
import { fetchJourneys as fetchJourneysByMention } from "@/services/inscription-service";
import {
  fetchTeachingUnits,
  useCreateTeachingUnit,
  useDeleteTeachingUnit,
  useUpdateTeachingUnit
} from "@/services/teaching-unit-service";
import { ActionButton } from "@/components/action-button";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { useForm } from "react-hook-form";
import { cn } from "@/lib/utils";
import { Journey } from "@/models/journey";

type TeachingUnitFilters = {
  id_mention: string;
  id_journey: string;
  semester: string;
  search: string;
};

const semesters = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"];

type TeachingUnitFormValues = {
  name: string;
  id_journey: string;
  semester: string;
};

const defaultFormValues: TeachingUnitFormValues = {
  name: "",
  id_journey: "",
  semester: ""
};

const toFormValues = (
  teachingUnits?: TeachingUnit | null
): TeachingUnitFormValues => ({
  name: teachingUnits?.name ?? "",
  id_journey: teachingUnits?.id_journey ? String(teachingUnits.id_journey) : "",
  semester: teachingUnits?.semester ?? ""
});

const toPayload = (values: TeachingUnitFormValues): TeachingUnitPayload => ({
  name: values.name.trim(),
  semester: values.semester,
  id_journey: Number(values.id_journey)
});

interface TeachingUnitFormProps {
  mode: "create" | "edit";
  initialValues?: TeachingUnitFormValues;
  isSubmitting: boolean;
  journeyOptions: JourneyOption[];
  semesterOptions: string[];
  onSubmit: (values: TeachingUnitFormValues) => Promise<void>;
  onCancel: () => void;
}

const TeachingUnitForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  journeyOptions,
  semesterOptions
}: TeachingUnitFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue
  } = useForm<TeachingUnitFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  const selectedPlugged = watch("id_journey");

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  useEffect(() => {
    if (!selectedPlugged && journeyOptions.length > 0) {
      setValue("id_journey", String(journeyOptions[0].id));
    }
  }, [journeyOptions, selectedPlugged, setValue]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="teaching-unit-name">
          Name
        </label>
        <Input
          id="teaching-unit-name"
          placeholder="e.g. Génie logiciel"
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="mention-plugged">
          Parcours
        </label>
        <Select
          value={watch("id_journey")}
          onValueChange={(value) => setValue("id_journey", value)}
        >
          <SelectTrigger
            className={cn(
              "h-11",
              errors.id_journey && "border-destructive text-destructive"
            )}
          >
            <SelectValue placeholder="Select plugged" />
          </SelectTrigger>
          <SelectContent>
            {journeyOptions.map((journey: JourneyOption) => (
              <SelectItem key={journey.id} value={String(journey.id)}>
                {journey.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {errors.id_journey ? (
          <p className="text-xs text-destructive">
            {errors.id_journey.message}
          </p>
        ) : null}
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="mention-plugged">
          Semestre
        </label>
        <Select
          value={watch("semester")}
          onValueChange={(value) => setValue("semester", value)}
        >
          <SelectTrigger
            className={cn(
              "h-11",
              errors.semester && "border-destructive text-destructive"
            )}
          >
            <SelectValue placeholder="Selectioner le Semestre" />
          </SelectTrigger>
          <SelectContent>
            {semesterOptions.map((semester: string) => (
              <SelectItem key={semester} value={semester}>
                {semester}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {errors.semester ? (
          <p className="text-xs text-destructive">{errors.semester.message}</p>
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
              : "Create mention"}
        </Button>
      </div>
    </form>
  );
};

export const TeachingUnitPage = () => {
  const defaultSemester = semesters[0];
  const STORAGE_KEY = "teaching-units.filters";

  const createTeachingUnit = useCreateTeachingUnit();
  const updateTeachingUnit = useUpdateTeachingUnit();
  const deleteTeachingUnit = useDeleteTeachingUnit();

  type Feedback = { type: "success" | "error"; text: string };
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const readStoredFilters = (): TeachingUnitFilters | null => {
    if (typeof window === "undefined") return null;
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    try {
      const parsed = JSON.parse(raw);
      if (
        parsed &&
        typeof parsed === "object" &&
        "id_mention" in parsed &&
        "id_journey" in parsed &&
        "semester" in parsed &&
        "search" in parsed
      ) {
        return parsed as TeachingUnitFilters;
      }
    } catch {
      return null;
    }
    return null;
  };

  const [filters, setFilters] = useState<TeachingUnitFilters>(() => {
    const stored = readStoredFilters();
    return (
      stored ?? {
        id_year: "",
        register_type: "",
        id_mention: "",
        id_journey: "",
        semester: defaultSemester,
        search: ""
      }
    );
  });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const offset = (page - 1) * pageSize;

  const { mentionOptions, isLoadingMentions } = useLookupOptions({
    includeMentions: true
  });

  const journeyQuery = useQuery({
    queryKey: ["teaching-units", "journeys", filters.id_mention],
    queryFn: () => fetchJourneysByMention(Number(filters.id_mention)),
    enabled: Boolean(filters.id_mention)
  });

  const availableJourneys = useMemo(
    () =>
      (journeyQuery.data ?? []).map((journey: any) => ({
        id: String(journey.id),
        label: journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
        id_mention:
          journey.id_mention !== undefined
            ? String(journey.id_mention)
            : String(filters.id_mention),
        semesterList: Array.isArray(journey.semester_list)
          ? journey.semester_list
              .map((entry: any) =>
                typeof entry === "string"
                  ? entry
                  : (entry?.semester ?? entry?.semester_list ?? null)
              )
              .filter((sem: any): sem is string => Boolean(sem))
          : []
      })),
    [journeyQuery.data, filters.id_mention]
  );

  useEffect(() => {
    if (!mentionOptions.length) return;
    setFilters((prev) => {
      const nextMention = prev.id_mention || mentionOptions[0].id;
      const nextSemester = semesters.includes(prev.semester)
        ? prev.semester
        : defaultSemester;
      return { ...prev, id_mention: nextMention, semester: nextSemester };
    });
  }, [mentionOptions, defaultSemester]);

  useEffect(() => {
    const firstJourney = availableJourneys[0];
    if (!firstJourney) return;
    setFilters((prev) => {
      if (prev.id_journey) return prev;
      const nextSemester =
        allowedSemestersForJourney(firstJourney.id)[0] ??
        prev.semester ??
        defaultSemester;
      return {
        ...prev,
        id_journey: firstJourney.id,
        semester: semesters.includes(nextSemester) ? nextSemester : defaultSemester
      };
    });
  }, [availableJourneys, defaultSemester]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
  }, [filters]);

  const teachingUnitQuery = useQuery({
    queryKey: ["teaching-units", { filters, page, pageSize }],
    queryFn: () => {
      const wheres: Array<Record<string, any>> = [];
      if (filters.id_journey) {
        wheres.push({
          key: "id_journey",
          operator: "==",
          value: Number(filters.id_journey)
        });
      }
      if (filters.semester) {
        wheres.push({
          key: "semester",
          operator: "==",
          value: filters.semester
        });
      }
      if (filters.search.trim()) {
        wheres.push({
          key: "name",
          operator: "like",
          value: `%${filters.search.trim()}%`
        });
      }
      return fetchTeachingUnits({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "journey{id,id_mention,name,abbreviation}",
          "journey.semester_list",
          "journey.mention{id,name,abbreviation}"
        ]),
        offset,
        limit: pageSize
      });
    }
  });

  const teachingUnits = teachingUnitQuery.data?.data ?? [];
  const totalTeachingUnits =
    teachingUnitQuery.data?.count ?? teachingUnitQuery.data?.data?.length ?? 0;

  const [teachingUnitToArchive, setTeachingUnitToArchive] =
    useState<TeachingUnit | null>(null);

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingUnit, setEditingUnit] = useState<TeachingUnit | null>(null);
  const [deletingUnit, setDeletingUnit] = useState<TeachingUnit | null>(null);
  const [formSubmitting, setFormSubmitting] = useState(false);

  const allowedSemestersForJourney = useCallback(
    (journeyId?: string) => {
      const journey = availableJourneys.find((j) => j.id === journeyId);
      if (
        journey &&
        Array.isArray((journey as any).semesterList) &&
        (journey as any).semesterList.length
      ) {
        return (journey as any).semesterList as string[];
      }
      return semesters;
    },
    [availableJourneys]
  );

  const handleFiltersChange = useCallback((next: any) => {
    setFilters((prev) => ({
      ...prev,
      id_mention: next.id_mention,
      id_journey: next.id_journey,
      semester: next.semester
    }));
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<TeachingUnit>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Teaching unit",
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium">{row.original.name}</span>
          </div>
        )
      },
      {
        accessorKey: "semester",
        header: "Semester",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.semester}
          </span>
        )
      },
      {
        id: "journey",
        header: "Journey",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="flex items-center gap-2 text-sm text-muted-foreground">
              <Layers className="h-4 w-4 text-muted-foreground" />
              {row.original.journey?.name ??
                row.original.journey?.abbreviation ??
                "—"}
            </span>
            <span className="text-xs text-muted-foreground">
              {row.original.journey?.mention?.name ??
                row.original.journey?.mention?.abbreviation ??
                ""}
            </span>
          </div>
        )
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <ActionButton
            row={row}
            handleEdit={() => {
              setFilters((prev) => ({
                ...prev,
                id_journey: row.original.journey?.id
                  ? String(row.original.journey.id)
                  : prev.id_journey,
                semester: row.original.semester || prev.semester,
                id_mention: row.original.journey?.mention?.id
                  ? String(row.original.journey.mention.id)
                  : prev.id_mention
              }));
              setEditingUnit(row.original);
              setIsFormOpen(true);
            }}
            setConfirmDelete={setTeachingUnitToArchive}
          />
        )
      }
    ];
  }, []);

  const handleOpenCreate = () => {
    setEditingUnit(null);
    setIsFormOpen(true);
  };

  const closeForm = useCallback(() => {
    setEditingUnit(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: TeachingUnitFormValues) => {
      try {
        if (editingUnit) {
          await updateTeachingUnit.mutateAsync({
            id: Number(editingUnit.id),
            payload: toPayload(values)
          });
          setFeedback({
            type: "success",
            text: "Mention updated successfully."
          });
        } else {
          await createTeachingUnit.mutateAsync(toPayload(values));
          setFeedback({
            type: "success",
            text: "Mention created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save mention.";
        setFeedback({ type: "error", text: message });
      }
    },
    [createTeachingUnit, updateTeachingUnit, editingUnit, closeForm]
  );

  const handleDelete = useCallback(async () => {
    if (!teachingUnitToArchive) {
      return;
    }
    try {
      await deleteTeachingUnit.mutateAsync(Number(teachingUnitToArchive.id));
      setFeedback({ type: "success", text: "Mention archived successfully." });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to archive Teaching unit.";
      setFeedback({ type: "error", text: message });
    } finally {
      setTeachingUnitToArchive(null);
    }
  }, [deleteTeachingUnit, teachingUnitToArchive]);

  const onPageChange = (nextPage: number) => setPage(Math.max(1, nextPage));
  const onPageSizeChange = (nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  };

  const isSubmitting =
    createTeachingUnit.isPending || updateTeachingUnit.isPending;
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Teaching Units
          </h1>
          <p className="text-sm text-muted-foreground">
            Filter teaching units by mention, journey, and semester.
          </p>
        </div>
      </div>

      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        <div className="flex flex-wrap items-center gap-3">
          <Input
            placeholder="Search by teaching unit name"
            value={filters.search}
            onChange={(event) =>
              setFilters((prev) => ({ ...prev, search: event.target.value }))
            }
            className="w-full sm:w-80"
          />
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              onClick={() => {
                setFilters((prev) => ({
                  ...prev,
                  search: ""
                }));
                setPage(1);
              }}
            >
              Reset
            </Button>
            <Button onClick={handleOpenCreate} className="gap-2">
              <Plus className="h-4 w-4" />
              Add teaching unit
            </Button>
          </div>
        </div>

        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={availableJourneys}
          semesters={semesters}
          journeysLoading={journeyQuery.isFetching}
          showLevel={false}
          showResetButton={false}
          showActiveFilters={true}
          filterClassname="grid gap-4 lg:grid-cols-2"
        />

        <DataTable
          columns={columns}
          data={teachingUnits}
          isLoading={teachingUnitQuery.isFetching || isLoadingMentions}
          totalItems={totalTeachingUnits}
          page={page}
          pageSize={pageSize}
          onPageChange={onPageChange}
          onPageSizeChange={onPageSizeChange}
          enableColumnVisibility
          enableViewToggle
          searchPlaceholder="Search teaching units"
        />
      </div>

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingUnit ? "Edit teaching unit" : "Create teaching unit"}
            </DialogTitle>
            <DialogDescription>
              Define the teaching unit name, journey, and semester.
            </DialogDescription>
          </DialogHeader>
          <TeachingUnitForm
            mode={editingUnit ? "edit" : "create"}
            initialValues={toFormValues(editingUnit)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            journeyOptions={availableJourneys}
            semesterOptions={semesters}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(teachingUnitToArchive)}
        title="Delete teaching unit"
        description={
          teachingUnitToArchive ? (
            <>
              Delete <strong>{teachingUnitToArchive.name}</strong>? This action
              cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={formSubmitting}
        onCancel={() => setTeachingUnitToArchive(null)}
        onConfirm={handleDelete}
      />
    </div>
  );
};
