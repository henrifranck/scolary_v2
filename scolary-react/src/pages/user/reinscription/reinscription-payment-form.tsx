import { Button } from "@/components/ui/button";
import { Check, Pencil, Plus, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import {
  EditableSection,
  StudentAnnualProps,
  StudentPaymentState,
  StudentSemesterState
} from "@/components/student-form/student-form-types";
import { StudentFormInfoItem } from "@/components/student-form/student-form-info-item";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import formatRepeatStatus from "@/lib/enum/repeat-status-enum";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { RegistrationForm } from "../registration/registration-form";
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
import { PaymentForm } from "../payment/payment-form";

interface ReinscriptionAnnualFormProps {
  annualRegister: Array<StudentAnnualProps>;
  editingSections: Record<EditableSection, boolean>;
  cardNumber?: string;
  filters?: any;
}

export const handleFormSubmit = (e: React.FormEvent) => {};

export const ReinscriptionAnnualRegister = ({
  annualRegister,
  editingSections,
  cardNumber,
  filters
}: ReinscriptionAnnualFormProps) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [annualRegisterDrafts, setAnnualRegisterDrafts] = useState<
    Array<StudentAnnualProps & { isEditing?: boolean; isNew?: boolean }>
  >([]);
  const [paymentDrafts, setPaymentDrafts] = useState<
    Record<string, StudentPaymentState[]>
  >({});
  const [registrationDrafts, setRegistrationDrafts] = useState<
    Record<string, StudentSemesterState[]>
  >({});
  const [editingPaymentIndexByAnnual, setEditingPaymentIndexByAnnual] =
    useState<Record<string, number | null>>({});
  const [editingRegistrationIndexByAnnual, setEditingRegistrationIndexByAnnual] =
    useState<Record<string, number | null>>({});
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
  const [saveError, setSaveError] = useState<string | null>(null);
  const [savingIndex, setSavingIndex] = useState<number | null>(null);
  const [annualRegisterLoading, setAnnualRegisterLoading] = useState(false);
  const [confirmDeleteTarget, setConfirmDeleteTarget] = useState<{
    type: "annual" | "payment" | "registration";
    index: number;
    itemIndex?: number;
  } | null>(null);

  const emptyJourney = {
    id: 0,
    name: "",
    abbreviation: "",
    id_mention: 0
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

  const mentionId = filters?.id_mention ?? filters?.mentionId ?? "";
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
      register_semester: registrationDrafts[key] ?? []
    };
  };

  const displayAnnualRegisters = annualRegisterDrafts.length
    ? annualRegisterDrafts.map(mergeAnnualWithDrafts)
    : annualRegister;
  const hasRegistrationEntries = annualRegisterDrafts.some(
    (annual, index) => (registrationDrafts[getAnnualKey(annual, index)] ?? []).length
  );
  const hasPaymentEntries = annualRegisterDrafts.some(
    (annual, index) => (paymentDrafts[getAnnualKey(annual, index)] ?? []).length
  );

  useEffect(() => {
    let isMounted = true;

    const loadJourneys = async () => {
      if (!mentionId) {
        if (isMounted) {
          setJourneyOptions([]);
        }
        return;
      }

      try {
        const journeys = await fetchJourneys(mentionId);
        const normalized = journeys.map((journey) => {
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
            label:
              journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
            semesterList,
            mentionId: journey.id_mention
              ? String(journey.id_mention)
              : undefined
          };
        });

        if (isMounted) {
          setJourneyOptions(normalized);
        }
      } catch (error) {
        if (isMounted) {
          setJourneyOptions([]);
        }
      }
    };

    loadJourneys();

    return () => {
      isMounted = false;
    };
  }, [mentionId]);
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
    const initialRegistrationDrafts: Record<string, StudentSemesterState[]> = {};
    normalized.forEach((annual, index) => {
      const key = getAnnualKey(annual, index);
      initialPaymentDrafts[key] =
        annual.payment && annual.payment.length ? annual.payment : [];
      initialRegistrationDrafts[key] =
        annual.register_semester && annual.register_semester.length
          ? annual.register_semester
          : [];
    });
    setPaymentDrafts(initialPaymentDrafts);
    setRegistrationDrafts(initialRegistrationDrafts);
    setSavedPaymentDrafts(initialPaymentDrafts);
    setSavedRegistrationDrafts(initialRegistrationDrafts);
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
  }, [annualRegister]);

  useEffect(() => {
    if (!dialogOpen) {
      return;
    }
    const trimmed = cardNumber?.trim() ?? "";
    if (!trimmed) {
      return;
    }
    const academicYearId =
      filters?.academicYearId ??
      filters?.id_year ??
      filters?.id_enter_year ??
      filters?.id_academic_year;
    let isMounted = true;
    setAnnualRegisterLoading(true);
    fetchAnnualRegisterByCardNumber(trimmed, academicYearId ?? undefined)
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
        normalized.forEach((annual, index) => {
          const key = getAnnualKey(annual, index);
          initialPaymentDrafts[key] =
            annual.payment && annual.payment.length ? annual.payment : [];
          initialRegistrationDrafts[key] =
            annual.register_semester && annual.register_semester.length
              ? annual.register_semester
              : [];
        });
        setPaymentDrafts(initialPaymentDrafts);
        setRegistrationDrafts(initialRegistrationDrafts);
        setSavedPaymentDrafts(initialPaymentDrafts);
        setSavedRegistrationDrafts(initialRegistrationDrafts);
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
    const cardValue = cardNumber?.trim() ?? "";
    const academicYearId = Number(
      filters?.id_year ?? filters?.academicYearId
    );

    if (!cardValue) {
      setSaveError("Le numéro de carte est requis pour enregistrer.");
      return;
    }
    if (!academicYearId) {
      setSaveError("L'année académique est requise pour enregistrer.");
      return;
    }

    try {
      const created = await createAnnualRegister({
        num_carte: cardValue,
        id_academic_year: academicYearId,
        semester_count: 1
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
      setPaymentDrafts((previous) => ({
        ...previous,
        [newKey]: []
      }));
      setRegistrationDrafts((previous) => ({
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
      return !(paymentDrafts[key]?.length);
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
      [targetKey]: (paymentDrafts[targetKey]?.length ?? 0)
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
      return !(registrationDrafts[key]?.length);
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
      [targetKey]: (registrationDrafts[targetKey]?.length ?? 0)
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
    const savedRegistration = savedRegistrationDrafts[targetKey]?.[
      registrationIndex
    ];
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
      let savedRegisterSemester:any = registrationDrafts[draftKey]?.[itemIndex];
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
            id_journey: journeyId
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
    <div className="space-y-4 rounded-xl border bg-muted/20 p-5 max-h-[320px] overflow-y-auto">
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm font-semibold text-foreground">Scolarité</p>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="h-8 gap-2 px-3"
          onClick={() => setDialogOpen(true)}
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
      <Tabs defaultValue="registration" className="space-y-3">
        <TabsList className="grid w-full grid-cols-2 md:w-auto">
          <TabsTrigger value="registration">Registration</TabsTrigger>
          <TabsTrigger value="payment">Payment</TabsTrigger>
        </TabsList>

        <TabsContent value="payment" className="space-y-2">
          {displayAnnualRegisters?.map((annual, index) => (
            <div key={index} className="grid gap-4">
              {annual?.payment?.length ? (
                annual.payment.map((payment, paymentIndex) => (
                  <div
                    key={`${index}-payment-${paymentIndex}`}
                    className="grid gap-4 rounded-lg border border-dashed bg-background/60 p-3"
                  >
                    <div className="grid gap-4 sm:grid-cols-2">
                      <StudentFormInfoItem
                        label="Numéro de reçu"
                        value={payment?.num_receipt || "N/A"}
                      />
                      <StudentFormInfoItem
                        label="Date de reçu"
                        value={payment?.date_receipt || "N/A"}
                      />
                    </div>
                    <StudentFormInfoItem
                      label="Montant payé"
                      value={payment?.payed ? `${payment.payed} Ar` : "N/A"}
                    />
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  Aucun paiement enregistré.
                </p>
              )}
            </div>
          ))}
        </TabsContent>
        <TabsContent value="registration" className="space-y-2">
          {displayAnnualRegisters?.map((annual, index) => (
            <div key={index} className="grid gap-4">
              {annual?.register_semester?.length ? (
                annual.register_semester.map((semester, semesterIndex) => (
                  <div
                    key={`${index}-semester-${semesterIndex}`}
                    className="grid gap-4 rounded-lg border border-dashed bg-background/60 p-3"
                  >
                    <div className="grid gap-4 sm:grid-cols-2">
                      <StudentFormInfoItem
                        label="Semestre"
                        value={semester?.semester || "N/A"}
                      />
                      <StudentFormInfoItem
                        label="Statut de redoublement"
                        value={
                          formatRepeatStatus(semester?.repeat_status) || "N/A"
                        }
                      />
                    </div>
                    <StudentFormInfoItem
                      label="Parcours"
                      value={semester?.journey?.name || "N/A"}
                    />
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  Aucune inscription enregistrée.
                </p>
              )}
            </div>
          ))}
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
                ) : <Button
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
                </Button>}
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
            <div className="flex-1 overflow-y-auto px-6 pb-6 pt-4 space-y-4">
              <Tabs defaultValue="registration" className="space-y-3">
                <TabsList className="grid w-full grid-cols-2 md:w-auto">
                  <TabsTrigger value="registration">Registration</TabsTrigger>
                  <TabsTrigger value="payment">Payment</TabsTrigger>
                </TabsList>
                <TabsContent value="registration" className="space-y-4">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium">Inscriptions</p>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="h-8 gap-2 px-3"
                      onClick={handleAddRegistration}
                      disabled={!annualRegisterDrafts.length}
                    >
                      <Plus className="h-4 w-4" />
                      Ajouter
                    </Button>
                  </div>
                  {annualRegisterDrafts.length && hasRegistrationEntries ? (
                    annualRegisterDrafts.flatMap((annual, index) => {
                      const mergedAnnual = mergeAnnualWithDrafts(annual, index);
                      return (mergedAnnual.register_semester ?? []).map(
                        (_entry, registrationIndex) => (
                          <RegistrationForm
                            key={`${annual.id ?? "new"}-${index}-${registrationIndex}`}
                            annual={mergedAnnual}
                            index={index}
                            registrationIndex={registrationIndex}
                            filters={filters}
                            journeyOptions={journeyOptions}
                        onToggleEdit={(annualIndex, registrationIndex) => {
                          const annualKey = getAnnualKey(annual, annualIndex);
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
                        onCancel={handleCancelRegistrationEdit}
                        onSave={handleSaveAnnualRegister}
                            onUpdateRegistrationField={updateRegistrationField}
                        isSaving={savingIndex === index}
                        isEditing={
                          editingRegistrationIndexByAnnual[
                            getAnnualKey(annual, index)
                          ] === registrationIndex
                        }
                      />
                        )
                      );
                    })
                  ) : (
                    <p className="text-sm text-muted-foreground">
                      Aucune inscription à afficher.
                    </p>
                  )}
                </TabsContent>
                <TabsContent value="payment" className="space-y-4">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium">Paiements</p>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="h-8 gap-2 px-3"
                      onClick={handleAddPayment}
                      disabled={!annualRegisterDrafts.length}
                    >
                      <Plus className="h-4 w-4" />
                      Ajouter
                    </Button>
                  </div>
                  {annualRegisterDrafts.length && hasPaymentEntries ? (
                    annualRegisterDrafts.flatMap((annual, index) => {
                      const mergedAnnual = mergeAnnualWithDrafts(annual, index);
                      return (mergedAnnual.payment ?? []).map(
                        (_entry, paymentIndex) => (
                          <PaymentForm
                            key={`${annual.id ?? "new"}-${index}-${paymentIndex}`}
                            annual={mergedAnnual}
                            index={index}
                            paymentIndex={paymentIndex}
                            filters={filters}
                            journeyOptions={journeyOptions}
                        onToggleEdit={(annualIndex, paymentIndex) => {
                          const annualKey = getAnnualKey(annual, annualIndex);
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
                        onCancel={handleCancelPaymentEdit}
                        onSave={handleSaveAnnualRegister}
                        onUpdatePaymentField={updatePaymentField}
                        isSaving={savingIndex === index}
                        isEditing={
                          editingPaymentIndexByAnnual[
                            getAnnualKey(annual, index)
                          ] === paymentIndex
                        }
                      />
                        )
                      );
                    })
                  ) : (
                    <p className="text-sm text-muted-foreground">
                      Aucun paiement à afficher.
                    </p>
                  )}
                </TabsContent>
              </Tabs>
            </div>

            <DialogFooter className="sticky bottom-0 z-10 mt-auto border-t bg-background/95 px-6 py-4 backdrop-blur">
              <Button type="submit" disabled={formSubmitting}>
                {"Fermer"}
              </Button>
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
