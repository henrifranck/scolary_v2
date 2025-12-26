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
  AcademicYearOption,
  type AcademicFilterValue,
  type JourneyOption
} from "../../../components/filters/academic-filters";
import {
  fetchReinscriptionsWithMeta,
  type ReinscriptionStudent,
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
import {
  fetchMentions,
  fetchJourneys as fetchJourneysByMention,
  fetchCollegeYears
} from "../../../services/inscription-service";
import {
  updateStudentProfile,
  uploadStudentPicture,
  softDeleteStudent,
  type StudentUpdatePayload
} from "../../../services/student-service";
import { StudentForm } from "@/components/student-form/student-form";
import { StudentFormState } from "@/components/student-form/student-form-types";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { printStudentCards, printStudentsList } from "@/services/print-service";
import { PdfViewerModal } from "@/components/pdf-viewer-modal";
import { Mention, MentionOption } from "@/models/mentions";
import { ActionButton } from "@/components/action-button";

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
  job: "",
  enrollmentStatus: "",
  mentionId: "",
  journeyId: "",
  semester: "",
  status: "",
  notes: "",
  picture: "",
  pictureFile: null,
  annualRegister: [],
  ...overrides
});

const createEditingSectionsState = (): Record<EditableSection, boolean> => ({
  contact: false,
  birth: false,
  identity: false,
  school: false
});

const buildStudentUpdatePayload = (
  state: StudentFormState
): StudentUpdatePayload => {
  const payload: StudentUpdatePayload = {
    id: state.studentRecordId || undefined,
    num_select: state.studentId || undefined,
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
    job: state.job || undefined,
    picture: state.picture || undefined,
    id_mention: state.mentionId || undefined,
    id_journey: state.journeyId || undefined,
    active_semester: state.semester || undefined,
    enrollment_status: state.enrollmentStatus || state.status || undefined,
    notes: state.notes || undefined
  };

  return Object.fromEntries(
    Object.entries(payload).filter(
      ([, value]) => value !== undefined && value !== ""
    )
  ) as StudentUpdatePayload;
};

const getAvatarUrl = (fullName: string) => {
  const name = encodeURIComponent(fullName);
  return `https://ui-avatars.com/api/?name=${name}&background=random&color=fff&size=64`;
};

const InfoItem = ({ label, value }: { label: string; value?: string }) => (
  <div className="space-y-1 rounded-md border border-dashed border-border/60 bg-background/50 p-3">
    <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
      {label}
    </p>
    <p className="text-sm font-semibold text-foreground">
      {value?.trim() ? value : "—"}
    </p>
  </div>
);

const semesterToLevel = (semester?: string) => {
  const num = Number(String(semester ?? "").replace(/\D/g, ""));
  if (num <= 2) return "L1";
  if (num <= 4) return "L2";
  if (num <= 6) return "L3";
  if (num <= 8) return "M1";
  return "M2";
};

