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

interface RegistrationFormProps {
  annual: StudentAnnualProps & { isEditing?: boolean; isNew?: boolean };
  index: number;
  registrationIndex: number;
  isEditing: boolean;
  filters?: any;
  journeyOptions: Array<{
    id: string;
    label: string;
    semesterList: string[];
  }>;
  onToggleEdit: (index: number, registrationIndex: number) => void;
  onCancel: (index: number, registrationIndex: number) => void;
  onSave: (
    index: number,
    mode: "registration" | "payment",
    itemIndex: number
  ) => void;
  onDelete: (index: number, registrationIndex: number) => void;
  onUpdateRegistrationField: (
    index: number,
    registrationIndex: number,
    field: "semester" | "repeat_status" | "journey",
    value: string
  ) => void;
  isSaving?: boolean;
}

export const RegistrationForm = ({
  annual,
  index,
  registrationIndex,
  isEditing,
  filters,
  journeyOptions,
  onToggleEdit,
  onCancel,
  onSave,
  onDelete,
  onUpdateRegistrationField,
  isSaving
}: RegistrationFormProps) => {
  const repeatStatusOptions = Object.values(RepeatStatusEnum);
  const registrationEntry = annual?.register_semester?.[registrationIndex];
  const selectedJourneyId = registrationEntry?.id_journey
    ? String(registrationEntry.id_journey)
    : registrationEntry?.journey?.id
      ? String(registrationEntry.journey.id)
      : "";
  const selectedJourney = journeyOptions.find(
    (journey) => journey.id === selectedJourneyId
  );
  const semesterOptions = selectedJourney?.semesterList ?? [];
  const selectedSemesterValue = registrationEntry?.semester || "";
  const academicYearName = annual?.academic_year?.name || "";
  const semesterValue = semesterOptions.includes(selectedSemesterValue)
    ? selectedSemesterValue
    : "";

  return (
    <div className="space-y-4 rounded-xl border bg-muted/20 p-4 max-h-[350px] overflow-y-auto">
      <div className="flex items-center justify-end">
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-8 gap-2 px-3 text-destructive hover:text-destructive"
            onClick={() => onDelete(index, registrationIndex)}
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
                onClick={() => onCancel(index, registrationIndex)}
                disabled={isSaving}
              >
                Annuler
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 gap-2 px-3"
                onClick={() =>
                  onSave(index, "registration", registrationIndex)
                }
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
              onClick={() => onToggleEdit(index, registrationIndex)}
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
                      Semestre
                    </label>
                    <Select
                      value={semesterValue}
                      required
                      aria-required="true"
                      onValueChange={(value) =>
                        onUpdateRegistrationField(
                          index,
                          registrationIndex,
                          "semester",
                          value
                        )
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
                      value={registrationEntry?.repeat_status || ""}
                      required
                      aria-required="true"
                      onValueChange={(value) =>
                        onUpdateRegistrationField(
                          index,
                          registrationIndex,
                          "repeat_status",
                          value
                        )
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
                    required
                    aria-required="true"
                    onValueChange={(value) =>
                      onUpdateRegistrationField(
                        index,
                        registrationIndex,
                        "journey",
                        value
                      )
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
                    value={registrationEntry?.semester || "N/A"}
                  />
                  <StudentFormInfoItem
                    label="Statut de redoublement"
                    value={
                      formatRepeatStatus(registrationEntry?.repeat_status) ||
                      "N/A"
                    }
                  />
                </div>
                <StudentFormInfoItem
                  label="Parcours"
                  value={registrationEntry?.journey?.name || "N/A"}
                />
              </>
            )}
          </div>
        </div>
    </div>
  );
};
