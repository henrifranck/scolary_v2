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

interface PaymentFormProps {
  annual: StudentAnnualProps & { isEditing?: boolean; isNew?: boolean };
  index: number;
  paymentIndex: number;
  isEditing: boolean;
  filters?: any;
  journeyOptions: Array<{
    id: string;
    label: string;
    semesterList: string[];
  }>;
  onToggleEdit: (index: number, paymentIndex: number) => void;
  onCancel: (index: number, paymentIndex: number) => void;
  onSave: (
    index: number,
    mode: "registration" | "payment",
    itemIndex: number
  ) => void;
  onDelete: (index: number, paymentIndex: number) => void;
  onUpdatePaymentField: (
    index: number,
    paymentIndex: number,
    field: "num_receipt" | "date_receipt" | "payed" | "description",
    value: string | number
  ) => void;
  isSaving?: boolean;
}

export const PaymentForm = ({
  annual,
  index,
  paymentIndex,
  isEditing,
  filters,
  journeyOptions,
  onToggleEdit,
  onCancel,
  onSave,
  onDelete,
  onUpdatePaymentField,
  isSaving
}: PaymentFormProps) => {
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
  const academicYearName = annual?.academic_year?.name || "";
  const semesterValue = semesterOptions.includes(selectedSemesterValue)
    ? selectedSemesterValue
    : "";

  const paymentEntry = annual?.payment?.[paymentIndex];

  return (
    <div className="space-y-4 rounded-xl border bg-muted/20 p-4 max-h-[350px] overflow-y-auto">
      <div className="flex items-center justify-end">
        <div className="flex items-center gap-2">

          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-8 gap-2 px-3 text-destructive hover:text-destructive"
            onClick={() => onDelete(index, paymentIndex)}
            disabled={isSaving}
          >
            <Trash2 className="h-4 w-4" />
            Supprimer
          </Button>
          {isEditing ? (
            <>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 gap-2 px-3"
                onClick={() => onCancel(index, paymentIndex)}
                disabled={isSaving}
              >
                Annuler
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 gap-2 px-3"
                onClick={() => onSave(index, "payment", paymentIndex)}
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
              onClick={() => onToggleEdit(index, paymentIndex)}
              disabled={isSaving}
            >
              <Pencil className="h-4 w-4" />
              Modifier
            </Button>
          )}
        </div>
      </div>

        <div  className="space-y-2">
          <div className="grid gap-4">
            {isEditing ? (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Numéro de reçu
                    </label>
                    <Input
                      value={paymentEntry?.num_receipt || ""}
                      required
                      onChange={(event) =>
                        onUpdatePaymentField(
                          index,
                          paymentIndex,
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
                      value={paymentEntry?.date_receipt || ""}
                      required
                      onChange={(event) =>
                        onUpdatePaymentField(
                          index,
                          paymentIndex,
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
                    min={1}
                    required
                    value={paymentEntry?.payed ?? 0}
                    onChange={(event) =>
                      onUpdatePaymentField(
                        index,
                        paymentIndex,
                        "payed",
                        Number(event.target.value)
                      )
                    }
                    placeholder="Saisir le montant"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                    Description
                  </label>
                  <Input
                    value={paymentEntry?.description || ""}
                    onChange={(event) =>
                      onUpdatePaymentField(
                        index,
                        paymentIndex,
                        "description",
                        event.target.value
                      )
                    }
                    placeholder="Ajouter une description"
                  />
                </div>
              </>
            ) : (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <StudentFormInfoItem
                    label="Numéro de reçu"
                    value={paymentEntry?.num_receipt || "N/A"}
                  />
                  <StudentFormInfoItem
                    label="Date de reçu"
                    value={paymentEntry?.date_receipt || "N/A"}
                  />
                </div>
                <StudentFormInfoItem
                  label="Montant payé"
                  value={
                    paymentEntry?.payed
                      ? `${paymentEntry.payed} Ar`
                      : "N/A"
                  }
                />
                <StudentFormInfoItem
                  label="Description"
                  value={paymentEntry?.description || "N/A"}
                />
              </>
            )}
          </div>
        </div>
    </div>
  );
};
