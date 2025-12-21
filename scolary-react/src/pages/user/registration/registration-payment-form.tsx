import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import formatRepeatStatus, {
  RepeatStatusEnum
} from "@/lib/enum/repeat-status-enum";
import { Check, Pencil, Trash2 } from "lucide-react";
import { StudentFormInfoItem } from "@/components/student-form/student-form-info-item";
import { StudentAnnualProps } from "@/components/student-form/student-form-types";

interface RegistrationPaymentFormProps {
  annual: StudentAnnualProps & { isEditing?: boolean; isNew?: boolean };
  index: number;
  filters?: any;
  journeyOptions: Array<{
    id: string;
    label: string;
    semesterList: string[];
  }>;
  onToggleEdit: (index: number) => void;
  onCancel: (index: number) => void;
  onSave: (index: number) => void;
  onDelete: (index: number) => void;
  onUpdatePaymentField: (
    index: number,
    field: "num_receipt" | "date_receipt" | "payed",
    value: string | number
  ) => void;
  onUpdateRegistrationField: (
    index: number,
    field: "semester" | "repeat_status" | "journey",
    value: string
  ) => void;
  isSaving?: boolean;
}

export const RegistrationPaymentForm = ({
  annual,
  index,
  filters,
  journeyOptions,
  onToggleEdit,
  onCancel,
  onSave,
  onDelete,
  onUpdatePaymentField,
  onUpdateRegistrationField,
  isSaving
}: RegistrationPaymentFormProps) => {
  const repeatStatusOptions = Object.values(RepeatStatusEnum);
  const selectedJourneyId = annual?.register_semester?.[0]?.id_journey
    ? String(annual.register_semester[0].id_journey)
    : annual?.register_semester?.[0]?.journey?.id
      ? String(annual.register_semester[0].journey.id)
      : "";
  const selectedJourney = journeyOptions.find(
    (journey) => journey.id === selectedJourneyId
  );
  const semesterOptions = selectedJourney?.semesterList ?? [];
  const selectedSemesterValue = annual?.register_semester?.[0]?.semester || "";
  const semesterValue = semesterOptions.includes(selectedSemesterValue)
    ? selectedSemesterValue
    : "";

  return (
    <div className="space-y-4 rounded-xl border bg-muted/20 p-5 max-h-[320px] overflow-y-auto">
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm font-semibold text-foreground">
          {filters?.id_year}
        </p>
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-8 gap-2 px-3 text-destructive hover:text-destructive"
            onClick={() => onDelete(index)}
            disabled={isSaving}
          >
            <Trash2 className="h-4 w-4" />
            Supprimer
          </Button>
          {annual.isEditing ? (
            <>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 gap-2 px-3"
                onClick={() => onCancel(index)}
                disabled={isSaving}
              >
                Annuler
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 gap-2 px-3"
                onClick={() => onSave(index)}
                disabled={isSaving}
              >
                <Check className="h-4 w-4" />
                Terminer
              </Button>
            </>
          ) : (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="h-8 gap-2 px-3"
              onClick={() => onToggleEdit(index)}
              disabled={isSaving}
            >
              <Pencil className="h-4 w-4" />
              Modifier
            </Button>
          )}
        </div>
      </div>
      <Tabs defaultValue="registration" className="space-y-3">
        <TabsList className="grid w-full grid-cols-2 md:w-auto">
          <TabsTrigger value="registration">Registration</TabsTrigger>
          <TabsTrigger value="payment">Payment</TabsTrigger>
        </TabsList>

        <TabsContent value="payment" className="space-y-2">
          <div className="grid gap-4">
            {annual.isEditing ? (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Numéro de reçu
                    </label>
                    <Input
                      value={annual?.payment[0]?.num_receipt || ""}
                      onChange={(event) =>
                        onUpdatePaymentField(
                          index,
                          "num_receipt",
                          event.target.value
                        )
                      }
                      placeholder="Saisir le numéro de reçu"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Date de reçu
                    </label>
                    <Input
                      type="date"
                      value={annual?.payment[0]?.date_receipt || ""}
                      onChange={(event) =>
                        onUpdatePaymentField(
                          index,
                          "date_receipt",
                          event.target.value
                        )
                      }
                    />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                    Montant payé
                  </label>
                  <Input
                    type="number"
                    value={annual?.payment[0]?.payed ?? 0}
                    onChange={(event) =>
                      onUpdatePaymentField(
                        index,
                        "payed",
                        Number(event.target.value)
                      )
                    }
                    placeholder="Saisir le montant"
                  />
                </div>
              </>
            ) : (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <StudentFormInfoItem
                    label="Numéro de reçu"
                    value={annual?.payment[0]?.num_receipt || "N/A"}
                  />
                  <StudentFormInfoItem
                    label="Date de reçu"
                    value={annual?.payment[0]?.date_receipt || "N/A"}
                  />
                </div>
                <StudentFormInfoItem
                  label="Montant payé"
                  value={
                    annual?.payment[0]?.payed
                      ? `${annual.payment[0].payed} Ar`
                      : "N/A"
                  }
                />
              </>
            )}
          </div>
        </TabsContent>
        <TabsContent value="registration" className="space-y-2">
          <div className="grid gap-4">
            {annual.isEditing ? (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Semestre
                    </label>
                    <Select
                      value={semesterValue}
                      onValueChange={(value) =>
                        onUpdateRegistrationField(index, "semester", value)
                      }
                    >
                      <SelectTrigger>
                        <SelectValue
                          placeholder={
                            semesterOptions.length
                              ? "Sélectionner le semestre"
                              : "Sélectionner un parcours"
                          }
                        />
                      </SelectTrigger>
                      <SelectContent>
                        {semesterOptions.length ? (
                          semesterOptions.map((semester) => (
                            <SelectItem key={semester} value={semester}>
                              {semester}
                            </SelectItem>
                          ))
                        ) : (
                          <SelectItem value="__no_semester" disabled>
                            Aucun semestre disponible
                          </SelectItem>
                        )}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Statut de redoublement
                    </label>
                    <Select
                      value={annual?.register_semester[0]?.repeat_status || ""}
                      onValueChange={(value) =>
                        onUpdateRegistrationField(index, "repeat_status", value)
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner le statut" />
                      </SelectTrigger>
                      <SelectContent>
                        {repeatStatusOptions.map((status) => (
                          <SelectItem key={status} value={status}>
                            {formatRepeatStatus(status)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                    Parcours
                  </label>
                  <Select
                    value={selectedJourneyId}
                    onValueChange={(value) =>
                      onUpdateRegistrationField(index, "journey", value)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Sélectionner le parcours" />
                    </SelectTrigger>
                    <SelectContent>
                      {journeyOptions.length ? (
                        journeyOptions.map((journey) => (
                          <SelectItem key={journey.id} value={journey.id}>
                            {journey.label}
                          </SelectItem>
                        ))
                      ) : (
                        <SelectItem value="__no_journey" disabled>
                          Aucun parcours disponible
                        </SelectItem>
                      )}
                    </SelectContent>
                  </Select>
                </div>
              </>
            ) : (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <StudentFormInfoItem
                    label="Semestre"
                    value={annual?.register_semester[0]?.semester || "N/A"}
                  />
                  <StudentFormInfoItem
                    label="Statut de redoublement"
                    value={
                      formatRepeatStatus(
                        annual?.register_semester[0]?.repeat_status
                      ) || "N/A"
                    }
                  />
                </div>
                <StudentFormInfoItem
                  label="Parcours"
                  value={annual?.register_semester[0]?.journey.name || "N/A"}
                />
              </>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};
