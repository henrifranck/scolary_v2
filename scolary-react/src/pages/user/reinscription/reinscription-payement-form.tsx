import { Button } from "@/components/ui/button";
import { Check, Pencil, Plus } from "lucide-react";
import { useEffect, useState } from "react";
import { EditableSection, ReinscriptionAnnualProps } from "./reinscription-form-type";
import { InfoItem } from "./reinscription-form-info-item";
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
import { RegistrationPaymentForm } from "../registration/registration-payment-form";
import { fetchJourneys } from "@/services/inscription-service";
import {
  createAnnualRegister,
  createPayement,
  createRegisterSemester,
  deleteAnnualRegister,
  fetchAnnualRegisterByCardNumber,
  updatePayement,
  updateRegisterSemester
} from "@/services/annual-register-service";

interface ReinscriptionAnnualFormProps {
  annualRegister: Array<ReinscriptionAnnualProps>;
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
    Array<ReinscriptionAnnualProps & { isEditing?: boolean; isNew?: boolean }>
  >([]);
  const [journeyOptions, setJourneyOptions] = useState<
    Array<{ id: string; label: string; semesterList: string[]; mentionId?: string }>
  >([]);
  const [savedAnnualRegisters, setSavedAnnualRegisters] = useState<
    Array<ReinscriptionAnnualProps>
  >([]);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [savingIndex, setSavingIndex] = useState<number | null>(null);
  const [annualRegisterLoading, setAnnualRegisterLoading] = useState(false);

  const emptyJourney = {
    id: 0,
    name: "",
    abbreviation: "",
    id_mention: 0
  };

  const createEmptyAnnualRegister = () => ({
    payment: [
      {
        id: undefined,
        num_receipt: "",
        date_receipt: "",
        payed: 0
      }
    ],
    register_semester: [
      {
        id: undefined,
        id_journey: undefined,
        semester: "",
        repeat_status: "",
        journey: { ...emptyJourney }
      }
    ],
    isEditing: true,
    isNew: true
  });

