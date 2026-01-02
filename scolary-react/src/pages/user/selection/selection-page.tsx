import { useCallback, useEffect, useMemo, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import type { Row } from "@tanstack/react-table";

import { Button } from "../../../components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle
} from "../../../components/ui/dialog";
import {
  DataTable,
  type ColumnDef
} from "../../../components/data-table/data-table";
import {
  AcademicFilters,
  type AcademicFilterValue,
  type JourneyOption
} from "../../../components/filters/academic-filters";
import {
  useSelectionStudents,
  type SelectionStudent,
  type SelectionStatus
} from "../../../services/selection-service";
import { StudentForm } from "@/components/student-form/student-form";
import { StudentFormState } from "@/components/student-form/student-form-types";
import { DialogFooter } from "@/components/ui/dialog";
import {
  createStudent,
  fetchStudentByNumSelect,
  softDeleteStudent,
  updateStudentProfile
} from "@/services/student-service";
import { Pencil, Trash2 } from "lucide-react";
import { useLookupOptions } from "@/hooks/use-lookup-options";
import { printSelectionList } from "@/services/print-service";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { PdfViewerModal } from "@/components/pdf-viewer-modal";
import { ConfirmDialog } from "@/components/confirm-dialog";

const semesters = Array.from({ length: 10 }, (_, index) => `S${index + 1}`);

const journeyOptions: JourneyOption[] = [];
type DialogMode = "create" | "edit";

const createEmptyFormState = (): StudentFormState => ({
  studentRecordId: "",
  studentId: "",
  cardNumber: "",
  firstName: "",
  lastName: "",
  fullName: "",
  email: "",
  address: "",
  sex: "",
  maritalStatus: "",
  phoneNumber: "",
  cinNumber: "",
  cinIssueDate: "",
  cinIssuePlace: "",
  birthDate: "",
  birthPlace: "",
  baccalaureateNumber: "",
  baccalaureateCenter: "",
  baccalaureateYear: "",
  baccalaureateSerieId: "",
  job: "",
  enrollmentStatus: "",
  level: "",
  mentionId: "",
  journeyId: "",
  semester: "",
  status: "",
  mean: 0,
  picture: "",
  pictureFile: null,
  lastUpdate: "",
  mentionLabel: "",
  annualRegister: []
});

const statusStyles: Record<
  SelectionStatus,
  { text: string; badge: string; dot: string }
> = {
  Pending: {
    text: "text-muted-foreground",
    badge: "bg-slate-100 text-slate-700",
    dot: "bg-slate-400"
  },
  Rejected: {
    text: "text-amber-600",
    badge: "bg-amber-100 text-amber-700",
    dot: "bg-amber-500"
  },
  Selected: {
    text: "text-emerald-600",
    badge: "bg-emerald-100 text-emerald-700",
    dot: "bg-emerald-500"
  },
  Registered: {
    text: "text-blue-600",
    badge: "bg-blue-100 text-blue-700",
    dot: "bg-blue-500"
  },
  Former: {
    text: "text-gray-600",
    badge: "bg-gray-100 text-gray-700",
    dot: "bg-gray-500"
  }
};

const getAvatarUrl = (fullName: string) => {
  const name = encodeURIComponent(fullName);
  return `https://ui-avatars.com/api/?name=${name}&background=random&color=fff&size=64`;
};

