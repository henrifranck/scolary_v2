import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import type { Row } from "@tanstack/react-table";

import { Button } from "../../../components/ui/button";
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
  fetchReinscriptionsWithMeta,
  type ReinscriptionStatus
} from "../../../services/reinscription-service";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "../../../components/ui/dialog";
import { fetchJourneys as fetchJourneysByMention } from "../../../services/inscription-service";
import {
  updateStudentProfile,
  uploadStudentPicture,
  softDeleteStudent
} from "../../../services/student-service";
import { StudentForm } from "@/components/student-form/student-form";
import {
  StudentFormState,
  StudentProfile
} from "@/components/student-form/student-form-types";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { printStudentCards, printStudentsList } from "@/services/print-service";
import { PdfViewerModal } from "@/components/pdf-viewer-modal";
import { ActionButton } from "@/components/action-button";
import { useLookupOptions } from "@/hooks/use-lookup-options";

const semesters = Array.from({ length: 10 }, (_, index) => `S${index + 1}`);

const statusStyles: Record<
  ReinscriptionStatus,
  { text: string; badge: string; dot: string }
> = {
  Pending: {
    text: "text-muted-foreground",
    badge: "bg-slate-100 text-slate-700",
    dot: "bg-slate-400"
  },
  "In progress": {
    text: "text-amber-600",
    badge: "bg-amber-100 text-amber-700",
    dot: "bg-amber-500"
  },
  Validated: {
    text: "text-emerald-600",
    badge: "bg-emerald-100 text-emerald-700",
    dot: "bg-emerald-500"
  }
};

type ReinscriptionFormMode = "create" | "edit";
type EditableSection = "contact" | "birth" | "identity" | "school";

const createFormState = (
  overrides: Partial<StudentFormState> = {}
): StudentFormState => ({
  studentRecordId: "",
  studentId: "",
  cardNumber: "",
  firstName: "",
  fullName: "",
  phoneNumber: "",
  lastName: "",
  email: "",
  address: "",
  sex: "",
  maritalStatus: "",
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
  mentionId: "",
  journeyId: "",
  semester: "",
  status: "",
  mean: 0,
  picture: "",
  pictureFile: null,
  journeyLabel: "",
  mentionLabel: "",
  lastUpdate: "",
  annualRegister: [],
  ...overrides
});

const createEditingSectionsState = (): Record<EditableSection, boolean> => ({
  contact: false,
  birth: false,
  identity: false,
  school: false
});

const buildStudentUpdatePayload = (state: StudentFormState): StudentProfile => {
  const payload: StudentProfile = {
    id: state.studentRecordId || undefined,
    num_select: state.selectNumber || undefined,
    num_carte: state.cardNumber || undefined,
    first_name: state.firstName || undefined,
    last_name: state.lastName || undefined,
    email: state.email || undefined,
    address: state.address || undefined,
    sex: state.sex || undefined,
    martial_status: state.maritalStatus || undefined,
    num_of_cin: state.cinNumber || undefined,
    date_of_cin: state.cinIssueDate || undefined,
    place_of_cin: state.cinIssuePlace || undefined,
    date_of_birth: state.birthDate || undefined,
    place_of_birth: state.birthPlace || undefined,
    num_of_baccalaureate: state.baccalaureateNumber || undefined,
    center_of_baccalaureate: state.baccalaureateCenter || undefined,
    year_of_baccalaureate: state.baccalaureateYear || undefined,
    id_baccalaureate_series: state.baccalaureateSerieId || undefined,
    job: state.job || undefined,
    picture: state.picture || undefined,
    id_mention: state.mentionId || undefined,
    id_nationality: state.nationalityId,
    enrollment_status: state.enrollmentStatus || state.status || undefined,
    mean: state.mean || 0,
    mother_name: state.motherName || undefined,
    mother_job: state.motherJob || undefined,
    father_name: state.fatherName || undefined,
    father_job: state.fatherJob || undefined,
    parent_address: state.parentAdress || undefined,
    annual_register: state.annualRegister || undefined,
    phone_number: state.phoneNumber || undefined
  };

  return Object.fromEntries(
    Object.entries(payload).filter(
      ([, value]) => value !== undefined && value !== ""
    )
  ) as StudentProfile;
};

