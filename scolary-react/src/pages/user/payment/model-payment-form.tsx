import { Button } from "@/components/ui/button";
import { Check, Pencil, Plus, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  EditableSection,
  StudentAnnualProps,
  StudentDocumentState,
  StudentPaymentState,
  StudentSemesterState
} from "@/components/student-form/student-form-types";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { fetchJourneys } from "@/services/inscription-service";
import {
  createAnnualRegister,
  createPayment,
  createRegisterSemester,
  deletePayment,
  deleteAnnualRegister,
  deleteRegisterSemester,
  fetchAnnualRegisterByCardNumber,
  updatePayment,
  updateRegisterSemester
} from "@/services/annual-register-service";
import { ConfirmDialog } from "@/components/confirm-dialog";
import {
  deleteDocument,
  updateDocument,
  uploadDocument
} from "@/services/document-service";
import { fetchAvailableServices } from "@/services/available-service";
import { fetchAvailableServiceRequiredDocuments } from "@/services/available-service-required-document";
import { fetchEnrollmentFees } from "@/services/enrollment-fee-service";
import { DocumentEditor, DocumentSummary } from "./model-payment-document";
import {
  RegistrationEditor,
  RegistrationSummary
} from "./model-payment-registration";
import { PaymentEditor, PaymentSummary } from "./model-payment-payment";
import { RequiredDocument } from "@/models/required-document";

interface ReinscriptionAnnualFormProps {
  annualRegister: Array<StudentAnnualProps>;
  editingSections: Record<EditableSection, boolean>;
  cardNumber?: string;
  filters?: any;
  defaultMentionId?: string;
  disabledEditing?: boolean;
  registerType: string;
  studentFullName?: string;
  onRegistrationStatusChange?: (hasRegistration: boolean) => void;
}

export const handleFormSubmit = (e: React.FormEvent) => {};

