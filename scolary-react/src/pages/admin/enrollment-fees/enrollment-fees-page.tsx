import { useCallback, useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import { Banknote, Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { DataTable, type ColumnDef } from "@/components/data-table/data-table";
import { ConfirmDialog } from "@/components/confirm-dialog";
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
import { cn } from "@/lib/utils";
import {
  type EnrollmentFee,
  type EnrollmentFeePayload,
  useEnrollmentFees,
  useCreateEnrollmentFee,
  useUpdateEnrollmentFee,
  useDeleteEnrollmentFee
} from "@/services/enrollment-fee-service";
import { useAcademicYears } from "@/services/academic-year-service";
import { useMentions } from "@/services/mention-service";
import { ActionButton } from "@/components/action-button";
import { Mention, MentionOption } from "@/models/mentions";
import { RegisterType, RegisterTypeValue } from "@/lib/enum/repeat-status-enum";

type EnrollmentFeeFormValues = {
  level: string;
  price: string;
  id_academic_year?: string;
  id_mention?: string;
  register_type?: string;
};

const NONE_VALUE = "none";

const levelOptions = ["L1", "L2", "L3", "M1", "M2"];
const registerOptions = [
  { value: "REGISTRATION", label: "Inscription ou Ré-inscription" },
  { value: "SELECTION", label: "Séléction de dossier" }
];

const defaultFormValues: EnrollmentFeeFormValues = {
  level: "",
  price: "",
  id_academic_year: NONE_VALUE,
  id_mention: NONE_VALUE,
  register_type: NONE_VALUE
};

const toFormValues = (fee?: EnrollmentFee | null): EnrollmentFeeFormValues => ({
  level: fee?.level ?? "",
  price: fee?.price != null ? String(fee.price) : "",
  id_academic_year: fee?.id_academic_year
    ? String(fee.id_academic_year)
    : NONE_VALUE,
  id_mention: fee?.id_mention ? String(fee.id_mention) : NONE_VALUE,
  register_type: fee?.register_type ?? RegisterType.REGISTRATION
});

const toPayload = (values: EnrollmentFeeFormValues): EnrollmentFeePayload => ({
  level: values.level,
  price: Number(values.price),
  register_type: values.register_type,
  id_academic_year:
    values.id_academic_year && values.id_academic_year !== NONE_VALUE
      ? Number(values.id_academic_year)
      : undefined,
  id_mention:
    values.id_mention && values.id_mention !== NONE_VALUE
      ? Number(values.id_mention)
      : undefined
});

interface EnrollmentFeeFormProps {
  mode: "create" | "edit";
  initialValues?: EnrollmentFeeFormValues;
  isSubmitting: boolean;
  academicYearOptions: Array<{ id: string; label: string }>;
  mentionOptions: Array<{ id: string; label: string }>;
  onSubmit: (values: EnrollmentFeeFormValues) => Promise<void>;
  onCancel: () => void;
}

const EnrollmentFeeForm = ({
  mode,
  initialValues,
  isSubmitting,
  academicYearOptions,
  mentionOptions,
  onSubmit,
  onCancel
}: EnrollmentFeeFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch
  } = useForm<EnrollmentFeeFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  const levelValue = watch("level");
  const priceValue = watch("price");

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="enrollment-fee-level">
            Level
          </label>
          <Select
            defaultValue={initialValues?.level || undefined}
            onValueChange={(value) =>
              reset((prev) => ({ ...prev, level: value }), {
                keepDefaultValues: false
              })
            }
          >
            <SelectTrigger
              id="enrollment-fee-level"
              className={cn(errors.level && "border-destructive")}
            >
              <SelectValue placeholder="Select a level" />
            </SelectTrigger>
            <SelectContent>
              {levelOptions.map((level) => (
                <SelectItem key={level} value={level}>
                  {level}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.level ? (
            <p className="text-xs text-destructive">{errors.level.message}</p>
          ) : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="enrollment-fee-price">
            Price
          </label>
          <Input
            id="enrollment-fee-price"
            type="number"
            step="0.01"
            placeholder="0.00"
            className={cn(
              errors.price && "border-destructive text-destructive"
            )}
            {...register("price", { required: "Price is required" })}
          />
          {errors.price ? (
            <p className="text-xs text-destructive">{errors.price.message}</p>
          ) : null}
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="enrollment-fee-year">
            Academic year
          </label>
          <Select
            defaultValue={
              initialValues?.id_academic_year &&
              initialValues.id_academic_year !== NONE_VALUE
                ? initialValues.id_academic_year
                : undefined
            }
            onValueChange={(value) =>
              reset((prev) => ({ ...prev, id_academic_year: value }), {
                keepDefaultValues: false
              })
            }
          >
            <SelectTrigger id="enrollment-fee-year">
              <SelectValue placeholder="Optional" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={NONE_VALUE}>None</SelectItem>
              {academicYearOptions.map((year) => (
                <SelectItem key={year.id} value={year.id}>
                  {year.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <label
            className="text-sm font-medium"
            htmlFor="enrollment-fee-mention"
          >
            Mention
          </label>
          <Select
            defaultValue={
              initialValues?.id_mention &&
              initialValues.id_mention !== NONE_VALUE
                ? initialValues.id_mention
                : undefined
            }
            onValueChange={(value) =>
              reset((prev) => ({ ...prev, id_mention: value }), {
                keepDefaultValues: false
              })
            }
          >
            <SelectTrigger id="enrollment-fee-mention">
              <SelectValue placeholder="Optional" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={NONE_VALUE}>None</SelectItem>
              {mentionOptions.map((mention) => (
                <SelectItem key={mention.id} value={mention.id}>
                  {mention.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="enrollment-fee-level">
            Type
          </label>
          <Select
            defaultValue={initialValues?.register_type || undefined}
            onValueChange={(value) =>
              reset((prev) => ({ ...prev, register_type: value }), {
                keepDefaultValues: false
              })
            }
          >
            <SelectTrigger
              id="enrollment-fee-level"
              className={cn(errors.level && "border-destructive")}
            >
              <SelectValue placeholder="Select a level" />
            </SelectTrigger>
            <SelectContent>
              {registerOptions.map((register) => (
                <SelectItem key={register.value} value={register.value}>
                  {register.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.register_type ? (
            <p className="text-xs text-destructive">
              {errors.register_type.message}
            </p>
          ) : null}
        </div>
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
              : "Create fee"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const EnrollmentFeesPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingFee, setEditingFee] = useState<EnrollmentFee | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [feeToDelete, setFeeToDelete] = useState<EnrollmentFee | null>(null);
  const [selectedYear, setSelectedYear] = useState<string>("all");
  const [selectedMention, setSelectedMention] = useState<string>("all");
  const [selectedLevel, setSelectedLevel] = useState<string>("all");
  const [selectedRegistrationType, setSelectedRegistrationType] =
    useState<string>("all");
  const [isMigrating, setIsMigrating] = useState(false);

  const offset = (page - 1) * pageSize;
  const {
    data: feesResponse,
    isPending,
    isError,
    error
  } = useEnrollmentFees({
    offset,
    limit: pageSize,
    relation: JSON.stringify([
      "mention{id,name,abbreviation}",
      "academinc_year{id,name}"
    ]),
    where: JSON.stringify([
      ...(selectedLevel !== "all"
        ? [{ key: "level", operator: "==", value: selectedLevel }]
        : []),
      ...(selectedYear !== "all"
        ? [
            {
              key: "id_academic_year",
              operator: "==",
              value: Number(selectedYear)
            }
          ]
        : []),
      ...(selectedMention !== "all"
        ? [
            {
              key: "id_mention",
              operator: "==",
              value: Number(selectedMention)
            }
          ]
        : []),
      ...(selectedRegistrationType !== "all"
        ? [
            {
              key: "register_type",
              operator: "==",
              value: selectedRegistrationType
            }
          ]
        : [])
    ])
  });
  const { data: allFeesResponse } = useEnrollmentFees({
    limit: 5000,
    relation: JSON.stringify([
      "mention{id,name,abbreviation}",
      "academinc_year{id,name}"
    ])
  });
  const { data: yearResponse } = useAcademicYears({ limit: 200 });
  const { data: mentionResponse } = useMentions({ limit: 200 });

  const academicYearOptions =
    yearResponse?.data?.map((year) => ({
      id: String(year.id),
      label: year.name ?? `Year ${year.id}`
    })) ?? [];
  const mentionOptions =
    mentionResponse?.data?.map((mention: Mention) => ({
      id: String(mention.id),
      label: mention.name ?? mention.abbreviation ?? `Mention ${mention.id}`
    })) ?? [];

  const fees = feesResponse?.data ?? [];
  const totalFees = feesResponse?.count ?? fees.length;
  const allFees = allFeesResponse?.data ?? [];

  const createFee = useCreateEnrollmentFee();
  const updateFee = useUpdateEnrollmentFee();
  const deleteFee = useDeleteEnrollmentFee();

  const openCreateForm = useCallback(() => {
    setEditingFee(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((fee: EnrollmentFee) => {
    setEditingFee(fee);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingFee(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: EnrollmentFeeFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingFee) {
          await updateFee.mutateAsync({ id: editingFee.id, payload });
          setFeedback({
            type: "success",
            text: "Enrollment fee updated successfully."
          });
        } else {
          await createFee.mutateAsync(payload);
          setFeedback({
            type: "success",
            text: "Enrollment fee created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save the enrollment fee.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createFee, editingFee, updateFee]
  );

  const handleDelete = useCallback(async () => {
    if (!feeToDelete) {
      return;
    }
    try {
      await deleteFee.mutateAsync(feeToDelete.id);
      setFeedback({
        type: "success",
        text: "Enrollment fee deleted successfully."
      });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete the enrollment fee.";
      setFeedback({ type: "error", text: message });
    } finally {
      setFeeToDelete(null);
    }
  }, [deleteFee, feeToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextPageSize: number) => {
    setPageSize(nextPageSize);
    setPage(1);
  }, []);

  const handleYearFilterChange = useCallback((value: string) => {
    setSelectedYear(value);
    setPage(1);
  }, []);

  const handleMentionFilterChange = useCallback((value: string) => {
    setSelectedMention(value);
    setPage(1);
  }, []);

  const handleLevelFilterChange = useCallback((value: string) => {
    setSelectedLevel(value);
    setPage(1);
  }, []);

  const handleRegistrationTypelFilterChange = useCallback((value: string) => {
    setSelectedRegistrationType(value);
    setPage(1);
  }, []);

  const feesByYear = useMemo(() => {
    const map = new Map<string, number>();
    allFees.forEach((fee) => {
      const key = fee.id_academic_year ? String(fee.id_academic_year) : "none";
      map.set(key, (map.get(key) ?? 0) + 1);
    });
    return map;
  }, [allFees]);

  const lastYearWithData = useMemo(() => {
    const years = [...(yearResponse?.data ?? [])].sort(
      (a, b) => (b.id ?? 0) - (a.id ?? 0)
    );
    return years.find(
      (year) =>
        String(year.id) !== selectedYear &&
        (feesByYear.get(String(year.id)) ?? 0) > 0
    );
  }, [feesByYear, yearResponse?.data, selectedYear]);

  const canMigrateFromLastYear =
    selectedYear !== "all" &&
    (feesResponse?.count ?? 0) === 0 &&
    lastYearWithData;

  const columns = useMemo<ColumnDef<EnrollmentFee>[]>(() => {
    return [
      {
        accessorKey: "level",
        header: "Level"
      },
      {
        accessorKey: "price",
        header: "Price",
        cell: ({ row }) =>
          Intl.NumberFormat("fr-FR", {
            style: "currency",
            currency: "MGA"
          }).format(row.original.price)
      },
      {
        id: "academic_year",
        header: "Academic year",
        cell: ({ row }) =>
          row.original.academinc_year?.name ??
          academicYearOptions.find(
            (y) => y.id === String(row.original.id_academic_year)
          )?.label ??
          "—"
      },
      {
        id: "mention",
        header: "Mention",
        cell: ({ row }) => row.original.mention?.name || "—"
      },
      {
        id: "register_type",
        header: "Registration type",
        cell: ({ row }) =>
          row.original.register_type
            ? RegisterTypeValue[row.original.register_type]
            : "—"
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <ActionButton
            row={row}
            setConfirmDelete={setFeeToDelete}
            handleEdit={handleEdit}
          />
        )
      }
    ];
  }, [academicYearOptions, handleEdit, mentionOptions]);

  const isSubmitting = createFee.isPending || updateFee.isPending;

  const handleMigrateFromLastYear = useCallback(async () => {
    if (!lastYearWithData || selectedYear === "all") {
      return;
    }
    const sourceFees = allFees.filter(
      (fee) =>
        String(fee.id_academic_year ?? "") === String(lastYearWithData.id)
    );
    if (!sourceFees.length) {
      setFeedback({
        type: "error",
        text: "Aucune donnée à migrer depuis l'année précédente."
      });
      return;
    }
    setIsMigrating(true);
    try {
      for (const fee of sourceFees) {
        await createFee.mutateAsync({
          level: fee.level,
          price: fee.price,
          id_academic_year: Number(selectedYear),
          id_mention: fee.id_mention ?? undefined
        });
      }
      setFeedback({
        type: "success",
        text: `Migration effectuée depuis ${lastYearWithData.name}.`
      });
    } catch (migrationError) {
      const message =
        migrationError instanceof Error
          ? migrationError.message
          : "Migration échouée.";
      setFeedback({ type: "error", text: message });
    } finally {
      setIsMigrating(false);
    }
  }, [allFees, createFee, lastYearWithData, selectedYear]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex items-center gap-2">
          <Banknote className="h-5 w-5 text-muted-foreground" />
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">
              Enrollment fees
            </h1>
            <p className="text-sm text-muted-foreground">
              Manage tuition fees by level, mention and academic year.
            </p>
          </div>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add enrollment fee
        </Button>
      </div>

      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <div className="space-y-1">
          <label className="text-sm font-medium text-muted-foreground">
            Filter by level
          </label>
          <Select value={selectedLevel} onValueChange={handleLevelFilterChange}>
            <SelectTrigger className="h-10">
              <SelectValue placeholder="All levels" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              {levelOptions.map((level) => (
                <SelectItem key={level} value={level}>
                  {level}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-1">
          <label className="text-sm font-medium text-muted-foreground">
            Filter by academic year
          </label>
          <Select value={selectedYear} onValueChange={handleYearFilterChange}>
            <SelectTrigger className="h-10">
              <SelectValue placeholder="All years" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              {academicYearOptions.map((year) => (
                <SelectItem key={year.id} value={year.id}>
                  {year.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-1">
          <label className="text-sm font-medium text-muted-foreground">
            Filter by mention
          </label>
          <Select
            value={selectedMention}
            onValueChange={handleMentionFilterChange}
          >
            <SelectTrigger className="h-10">
              <SelectValue placeholder="All mentions" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              {mentionOptions.map((mention: MentionOption) => (
                <SelectItem key={mention.id} value={mention.id}>
                  {mention.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium text-muted-foreground">
            Filter Type
          </label>
          <Select
            value={selectedRegistrationType}
            onValueChange={handleRegistrationTypelFilterChange}
          >
            <SelectTrigger className="h-10">
              <SelectValue placeholder="All levels" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              {registerOptions.map((register) => (
                <SelectItem key={register.value} value={register.value}>
                  {register.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {canMigrateFromLastYear && lastYearWithData ? (
        <div className="flex flex-col gap-2 rounded-md border bg-muted/30 p-4 md:flex-row md:items-center md:justify-between">
          <div className="text-sm">
            <p className="font-medium">
              Aucun frais pour{" "}
              {academicYearOptions.find((y) => y.id === selectedYear)?.label}
            </p>
            <p className="text-muted-foreground">
              Vous pouvez importer les frais depuis {lastYearWithData.name} (
              {feesByYear.get(String(lastYearWithData.id)) ?? 0}{" "}
              enregistrements).
            </p>
          </div>
          <Button
            size="sm"
            onClick={handleMigrateFromLastYear}
            disabled={isMigrating || createFee.isPending}
          >
            {isMigrating
              ? "Migration..."
              : "Migrer depuis l'année " + lastYearWithData.name}
          </Button>
        </div>
      ) : null}

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
            setEditingFee(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-xl">
          <DialogHeader>
            <DialogTitle>
              {editingFee ? "Edit enrollment fee" : "Create new enrollment fee"}
            </DialogTitle>
            <DialogDescription>
              Define the price of enrollment for a given level, mention, and
              academic year.
            </DialogDescription>
          </DialogHeader>
          <EnrollmentFeeForm
            mode={editingFee ? "edit" : "create"}
            initialValues={toFormValues(editingFee)}
            isSubmitting={isSubmitting}
            academicYearOptions={academicYearOptions}
            mentionOptions={mentionOptions}
            onSubmit={handleSubmit}
            onCancel={closeForm}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(feeToDelete)}
        title="Delete enrollment fee"
        description={
          feeToDelete ? (
            <>
              Are you sure you want to delete the fee for{" "}
              <strong>{feeToDelete.level}</strong>?
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteFee.isPending}
        onCancel={() => setFeeToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={fees}
        isLoading={isPending}
        searchPlaceholder="Search fees"
        emptyText={
          isError ? (error?.message ?? "Unable to load fees") : "No fees found"
        }
        totalItems={totalFees}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
