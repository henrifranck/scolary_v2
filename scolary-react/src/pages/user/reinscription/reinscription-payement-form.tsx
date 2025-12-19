import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Check, Pencil } from "lucide-react";
import { useCallback, useState } from "react";
import {
  EditableSection,
  FormItemComponentType,
  FormItemType,
  ReinscriptionAnnualProps,
  ReinscriptionFormState
} from "./reinscription-form-type";
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
import { ReinscriptionForm } from "./reinscription-form";
import { RegistrationPaymentForm } from "../registration/registration-payment-form";

interface ReinscriptionAnnualFormProps {
  annualRegister: Array<ReinscriptionAnnualProps>;
  setEditingSections: (value: any) => any;
  editingSections: Record<EditableSection, boolean>;
  cardNumber?: string;
  filters?: any;
}

export const handleFormSubmit = (e: React.FormEvent) => {};

export const ReinscriptionAnnualRegister = ({
  annualRegister,
  setEditingSections,
  editingSections,
  cardNumber,
  filters
}: ReinscriptionAnnualFormProps) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const toggleSectionEditing = useCallback((section: EditableSection) => {
    setEditingSections((previous: any) => ({
      ...previous,
      [section]: !previous[section]
    }));
  }, []);

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
              <DialogTitle>"Create reinscription"</DialogTitle>
              <DialogDescription>
                "This student already exists in the database. Review the key
                information before confirming the reinscription."
              </DialogDescription>
            </DialogHeader>
            <RegistrationPaymentForm
              cardNumber={cardNumber}
              filters={filters}
            />

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