const getAvatarUrl = (fullName: string) => {
  const name = encodeURIComponent(fullName);
  return `https://ui-avatars.com/api/?name=${name}&background=random&color=fff&size=64`;
};

export const InscriptionPage = () => {
  const defaultSemester = semesters[0] ?? "";

  const { mentionOptions, isLoadingMentions, isLoadingAvailableModels } =
    useLookupOptions({
      includeMentions: true,
      includeAvailableModels: true
    });

  const FILTERS_STORAGE_KEY = "inscription.filters";
  const resolveHeaderAcademicYear = () => {
    if (typeof window === "undefined") {
      return "";
    }
    const stored = window.localStorage.getItem("selected_academic_year");
    if (!stored || stored === "all") {
      return "";
    }
    return stored;
  };

  const readStoredFilters = (): AcademicFilterValue | null => {
    if (typeof window === "undefined") {
      return null;
    }
    const raw = window.localStorage.getItem(FILTERS_STORAGE_KEY);
    if (!raw) {
      return null;
    }
    try {
      const parsed = JSON.parse(raw);
      if (
        parsed &&
        typeof parsed === "object" &&
        "id_mention" in parsed &&
        "id_journey" in parsed &&
        "semester" in parsed &&
        "register_type" in parsed &&
        "level" in parsed
      ) {
        const headerYear = resolveHeaderAcademicYear();
        return {
          ...(parsed as AcademicFilterValue),
          id_year: headerYear || (parsed as AcademicFilterValue).id_year || ""
        };
      }
    } catch {
      return null;
    }
    return null;
  };

  const [filters, setFilters] = useState<AcademicFilterValue>(() => {
    const stored = readStoredFilters();
    return (
      stored ?? {
        id_mention: "",
        id_journey: "",
        semester: defaultSemester,
        id_year: resolveHeaderAcademicYear(),
        level: "",
        register_type: "REGISTRATION"
      }
    );
  });
  const [filtersCollapsed, setFiltersCollapsed] = useState<boolean>(() => {
    if (typeof window === "undefined") {
      return false;
    }
    const raw = window.localStorage.getItem(`${FILTERS_STORAGE_KEY}.collapsed`);
    return raw === "true";
  });

  useEffect(() => {
    if (!mentionOptions.length) {
      return;
    }

    setFilters((previous) => {
      if (previous.id_mention) {
        return previous;
      }

      return {
        ...previous,
        id_mention: mentionOptions[0].id
      };
    });
  }, [mentionOptions]);

  useEffect(() => {
    const headerYear = resolveHeaderAcademicYear();
    if (!headerYear) return;
    setFilters((previous) => {
      if (previous.id_year === headerYear) {
        return previous;
      }
      return { ...previous, id_year: headerYear };
    });
  }, []);

  useEffect(() => {
    const handler = (event: Event) => {
      const detail =
        event instanceof CustomEvent ? String(event.detail ?? "") : "";
      const next =
        detail === "all" ? "" : detail || resolveHeaderAcademicYear();
      setFilters((previous) => ({ ...previous, id_year: next }));
    };
    if (typeof window === "undefined") return;
    window.addEventListener("academicYearChanged", handler);
    return () => window.removeEventListener("academicYearChanged", handler);
  }, []);

  const journeyQuery = useQuery({
    queryKey: ["reinscription", "journeys", filters.id_mention],
    queryFn: () => fetchJourneysByMention(Number(filters.id_mention)),
    enabled: Boolean(filters.id_mention),
    staleTime: 1000 * 60 * 30,
    gcTime: 1000 * 60 * 120,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchOnMount: false
  });

  const journeyOptions: JourneyOption[] = useMemo(() => {
    const journeys = journeyQuery.data ?? [];
    return journeys.map((journey) => {
      const semesterList = Array.isArray(journey.semester_list)
        ? journey.semester_list
            .map((entry) =>
              typeof entry === "string" ? entry : (entry?.semester ?? null)
            )
            .filter((semester): semester is string => Boolean(semester))
        : [];

      return {
        id: String(journey.id),
        label: journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
        id_mention: journey.id_mention
          ? String(journey.id_mention)
          : filters.id_mention,
        semesterList
      };
    });
  }, [filters.id_mention, journeyQuery.data]);

  useEffect(() => {
    if (!filters.id_mention) {
      setFilters((previous) =>
        previous.id_journey ? { ...previous, id_journey: "" } : previous
      );
      return;
    }

    if (!journeyOptions.length) {
      setFilters((previous) =>
        previous.id_journey ? { ...previous, id_journey: "" } : previous
      );
      return;
    }

    setFilters((previous) => {
      const hasCurrentJourney = journeyOptions.some(
        (journey) => journey.id === previous.id_journey
      );
      const nextJourneyId = hasCurrentJourney
        ? previous.id_journey
        : (journeyOptions[0]?.id ?? "");
      const nextJourney = journeyOptions.find(
        (journey) => journey.id === nextJourneyId
      );
      const allowedSemesters =
        nextJourney?.semesterList?.length && semesters.length
          ? nextJourney.semesterList
          : semesters;
      const resolvedSemester = allowedSemesters.includes(previous.semester)
        ? previous.semester
        : (allowedSemesters[0] ?? "");

      if (
        nextJourneyId === previous.id_journey &&
        resolvedSemester === previous.semester
      ) {
        return previous;
      }

      return {
        ...previous,
        id_journey: nextJourneyId,
        semester: resolvedSemester
      };
    });
  }, [journeyOptions, filters.id_mention]);

  const handleFiltersChange = useCallback((next: AcademicFilterValue) => {
    setFilters(next);
  }, []);

  const journeysLoading =
    journeyQuery.isPending ||
    journeyQuery.isFetching ||
    journeyQuery.isRefetching;

  const availableJourneys = useMemo(
    () =>
      journeyOptions.filter(
        (journey) => journey.id_mention === filters.id_mention
      ),
    [journeyOptions, filters.id_mention]
  );

  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const offset = (page - 1) * pageSize;

  const hasRequiredFilters = Boolean(
    filters.id_mention && filters.id_year && filters.id_journey && filters.level
  );

  useEffect(() => {
    setPage(1);
  }, [
    filters.id_mention,
    filters.id_journey,
    filters.id_year,
    filters.semester,
    filters.register_type,
    filters.level
  ]);

  const reinscriptionQuery = useQuery({
    queryKey: ["reinscription", "students", { filters, page, pageSize }],
    queryFn: () =>
      fetchReinscriptionsWithMeta({
        ...filters,
        limit: pageSize,
        offset
      }),
    enabled: hasRequiredFilters
  });

  const students = reinscriptionQuery.data?.data ?? [];
  const totalStudents = reinscriptionQuery.data?.count ?? 0;
  const displayedStudentCount = totalStudents || students.length;
  const studentsLoading = hasRequiredFilters
    ? reinscriptionQuery.isFetching || reinscriptionQuery.isPending
    : false;

  const isPageLoading =
    journeysLoading ||
    reinscriptionQuery.isFetching ||
    reinscriptionQuery.isPending ||
    isLoadingMentions ||
    isLoadingAvailableModels;

  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogMode, setDialogMode] = useState<ReinscriptionFormMode>("create");
  const [formState, setFormState] = useState<StudentFormState>(() =>
    createFormState({ semester: defaultSemester })
  );
  const [hasRegisterSemester, setHasRegisterSemester] = useState(false);
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [headerSearchQuery, setHeaderSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<StudentFormState[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [editingSections, setEditingSections] = useState<
    Record<EditableSection, boolean>
  >(() => createEditingSectionsState());
  const [formError, setFormError] = useState<string | null>(null);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [confirmDeleteStudent, setConfirmDeleteStudent] =
    useState<StudentFormState | null>(null);
  const [allowRegisterForm, setAllowRegisterForm] = useState(false);
  const [printError, setPrintError] = useState<string | null>(null);
  const [pdfViewer, setPdfViewer] = useState<{
    open: boolean;
    url?: string;
    urls?: string[];
    title?: string;
  }>({ open: false });

  useEffect(() => {
    if (!formError) return;
    const timer = window.setTimeout(() => setFormError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [formError]);

  useEffect(() => {
    if (!deleteError) return;
    const timer = window.setTimeout(() => setDeleteError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [deleteError]);

  useEffect(() => {
    if (!printError) return;
    const timer = window.setTimeout(() => setPrintError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [printError]);

  useEffect(() => {
    if (!dialogOpen) {
      setEditingSections(createEditingSectionsState());
      setFormError(null);
      setFormSubmitting(false);
      setHasRegisterSemester(false);
    }
  }, [dialogOpen]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    window.localStorage.setItem(FILTERS_STORAGE_KEY, JSON.stringify(filters));
  }, [filters]);

  const runHeaderSearch = useCallback(
    async (query: string) => {
      setSearchError(null);
      setSearchLoading(true);
      try {
        const response = await fetchReinscriptionsWithMeta({
          search: query,
          limit: 50,
          offset: 0,
          skipRegisterType: true
        });
        setSearchResults(response.data ?? []);
      } catch (error) {
        setSearchError(
          error instanceof Error
            ? error.message
            : "Impossible de charger les étudiants."
        );
        setSearchResults([]);
      } finally {
        setSearchLoading(false);
      }
    },
    [filters]
  );

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const handleHeaderSearch = (event: Event) => {
      const detail =
        event instanceof CustomEvent
          ? (event.detail as { scope?: string; query?: string })
          : {};
      if (detail.scope !== "student") {
        return;
      }
      const query = String(detail.query ?? "").trim();
      if (!query) {
        return;
      }
      setHeaderSearchQuery(query);
      setSearchModalOpen(true);
      void runHeaderSearch(query);
    };
    window.addEventListener("app-search", handleHeaderSearch);
    return () => window.removeEventListener("app-search", handleHeaderSearch);
  }, [runHeaderSearch]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    window.localStorage.setItem(
      `${FILTERS_STORAGE_KEY}.collapsed`,
      filtersCollapsed ? "true" : "false"
    );
  }, [filtersCollapsed]);

  const handleCreateStudent = useCallback(() => {
    setDialogMode("create");
    setFormState(
      createFormState({
        semester: filters.semester ?? "",
        mentionId: filters.id_mention ?? "",
        journeyId: filters.id_journey ?? ""
      })
    );
    setDialogOpen(true);
  }, [filters]);

  const handleEditStudent = useCallback((student: StudentFormState) => {
    setDialogMode("edit");
    setFormState(
      createFormState({
        studentRecordId: student.studentRecordId,
        studentId: student.studentId,
        cardNumber: student.cardNumber,
        selectNumber: student.selectNumber,
        firstName: student.firstName,
        lastName: student.lastName,
        email: student.email,
        address: student.address,
        cinNumber: student.cinNumber,
        cinIssueDate: student.cinIssueDate,
        cinIssuePlace: student.cinIssuePlace,
        birthDate: student.birthDate,
        birthPlace: student.birthPlace,
        mentionId: student.mentionId,
        journeyId: student.journeyId,
        semester: student.semester,
        baccalaureateSerieId: String(student.baccalaureateSerieId),
        baccalaureateYear: student.baccalaureateYear,
        baccalaureateCenter: student.baccalaureateCenter,
        generatedLevel: student.generatedLevel,
        status: student.status,
        lastUpdate: student.lastUpdate,
        picture: student.picture,
        fullName: student.fullName,
        enrollmentStatus: student.enrollmentStatus,
        job: student.job,
        maritalStatus: student.maritalStatus,
        phoneNumber: student.phoneNumber,
        mean: student.mean,
        annualRegister: student.annualRegister
      })
    );
    setDialogOpen(true);
  }, []);

  const handleFormSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);

    const trimmedCardNumber = (formState.cardNumber || "").trim();
    const missingCardNumber = !trimmedCardNumber;
    if (missingCardNumber && !allowRegisterForm) {
      setAllowRegisterForm(true);
    }

    const recordId = (formState.studentRecordId || "").trim();
    if (!recordId) {
      setFormError(
        "Impossible de déterminer l'identifiant interne de l'étudiant. Veuillez d'abord rechercher l'étudiant."
      );
      return;
    }

    setFormSubmitting(true);
    try {
      const payload: StudentProfile = {
        ...buildStudentUpdatePayload({
          ...formState,
          cardNumber: trimmedCardNumber
        }),
        new_registration: dialogMode !== "edit"
      };
      const updatedStudent = await updateStudentProfile(recordId, payload);

      // Keep the form in sync with the generated card/selection numbers so warnings disappear.
      setFormState((previous) => {
        const resolvedCard = updatedStudent.num_carte ?? previous.cardNumber;
        const resolvedSelect =
          updatedStudent.num_select ?? previous.selectNumber;
        const resolvedId = updatedStudent.id
          ? String(updatedStudent.id)
          : previous.studentId;

        return {
          ...previous,
          cardNumber: resolvedCard ?? "",
          selectNumber: resolvedSelect ?? "",
          studentId: resolvedId,
          fullName:
            `${updatedStudent.last_name ?? previous.lastName ?? ""} ${updatedStudent.first_name ?? previous.firstName ?? ""}`.trim() ||
            previous.fullName
        };
      });

      const resolvedCardNumber = (
        updatedStudent.num_carte ?? trimmedCardNumber
      ).trim();
      const shouldCloseDialog =
        dialogMode === "edit" ||
        (!missingCardNumber &&
          hasRegisterSemester &&
          Boolean(resolvedCardNumber));
      if (shouldCloseDialog) {
        setDialogOpen(false);
      }
      if (formState.pictureFile) {
        const updatedStudent = await uploadStudentPicture(
          recordId,
          formState.pictureFile
        );
        setFormState((previous: any) => ({
          ...previous,
          picture: updatedStudent.picture ?? previous.picture,
          pictureFile: null
        }));
      }
      // setDialogOpen(false);
      void reinscriptionQuery.refetch();
    } catch (error) {
      setFormError(
        error instanceof Error
          ? error.message
          : "Impossible d'enregistrer les modifications."
      );
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleSoftDelete = useCallback(
    async (student: StudentFormState) => {
      setDeleteError(null);
      setDeletingId(student.studentRecordId);
      try {
        await softDeleteStudent(student.studentRecordId);
        void reinscriptionQuery.refetch();
      } catch (error) {
        setDeleteError(
          error instanceof Error
            ? error.message
            : "Impossible de supprimer l'étudiant."
        );
      } finally {
        setDeletingId(null);
      }
    },
    [reinscriptionQuery]
  );

  const handlePageChange = (nextPage: number) => {
    setPage(Math.max(1, nextPage));
  };

  const handlePageSizeChange = (nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  };

  const studentColumns = useMemo<ColumnDef<StudentFormState>[]>(
    () => [
      {
        accessorKey: "fullName",
        header: "Nom et prénom",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.fullName}</span>
            <span className="text-xs text-muted-foreground">
              {row.original.cardNumber}
            </span>
          </div>
        )
      },
      {
        accessorKey: "status",
        header: "Status",
        cell: ({ row }) => {
          const value = row.original.status;
          const style =
            statusStyles[value as ReinscriptionStatus] ?? statusStyles.Pending;

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
          <ActionButton
            deletingId={deletingId}
            row={row}
            handleEdit={handleEditStudent}
            setConfirmDelete={setConfirmDeleteStudent}
          />
        )
      }
    ],
    [handleEditStudent, handleSoftDelete, deletingId]
  );

  const renderStudentCard = useCallback(
    (row: Row<StudentFormState>) => {
      const student = row.original;
      const statusStyle =
        statusStyles[student.status as ReinscriptionStatus] ??
        statusStyles.Pending;
      const avatarUrl =
        resolveAssetUrl(student.picture) || getAvatarUrl(student.fullName);

      return (
        <div className="flex h-full flex-col gap-4 rounded-lg border bg-background p-5 shadow-sm">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-3">
              <img
                src={avatarUrl}
                alt={student.fullName}
                className="h-8 w-8 shrink-0 rounded-full"
              />
              <div>
                <p className="text-sm font-semibold leading-tight text-foreground">
                  {student.fullName}
                </p>
                <p className="text-xs text-muted-foreground">
                  {student.studentRecordId}
                </p>
              </div>
            </div>
            <span
              className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium ${statusStyle.badge}`}
            >
              <span className={`h-1.5 w-1.5 rounded-full ${statusStyle.dot}`} />
              {student.status}
            </span>
          </div>
          <div className="space-y-2 text-sm">
            <div>
              <p className="font-medium leading-tight text-foreground">
                {student.journeyLabel}
              </p>
              <p className="text-xs text-muted-foreground">
                Semester {student.semester}
              </p>
            </div>
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>{student.mentionLabel}</span>
              <span>Last update {student.lastUpdate}</span>
            </div>
            <div className="flex justify-end">
              <Button
                size="sm"
                variant="outline"
                onClick={() => handleEditStudent(student)}
              >
                Edit
              </Button>
            </div>
          </div>
        </div>
      );
    },
    [handleEditStudent]
  );

  return (
    <div className="space-y-6">
      {isPageLoading && (
        <div className="sticky top-0 z-20 flex items-center gap-2 rounded-md border bg-muted/40 px-3 py-2 text-sm text-muted-foreground backdrop-blur">
          <div className="h-3 w-3 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          Chargement des données...
        </div>
      )}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Inscription</h1>
          <p className="text-sm text-muted-foreground">
            Filtrez par semestre, mention et parcours pour suivre le statut d'inscription.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button size="sm" onClick={handleCreateStudent}>
            Créer un étudiant
          </Button>
        </div>
      </div>
      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={journeyOptions}
          semesters={semesters}
          journeysLoading={journeysLoading}
          showResetButton={true}
          showActiveFilters={true}
          collapsed={filtersCollapsed}
          onCollapsedChange={setFiltersCollapsed}
          showLevel={true}
          filterClassname="grid gap-4 lg:grid-cols-3"
          summarySlot={
            <div className="rounded-md border bg-muted/10 p-4 text-sm text-muted-foreground">
              <div className="grid gap-2 md:grid-cols-3">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Étudiants correspondants :
                  </span>
                  <span className="font-semibold text-primary">
                    {displayedStudentCount}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Parcours disponibles :
                  </span>
                  <span className="font-semibold text-primary">
                    {availableJourneys.length}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Semestre sélectionné :
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
          isLoading={studentsLoading}
          totalItems={totalStudents}
          page={page}
          pageSize={pageSize}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
        />
        {deleteError ? (
          <p className="text-sm text-destructive">{deleteError}</p>
        ) : null}
        {printError ? (
          <p className="text-sm text-destructive">{printError}</p>
        ) : null}
      </div>

      <PdfViewerModal
        open={pdfViewer.open}
        url={pdfViewer.url}
        title={pdfViewer.title}
        onOpenChange={(open) => setPdfViewer((prev) => ({ ...prev, open }))}
      />

      <Dialog open={searchModalOpen} onOpenChange={setSearchModalOpen}>
        <DialogContent className="sm:max-w-2xl h-[70vh] max-h-[70vh] overflow-hidden p-0 flex flex-col min-h-0">
          <DialogHeader className="sticky top-0 z-10 border-b bg-background/95 px-6 py-4 backdrop-blur">
            <DialogTitle>Search students</DialogTitle>
            <DialogDescription>
              Results for "{headerSearchQuery}"
            </DialogDescription>
          </DialogHeader>
          <div className="flex-1 overflow-y-auto px-6 py-4">
            {searchLoading ? (
              <p className="text-sm text-muted-foreground">
                Searching students...
              </p>
            ) : searchError ? (
              <p className="text-sm text-destructive">{searchError}</p>
            ) : searchResults.length ? (
              <div className="space-y-2">
                {searchResults.map((student) => (
                  <Button
                    key={`${student.studentRecordId}-${student.studentId}`}
                    type="button"
                    variant="ghost"
                    className="w-full justify-between border border-transparent hover:border-border"
                    onClick={() => {
                      handleEditStudent(student);
                      setSearchModalOpen(false);
                    }}
                  >
                    <span className="text-left">
                      <span className="block font-medium">
                        {student.fullName}
                      </span>
                      <span className="block text-xs text-muted-foreground">
                        {student.studentId} · {student.journeyLabel}
                      </span>
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {student.semester || "—"}
                    </span>
                  </Button>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No students match this search.
              </p>
            )}
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent
          className="sm:max-w-4xl lg:max-w-6xl h-[90vh] max-h-[90vh] overflow-hidden p-0 flex flex-col min-h-0"
          onInteractOutside={(event) => event.preventDefault()}
          onEscapeKeyDown={(event) => event.preventDefault()}
        >
          <form
            className="flex flex-1 flex-col min-h-0"
            onSubmit={handleFormSubmit}
          >
            <DialogHeader className="sticky top-0 z-10 border-b bg-background/95 px-6 py-4 backdrop-blur">
              <DialogTitle>
                {dialogMode === "edit"
                  ? "Edit reinscription"
                  : "Create reinscription"}
              </DialogTitle>
              <DialogDescription>
                {dialogMode === "edit"
                  ? `Update student ${formState.studentId}`
                  : "This student already exists in the database. Review the key information before confirming the reinscription."}
              </DialogDescription>
            </DialogHeader>
            <StudentForm
              formError={formError}
              formState={formState}
              setFormState={setFormState}
              dialogMode={dialogMode}
              filters={filters}
              mentionOptions={mentionOptions}
              disabledEditing={!formState.studentRecordId}
              registerType="REGISTRATION"
              newRegistration={true}
              onRegistrationStatusChange={setHasRegisterSemester}
              annualRegisterDisabled={
                !allowRegisterForm && !(formState.cardNumber || "").trim()
              }
            />

            <DialogFooter className="sticky bottom-0 z-10 mt-auto border-t bg-background/95 px-6 py-4 backdrop-blur">
              <Button
                type="button"
                variant="outline"
                onClick={() => setDialogOpen(false)}
                disabled={formSubmitting}
              >
                Annuler
              </Button>
              <Button
                type="submit"
                disabled={
                  formSubmitting ||
                  ((formState.cardNumber || "").trim() !== "" &&
                    !hasRegisterSemester) ||
                  (!allowRegisterForm &&
                    !(formState.cardNumber || "").trim() &&
                    formState.enrollmentStatus === "pending")
                }
              >
                {formSubmitting
                  ? "Enregistrement..."
                  : dialogMode === "edit"
                    ? "Enregistrer les modifications"
                    : (formState.cardNumber || "").trim() || allowRegisterForm
                      ? "Confirmer l'inscription"
                      : formState.enrollmentStatus === "pending"
                        ? "Etudiant n'a pas séléctionné"
                        : "Suivant"}
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
          deletingId === confirmDeleteStudent?.studentRecordId
        }
        onCancel={() => setConfirmDeleteStudent(null)}
        onConfirm={() => {
          if (confirmDeleteStudent) {
            handleSoftDelete(confirmDeleteStudent);
            setConfirmDeleteStudent(null);
          }
        }}
      />
    </div>
  );
};
