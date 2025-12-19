import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { fetchStudentByCardNumber } from "@/services/student-service";
import { Check, Pencil } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  EditableSection,
  FormItemComponentType,
  ReinscriptionAnnualProps,
  ReinscriptionFormState,
  StudentProfile
} from "./reinscription-form-type";
import { ReinscriptionFormItem } from "./reinscription-form-item";
import { InfoItem } from "./reinscription-form-info-item";
import {
  informationDataBirth,
  informationDataContact,
  informationDataIdentity
} from "./information-form-data";
import { ReinscriptionFilters } from "@/services/reinscription-service";
import { ReinscriptionAnnualRegister } from "./reinscription-payement-form";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";

type dialogMode = "edit" | "create";

const createEditingSectionsState = (): Record<EditableSection, boolean> => ({
  contact: false,
  birth: false,
  identity: false,
  school: false,
  personal: false
});

interface ReinscriptionFormProps {
  formError: string | null;
  formState: ReinscriptionFormState;
  setFormState: (value: any) => any;
  dialogMode: dialogMode;
  filters: ReinscriptionFilters;
}

export const ReinscriptionForm = ({
  formError,
  formState,
  setFormState,
  dialogMode,
  filters
}: ReinscriptionFormProps) => {
  const lastLookupKeyRef = useRef<string>("");
  const [studentLookupLoading, setStudentLookupLoading] = useState(false);
  const [annualRegister, setAnnualRegister] = useState<
    ReinscriptionAnnualProps[]
  >([]);
  const [studentLookupError, setStudentLookupError] = useState<string | null>(
    null
  );
  const [picturePreview, setPicturePreview] = useState<string | null>(null);
  const pictureInputId = "student-picture-upload";

  const [inputContact] = useState<FormItemComponentType>(
    informationDataContact
  );
  const [inputBirth] = useState<FormItemComponentType>(informationDataBirth);
  const [inputIdentity] = useState<FormItemComponentType>(
    informationDataIdentity
  );
  useEffect(() => {
    console.log("STATE annualRegister =", annualRegister);
  }, [annualRegister]);

  const toggleSectionEditing = useCallback((section: EditableSection) => {
    setEditingSections((previous) => ({
      ...previous,
      [section]: !previous[section]
    }));
  }, []);

  const [editingSections, setEditingSections] = useState<
    Record<EditableSection, boolean>
  >(() => createEditingSectionsState());

  const handleFormChange = useCallback(
    (key: keyof ReinscriptionFormState, value: string) => {
      setFormState((previous: any) => ({
        ...previous,
        [key]: value
      }));

      if (key === "cardNumber") {
        setStudentLookupError(null);
      }
    },
    []
  );

  const populateStudentFields = useCallback(
    (student: StudentProfile) => {
      if (!student) {
        return;
      }

      const studentYear = student.annual_register?.[0];
      const resolvedJourneyId =
        studentYear?.register_semester[0]?.journey?.id ?? null;
      const resolvedMentionId =
        student.id_mention ??
        studentYear?.register_semester[0]?.journey?.id_mention ??
        null;
      const resolvedSemester =
        student.active_semester ??
        studentYear?.register_semester[0]?.semester ??
        "";
      setFormState((previous: any) => ({
        ...previous,
        studentRecordId: student.id
          ? String(student.id)
          : previous.studentRecordId,
        studentId:
          student.num_select ??
          (student.id ? String(student.id) : previous.studentId),
        cardNumber: student.num_carte ?? previous.cardNumber,
        firstName: student.first_name ?? previous.firstName,
        lastName: student.last_name ?? previous.lastName,
        email: student.email ?? previous.email,
        address: student.address ?? previous.address,
        cinNumber: student.num_of_cin ?? student.num_cin ?? previous.cinNumber,
        cinIssueDate: student.date_of_cin ?? previous.cinIssueDate,
        cinIssuePlace: student.place_of_cin ?? previous.cinIssuePlace,
        birthDate: student.date_of_birth ?? previous.birthDate,
        birthPlace: student.place_of_birth ?? previous.birthPlace,
        picture:
          student.picture ??
          student.photo_url ??
          previous.picture,
        pictureFile: null,
        mentionId: resolvedMentionId
          ? String(resolvedMentionId)
          : previous.mentionId,
        journeyId: resolvedJourneyId
          ? String(resolvedJourneyId)
          : previous.journeyId,
        semester: resolvedSemester || previous.semester,
        status: student.enrollment_status ?? previous.status
      }));
      setStudentLookupError(null);
    },
    [setFormState]
  );

  const handleStudentLookup = useCallback(
    async (force = false) => {
      const trimmed = formState.cardNumber.trim();
      if (!trimmed) {
        setStudentLookupError("Veuillez saisir un numéro de carte.");
        return;
      }

      const lookupKey = `${trimmed}|${filters.id_year}|${filters.semester}`;
      if (!force && lookupKey === lastLookupKeyRef.current) {
        return;
      }
      lastLookupKeyRef.current = lookupKey;

      setStudentLookupLoading(true);
      setStudentLookupError(null);
      try {
        const profile = await fetchStudentByCardNumber(filters, trimmed);

        console.log("PROFILE =", profile);
        console.log(
          "profile.annual_register =",
          (profile as any).annual_register
        );
        console.log(
          "profile.data?.annual_register =",
          (profile as any).data?.annual_register
        );

        const student = (profile as any).data ?? profile;

        console.log("student.annual_register =", student.annual_register);

        const rawAnnual = Array.isArray(student.annual_register)
          ? student.annual_register
          : [];
        const normalizedAnnual = rawAnnual
          .map((entry: any) => {
            const payment =
              entry?.payment ?? entry?.payement ?? entry?.payments ?? [];
            return { ...entry, payment };
          })
          .filter(
            (entry: any) =>
              Array.isArray(entry?.register_semester) &&
              entry.register_semester.length > 0
          );

        setAnnualRegister(normalizedAnnual);
        populateStudentFields(student as StudentProfile);
      } catch (error) {
        setStudentLookupError(
          error instanceof Error
            ? error.message
            : "Impossible de charger l'étudiant."
        );
      } finally {
        setStudentLookupLoading(false);
      }
    },
    [formState.cardNumber, populateStudentFields, filters]
  );

  const handlePictureUpload = useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (!file) {
        return;
      }
      setFormState((previous: any) => ({
        ...previous,
        pictureFile: file
      }));
    },
    [setFormState]
  );

  useEffect(() => {
    if (!formState.pictureFile) {
      setPicturePreview(null);
      return;
    }
    const previewUrl = URL.createObjectURL(formState.pictureFile);
    setPicturePreview(previewUrl);
    return () => {
      URL.revokeObjectURL(previewUrl);
    };
  }, [formState.pictureFile]);

  useEffect(() => {
    if (dialogMode !== "edit") {
      lastLookupKeyRef.current = "";
      return;
    }

    const trimmed = formState.cardNumber.trim();
    if (!trimmed) {
      return;
    }

    void handleStudentLookup(false);
  }, [dialogMode, formState.cardNumber, handleStudentLookup]);

  return (
    <div className="flex-1 overflow-y-auto px-6 py-4 min-h-0">
      <div className="space-y-4">
        {formError && (
          <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-2 text-sm text-destructive">
            {formError}
          </div>
        )}
        <div className="space-y-6">
          <div className="rounded-xl border bg-card/80 p-5 shadow-sm space-y-5">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">
                Numéro de carte étudiant
              </label>
              <div className="flex flex-col gap-2 sm:flex-row">
                <Input
                  value={formState.cardNumber}
                  onChange={(event) =>
                    handleFormChange("cardNumber", event.target.value)
                  }
                  placeholder="Ex: SCT-000123"
                />
                <Button
                  type="button"
                  onClick={() => handleStudentLookup(true)}
                  disabled={
                    studentLookupLoading || !formState.cardNumber.trim().length
                  }
                >
                  {studentLookupLoading ? "Recherche..." : "Rechercher"}
                </Button>
              </div>
              <p className="text-xs text-muted-foreground">
                Entrez le numéro pour charger automatiquement les informations
                enregistrées dans la base.
              </p>
              {studentLookupError && (
                <p className="text-sm text-destructive">{studentLookupError}</p>
              )}
            </div>
            <div className="grid gap-4 sm:grid-cols-1 lg:grid-cols-2">
              <div className="grid gap-4 lg:grid-cols-1">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-foreground">
                    Informations personnelles
                  </p>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="h-8 gap-2 px-3"
                    onClick={() => toggleSectionEditing("personal")}
                  >
                    {editingSections.personal ? (
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
                {editingSections.personal ? (
                  <>
                    <div>
                      <div className="space-y-1.5">
                        <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                          Nom
                        </label>
                        <Input
                          value={formState.lastName}
                          onChange={(event) =>
                            handleFormChange("lastName", event.target.value)
                          }
                          placeholder="Nom de famille"
                        />
                      </div>
                      <div className="space-y-1.5">
                        <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                          Prenom
                        </label>
                        <Input
                          value={formState.firstName}
                          onChange={(event) =>
                            handleFormChange("firstName", event.target.value)
                          }
                          placeholder="Prénom(s)"
                        />
                      </div>
                      <div className="space-y-1.5">
                        <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                          Email
                        </label>
                        <Input
                          value={formState.email}
                          onChange={(event) =>
                            handleFormChange("email", event.target.value)
                          }
                          placeholder="Adresse email"
                        />
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <InfoItem
                      label="Nom complet"
                      value={`${formState.lastName} ${formState.firstName}`}
                    />
                    <InfoItem label="Email" value={formState.email} />
                  </>
                )}
              </div>
              <div className="space-y-4">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-foreground">
                    Photo étudiant
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="relative h-24 w-24">
                    {picturePreview || formState.picture ? (
                      <img
                        src={picturePreview ?? resolveAssetUrl(formState.picture)}
                        alt="Photo étudiant"
                        className="h-24 w-24 rounded-full border object-cover"
                      />
                    ) : (
                      <div className="h-24 w-24 rounded-full border bg-muted/20" />
                    )}
                    <label
                      htmlFor={pictureInputId}
                      className="absolute -bottom-1 -right-1 inline-flex h-8 w-8 items-center justify-center rounded-full border bg-background shadow-sm hover:bg-muted/50 cursor-pointer"
                    >
                      <Pencil className="h-4 w-4" />
                    </label>
                    <input
                      id={pictureInputId}
                      type="file"
                      accept="image/*"
                      onChange={handlePictureUpload}
                      className="hidden"
                    />
                  </div>
                  <p className="text-xs text-muted-foreground">
                    La photo sera envoyée au moment d'enregistrer.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <ReinscriptionFormItem
              name={"Coordonnées"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={inputContact}
              classnNames="grid gap-4"
            />

            <ReinscriptionFormItem
              name={"Informations sur la naissance"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={inputBirth}
              classnNames="grid gap-4 sm:grid-cols-2"
            />

            {/* <div className="space-y-4 rounded-xl border bg-muted/20 p-5 max-h-[320px] overflow-y-auto">
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-semibold text-foreground">
                  Informations sur la naissance
                </p>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-8 gap-2 px-3"
                  onClick={() => toggleSectionEditing("birth")}
                >
                  {editingSections.birth ? (
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
              {editingSections.birth ? (
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Date de naissance
                    </label>
                    <Input
                      type="date"
                      value={formState.birthDate}
                      onChange={(event) =>
                        handleFormChange("birthDate", event.target.value)
                      }
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Lieu de naissance
                    </label>
                    <Input
                      value={formState.birthPlace}
                      onChange={(event) =>
                        handleFormChange("birthPlace", event.target.value)
                      }
                      placeholder="Ville ou district"
                    />
                  </div>
                </div>
              ) : (
                <div className="grid gap-4 sm:grid-cols-2">
                  <InfoItem
                    label="Date de naissance"
                    value={formState.birthDate}
                  />
                  <InfoItem
                    label="Lieu de naissance"
                    value={formState.birthPlace}
                  />
                </div>
              )}
            </div> */}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <ReinscriptionFormItem
              name={"Carte d'identité"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={inputIdentity}
              classnNames="grid gap-4 sm:grid-cols-2"
            />

            <ReinscriptionAnnualRegister
              annualRegister={annualRegister}
              editingSections={editingSections}
              cardNumber={formState.cardNumber}
              filters={filters}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
