import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Check, Pencil } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import formatRepeatStatus from "@/lib/enum/repeat-status-enum";
import { InfoItem } from "../reinscription/reinscription-form-info-item";
import {
  ReinscriptionAnnualProps,
  EditableSection
} from "../reinscription/reinscription-form-type";
import { fetchAnnualRegisterByCardNumber } from "@/services/annual-register-service";

interface RegistrationPaymentFormProps {
  cardNumber?: string;
  filters?: any;
}

export const RegistrationPaymentForm = ({
  cardNumber,
  filters
}: RegistrationPaymentFormProps) => {
  const [annualRegister, setAnnualRegister] = useState<
    Array<ReinscriptionAnnualProps>
  >([]);

  const [annualRegisterLoading, setAnnualRegisterLoading] = useState(false);
  const [annualRegisterError, setAnnualRegisterError] = useState("");

  const handleAnnualRegisterLookup = useCallback(
    async (force = false) => {
      const trimmed = cardNumber?.trim() ?? "";

      try {
        const annualRegister = (await fetchAnnualRegisterByCardNumber(trimmed))
          .data;
        setAnnualRegister(annualRegister);
        console.log("PROFILE =", annualRegister);
      } catch (error) {
        setAnnualRegisterLoading(false);
        setAnnualRegisterError("Erreur lors de la récupération des données.");
      } finally {
        setAnnualRegisterLoading(false);
      }
    },
    [cardNumber]
  );

  useEffect(() => {
    if (cardNumber) {
      handleAnnualRegisterLookup();
    }
  }, [cardNumber]);

  return (
    <div className="space-y-4 rounded-xl border bg-muted/20 p-5 max-h-[320px] overflow-y-auto">
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm font-semibold text-foreground">
          {filters?.id_year}
        </p>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="h-8 gap-2 px-3"
          onClick={() => {}}
        >
          <Check className="h-4 w-4" />
          Terminer
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
    </div>
  );
};