export const ReinscriptionPage = () => {
  const defaultSemester = semesters[0] ?? "";

  const { data: mentionData = [] } = useQuery({
    queryKey: ["reinscription", "mentions"],
    queryFn: () => fetchMentions({ user_only: true })
  });

  const { data: collegeYearData = [] } = useQuery({
    queryKey: ["reinscription", "collegeYears"],
    queryFn: fetchCollegeYears
  });

  const mentionOptions: MentionOption[] = useMemo(
    () =>
      mentionData.map((mention: Mention) => ({
        id: String(mention.id),
        label: mention.name ?? mention.name ?? `Mention ${mention.id}`
      })),
    [mentionData]
  );

  const yearOptions: AcademicYearOption[] = useMemo(
    () =>
      collegeYearData.map((year) => ({
        id: String(year.id),
        label: year.name ?? `Year ${year.id}`
      })),
    [collegeYearData]
  );

  const FILTERS_STORAGE_KEY = "reinscription.filters";

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
        "id_year" in parsed
      ) {
        return parsed as AcademicFilterValue;
      }
    } catch {
      return null;
    }
    return null;
  };

  const [journeyOptions, setJourneyOptions] = useState<JourneyOption[]>([]);
  const [journeysLoading, setJourneysLoading] = useState(false);

  const [filters, setFilters] = useState<AcademicFilterValue>(() => {
    const stored = readStoredFilters();
    return (
      stored ?? {
        id_mention: "",
        id_journey: "",
        semester: defaultSemester,
        id_year: ""
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
    if (filters.id_year || !yearOptions.length) {
      return;
    }

    setFilters((previous) => ({
      ...previous,
      id_year: yearOptions[0].id
    }));
  }, [yearOptions, filters.id_year]);

  useEffect(() => {
    const currentMentionId = filters.id_mention;
    if (!currentMentionId) {
      setJourneyOptions([]);
      setJourneysLoading(false);
      setFilters((previous) =>
        previous.id_journey ? { ...previous, id_journey: "" } : previous
      );
      return;
    }

    let cancelled = false;
    const loadJourneys = async () => {
      setJourneysLoading(true);
      try {
        const journeys = await fetchJourneysByMention(Number(currentMentionId));
        if (cancelled) {
          return;
        }

        const mappedJourneys: JourneyOption[] = journeys.map((journey) => {
          const semesterList = Array.isArray(journey.semester_list)
            ? journey.semester_list
                .map((entry) =>
                  typeof entry === "string" ? entry : (entry?.semester ?? null)
                )
                .filter((semester): semester is string => Boolean(semester))
            : [];

          return {
            id: String(journey.id),
            label:
              journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
            id_mention: currentMentionId,
            semesterList
          };
        });

        setJourneyOptions(mappedJourneys);
        setFilters((previous) => {
          const hasCurrentJourney = mappedJourneys.some(
            (journey) => journey.id === previous.id_journey
          );
          const nextJourneyId = hasCurrentJourney
            ? previous.id_journey
            : (mappedJourneys[0]?.id ?? "");
          const nextJourney = mappedJourneys.find(
            (journey) => journey.id === nextJourneyId
          );
          const allowedSemesters =
            nextJourney?.semesterList?.length && semesters.length
              ? nextJourney.semesterList
              : semesters;
          const resolvedSemester = allowedSemesters.includes(previous.semester)
            ? previous.semester
            : (allowedSemesters[0] ?? "");

          return {
            ...previous,
            id_journey: nextJourneyId,
            semester: resolvedSemester
          };
        });
      } catch {
        if (!cancelled) {
          setJourneyOptions([]);
          setFilters((previous) =>
            previous.id_journey ? { ...previous, id_journey: "" } : previous
          );
        }
      } finally {
        if (!cancelled) {
          setJourneysLoading(false);
        }
      }
    };

    void loadJourneys();
    return () => {
      cancelled = true;
    };
  }, [filters.id_mention]);

  const handleFiltersChange = useCallback((next: AcademicFilterValue) => {
    setFilters(next);
  }, []);

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
    filters.id_mention && filters.id_year && filters.id_journey
  );

  useEffect(() => {
    setPage(1);
  }, [
    filters.id_mention,
    filters.id_journey,
    filters.id_year,
    filters.semester
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

  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogMode, setDialogMode] = useState<ReinscriptionFormMode>("create");
  const [formState, setFormState] = useState<StudentFormState>(() =>
    createFormState({ semester: defaultSemester })
  );
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [headerSearchQuery, setHeaderSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<ReinscriptionStudent[]>(
    []
  );
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
    useState<ReinscriptionStudent | null>(null);
  const [printError, setPrintError] = useState<string | null>(null);
  const [printingList, setPrintingList] = useState(false);
  const [printingCards, setPrintingCards] = useState(false);
  const [printingCardsBack, setPrintingCardsBack] = useState(false);
  const [pdfViewer, setPdfViewer] = useState<{
    open: boolean;
    url?: string;
    title?: string;
  }>({ open: false });

  useEffect(() => {
    if (!dialogOpen) {
      setEditingSections(createEditingSectionsState());
      setFormError(null);
      setFormSubmitting(false);
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
          offset: 0
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
  const toggleSectionEditing = useCallback((section: EditableSection) => {
    setEditingSections((previous) => ({
      ...previous,
      [section]: !previous[section]
    }));
  }, []);

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

  const handleEditStudent = useCallback((student: ReinscriptionStudent) => {
    setDialogMode("edit");
    setFormState(
      createFormState({
        studentRecordId: student.recordId,
        studentId: student.id,
        cardNumber: student.id,
        firstName: student.firstName,
        lastName: student.lastName,
        email: "",
        address: "",
        cinNumber: "",
        cinIssueDate: "",
        cinIssuePlace: "",
        birthDate: "",
        birthPlace: "",
        mentionId: student.mentionId,
        journeyId: student.journeyId,
        semester: student.semester
      })
    );
    setDialogOpen(true);
  }, []);

  const handleFormSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);

    const trimmedCardNumber = (formState.cardNumber || "").trim();
    if (!trimmedCardNumber) {
      setFormError(
        "Le numéro de carte est requis pour enregistrer les modifications."
      );
      return;
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
      const payload = buildStudentUpdatePayload({
        ...formState,
        cardNumber: trimmedCardNumber
      });
      await updateStudentProfile(recordId, payload);
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
      setDialogOpen(false);
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
    async (student: ReinscriptionStudent) => {
      setDeleteError(null);
      setDeletingId(student.recordId);
      try {
        await softDeleteStudent(student.recordId);
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

  const studentColumns = useMemo<ColumnDef<ReinscriptionStudent>[]>(
    () => [
      {
        accessorKey: "fullName",
        header: "Nom et prénom",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.fullName}</span>
            <span className="text-xs text-muted-foreground">
              {row.original.id}
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
          // <div className="flex justify-end gap-2">
          //   <Button
          //     size="sm"
          //     variant="outline"
          //     onClick={() => handleEditStudent(row.original)}
          //   >
          //     Edit
          //   </Button>
          //   <Button
          //     size="sm"
          //     variant="destructive"
          //     onClick={() => setConfirmDeleteStudent(row.original)}
          //     disabled={deletingId === row.original.recordId}
          //   >
          //     Delete
          //   </Button>
          // </div>
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
    (row: Row<ReinscriptionStudent>) => {
      const student = row.original;
      const statusStyle =
        statusStyles[student.status as ReinscriptionStatus] ??
        statusStyles.Pending;
      const avatarUrl =
        resolveAssetUrl(student.photoUrl) || getAvatarUrl(student.fullName);

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
                <p className="text-xs text-muted-foreground">{student.id}</p>
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

  const handlePrintList = async () => {
    setPrintError(null);
    if (!filters.id_year || !filters.semester || !filters.id_journey) {
      setPrintError(
        "Veuillez sélectionner une année universitaire, un semestre et un parcours."
      );
      return;
    }
    setPrintingList(true);
    try {
      const result = await printStudentsList({
        idYear: filters.id_year,
        semester: filters.semester,
        journeyId: filters.id_journey
      });
      const url = resolveAssetUrl(result.url || result.path);
      if (!url) {
        throw new Error("Impossible de générer la liste.");
      }
      setPdfViewer({
        open: true,
        url,
        title: "Liste des étudiants inscrits"
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
  };

  const handlePrintCards = async () => {
    setPrintError(null);
    if (!filters.id_mention || !filters.id_year) {
      setPrintError("Veuillez sélectionner une mention et une année.");
      return;
    }
    setPrintingCards(true);
    try {
      const responses = await printStudentCards({
        mentionId: filters.id_mention,
        academicYearId: filters.id_year,
        journeyId: filters.id_journey || undefined,
        level: semesterToLevel(filters.semester)
      });
      const result = Array.isArray(responses) ? responses[0] : undefined;
      const url = resolveAssetUrl(result?.url || result?.path);
      if (!url) {
        throw new Error("Impossible de générer les cartes.");
      }
      setPdfViewer({
        open: true,
        url,
        title: "Cartes étudiant - recto"
      });
    } catch (error) {
      setPrintError(
        error instanceof Error
          ? error.message
          : "Impossible de générer les cartes."
      );
    } finally {
      setPrintingCards(false);
    }
  };

  const handlePrintCardsBack = async () => {
    setPrintError(null);
    if (!filters.id_mention || !filters.id_year) {
      setPrintError("Veuillez sélectionner une mention et une année.");
      return;
    }
    setPrintingCardsBack(true);
    try {
      const responses = await printStudentCards({
        mentionId: filters.id_mention,
        academicYearId: filters.id_year,
        journeyId: filters.id_journey || undefined,
        level: semesterToLevel(filters.semester)
      });
      const result = Array.isArray(responses) ? responses[1] : undefined;
      const url = resolveAssetUrl(result?.url || result?.path);
      if (!url) {
        throw new Error("Impossible de générer les cartes.");
      }
      setPdfViewer({
        open: true,
        url,
        title: "Cartes étudiant - verso"
      });
    } catch (error) {
      setPrintError(
        error instanceof Error
          ? error.message
          : "Impossible de générer les cartes."
      );
    } finally {
      setPrintingCardsBack(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Re-inscription
          </h1>
          <p className="text-sm text-muted-foreground">
            Filter students by semester, mention and journey to follow their
            re-inscription status.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button size="sm" onClick={handleCreateStudent}>
            Create student
          </Button>
          <Button
            size="sm"
            variant="secondary"
            onClick={handlePrintList}
            disabled={printingList || !filters.id_year}
          >
            {printingList ? "Preparing..." : "Print list"}
          </Button>
          <Button
            size="sm"
            variant="secondary"
            onClick={handlePrintCards}
            disabled={printingCards || !filters.id_mention}
          >
            {printingCards ? "Preparing..." : "Print cards (front)"}
          </Button>
          <Button
            size="sm"
            variant="secondary"
            onClick={handlePrintCardsBack}
            disabled={printingCardsBack || !filters.id_mention}
          >
            {printingCardsBack ? "Preparing..." : "Print cards (back)"}
          </Button>
        </div>
      </div>
      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={journeyOptions}
          academicYearOptions={yearOptions}
          semesters={semesters}
          journeysLoading={journeysLoading}
          showResetButton={true}
          showActiveFilters={true}
          collapsed={filtersCollapsed}
          onCollapsedChange={setFiltersCollapsed}
          showLevel={false}
          filterClassname="grid gap-4 lg:grid-cols-3"
          summarySlot={
            <div className="rounded-md border bg-muted/10 p-4 text-sm text-muted-foreground">
              <div className="grid gap-2 md:grid-cols-3">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Students matching filters:
                  </span>
                  <span className="font-semibold text-primary">
                    {displayedStudentCount}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    Available journeys:
                  </span>
                  <span className="font-semibold text-primary">
                    {availableJourneys.length}
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
                    key={`${student.recordId}-${student.id}`}
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
                        {student.id} · {student.journeyLabel}
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
        <DialogContent className="sm:max-w-4xl lg:max-w-6xl h-[90vh] max-h-[90vh] overflow-hidden p-0 flex flex-col min-h-0">
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
            />

            <DialogFooter className="sticky bottom-0 z-10 mt-auto border-t bg-background/95 px-6 py-4 backdrop-blur">
              <Button
                type="button"
                variant="outline"
                onClick={() => setDialogOpen(false)}
                disabled={formSubmitting}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={formSubmitting}>
                {formSubmitting
                  ? "Saving..."
                  : dialogMode === "edit"
                    ? "Save changes"
                    : "Confirm reinscription"}
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
          deletingId === confirmDeleteStudent?.recordId
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