export const DossierSelectionPage = () => {
  const defaultSemester = semesters[0] ?? "";

  const { mentionOptions, academicYearOptions: yearOptions } = useLookupOptions(
    { includeMentions: true, includeAcademicYears: true }
  );

  const FILTERS_STORAGE_KEY = "selection.filters";

  const readStoredFilters = (): {
    filters: AcademicFilterValue | null;
    enrollmentFilter: SelectionStatus | "All";
  } => {
    if (typeof window === "undefined") {
      return { filters: null, enrollmentFilter: "All" };
    }
    const raw = window.localStorage.getItem(FILTERS_STORAGE_KEY);
    if (!raw) {
      return { filters: null, enrollmentFilter: "All" };
    }
    try {
      const parsed = JSON.parse(raw);
      if (
        parsed &&
        typeof parsed === "object" &&
        "id_mention" in parsed &&
        "id_journey" in parsed &&
        "semester" in parsed &&
        "id_year" in parsed &&
        "register_type" in parsed
      ) {
        const enrollmentFilter =
          typeof parsed.enrollmentFilter === "string"
            ? (parsed.enrollmentFilter as SelectionStatus | "All")
            : "All";
        return {
          filters: parsed as AcademicFilterValue,
          enrollmentFilter
        };
      }
    } catch {
      return { filters: null, enrollmentFilter: "All" };
    }
    return { filters: null, enrollmentFilter: "All" };
  };

  const stored = readStoredFilters();

  const [filters, setFilters] = useState<AcademicFilterValue>(
    stored.filters ?? {
      id_mention: "",
      id_journey: "",
      semester: defaultSemester,
      id_year: "",
      level: "",
      register_type: "SELECTION"
    }
  );
  const [formState, setFormState] = useState<StudentFormState>(
    createEmptyFormState()
  );
  const [formError, setFormError] = useState<string | null>(null);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const queryClient = useQueryClient();
  const [dialogMode, setDialogMode] = useState<DialogMode>("create");
  const [hasCreatedStudent, setHasCreatedStudent] = useState(false);
  const [enrollmentFilter, setEnrollmentFilter] = useState<
    SelectionStatus | "All"
  >(stored.enrollmentFilter ?? "All");
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [printError, setPrintError] = useState<string | null>(null);
  const [printingList, setPrintingList] = useState(false);
  const [pdfViewer, setPdfViewer] = useState<{
    open: boolean;
    url?: string;
    title?: string;
  }>({ open: false });
  const [confirmDeleteStudent, setConfirmDeleteStudent] =
    useState<SelectionStudent | null>(null);
  const handleFiltersChange = useCallback((next: AcademicFilterValue) => {
    setFilters(next);
  }, []);

  useEffect(() => {
    if (!formError) return;
    const timer = window.setTimeout(() => setFormError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [formError]);

  useEffect(() => {
    if (!printError) return;
    const timer = window.setTimeout(() => setPrintError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [printError]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    window.localStorage.setItem(
      FILTERS_STORAGE_KEY,
      JSON.stringify({ ...filters, enrollmentFilter })
    );
  }, [filters, enrollmentFilter]);

  useEffect(() => {
    if (filters.id_mention || !mentionOptions.length) {
      return;
    }
    setFilters((previous) => ({
      ...previous,
      id_mention: mentionOptions[0].id
    }));
  }, [filters.id_mention, mentionOptions]);

  useEffect(() => {
    if (filters.id_year || !yearOptions.length) {
      return;
    }
    setFilters((previous) => ({
      ...previous,
      id_year: yearOptions[0].id
    }));
  }, [filters.id_year, yearOptions]);

  const selectionFilters = useMemo(
    () => ({
      ...filters,
      id_enter_year: filters.id_year,
      level: filters.level,
      enrollmentStatus:
        enrollmentFilter === "All" ? undefined : enrollmentFilter
    }),
    [filters, enrollmentFilter]
  );

  const { data: students = [] } = useSelectionStudents(selectionFilters);
  const handleCreate = useCallback(() => {
    setDialogMode("create");
    setHasCreatedStudent(false);
    setFormState((prev) => ({
      ...createEmptyFormState(),
      mentionId: filters.id_mention ?? "",
      semester: filters.semester ?? "",
      journeyId: filters.id_journey ?? "",
      level: filters.level ?? ""
    }));
    setDialogOpen(true);
  }, [filters.id_journey, filters.id_mention, filters.semester]);

  const handleEdit = useCallback((student: SelectionStudent) => {
    setDialogMode("edit");
    setHasCreatedStudent(false);
    const load = async () => {
      try {
        const profile = await fetchStudentByNumSelect(student.numSelect);
        setFormState({
          ...createEmptyFormState(),
          studentRecordId: profile.id ? String(profile.id) : student.recordId,
          studentId: profile.num_select ?? student.numSelect,
          cardNumber: profile.num_carte ?? student.id,
          firstName: profile.first_name ?? "",
          lastName: profile.last_name ?? "",
          email: profile.email ?? "",
          address: profile.address ?? "",
          phoneNumber: profile.phone_number ?? "",
          sex: profile.sex ?? "",
          maritalStatus: profile.martial_status ?? "",
          cinNumber: profile.num_of_cin ?? profile.num_cin ?? "",
          cinIssueDate: profile.date_of_cin ?? "",
          cinIssuePlace: profile.place_of_cin ?? "",
          birthDate: profile.date_of_birth ?? "",
          birthPlace: profile.place_of_birth ?? "",
          baccalaureateNumber: profile.num_of_baccalaureate ?? "",
          baccalaureateCenter: profile.center_of_baccalaureate ?? "",
          baccalaureateSerieId: profile.id_baccalaureate_series ?? "",
          baccalaureateYear: profile.year_of_baccalaureate ?? "",
          job: profile.job ?? "",
          fatherName: profile.father_name ?? "",
          fatherJob: profile.father_job ?? "",
          motherName: profile.mother_name ?? "",
          motherJob: profile.mother_job ?? "",
          parentAdress: profile.parent_address ?? "",
          nationalityId: profile.id_nationality
            ? String(profile.id_nationality)
            : undefined,
          picture: profile.picture ?? "",
          enrollmentStatus: profile.enrollment_status ?? "",
          mentionId: profile.id_mention
            ? String(profile.id_mention)
            : student.mentionId,
          journeyId: profile.id_journey ? String(profile.id_journey) : "",
          semester: profile.active_semester ?? "",
          status: profile.enrollment_status ?? "",
          level: profile.level ?? filters.level ?? "",
          mean: 0
        });
        setDialogOpen(true);
      } catch (error) {
        setFormError(
          error instanceof Error
            ? error.message
            : "Impossible de charger les détails de l'étudiant."
        );
      }
    };
    void load();
  }, []);

  const handleDelete = useCallback(
    async (student: SelectionStudent) => {
      const targetId = student.apiId || student.recordId;
      setDeletingId(targetId);
      try {
        await softDeleteStudent(targetId);
        await queryClient.invalidateQueries({ queryKey: ["selections"] });
      } finally {
        setDeletingId(null);
      }
    },
    [queryClient]
  );

  const renderStudentCard = useCallback(
    (row: Row<SelectionStudent>) => {
      const student = row.original;
      const statusStyle = statusStyles[student.enrollment_status];

      return (
        <div className="flex h-full flex-col gap-4 rounded-lg border bg-background p-5 shadow-sm">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-3">
              <img
                src={getAvatarUrl(student.fullName)}
                alt={student.fullName}
                className="h-8 w-8 shrink-0 rounded-full"
              />
              <div>
                <p className="text-sm font-semibold leading-tight text-foreground">
                  {student.fullName}
                </p>
                <p className="text-xs text-muted-foreground">{student.id}</p>
              </div>
            </div>
            <span
              className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium ${statusStyle.badge}`}
            >
              <span className={`h-1.5 w-1.5 rounded-full ${statusStyle.dot}`} />
              {student.enrollment_status}
            </span>
          </div>
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{student.mentionLabel}</span>
            <span>Last update {student.lastUpdate}</span>
          </div>
          <div className="flex justify-end gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleEdit(student)}
            >
              Edit
            </Button>
            <Button
              size="sm"
              variant="destructive"
              onClick={() => setConfirmDeleteStudent(student)}
              disabled={deletingId === student.recordId}
            >
              Delete
            </Button>
          </div>
        </div>
      );
    },
    [deletingId, handleDelete, handleEdit]
  );

  const studentColumns = useMemo<ColumnDef<SelectionStudent>[]>(
    () => [
      {
        accessorKey: "fullName",
        header: "Student",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.fullName}</span>
            <span className="text-xs text-muted-foreground">
              {row.original.numSelect}
            </span>
          </div>
        )
      },
      {
        accessorKey: "phoneNumber",
        header: "Télephone",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.phoneNumber}
          </span>
        )
      },
      {
        accessorKey: "status",
        header: "Status",
        cell: ({ row }) => {
          const value = row.original.enrollment_status;
          const style = statusStyles[value];
          return (
            <span className={`text-xs font-semibold ${style.text}`}>
              {value}
            </span>
          );
        }
      },
      {
        accessorKey: "lastUpdate",
        header: "Last update",
        cell: ({ row }) => (
          <span className="text-xs text-muted-foreground">
            {row.original.lastUpdate}
          </span>
        )
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              aria-label="Edit"
              onClick={() => handleEdit(row.original)}
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 text-destructive hover:text-destructive"
              aria-label="Delete"
              onClick={() => setConfirmDeleteStudent(row.original)}
              disabled={deletingId === (row.original.apiId || row.original.recordId)}
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        )
      }
    ],
    [deletingId, handleDelete, handleEdit]
  );

  const handleCreateStudent = useCallback(
    async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      setFormError(null);
      if (!filters.id_mention || !filters.id_year) {
        setFormError("Sélectionnez une mention et une année académique.");
        return;
      }

      const payload = {
        num_select: formState.studentId || undefined,
        num_carte: formState.cardNumber || undefined,
        first_name: formState.firstName || undefined,
        last_name: formState.lastName || undefined,
        email: formState.email || undefined,
        address: formState.address || undefined,
        sex: formState.sex || undefined,
        martial_status: formState.maritalStatus || undefined,
        num_of_cin: formState.cinNumber || undefined,
        date_of_cin: formState.cinIssueDate || undefined,
        place_of_cin: formState.cinIssuePlace || undefined,
        date_of_birth: formState.birthDate || undefined,
        place_of_birth: formState.birthPlace || undefined,
        phone_number: formState.phoneNumber || undefined,
        num_of_baccalaureate: formState.baccalaureateNumber || undefined,
        center_of_baccalaureate: formState.baccalaureateCenter || undefined,
        year_of_baccalaureate: formState.baccalaureateYear || undefined,
        id_baccalaureate_series: formState.baccalaureateSerieId || undefined,
        job: formState.job || "Etudiant",
        level: formState.level || filters.level || undefined,
        id_mention: formState.mentionId || filters.id_mention,
        id_journey: formState.journeyId || undefined,
        active_semester: formState.semester || filters.semester,
        enrollment_status: formState.enrollmentStatus || undefined,
        id_enter_year: filters.id_year,
        father_name: formState.fatherName || undefined,
        father_job: formState.fatherJob || undefined,
        mother_name: formState.motherName || undefined,
        mother_job: formState.motherJob || undefined,
        parent_address: formState.parentAdress || undefined,
        nationality_id: formState.nationalityId || undefined,
        picture: formState.picture || undefined
      };

      try {
        setFormSubmitting(true);
      if (dialogMode === "edit" && formState.studentRecordId) {
        await updateStudentProfile(formState.studentRecordId, payload);
      } else {
        const created = await createStudent(payload);
        setHasCreatedStudent(true);
        setDialogMode("edit");
        setFormState((prev) => ({
          ...prev,
          studentRecordId: created.id ? String(created.id) : prev.studentRecordId,
          studentId: created.num_select ?? prev.studentId,
          cardNumber: created.num_carte ?? prev.cardNumber
        }));
        setFormSubmitting(false);
        return;
      }
      await queryClient.invalidateQueries({ queryKey: ["selections"] });
      setDialogOpen(false);
    } catch (error) {
      setFormError(
          error instanceof Error
            ? error.message
            : "Erreur lors de l'enregistrement de l'étudiant."
        );
      } finally {
        setFormSubmitting(false);
      }
    },
    [filters, formState, queryClient]
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Dossier selection
          </h1>
          <p className="text-sm text-muted-foreground">
            Filter students and track dossier selection progress.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button size="sm" variant="outline" onClick={handleCreate}>
            Ajout étudiant
          </Button>
          <Button
            size="sm"
            variant="secondary"
            disabled={!filters.id_mention || !filters.id_year}
            onClick={async () => {
              setPrintError(null);
              if (!filters.id_year || !filters.id_mention) {
                setPrintError(
                  "Veuillez sélectionner une mention et une année pour imprimer la liste."
                );
                return;
              }
              setPrintingList(true);
              try {
                const result = await printSelectionList({
                  idYear: filters.id_year,
                  mentionId: filters.id_mention
                });
                const url = resolveAssetUrl(result.url || result.path);
                if (!url) {
                  throw new Error("Impossible de générer la liste.");
                }
                setPdfViewer({
                  open: true,
                  url,
                  title: "Liste des étudiants admis (sélection)"
                });
              } catch (error) {
                setPrintError(
                  error instanceof Error
                    ? error.message
                    : "Impossible de générer la liste."
                );
              } finally {
                setPrintingList(false);
              }
            }}
          >
            {printingList ? "Préparation..." : "Imprimer la liste"}
          </Button>
        </div>
      </div>
      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        {printError && (
          <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-2 text-sm text-destructive">
            {printError}
          </div>
        )}
        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={journeyOptions}
          levelOptions={[
            { value: "L1", label: "L1" },
            { value: "L2", label: "L2" },
            { value: "L3", label: "L3" },
            { value: "M1", label: "M1" },
            { value: "M2", label: "M2" }
          ]}
          academicYearOptions={yearOptions}
          semesters={semesters}
          showJourney={false}
          showLevel={true}
          showResetButton={true}
          showActiveFilters={true}
          filterClassname="grid gap-4 lg:grid-cols-3"
          summarySlot={
            <div className="rounded-md border bg-muted/10 p-4 text-sm text-muted-foreground space-y-3">
              <div className="flex flex-wrap items-center gap-3">
                <span className="font-medium text-foreground">Statut dossier</span>
                <select
                  className="h-9 rounded-md border bg-background px-2 text-sm text-foreground"
                  value={enrollmentFilter}
                  onChange={(e) =>
                    setEnrollmentFilter(
                      (e.target.value as SelectionStatus | "All") || "All"
                    )
                  }
                >
                  <option value="All">Tous</option>
                  <option value="Selected">Admis</option>
                  <option value="Pending">En attente</option>
                  <option value="Rejected">Rejeté</option>
                  <option value="Registered">Inscrit</option>
                  <option value="Former">Ancien</option>
                </select>
              </div>
              <div className="grid gap-2 md:grid-cols-2">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Students matching filters:
                  </span>
                  <span className="font-semibold text-primary">
                    {students.length}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Selected semester:
                  </span>
                  <span className="font-semibold text-primary">
                    {filters.semester || "—"}
                  </span>
                </div>
              </div>
            </div>
          }
        />
        <DataTable
          columns={studentColumns}
          data={students}
          searchPlaceholder="Search students"
          enableViewToggle
          enableColumnVisibility
          renderGridItem={renderStudentCard}
          gridClassName="sm:grid-cols-2 xl:grid-cols-3"
          gridEmptyState={
            <div className="flex h-40 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground">
              No students matching filters.
            </div>
          }
        />
        <PdfViewerModal
          open={pdfViewer.open}
          url={pdfViewer.url}
          title={pdfViewer.title}
          onOpenChange={(open) =>
            setPdfViewer((prev) => ({
              ...prev,
              open
            }))
          }
        />
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent
          className="sm:max-w-5xl lg:max-w-6xl h-[80vh] max-h-[80vh] overflow-hidden p-0 flex flex-col min-h-0"
          onInteractOutside={(event) => event.preventDefault()}
          onEscapeKeyDown={(event) => event.preventDefault()}
        >
          <DialogHeader className="px-6 pt-6 pb-2">
            <DialogTitle>
              {dialogMode === "edit" ? "Modifier étudiant" : "Ajout étudiant"}
            </DialogTitle>
          </DialogHeader>
          <form
            className="flex flex-1 flex-col min-h-0"
            onSubmit={handleCreateStudent}
          >
            {hasCreatedStudent && dialogMode === "edit" && (
              <div className="px-6 py-3 text-center text-sm font-semibold text-emerald-700 bg-emerald-50 border-b border-emerald-200">
                Étudiant créé. Vous pouvez maintenant compléter la scolarité.
              </div>
            )}
            <div className="flex-1 overflow-y-auto">
              <StudentForm
                formError={formError}
                formState={formState}
                setFormState={setFormState}
                dialogMode={dialogMode}
                filters={{
                  id_mention: filters.id_mention,
                  id_year: filters.id_year,
                  id_enter_year: filters.id_year,
                  semester: filters.semester
                }}
                enableLookup={false}
                enablePicture={false}
                mentionOptions={mentionOptions}
                registerType="SELECTION"
                annualRegisterDisabled={
                  !hasCreatedStudent && dialogMode === "create"
                }
                annualRegisterDisabledMessage="Créez d'abord l'étudiant (bouton Suivant), puis complétez la scolarité."
              />
            </div>
            <DialogFooter className="px-6 py-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={() => setDialogOpen(false)}
              >
                Annuler
              </Button>
              <Button type="submit" disabled={formSubmitting}>
                {formSubmitting
                  ? "Enregistrement..."
                  : dialogMode === "create" && !hasCreatedStudent
                    ? "Suivant"
                    : "Enregistrer"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(confirmDeleteStudent)}
        title="Supprimer l'étudiant ?"
        description={
          confirmDeleteStudent
            ? `Cette action masquera ${confirmDeleteStudent.fullName} de la liste.`
            : undefined
        }
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        destructive
        isConfirming={
          Boolean(confirmDeleteStudent) &&
          deletingId ===
            (confirmDeleteStudent?.apiId || confirmDeleteStudent?.recordId)
        }
        onCancel={() => setConfirmDeleteStudent(null)}
        onConfirm={() => {
          if (confirmDeleteStudent) {
            handleDelete(confirmDeleteStudent);
            setConfirmDeleteStudent(null);
          }
        }}
      />
    </div>
  );
};
