import { StudentAnnualProps } from "@/components/student-form/student-form-types";
import { StudentFormInfoItem } from "@/components/student-form/student-form-info-item";
import formatRepeatStatus from "@/lib/enum/repeat-status-enum";

import { RegistrationForm } from "../registration/registration-form";

type RegistrationSummaryProps = {
  displayAnnualRegisters: Array<StudentAnnualProps>;
};

type RegistrationEditorProps = {
  annualRegisterDrafts: Array<
    StudentAnnualProps & { isEditing?: boolean; isNew?: boolean }
  >;
  hasRegistrationEntries: boolean;
  mergeAnnualWithDrafts: (
    annual: StudentAnnualProps & { isEditing?: boolean; isNew?: boolean },
    index: number
  ) => StudentAnnualProps & { isEditing?: boolean; isNew?: boolean };
  filters?: any;
  journeyOptions: Array<{
    id: string;
    label: string;
    semesterList: string[];
    mentionId?: string;
  }>;
  onAddRegistration: () => void;
  onSave: (
    index: number,
    mode: "registration" | "payment",
    itemIndex: number
  ) => void;
  onUpdateRegistrationField: (
    index: number,
    registrationIndex: number,
    field: "semester" | "repeat_status" | "journey",
    value: string
  ) => void;
  onCancel: (annualIndex: number, registrationIndex: number) => void;
  onToggleEdit: (annualIndex: number, registrationIndex: number) => void;
  onDelete: (annualIndex: number, registrationIndex: number) => void;
  editingRegistrationIndexByAnnual: Record<string, number | null>;
  getAnnualKey: (
    annual: StudentAnnualProps & { id?: number },
    index: number
  ) => string;
  savingIndex: number | null;
};

export const RegistrationSummary = ({
  displayAnnualRegisters
}: RegistrationSummaryProps) => (
  <div className="space-y-2">
    {displayAnnualRegisters?.map((annual, index) => (
      <div key={index} className="grid gap-4">
        {annual?.register_semester?.length ? (
          annual.register_semester.map((semester, semesterIndex) => (
            <div
              key={`${index}-semester-${semesterIndex}`}
              className="grid gap-2 rounded-lg border border-dashed bg-background/60 p-3"
            >
              <div className="grid gap-4 sm:grid-cols-2">
                <StudentFormInfoItem
                  label="Semestre"
                  value={semester?.semester || "N/A"}
                />
                <StudentFormInfoItem
                  label="Statut de redoublement"
                  value={formatRepeatStatus(semester?.repeat_status) || "N/A"}
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
  </div>
);

export const RegistrationEditor = ({
  annualRegisterDrafts,
  hasRegistrationEntries,
  mergeAnnualWithDrafts,
  filters,
  journeyOptions,
  onAddRegistration,
  onSave,
  onUpdateRegistrationField,
  onCancel,
  onToggleEdit,
  onDelete,
  editingRegistrationIndexByAnnual,
  getAnnualKey,
  savingIndex
}: RegistrationEditorProps) => (
  <div className="space-y-4">
    <div className="flex items-center justify-between gap-2">
      <p className="text-sm font-medium">Inscriptions</p>
      <button
        type="button"
        className="inline-flex h-8 items-center gap-2 rounded-md border border-input bg-background px-3 text-sm shadow-sm transition hover:bg-accent hover:text-accent-foreground disabled:opacity-50"
        onClick={onAddRegistration}
        disabled={!annualRegisterDrafts.length}
      >
        Ajouter
      </button>
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
              onToggleEdit={onToggleEdit}
              onDelete={onDelete}
              onCancel={onCancel}
              onSave={onSave}
              onUpdateRegistrationField={onUpdateRegistrationField}
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
  </div>
);
