import { StudentAnnualProps } from "@/components/student-form/student-form-types";
import { StudentFormInfoItem } from "@/components/student-form/student-form-info-item";

import { PaymentForm } from "./payment-form";

type PaymentSummaryProps = {
  displayAnnualRegisters: Array<StudentAnnualProps>;
};

type PaymentEditorProps = {
  annualRegisterDrafts: Array<
    StudentAnnualProps & { isEditing?: boolean; isNew?: boolean }
  >;
  hasPaymentEntries: boolean;
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
  onAddPayment: () => void;
  onSave: (
    index: number,
    mode: "registration" | "payment",
    itemIndex: number
  ) => void;
  onUpdatePaymentField: (
    index: number,
    paymentIndex: number,
    field: "num_receipt" | "date_receipt" | "payed" | "description",
    value: string | number
  ) => void;
  onCancel: (annualIndex: number, paymentIndex: number) => void;
  onToggleEdit: (annualIndex: number, paymentIndex: number) => void;
  onDelete: (annualIndex: number, paymentIndex: number) => void;
  editingPaymentIndexByAnnual: Record<string, number | null>;
  getAnnualKey: (
    annual: StudentAnnualProps & { id?: number },
    index: number
  ) => string;
  savingIndex: number | null;
};

export const PaymentSummary = ({
  displayAnnualRegisters
}: PaymentSummaryProps) => (
  <div className="space-y-2">
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
              <StudentFormInfoItem
                label="Description"
                value={payment?.description || "N/A"}
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
  </div>
);

export const PaymentEditor = ({
  annualRegisterDrafts,
  hasPaymentEntries,
  mergeAnnualWithDrafts,
  filters,
  journeyOptions,
  onAddPayment,
  onSave,
  onUpdatePaymentField,
  onCancel,
  onToggleEdit,
  onDelete,
  editingPaymentIndexByAnnual,
  getAnnualKey,
  savingIndex
}: PaymentEditorProps) => (
  <div className="space-y-4">
    <div className="flex items-center justify-between gap-2">
      <p className="text-sm font-medium">Paiements</p>
      <button
        type="button"
        className="inline-flex h-8 items-center gap-2 rounded-md border border-input bg-background px-3 text-sm shadow-sm transition hover:bg-accent hover:text-accent-foreground disabled:opacity-50"
        onClick={onAddPayment}
        disabled={!annualRegisterDrafts.length}
      >
        Ajouter
      </button>
    </div>
    {annualRegisterDrafts.length && hasPaymentEntries ? (
      annualRegisterDrafts.flatMap((annual, index) => {
        const mergedAnnual = mergeAnnualWithDrafts(annual, index);
        return (mergedAnnual.payment ?? []).map((_entry, paymentIndex) => (
          <PaymentForm
            key={`${annual.id ?? "new"}-${index}-${paymentIndex}`}
            annual={mergedAnnual}
            index={index}
            paymentIndex={paymentIndex}
            filters={filters}
            journeyOptions={journeyOptions}
            onToggleEdit={onToggleEdit}
            onDelete={onDelete}
            onCancel={onCancel}
            onSave={onSave}
            onUpdatePaymentField={onUpdatePaymentField}
            isSaving={savingIndex === index}
            isEditing={
              editingPaymentIndexByAnnual[getAnnualKey(annual, index)] ===
              paymentIndex
            }
          />
        ));
      })
    ) : (
      <p className="text-sm text-muted-foreground">
        Aucun paiement à afficher.
      </p>
    )}
  </div>
);