export const ReinscriptionAnnualRegister = ({
  annualRegister,
  editingSections,
  cardNumber,
  filters,
  defaultMentionId,
  disabledEditing = false,
  registerType,
  studentFullName,
  onRegistrationStatusChange
}: ReinscriptionAnnualFormProps) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [annualRegisterDrafts, setAnnualRegisterDrafts] = useState<
    Array<StudentAnnualProps & { isEditing?: boolean; isNew?: boolean }>
  >([]);
  const [paymentDrafts, setPaymentDrafts] = useState<
    Record<string, StudentPaymentState[]>
  >({});
  const [registrationDrafts, setRegistrationDrafts] = useState<
    Record<string, StudentSemesterState[]>
  >({});
  const [documentDrafts, setDocumentDrafts] = useState<
    Record<string, StudentDocumentState[]>
  >({});
  const [editingPaymentIndexByAnnual, setEditingPaymentIndexByAnnual] =
    useState<Record<string, number | null>>({});
  const [
    editingRegistrationIndexByAnnual,
    setEditingRegistrationIndexByAnnual
  ] = useState<Record<string, number | null>>({});
  const [journeyOptions, setJourneyOptions] = useState<
    Array<{
      id: string;
      label: string;
      semesterList: string[];
      mentionId?: string;
    }>
  >([]);
  const [savedAnnualRegisters, setSavedAnnualRegisters] = useState<
    Array<StudentAnnualProps>
  >([]);
  const [savedPaymentDrafts, setSavedPaymentDrafts] = useState<
    Record<string, StudentPaymentState[]>
  >({});
  const [savedRegistrationDrafts, setSavedRegistrationDrafts] = useState<
    Record<string, StudentSemesterState[]>
  >({});
  const [savedDocumentDrafts, setSavedDocumentDrafts] = useState<
    Record<string, StudentDocumentState[]>
  >({});
  const [saveError, setSaveError] = useState<string | null>(null);
  const [savingIndex, setSavingIndex] = useState<number | null>(null);
  const [annualRegisterLoading, setAnnualRegisterLoading] = useState(false);
  const [documentUploadError, setDocumentUploadError] = useState<string | null>(
    null
  );
  const [documentUploadingIndex, setDocumentUploadingIndex] = useState<
    number | null
  >(null);
  const [requiredDocuments, setRequiredDocuments] = useState<
    RequiredDocument[]
  >([]);
  const [documentStatus, setDocumentStatus] = useState<
    "none" | "missing" | "complete" | "not_applicable"
  >("not_applicable");
  const [paymentStatus, setPaymentStatus] = useState<
    "none" | "partial" | "complete" | "not_applicable"
  >("not_applicable");
  const [documentDescriptions, setDocumentDescriptions] = useState<
    Record<string, string>
  >({});
  const [confirmDeleteTarget, setConfirmDeleteTarget] = useState<{
    type: "annual" | "payment" | "registration";
    index: number;
    itemIndex?: number;
  } | null>(null);

  useEffect(() => {
    if (!saveError) return;
    const timer = window.setTimeout(() => setSaveError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [saveError]);

  useEffect(() => {
    if (!documentUploadError) return;
    const timer = window.setTimeout(() => setDocumentUploadError(null), 5000);
    return () => window.clearTimeout(timer);
  }, [documentUploadError]);

  useEffect(() => {
    if (!onRegistrationStatusChange) return;
    const hasDrafts = Object.values(registrationDrafts).some(
      (entries) => Array.isArray(entries) && entries.length > 0
    );
    const hasSaved = Object.values(savedRegistrationDrafts).some(
      (entries) => Array.isArray(entries) && entries.length > 0
    );
    onRegistrationStatusChange(hasDrafts || hasSaved);
  }, [registrationDrafts, savedRegistrationDrafts, onRegistrationStatusChange]);
  const routeUi =
    registerType === "REGISTRATION" ? "re-registration" : "selection";
  const { data: availableServiceData } = useQuery({
    queryKey: ["available-services", routeUi],
    queryFn: () =>
      fetchAvailableServices({
        where: JSON.stringify([
          { key: "route_ui", operator: "==", value: routeUi }
        ]),
        relation: JSON.stringify(["available_service_required_document"]),
        limit: 1
      }),
    staleTime: 1000 * 60 * 30,
    gcTime: 1000 * 60 * 120,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchOnMount: false
  });

  const availableServiceId = availableServiceData?.data?.[0]?.id;

  const { data: requiredDocData } = useQuery({
    queryKey: ["available-service-required-documents", availableServiceId],
    queryFn: () =>
      fetchAvailableServiceRequiredDocuments({
        where: JSON.stringify([
          {
            key: "id_available_service",
            operator: "==",
            value: availableServiceId
          }
        ]),
        relation: JSON.stringify(["required_document{id,name}"]),
        limit: 1000
      }),
    enabled: Boolean(availableServiceId),
    staleTime: 1000 * 60 * 30,
    gcTime: 1000 * 60 * 120,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchOnMount: false
  });

  const { data: enrollmentFeeData } = useQuery({
    queryKey: [
      "enrollment-fees",
      registerType,
      filters?.id_year,
      defaultMentionId ?? filters?.id_mention
    ],
    queryFn: () =>
      fetchEnrollmentFees({
        where: JSON.stringify([
          { key: "id_academic_year", operator: "==", value: filters?.id_year },
          {
            key: "id_mention",
            operator: "==",
            value: defaultMentionId ?? filters?.id_mention
          },
          { key: "register_type", operator: "==", value: registerType }
        ])
      }),
    enabled: Boolean(
      filters?.id_year && (defaultMentionId ?? filters?.id_mention)
    ),
    staleTime: 1000 * 60 * 30,
    gcTime: 1000 * 60 * 120,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchOnMount: false
  });

  useEffect(() => {
    const docs =
      requiredDocData?.data
        ?.map((entry) => entry.required_document)
        .filter((doc): doc is RequiredDocument => Boolean(doc)) ?? [];
    setRequiredDocuments(docs);
    setDocumentStatus(docs.length ? "missing" : "not_applicable");
  }, [requiredDocData]);

  const emptyJourney = {
    id: 0,
    name: "",
    abbreviation: "",
    id_mention: 0
  };

  const renderDocumentStatusBadge = (
    status: "none" | "missing" | "complete" | "not_applicable"
  ) => {
    const color =
      status === "complete"
        ? "bg-emerald-500"
        : status === "missing"
          ? "bg-amber-500"
          : status === "none"
            ? "bg-red-500"
            : "bg-muted-foreground/50";
    return <span className={`h-2.5 w-2.5 rounded-full ${color}`} />;
  };

  const renderPaymentStatusBadge = (
    status: "none" | "partial" | "complete" | "not_applicable"
  ) => {
    const color =
      status === "complete"
        ? "bg-emerald-500"
        : status === "partial"
          ? "bg-amber-500"
          : status === "none"
            ? "bg-red-500"
            : "bg-muted-foreground/50";
    return <span className={`h-2.5 w-2.5 rounded-full ${color}`} />;
  };

  const createEmptyPayment = () => ({
    id: undefined,
    num_receipt: "",
    date_receipt: "",
    payed: 0,
    description: ""
  });

  const createEmptyRegisterSemester = () => ({
    id: undefined,
    id_journey: undefined,
    semester: "",
    repeat_status: "",
    journey: { ...emptyJourney }
  });

  const createEmptyAnnualRegister = (
    academicYear?: StudentAnnualProps["academic_year"]
  ) => ({
    academic_year: academicYear,
    payment: [],
    register_semester: [],
    isEditing: true,
    isNew: true
  });

  const mentionId =
    defaultMentionId ?? filters?.id_mention ?? filters?.mentionId ?? "";
  const currentAcademicYear =
    annualRegisterDrafts[0]?.academic_year ?? annualRegister[0]?.academic_year;
  const currentAcademicYearName = currentAcademicYear?.name ?? "";

  const getAnnualKey = (
    annual: StudentAnnualProps & { id?: number },
    index: number
  ) => String(annual.id ?? index);

  const mergeAnnualWithDrafts = (
    annual: StudentAnnualProps & { isEditing?: boolean; isNew?: boolean },
    index: number
  ) => {
    const key = getAnnualKey(annual, index);
    return {
      ...annual,
      payment: paymentDrafts[key] ?? [],
      register_semester: registrationDrafts[key] ?? [],
      document: documentDrafts[key] ?? []
    };
  };

  const displayAnnualRegisters = annualRegisterDrafts.length
    ? annualRegisterDrafts.map(mergeAnnualWithDrafts)
    : annualRegister;
  const hasRegistrationEntries = annualRegisterDrafts.some(
    (annual, index) =>
      (registrationDrafts[getAnnualKey(annual, index)] ?? []).length
  );
  const hasPaymentEntries = annualRegisterDrafts.some(
    (annual, index) => (paymentDrafts[getAnnualKey(annual, index)] ?? []).length
  );

  useEffect(() => {
    if (!requiredDocuments.length) {
      setDocumentStatus("not_applicable");
      return;
    }

    const requiredIds = new Set(requiredDocuments.map((doc) => doc.id));
    const uploadedIds = new Set<number>();

    displayAnnualRegisters.forEach((annual) => {
      (annual.document ?? []).forEach((doc) => {
        if (
          doc.id_required_document &&
          requiredIds.has(doc.id_required_document)
        ) {
          uploadedIds.add(doc.id_required_document);
        }
      });
    });

    if (uploadedIds.size === 0) {
      setDocumentStatus("none");
    } else if (uploadedIds.size === requiredIds.size) {
      setDocumentStatus("complete");
    } else {
      setDocumentStatus("missing");
    }
  }, [displayAnnualRegisters, requiredDocuments]);

  useEffect(() => {
    if (!displayAnnualRegisters.length) {
      setPaymentStatus("not_applicable");
      return;
    }

    const statuses = displayAnnualRegisters
      .map((annual) => annual.payment_status as string | undefined)
      .filter(Boolean) as Array<
      "none" | "partial" | "complete" | "not_applicable"
    >;

    if (!statuses.length) {
      setPaymentStatus("not_applicable");
      return;
    }

    if (statuses.includes("none")) {
      setPaymentStatus("none");
    } else if (statuses.includes("partial")) {
      setPaymentStatus("partial");
    } else if (statuses.every((s) => s === "complete")) {
      setPaymentStatus("complete");
    } else {
      setPaymentStatus("not_applicable");
    }
  }, [displayAnnualRegisters]);

  const { data: journeyData } = useQuery({
    queryKey: ["journeys", "mention", mentionId],
    queryFn: () => fetchJourneys(mentionId),
    enabled: Boolean(mentionId),
    staleTime: 1000 * 60 * 30,
    gcTime: 1000 * 60 * 120,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchOnMount: false
  });

  useEffect(() => {
    if (!journeyData) {
      setJourneyOptions([]);
      return;
    }
    const normalized = journeyData.map((journey) => {
      const semesterList = Array.isArray(journey.semester_list)
        ? journey.semester_list
            .map((semester) =>
              typeof semester === "string"
                ? semester
                : (semester?.semester ?? "")
            )
            .filter((semester): semester is string => Boolean(semester))
        : [];

      return {
        id: String(journey.id),
        label: journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
        semesterList,
        mentionId: journey.id_mention ? String(journey.id_mention) : undefined
      };
    });
    setJourneyOptions(normalized);
  }, [journeyData]);
  useEffect(() => {
    const normalized = annualRegister.map((annual) => ({
      ...annual,
      isEditing: false,
      isNew: false
    }));
    setAnnualRegisterDrafts(normalized);
    setSavedAnnualRegisters(
      normalized.map(({ isEditing, isNew, ...rest }) => rest)
    );
    const initialPaymentDrafts: Record<string, StudentPaymentState[]> = {};
    const initialRegistrationDrafts: Record<string, StudentSemesterState[]> =
      {};
    const initialDocumentDrafts: Record<string, StudentDocumentState[]> = {};
    normalized.forEach((annual, index) => {
      const key = getAnnualKey(annual, index);
      initialPaymentDrafts[key] =
        annual.payment && annual.payment.length ? annual.payment : [];
      initialRegistrationDrafts[key] =
        annual.register_semester && annual.register_semester.length
          ? annual.register_semester
          : [];
      initialDocumentDrafts[key] =
        annual.document && annual.document.length ? annual.document : [];
    });
    setPaymentDrafts(initialPaymentDrafts);
    setRegistrationDrafts(initialRegistrationDrafts);
    setDocumentDrafts(initialDocumentDrafts);
    setSavedPaymentDrafts(initialPaymentDrafts);
    setSavedRegistrationDrafts(initialRegistrationDrafts);
    setSavedDocumentDrafts(initialDocumentDrafts);
    const initialEditingPayments: Record<string, number | null> = {};
    const initialEditingRegistrations: Record<string, number | null> = {};
    Object.keys(initialPaymentDrafts).forEach((key) => {
      initialEditingPayments[key] = null;
    });
    Object.keys(initialRegistrationDrafts).forEach((key) => {
      initialEditingRegistrations[key] = null;
    });
    setEditingPaymentIndexByAnnual(initialEditingPayments);
    setEditingRegistrationIndexByAnnual(initialEditingRegistrations);
    setDocumentDescriptions({});
  }, [annualRegister]);

  useEffect(() => {
    if (!dialogOpen) {
      return;
    }
    const identifier = cardNumber?.trim() ?? "";
    if (!identifier) {
      return;
    }
    const academicYearId =
      filters?.academicYearId ??
      filters?.id_year ??
      filters?.id_enter_year ??
      filters?.id_academic_year;
    let isMounted = true;
    setAnnualRegisterLoading(true);
    fetchAnnualRegisterByCardNumber(
      identifier,
      registerType,
      academicYearId ?? undefined
    )
      .then((response) => {
        if (!isMounted) {
          return;
        }
        const normalized = (response.data ?? []).map((annual) => ({
          ...annual,
          isEditing: false,
          isNew: false
        }));
        setAnnualRegisterDrafts(normalized);
        setSavedAnnualRegisters(
          normalized.map(({ isEditing, isNew, ...rest }) => rest)
        );
        const initialPaymentDrafts: Record<string, StudentPaymentState[]> = {};
        const initialRegistrationDrafts: Record<
          string,
          StudentSemesterState[]
        > = {};
        const initialDocumentDrafts: Record<string, StudentDocumentState[]> =
          {};
        normalized.forEach((annual, index) => {
          const key = getAnnualKey(annual, index);
          initialPaymentDrafts[key] =
            annual.payment && annual.payment.length ? annual.payment : [];
          initialRegistrationDrafts[key] =
            annual.register_semester && annual.register_semester.length
              ? annual.register_semester
              : [];
          initialDocumentDrafts[key] =
            annual.document && annual.document.length ? annual.document : [];
        });
        setPaymentDrafts(initialPaymentDrafts);
        setRegistrationDrafts(initialRegistrationDrafts);
        setDocumentDrafts(initialDocumentDrafts);
        setSavedPaymentDrafts(initialPaymentDrafts);
        setSavedRegistrationDrafts(initialRegistrationDrafts);
        setSavedDocumentDrafts(initialDocumentDrafts);
        const initialEditingPayments: Record<string, number | null> = {};
        const initialEditingRegistrations: Record<string, number | null> = {};
        Object.keys(initialPaymentDrafts).forEach((key) => {
          initialEditingPayments[key] = null;
        });
        Object.keys(initialRegistrationDrafts).forEach((key) => {
          initialEditingRegistrations[key] = null;
        });
        setEditingPaymentIndexByAnnual(initialEditingPayments);
        setEditingRegistrationIndexByAnnual(initialEditingRegistrations);
        setDocumentDescriptions({});
      })
      .catch((error) => {
        if (isMounted) {
          setSaveError(
            error instanceof Error
              ? error.message
              : "Erreur lors du chargement des inscriptions."
          );
        }
      })
      .finally(() => {
        if (isMounted) {
          setAnnualRegisterLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [dialogOpen, cardNumber]);

  const handleAddAnnualRegister = async () => {
    setSaveError(null);
    const identifier = cardNumber?.trim() ?? "";
    const academicYearId = Number(filters?.id_year ?? filters?.academicYearId);

    const idLabel =
      registerType === "SELECTION"
        ? "Le numéro de sélection est requis pour enregistrer."
        : "Le numéro de carte est requis pour enregistrer.";

    if (!identifier) {
      setSaveError(idLabel);
      return;
    }
    if (!academicYearId) {
      setSaveError("L'année académique est requise pour enregistrer.");
      return;
    }

    try {
      const created = await createAnnualRegister({
        ...(registerType === "SELECTION"
          ? { num_select: identifier }
          : { num_carte: identifier }),
        id_academic_year: academicYearId,
        semester_count: 1,
        register_type: registerType
      });
      if (!created?.id) {
        throw new Error("Impossible de créer la fiche annuelle.");
      }
      setAnnualRegisterDrafts((previous) => [
        ...previous,
        {
          ...createEmptyAnnualRegister(currentAcademicYear),
          id: created.id,
          academic_year: created.academic_year ?? currentAcademicYear,
          isEditing: true,
          isNew: true
        }
      ]);
      const newKey = String(created.id);
      const defaultFee = enrollmentFeeData?.data?.[0]?.price ?? 0;
      const defaultPayment =
        defaultFee > 0
          ? [
              {
                id: undefined,
                num_receipt: "",
                date_receipt: "",
                payed: defaultFee,
                description: "Frais d'inscription"
              }
            ]
          : [];
      setPaymentDrafts((previous) => ({
        ...previous,
        [newKey]: defaultPayment
      }));
      setRegistrationDrafts((previous) => ({
        ...previous,
        [newKey]: []
      }));
      setDocumentDrafts((previous) => ({
        ...previous,
        [newKey]: []
      }));
      setSavedPaymentDrafts((previous) => ({
        ...previous,
        [newKey]: []
      }));
      setSavedRegistrationDrafts((previous) => ({
        ...previous,
        [newKey]: []
      }));
      setSavedDocumentDrafts((previous) => ({
        ...previous,
        [newKey]: []
      }));
      setEditingPaymentIndexByAnnual((previous) => ({
        ...previous,
        [newKey]: null
      }));
      setEditingRegistrationIndexByAnnual((previous) => ({
        ...previous,
        [newKey]: null
      }));
    } catch (error) {
      setSaveError(
        error instanceof Error ? error.message : "Impossible d'ajouter."
      );
    }
  };

  const handleDeleteAnnualRegister = (index: number) => {
    const target = annualRegisterDrafts[index];
    setSaveError(null);
    if (!target?.id) {
      setAnnualRegisterDrafts((previous) =>
        previous.filter((_annual, annualIndex) => annualIndex !== index)
      );
      return;
    }

    const targetKey = getAnnualKey(target, index);
    setSavingIndex(index);
    deleteAnnualRegister(target.id)
      .then(() => {
        setAnnualRegisterDrafts((previous) =>
          previous.filter((_annual, annualIndex) => annualIndex !== index)
        );
        setSavedAnnualRegisters((previous) =>
          previous.filter((_annual, annualIndex) => annualIndex !== index)
        );
        setPaymentDrafts((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setRegistrationDrafts((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setDocumentDrafts((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setSavedPaymentDrafts((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setSavedRegistrationDrafts((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setSavedDocumentDrafts((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setEditingPaymentIndexByAnnual((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
        setEditingRegistrationIndexByAnnual((previous) => {
          const next = { ...previous };
          delete next[targetKey];
          return next;
        });
      })
      .catch((error) => {
        setSaveError(
          error instanceof Error ? error.message : "Impossible de supprimer."
        );
      })
      .finally(() => {
        setSavingIndex((current) => (current === index ? null : current));
      });
  };

  const handleAddPayment = () => {
    if (!annualRegisterDrafts.length) {
      return;
    }
    let targetIndex = annualRegisterDrafts.findIndex((annual, index) => {
      const key = getAnnualKey(annual, index);
      return !paymentDrafts[key]?.length;
    });
    if (targetIndex < 0) {
      targetIndex = 0;
    }
    const target = annualRegisterDrafts[targetIndex];
    const targetKey = getAnnualKey(target, targetIndex);
    setSaveError(null);
    setPaymentDrafts((previous) => ({
      ...previous,
      [targetKey]: [...(previous[targetKey] ?? []), createEmptyPayment()]
    }));
    setEditingPaymentIndexByAnnual((previous) => ({
      ...previous,
      [targetKey]: paymentDrafts[targetKey]?.length ?? 0
    }));
    setAnnualRegisterDrafts((previous) =>
      previous.map((annual, annualIndex) =>
        annualIndex === targetIndex ? { ...annual, isEditing: true } : annual
      )
    );
  };

  const handleAddRegistration = () => {
    if (!annualRegisterDrafts.length) {
      return;
    }
    let targetIndex = annualRegisterDrafts.findIndex((annual, index) => {
      const key = getAnnualKey(annual, index);
      return !registrationDrafts[key]?.length;
    });
    if (targetIndex < 0) {
      targetIndex = 0;
    }
    const target = annualRegisterDrafts[targetIndex];
    const targetKey = getAnnualKey(target, targetIndex);
    setSaveError(null);
    setRegistrationDrafts((previous) => ({
      ...previous,
      [targetKey]: [
        ...(previous[targetKey] ?? []),
        createEmptyRegisterSemester()
      ]
    }));
    setEditingRegistrationIndexByAnnual((previous) => ({
      ...previous,
      [targetKey]: registrationDrafts[targetKey]?.length ?? 0
    }));
    setAnnualRegisterDrafts((previous) =>
      previous.map((annual, annualIndex) =>
        annualIndex === targetIndex ? { ...annual, isEditing: true } : annual
      )
    );
  };

  const handleDeletePayment = (index: number, paymentIndex: number) => {
    const target = annualRegisterDrafts[index];
    const targetKey = getAnnualKey(target, index);
    const paymentEntry = paymentDrafts[targetKey]?.[paymentIndex];
    setSaveError(null);

    if (!paymentEntry?.id) {
      setPaymentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (_item, itemIndex) => itemIndex !== paymentIndex
        )
      }));
      setSavedPaymentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (_item, itemIndex) => itemIndex !== paymentIndex
        )
      }));
      setEditingPaymentIndexByAnnual((previous) => {
        const current = previous[targetKey];
        if (current === null || current === undefined) {
          return previous;
        }
        const nextIndex =
          current === paymentIndex
            ? null
            : current > paymentIndex
              ? current - 1
              : current;
        return {
          ...previous,
          [targetKey]: nextIndex
        };
      });
      return;
    }

    setSavingIndex(index);
    deletePayment(paymentEntry.id)
      .then(() => {
        setPaymentDrafts((previous) => ({
          ...previous,
          [targetKey]: (previous[targetKey] ?? []).filter(
            (_item, itemIndex) => itemIndex !== paymentIndex
          )
        }));
        setSavedPaymentDrafts((previous) => ({
          ...previous,
          [targetKey]: (previous[targetKey] ?? []).filter(
            (_item, itemIndex) => itemIndex !== paymentIndex
          )
        }));
        setEditingPaymentIndexByAnnual((previous) => {
          const current = previous[targetKey];
          if (current === null || current === undefined) {
            return previous;
          }
          const nextIndex =
            current === paymentIndex
              ? null
              : current > paymentIndex
                ? current - 1
                : current;
          return {
            ...previous,
            [targetKey]: nextIndex
          };
        });
      })
      .catch((error) => {
        setSaveError(
          error instanceof Error ? error.message : "Impossible de supprimer."
        );
      })
      .finally(() => {
        setSavingIndex((current) => (current === index ? null : current));
      });
  };

  const handleDeleteRegistration = (
    index: number,
    registrationIndex: number
  ) => {
    const target = annualRegisterDrafts[index];
    const targetKey = getAnnualKey(target, index);
    const registerEntry = registrationDrafts[targetKey]?.[registrationIndex];
    setSaveError(null);

    if (!registerEntry?.id) {
      setRegistrationDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (_item, itemIndex) => itemIndex !== registrationIndex
        )
      }));
      setSavedRegistrationDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (_item, itemIndex) => itemIndex !== registrationIndex
        )
      }));
      setEditingRegistrationIndexByAnnual((previous) => {
        const current = previous[targetKey];
        if (current === null || current === undefined) {
          return previous;
        }
        const nextIndex =
          current === registrationIndex
            ? null
            : current > registrationIndex
              ? current - 1
              : current;
        return {
          ...previous,
          [targetKey]: nextIndex
        };
      });
      return;
    }

    setSavingIndex(index);
    deleteRegisterSemester(registerEntry.id)
      .then(() => {
        setRegistrationDrafts((previous) => ({
          ...previous,
          [targetKey]: (previous[targetKey] ?? []).filter(
            (_item, itemIndex) => itemIndex !== registrationIndex
          )
        }));
        setSavedRegistrationDrafts((previous) => ({
          ...previous,
          [targetKey]: (previous[targetKey] ?? []).filter(
            (_item, itemIndex) => itemIndex !== registrationIndex
          )
        }));
        setEditingRegistrationIndexByAnnual((previous) => {
          const current = previous[targetKey];
          if (current === null || current === undefined) {
            return previous;
          }
          const nextIndex =
            current === registrationIndex
              ? null
              : current > registrationIndex
                ? current - 1
                : current;
          return {
            ...previous,
            [targetKey]: nextIndex
          };
        });
      })
      .catch((error) => {
        setSaveError(
          error instanceof Error ? error.message : "Impossible de supprimer."
        );
      })
      .finally(() => {
        setSavingIndex((current) => (current === index ? null : current));
      });
  };

  const updatePaymentField = (
    index: number,
    paymentIndex: number,
    field: "num_receipt" | "date_receipt" | "payed" | "description",
    value: string | number
  ) => {
    const target = annualRegisterDrafts[index];
    if (!target) {
      return;
    }
    const targetKey = getAnnualKey(target, index);
    setPaymentDrafts((previous) => {
      const current = previous[targetKey]?.length
        ? previous[targetKey]
        : [createEmptyPayment()];
      const next = [...current];
      const entry = next[paymentIndex] ?? createEmptyPayment();
      next[paymentIndex] = {
        ...entry,
        [field]: value
      };
      return {
        ...previous,
        [targetKey]: next
      };
    });
  };

  const updateRegistrationField = (
    index: number,
    registrationIndex: number,
    field: "semester" | "repeat_status" | "journey",
    value: string
  ) => {
    const target = annualRegisterDrafts[index];
    if (!target) {
      return;
    }
    const targetKey = getAnnualKey(target, index);
    setRegistrationDrafts((previous) => {
      const registerSemester = previous[targetKey]?.length
        ? previous[targetKey]
        : [createEmptyRegisterSemester()];
      const next = [...registerSemester];
      const currentSemester =
        next[registrationIndex] ?? createEmptyRegisterSemester();
      const selectedJourney =
        field === "journey"
          ? journeyOptions.find((journey) => journey.id === value)
          : undefined;
      const nextJourney =
        field === "journey"
          ? {
              ...(currentSemester.journey ?? emptyJourney),
              id: selectedJourney ? Number(selectedJourney.id) : 0,
              name: selectedJourney?.label ?? "",
              id_mention: selectedJourney?.mentionId
                ? Number(selectedJourney.mentionId)
                : (currentSemester.journey?.id_mention ?? 0)
            }
          : (currentSemester.journey ?? emptyJourney);
      const nextSemester =
        field === "semester"
          ? value
          : field === "journey" && selectedJourney?.semesterList.length
            ? selectedJourney.semesterList.includes(currentSemester.semester)
              ? currentSemester.semester
              : selectedJourney.semesterList[0]
            : currentSemester.semester;

      next[registrationIndex] = {
        ...currentSemester,
        semester: nextSemester,
        repeat_status:
          field === "repeat_status" ? value : currentSemester.repeat_status,
        id_journey:
          field === "journey"
            ? selectedJourney
              ? Number(selectedJourney.id)
              : undefined
            : currentSemester.id_journey,
        journey: nextJourney
      };
      return {
        ...previous,
        [targetKey]: next
      };
    });
  };

  const handleCancelPaymentEdit = (
    annualIndex: number,
    paymentIndex: number
  ) => {
    const target = annualRegisterDrafts[annualIndex];
    if (!target) {
      return;
    }
    const targetKey = getAnnualKey(target, annualIndex);
    const savedPayment = savedPaymentDrafts[targetKey]?.[paymentIndex];
    if (!savedPayment) {
      setPaymentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (_entry, entryIndex) => entryIndex !== paymentIndex
        )
      }));
    } else {
      setPaymentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).map((entry, entryIndex) =>
          entryIndex === paymentIndex ? savedPayment : entry
        )
      }));
    }
    setEditingPaymentIndexByAnnual((previous) => ({
      ...previous,
      [targetKey]: null
    }));
  };

  const handleCancelRegistrationEdit = (
    annualIndex: number,
    registrationIndex: number
  ) => {
    const target = annualRegisterDrafts[annualIndex];
    if (!target) {
      return;
    }
    const targetKey = getAnnualKey(target, annualIndex);
    const savedRegistration =
      savedRegistrationDrafts[targetKey]?.[registrationIndex];
    if (!savedRegistration) {
      setRegistrationDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (_entry, entryIndex) => entryIndex !== registrationIndex
        )
      }));
    } else {
      setRegistrationDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).map((entry, entryIndex) =>
          entryIndex === registrationIndex ? savedRegistration : entry
        )
      }));
    }
    setEditingRegistrationIndexByAnnual((previous) => ({
      ...previous,
      [targetKey]: null
    }));
  };

  const handleUploadDocument = async (
    annualIndex: number,
    file: File | null,
    id_required_document?: number
  ) => {
    if (!file) {
      return;
    }
    const target = annualRegisterDrafts[annualIndex];
    if (!target?.id) {
      setDocumentUploadError(
        "Veuillez enregistrer la fiche annuelle avant d'ajouter un document."
      );
      return;
    }
    const targetKey = getAnnualKey(target, annualIndex);
    setDocumentUploadError(null);
    setDocumentUploadingIndex(annualIndex);
    try {
      const description = documentDescriptions[targetKey] || undefined;
      const requiredDocName = id_required_document
        ? requiredDocuments.find((doc) => doc.id === id_required_document)?.name
        : null;
      const created = await uploadDocument({
        file,
        payload: {
          id_annual_register: target.id,
          name: requiredDocName || file.name,
          description,
          id_required_document
        }
      });
      const createdDoc: StudentDocumentState = {
        ...created,
        id_required_document:
          created.id_required_document ?? id_required_document,
        id_annual_register: created.id_annual_register ?? undefined
      };
      setDocumentDrafts((previous) => ({
        ...previous,
        [targetKey]: [...(previous[targetKey] ?? []), createdDoc]
      }));
      setSavedDocumentDrafts((previous) => ({
        ...previous,
        [targetKey]: [...(previous[targetKey] ?? []), createdDoc]
      }));
      setDocumentDescriptions((previous) => ({
        ...previous,
        [targetKey]: ""
      }));
    } catch (error) {
      setDocumentUploadError(
        error instanceof Error
          ? error.message
          : "Impossible d'ajouter le document."
      );
    } finally {
      setDocumentUploadingIndex((current) =>
        current === annualIndex ? null : current
      );
    }
  };

  const handleUpdateDocument = async (
    annualIndex: number,
    documentId: number,
    payload: {
      name?: string;
      description?: string;
      id_required_document?: number;
    }
  ) => {
    const target = annualRegisterDrafts[annualIndex];
    if (!target) {
      return;
    }
    const targetKey = getAnnualKey(target, annualIndex);
    setDocumentUploadError(null);
    try {
      const updated = await updateDocument(documentId, payload);
      const updatedDoc: StudentDocumentState = {
        ...updated,
        id_required_document:
          updated.id_required_document ?? payload.id_required_document,
        id_annual_register: updated.id_annual_register ?? undefined
      };
      setDocumentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).map((doc) =>
          doc.id === documentId ? updatedDoc : doc
        )
      }));
      setSavedDocumentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).map((doc) =>
          doc.id === documentId ? updatedDoc : doc
        )
      }));
    } catch (error) {
      setDocumentUploadError(
        error instanceof Error ? error.message : "Impossible de modifier."
      );
    }
  };

  const handleDeleteDocument = async (
    annualIndex: number,
    documentId: number
  ) => {
    const target = annualRegisterDrafts[annualIndex];
    if (!target) {
      return;
    }
    const targetKey = getAnnualKey(target, annualIndex);
    setDocumentUploadError(null);
    try {
      await deleteDocument(documentId);
      setDocumentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (doc) => doc.id !== documentId
        )
      }));
      setSavedDocumentDrafts((previous) => ({
        ...previous,
        [targetKey]: (previous[targetKey] ?? []).filter(
          (doc) => doc.id !== documentId
        )
      }));
    } catch (error) {
      setDocumentUploadError(
        error instanceof Error ? error.message : "Impossible de supprimer."
      );
    }
  };

  const handleSaveAnnualRegister = async (
    index: number,
    mode: "registration" | "payment",
    itemIndex: number
  ) => {
    const draft = annualRegisterDrafts[index];
    if (!draft) {
      return;
    }

    setSaveError(null);
    setSavingIndex(index);

    try {
      const annualId = draft.id;
      if (!annualId) {
        throw new Error(
          "Veuillez ajouter la fiche annuelle avant d'enregistrer."
        );
      }

      const draftKey = getAnnualKey(draft, index);
      let savedRegisterSemester: any =
        registrationDrafts[draftKey]?.[itemIndex];
      let savedPayment: any = paymentDrafts[draftKey]?.[itemIndex];

      if (mode === "registration") {
        const semesterEntry = registrationDrafts[draftKey]?.[itemIndex];
        if (!semesterEntry?.semester) {
          throw new Error("Veuillez sélectionner un semestre.");
        }
        const journeyId =
          semesterEntry.id_journey ?? semesterEntry.journey?.id ?? 0;
        if (!journeyId) {
          throw new Error("Veuillez sélectionner un parcours.");
        }
        if (!semesterEntry.repeat_status) {
          throw new Error("Veuillez sélectionner un statut de redoublement.");
        }
        const journeyName =
          semesterEntry.journey?.name ??
          semesterEntry.journey?.abbreviation ??
          journeyOptions.find(
            (journey) => Number(journey.id) === Number(journeyId)
          )?.label ??
          "";
        const academicYearName =
          draft.academic_year?.name ?? currentAcademicYearName;
        const templateVars = {
          card_number: cardNumber?.trim() ?? "",
          journey: journeyName,
          semester: semesterEntry.semester ?? "",
          full_name: (studentFullName ?? "").trim(),
          academic_year: academicYearName ?? ""
        };
        if (
          annualRegisterDrafts.some((annual, annualIndex) => {
            if (annualIndex === index) {
              return false;
            }
            if (!annual.id || !annualId) {
              return false;
            }
            const otherKey = getAnnualKey(annual, annualIndex);
            const otherSemester = registrationDrafts[otherKey]?.find(
              (_item, otherIndex) => otherIndex !== itemIndex
            );
            const otherJourneyId =
              otherSemester?.id_journey ?? otherSemester?.journey?.id ?? 0;
            return annual.id === annualId && otherJourneyId === journeyId;
          })
        ) {
          throw new Error(
            "Ce parcours est déjà enregistré pour cette fiche annuelle."
          );
        }

        if (semesterEntry.id) {
          savedRegisterSemester = await updateRegisterSemester(
            semesterEntry.id,
            {
              id_annual_register: annualId,
              semester: semesterEntry.semester,
              repeat_status: semesterEntry.repeat_status,
              id_journey: journeyId
            }
          );
        } else {
          savedRegisterSemester = await createRegisterSemester({
            id_annual_register: annualId,
            semester: semesterEntry.semester,
            repeat_status: semesterEntry.repeat_status,
            id_journey: journeyId,
            template_vars: templateVars
          });
        }
        savedRegisterSemester = {
          ...savedRegisterSemester,
          journey: semesterEntry.journey
        };
      }

      if (mode === "payment") {
        const paymentEntry = paymentDrafts[draftKey]?.[itemIndex];
        if (!paymentEntry) {
          throw new Error("Les informations de paiement sont requises.");
        }
        const payedValue = Number(paymentEntry?.payed ?? 0);
        if (
          !paymentEntry?.num_receipt ||
          !paymentEntry?.date_receipt ||
          Number.isNaN(payedValue) ||
          payedValue <= 0
        ) {
          throw new Error(
            "Numéro de reçu, date de reçu et montant payé sont requis."
          );
        }

        if (paymentEntry?.id) {
          savedPayment = await updatePayment(paymentEntry.id, {
            id_annual_register: annualId,
            num_receipt: paymentEntry.num_receipt,
            date_receipt: paymentEntry.date_receipt,
            payed: payedValue,
            description: paymentEntry.description
          });
        } else {
          savedPayment = await createPayment({
            id_annual_register: annualId,
            num_receipt: paymentEntry.num_receipt,
            date_receipt: paymentEntry.date_receipt,
            payed: payedValue,
            description: paymentEntry.description
          });
        }
      }

      const updatedAnnual = {
        ...draft,
        id: annualId,
        isEditing: false,
        isNew: false
      };

      setAnnualRegisterDrafts((previous) =>
        previous.map((annual, annualIndex) =>
          annualIndex === index ? updatedAnnual : annual
        )
      );
      setSavedAnnualRegisters((previous) => {
        const next = [...previous];
        next[index] = {
          id: updatedAnnual.id,
          payment: paymentDrafts[draftKey] ?? [],
          register_semester: registrationDrafts[draftKey] ?? []
        };
        return next;
      });
      if (savedPayment) {
        setPaymentDrafts((previous) => ({
          ...previous,
          [draftKey]: (previous[draftKey] ?? []).map((entry, entryIndex) =>
            entryIndex === itemIndex ? savedPayment : entry
          )
        }));
        setSavedPaymentDrafts((previous) => ({
          ...previous,
          [draftKey]: (previous[draftKey] ?? []).map((entry, entryIndex) =>
            entryIndex === itemIndex ? savedPayment : entry
          )
        }));
        setEditingPaymentIndexByAnnual((previous) => ({
          ...previous,
          [draftKey]: null
        }));
      }
      if (savedRegisterSemester) {
        setRegistrationDrafts((previous) => ({
          ...previous,
          [draftKey]: (previous[draftKey] ?? []).map((entry, entryIndex) =>
            entryIndex === itemIndex ? savedRegisterSemester : entry
          )
        }));
        setSavedRegistrationDrafts((previous) => ({
          ...previous,
          [draftKey]: (previous[draftKey] ?? []).map((entry, entryIndex) =>
            entryIndex === itemIndex ? savedRegisterSemester : entry
          )
        }));
        setEditingRegistrationIndexByAnnual((previous) => ({
          ...previous,
          [draftKey]: null
        }));
      }
    } catch (error) {
      setSaveError(
        error instanceof Error ? error.message : "Impossible d'enregistrer."
      );
    } finally {
      setSavingIndex((current) => (current === index ? null : current));
    }
  };

  return (
    <div className="space-y-4 p-5 overflow-y-auto">
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm font-semibold text-foreground">Scolarité</p>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="h-8 gap-2 px-3"
          onClick={() => setDialogOpen(true)}
          disabled={disabledEditing}
        >
          {editingSections.school ? (
            <>
              <Check className="h-4 w-4" />
              Terminer
            </>
          ) : (
            <>
              <Pencil className="h-4 w-4" />
              Modifier
            </>
          )}
        </Button>
      </div>

      <Tabs
        defaultValue={
          registerType === "REGISTRATION" ? "registration" : "payment"
        }
        className="space-y-3"
      >
        <TabsList
          className={
            registerType === "REGISTRATION"
              ? "grid w-full grid-cols-3 md:w-auto"
              : "grid w-full grid-cols-2 md:w-auto"
          }
        >
          {registerType === "REGISTRATION" && (
            <TabsTrigger value="registration">Registration</TabsTrigger>
          )}
          <TabsTrigger value="payment">
            <span className="relative inline-flex items-center gap-2">
              Payment
              {renderPaymentStatusBadge(paymentStatus)}
            </span>
          </TabsTrigger>
          <TabsTrigger value="document">
            <span className="relative inline-flex items-center gap-2">
              Document
              {renderDocumentStatusBadge(documentStatus)}
            </span>
          </TabsTrigger>
        </TabsList>
        {registerType === "REGISTRATION" && (
          <TabsContent
            value="registration"
            className="space-y-2 max-h-[260px] overflow-y-auto"
          >
            <RegistrationSummary
              displayAnnualRegisters={displayAnnualRegisters}
            />
          </TabsContent>
        )}
        <TabsContent
          value="payment"
          className="space-y-2 max-h-[260px] overflow-y-auto"
        >
          <PaymentSummary displayAnnualRegisters={displayAnnualRegisters} />
        </TabsContent>

        <TabsContent
          value="document"
          className="space-y-2 max-h-[260px] overflow-y-auto"
        >
          <DocumentSummary
            displayAnnualRegisters={displayAnnualRegisters}
            requiredDocuments={requiredDocuments}
          />
        </TabsContent>
      </Tabs>
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-xl lg:max-w-2xl h-[80vh] max-h-[80vh] overflow-hidden p-0 flex flex-col min-h-0">
          <form
            className="flex flex-1 flex-col min-h-0"
            onSubmit={handleFormSubmit}
          >
            <DialogHeader className="sticky top-0 z-10 border-b bg-background/95 px-6 py-4 backdrop-blur">
              <DialogTitle>Create reinscription</DialogTitle>
              {/* <DialogDescription>
                "This student already exists in the database. Review the key
                information before confirming the reinscription."
              </DialogDescription> */}
            </DialogHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center justify-start gap-2 px-6 pt-4">
                <p>{currentAcademicYearName || "Année académique"}</p>
              </div>
              <div className="flex items-center justify-end px-6 pt-4">
                {!annualRegisterDrafts.length ? (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="h-8 gap-2 px-3"
                    onClick={handleAddAnnualRegister}
                  >
                    <Plus className="h-4 w-4" />
                    Ajouter
                  </Button>
                ) : (
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="h-8 gap-2 px-3 text-destructive hover:text-destructive"
                    onClick={() =>
                      setConfirmDeleteTarget({ type: "annual", index: 0 })
                    }
                    disabled={!annualRegisterDrafts.length || savingIndex === 0}
                  >
                    <Trash2 className="h-4 w-4" />
                    Supprimer
                  </Button>
                )}
              </div>
            </div>
            {saveError ? (
              <p className="px-6 text-sm text-destructive">{saveError}</p>
            ) : null}
            {annualRegisterLoading ? (
              <p className="px-6 text-sm text-muted-foreground">
                Chargement des inscriptions...
              </p>
            ) : null}
            <div className="flex-1 px-6 pb-6 pt-4 space-y-4">
              <Tabs
                defaultValue={
                  registerType === "REGISTRATION" ? "registration" : "payment"
                }
                className="space-y-3"
              >
                <TabsList
                  className={
                    registerType === "REGISTRATION"
                      ? "grid w-full grid-cols-3 md:w-auto"
                      : "grid w-full grid-cols-2 md:w-auto"
                  }
                >
                  {registerType === "REGISTRATION" && (
                    <TabsTrigger value="registration">Registration</TabsTrigger>
                  )}

                  <TabsTrigger value="payment">
                    <span className="relative inline-flex items-center gap-2">
                      Payment
                      {renderPaymentStatusBadge(paymentStatus)}
                    </span>
                  </TabsTrigger>

                  <TabsTrigger value="document">
                    <span className="relative inline-flex items-center gap-2">
                      Document
                      {renderDocumentStatusBadge(documentStatus)}
                    </span>
                  </TabsTrigger>
                </TabsList>
                {registerType === "REGISTRATION" && (
                  <TabsContent
                    value="registration"
                    className="space-y-4 max-h-[520px] overflow-y-auto"
                  >
                    <RegistrationEditor
                      annualRegisterDrafts={annualRegisterDrafts}
                      hasRegistrationEntries={hasRegistrationEntries}
                      mergeAnnualWithDrafts={mergeAnnualWithDrafts}
                      filters={filters}
                      journeyOptions={journeyOptions}
                      onAddRegistration={handleAddRegistration}
                      onSave={handleSaveAnnualRegister}
                      onUpdateRegistrationField={updateRegistrationField}
                      onCancel={handleCancelRegistrationEdit}
                      onToggleEdit={(annualIndex, registrationIndex) => {
                        const annualKey = getAnnualKey(
                          annualRegisterDrafts[annualIndex],
                          annualIndex
                        );
                        setEditingRegistrationIndexByAnnual((previous) => ({
                          ...previous,
                          [annualKey]: registrationIndex
                        }));
                      }}
                      onDelete={(annualIndex, targetIndex) =>
                        setConfirmDeleteTarget({
                          type: "registration",
                          index: annualIndex,
                          itemIndex: targetIndex
                        })
                      }
                      editingRegistrationIndexByAnnual={
                        editingRegistrationIndexByAnnual
                      }
                      getAnnualKey={getAnnualKey}
                      savingIndex={savingIndex}
                    />
                  </TabsContent>
                )}
                <TabsContent
                  value="payment"
                  className="space-y-4 max-h-[520px] overflow-y-auto"
                >
                  <PaymentEditor
                    annualRegisterDrafts={annualRegisterDrafts}
                    hasPaymentEntries={hasPaymentEntries}
                    mergeAnnualWithDrafts={mergeAnnualWithDrafts}
                    filters={filters}
                    journeyOptions={journeyOptions}
                    onAddPayment={handleAddPayment}
                    onSave={handleSaveAnnualRegister}
                    onUpdatePaymentField={updatePaymentField}
                    onCancel={handleCancelPaymentEdit}
                    onToggleEdit={(annualIndex, paymentIndex) => {
                      const annualKey = getAnnualKey(
                        annualRegisterDrafts[annualIndex],
                        annualIndex
                      );
                      setEditingPaymentIndexByAnnual((previous) => ({
                        ...previous,
                        [annualKey]: paymentIndex
                      }));
                    }}
                    onDelete={(annualIndex, targetIndex) =>
                      setConfirmDeleteTarget({
                        type: "payment",
                        index: annualIndex,
                        itemIndex: targetIndex
                      })
                    }
                    editingPaymentIndexByAnnual={editingPaymentIndexByAnnual}
                    getAnnualKey={getAnnualKey}
                    savingIndex={savingIndex}
                  />
                </TabsContent>
                <TabsContent
                  value="document"
                  className="space-y-4 max-h-[520px] overflow-y-auto"
                >
                  <DocumentEditor
                    requiredDocuments={requiredDocuments}
                    annualRegisterDrafts={annualRegisterDrafts}
                    documentDrafts={documentDrafts}
                    documentDescriptions={documentDescriptions}
                    documentUploadError={documentUploadError}
                    documentUploadingIndex={documentUploadingIndex}
                    getAnnualKey={getAnnualKey}
                    handleUploadDocument={handleUploadDocument}
                    onDeleteDocument={handleDeleteDocument}
                    onUpdateDocument={handleUpdateDocument}
                    setDocumentDescriptions={setDocumentDescriptions}
                  />
                </TabsContent>
              </Tabs>
            </div>

            <DialogFooter className="sticky bottom-0 z-10 mt-auto border-t bg-background/95 px-6 py-4 backdrop-blur">
              {/* <Button type="submit" disabled={formSubmitting}>
                {"Fermer"}
              </Button> */}
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
      <ConfirmDialog
        open={confirmDeleteTarget !== null}
        title={
          confirmDeleteTarget?.type === "annual"
            ? "Supprimer la scolarité ?"
            : confirmDeleteTarget?.type === "payment"
              ? "Supprimer le paiement ?"
              : "Supprimer l'inscription ?"
        }
        description={
          confirmDeleteTarget?.type === "annual"
            ? "Cette action supprimera aussi les paiements et les semestres liés."
            : confirmDeleteTarget?.type === "payment"
              ? "Cette action supprimera uniquement le paiement."
              : "Cette action supprimera uniquement l'inscription."
        }
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        destructive
        isConfirming={
          confirmDeleteTarget !== null &&
          savingIndex === confirmDeleteTarget.index
        }
        onCancel={() => setConfirmDeleteTarget(null)}
        onConfirm={() => {
          if (!confirmDeleteTarget) {
            return;
          }
          if (confirmDeleteTarget.type === "annual") {
            handleDeleteAnnualRegister(confirmDeleteTarget.index);
          } else if (confirmDeleteTarget.type === "payment") {
            handleDeletePayment(
              confirmDeleteTarget.index,
              confirmDeleteTarget.itemIndex ?? 0
            );
          } else {
            handleDeleteRegistration(
              confirmDeleteTarget.index,
              confirmDeleteTarget.itemIndex ?? 0
            );
          }
          setConfirmDeleteTarget(null);
        }}
      />
    </div>
  );
};