  const mentionId = filters?.id_mention ?? filters?.mentionId ?? "";

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
                  typeof semester === "string" ? semester : semester?.semester ?? ""
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
      payment:
        annual.payment && annual.payment.length
          ? annual.payment
          : createEmptyAnnualRegister().payment,
      register_semester:
        annual.register_semester && annual.register_semester.length
          ? annual.register_semester
          : createEmptyAnnualRegister().register_semester,
      isEditing: false,
      isNew: false
    }));
    setAnnualRegisterDrafts(normalized);
    setSavedAnnualRegisters(
      normalized.map(({ isEditing, isNew, ...rest }) => rest)
    );
  }, [annualRegister]);

  useEffect(() => {
    if (!dialogOpen) {
      return;
    }
    const trimmed = cardNumber?.trim() ?? "";
    if (!trimmed) {
      return;
    }
    let isMounted = true;
    setAnnualRegisterLoading(true);
    fetchAnnualRegisterByCardNumber(trimmed)
      .then((response) => {
        if (!isMounted) {
          return;
        }
        const normalized = (response.data ?? []).map((annual) => ({
          ...annual,
          payment:
            annual.payment && annual.payment.length
              ? annual.payment
              : createEmptyAnnualRegister().payment,
          register_semester:
            annual.register_semester && annual.register_semester.length
              ? annual.register_semester
              : createEmptyAnnualRegister().register_semester,
          isEditing: false,
          isNew: false
        }));
        setAnnualRegisterDrafts(normalized);
        setSavedAnnualRegisters(
          normalized.map(({ isEditing, isNew, ...rest }) => rest)
        );
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

  const handleAddAnnualRegister = () => {
    setSaveError(null);
    setAnnualRegisterDrafts((previous) => [
      ...previous,
      createEmptyAnnualRegister()
    ]);
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

    setSavingIndex(index);
    deleteAnnualRegister(target.id)
      .then(() => {
        setAnnualRegisterDrafts((previous) =>
          previous.filter((_annual, annualIndex) => annualIndex !== index)
        );
        setSavedAnnualRegisters((previous) =>
          previous.filter((_annual, annualIndex) => annualIndex !== index)
        );
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

  const toggleItemEditing = (index: number) => {
    setAnnualRegisterDrafts((previous) =>
      previous.map((annual, annualIndex) =>
        annualIndex === index
          ? { ...annual, isEditing: !annual.isEditing }
          : annual
      )
    );
  };

  const updatePaymentField = (
    index: number,
    field: "num_receipt" | "date_receipt" | "payed",
    value: string | number
  ) => {
    setAnnualRegisterDrafts((previous) =>
      previous.map((annual, annualIndex) => {
        if (annualIndex !== index) {
          return annual;
        }

        const payment = annual.payment?.length
          ? annual.payment
          : createEmptyAnnualRegister().payment;

        return {
          ...annual,
          payment: [
            {
              ...payment[0],
              [field]: value
            }
          ]
        };
      })
    );
  };

  const updateRegistrationField = (
    index: number,
    field: "semester" | "repeat_status" | "journey",
    value: string
  ) => {
    setAnnualRegisterDrafts((previous) =>
      previous.map((annual, annualIndex) => {
        if (annualIndex !== index) {
          return annual;
        }

        const registerSemester = annual.register_semester?.length
          ? annual.register_semester
          : createEmptyAnnualRegister().register_semester;

        const currentSemester = registerSemester[0];
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
                  : currentSemester.journey?.id_mention ?? 0
              }
            : currentSemester.journey ?? emptyJourney;
        const nextSemester =
          field === "semester"
            ? value
            : field === "journey" && selectedJourney?.semesterList.length
              ? selectedJourney.semesterList.includes(currentSemester.semester)
                ? currentSemester.semester
                : selectedJourney.semesterList[0]
              : currentSemester.semester;

        return {
          ...annual,
          register_semester: [
            {
              ...currentSemester,
              semester: nextSemester,
              repeat_status:
                field === "repeat_status"
                  ? value
                  : currentSemester.repeat_status,
              id_journey:
                field === "journey"
                  ? selectedJourney
                    ? Number(selectedJourney.id)
                    : undefined
                  : currentSemester.id_journey,
              journey: nextJourney
            }
          ]
        };
      })
    );
  };

  const handleCancelEdit = (index: number) => {
    setSaveError(null);
    setAnnualRegisterDrafts((previous) => {
      const target = previous[index];
      if (!target) {
        return previous;
      }
      if (target.isNew) {
        return previous.filter((_annual, annualIndex) => annualIndex !== index);
      }
      const saved = savedAnnualRegisters[index];
      if (!saved) {
        return previous.map((annual, annualIndex) =>
          annualIndex === index ? { ...annual, isEditing: false } : annual
        );
      }
      return previous.map((annual, annualIndex) =>
        annualIndex === index
          ? {
              ...saved,
              payment: saved.payment?.length
                ? saved.payment
                : createEmptyAnnualRegister().payment,
              register_semester: saved.register_semester?.length
                ? saved.register_semester
                : createEmptyAnnualRegister().register_semester,
              isEditing: false,
              isNew: false
            }
          : annual
      );
    });
  };

  const handleSaveAnnualRegister = async (index: number) => {
    const draft = annualRegisterDrafts[index];
    if (!draft) {
      return;
    }

    setSaveError(null);
    setSavingIndex(index);

    try {
      let annualId = draft.id;
      const cardValue = cardNumber?.trim() ?? "";
      const academicYearId = Number(filters?.id_year ?? filters?.academicYearId);
      if (!annualId) {
        if (!cardValue) {
          throw new Error("Le numéro de carte est requis pour enregistrer.");
        }
        if (!academicYearId) {
          throw new Error("L'année académique est requise pour enregistrer.");
        }
        const created = await createAnnualRegister({
          num_carte: cardValue,
          id_academic_year: academicYearId,
          semester_count: 1
        });
        annualId = created.id;
        if (!annualId) {
          throw new Error("Impossible de créer la fiche annuelle.");
        }
      }

      const semesterEntry = draft.register_semester?.[0];
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
          const otherSemester = annual.register_semester?.[0];
          const otherJourneyId =
            otherSemester?.id_journey ?? otherSemester?.journey?.id ?? 0;
          return annual.id === annualId && otherJourneyId === journeyId;
        })
      ) {
        throw new Error(
          "Ce parcours est déjà enregistré pour cette fiche annuelle."
        );
      }

      let savedRegisterSemester: any = semesterEntry;
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

      const paymentEntry = draft.payment?.[0];
      let savedPayment: any = paymentEntry;
      const hasPaymentData =
        Boolean(paymentEntry?.num_receipt) ||
        Boolean(paymentEntry?.date_receipt) ||
        Boolean(paymentEntry?.payed);
      if (hasPaymentData) {
        if (!paymentEntry?.num_receipt || !paymentEntry?.date_receipt) {
          throw new Error("Veuillez renseigner le reçu et sa date.");
        }
        const payedValue = Number(paymentEntry?.payed ?? 0);
        if (paymentEntry?.id) {
          savedPayment = await updatePayement(paymentEntry.id, {
            id_annual_register: annualId,
            num_receipt: paymentEntry.num_receipt,
            date_receipt: paymentEntry.date_receipt,
            payed: payedValue
          });
        } else {
          savedPayment = await createPayement({
            id_annual_register: annualId,
            num_receipt: paymentEntry.num_receipt,
            date_receipt: paymentEntry.date_receipt,
            payed: payedValue
          });
        }
      }

      const updatedAnnual = {
        ...draft,
        id: annualId,
        payment: savedPayment ? [savedPayment] : draft.payment,
        register_semester: savedRegisterSemester
          ? [savedRegisterSemester]
          : draft.register_semester,
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
          payment: updatedAnnual.payment,
          register_semester: updatedAnnual.register_semester
        };
        return next;
      });
    } catch (error) {
      setSaveError(
        error instanceof Error
          ? error.message
          : "Impossible d'enregistrer."
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
          {annualRegister?.map((annual, index) => (
            <div key={index} className="grid gap-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <InfoItem
                  label="Numéro de reçu"
                  value={annual?.payment[0]?.num_receipt || "N/A"}
                />
                <InfoItem
                  label="Date de reçu"
                  value={annual?.payment[0]?.date_receipt || "N/A"}
                />
              </div>
              <InfoItem
                label="Montant payé"
                value={
                  annual?.payment[0]?.payed
                    ? `${annual.payment[0].payed} Ar`
                    : "N/A"
                }
              />
            </div>
          ))}
        </TabsContent>
        <TabsContent value="registration" className="space-y-2">
          {annualRegister?.map((annual, index) => (
            <div key={index} className="grid gap-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <InfoItem
                  label="Semestre"
                  value={annual?.register_semester[0]?.semester || "N/A"}
                />
                <InfoItem
                  label="Statut de redoublement"
                  value={
                    formatRepeatStatus(
                      annual?.register_semester[0]?.repeat_status
                    ) || "N/A"
                  }
                />
              </div>
              <InfoItem
                label="Parcours"
                value={annual?.register_semester[0]?.journey.name || "N/A"}
              />
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
            <div className="flex items-center justify-end px-6 pt-4">
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
              {annualRegisterDrafts.map((annual, index) => (
                <RegistrationPaymentForm
                  key={`${annual.isNew ? "new" : "annual"}-${index}`}
                  annual={annual}
                  index={index}
                  filters={filters}
                  journeyOptions={journeyOptions}
                  onToggleEdit={toggleItemEditing}
                  onDelete={handleDeleteAnnualRegister}
                  onCancel={handleCancelEdit}
                  onSave={handleSaveAnnualRegister}
                  onUpdatePaymentField={updatePaymentField}
                  onUpdateRegistrationField={updateRegistrationField}
                  isSaving={savingIndex === index}
                />
              ))}
            </div>

            <DialogFooter className="sticky bottom-0 z-10 mt-auto border-t bg-background/95 px-6 py-4 backdrop-blur">
              <Button type="submit" disabled={formSubmitting}>
                {"Fermer"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};
