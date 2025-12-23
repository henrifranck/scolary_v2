import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { useQuery } from "@tanstack/react-query";
import { fetchStudentByCardNumber } from "@/services/student-service";
import { Check, Pencil, Layers } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  EditableSection,
  FormItemComponentType,
  StudentAnnualProps,
  StudentFormState,
  StudentProfile
} from "./student-form-types";
import { StudentFormItem } from "./student-form-item";
import { StudentFormInfoItem } from "./student-form-info-item";
import {
  studentInformationBirth,
  studentInformationContact,
  studentInformationIdentity,
  studentInformationBaccalaureate,
  studentInformationSocial,
  studentInformationRegistration
} from "./student-form-data";
import { ReinscriptionFilters } from "@/services/reinscription-service";
import { ReinscriptionAnnualRegister } from "@/pages/user/reinscription/reinscription-payment-form";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { MentionOption } from "@/components/filters/academic-filters";
import { fetchMentions } from "@/services/inscription-service";

type dialogMode = "edit" | "create";

const formatMadagascarPhone = (raw: string) => {
  const digitsOnly = raw.replace(/\D/g, "");
  let local = digitsOnly;
  if (local.startsWith("261")) {
    local = local.slice(3);
  }
  if (local.startsWith("0")) {
    local = local.slice(1);
  }
  local = local.slice(0, 9);
  if (local && local[0] !== "3") {
    local = `3${local.slice(1)}`;
  }
  const groups = [2, 2, 3, 2];
  const parts: string[] = [];
  let index = 0;
  groups.forEach((len) => {
    if (index >= local.length) {
      return;
    }
    const part = local.slice(index, index + len);
    parts.push(part);
    index += len;
  });
  return `+261 ${parts.join(" ")}`.trim();
};

const createEditingSectionsState = (): Record<EditableSection, boolean> => ({
  contact: false,
  birth: false,
  identity: false,
  school: false,
  personal: false,
  baccalaureate: false,
  social: false,
  registration: false
});

interface StudentFormProps {
  formError: string | null;
  formState: StudentFormState;
  setFormState: (value: any) => any;
  dialogMode: dialogMode;
  filters: ReinscriptionFilters;
  enableLookup?: boolean;
  enablePicture?: boolean;
  mentionOptions?: MentionOption[];
}

export const StudentForm = ({
  formError,
  formState,
  setFormState,
  dialogMode,
  filters,
  enableLookup = true,
  enablePicture = true,
  mentionOptions = []
}: StudentFormProps) => {
  const { data: fetchedMentions = [], isLoading: isLoadingMentions } = useQuery({
    queryKey: ["student-form", "mentions"],
    queryFn: () => fetchMentions({ user_only: true }),
    enabled: mentionOptions.length === 0
  });
  const effectiveMentionOptions =
    mentionOptions.length > 0
      ? mentionOptions
      : fetchedMentions.map((mention) => ({
          id: String(mention.id),
          label: mention.name ?? mention.abbreviation ?? `Mention ${mention.id}`
        }));
  const lastLookupKeyRef = useRef<string>("");
  const [studentLookupLoading, setStudentLookupLoading] = useState(false);
  const [annualRegister, setAnnualRegister] = useState<StudentAnnualProps[]>(
    []
  );
  const [studentLookupError, setStudentLookupError] = useState<string | null>(
    null
  );
  const [picturePreview, setPicturePreview] = useState<string | null>(null);
  const pictureInputId = "student-picture-upload";

  const [inputContact] = useState<FormItemComponentType>(
    studentInformationContact
  );
  const [inputBirth] = useState<FormItemComponentType>(studentInformationBirth);
  const [inputIdentity] = useState<FormItemComponentType>(
    studentInformationIdentity
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
    (key: keyof StudentFormState, value: string) => {
      const nextValue =
        key === "phoneNumber" ? formatMadagascarPhone(value) : value;
      setFormState((previous: any) => ({
        ...previous,
        [key]: nextValue
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
        phoneNumber: student.phone_number ?? previous.phoneNumber,
        sex: student.sex ?? previous.sex,
        maritalStatus: student.martial_status ?? previous.maritalStatus,
        baccalaureateNumber:
          student.num_of_baccalaureate ?? previous.baccalaureateNumber,
        baccalaureateCenter:
          student.center_of_baccalaureate ?? previous.baccalaureateCenter,
        job: student.job ?? previous.job,
        cinNumber: student.num_of_cin ?? student.num_cin ?? previous.cinNumber,
        cinIssueDate: student.date_of_cin ?? previous.cinIssueDate,
        cinIssuePlace: student.place_of_cin ?? previous.cinIssuePlace,
        birthDate: student.date_of_birth ?? previous.birthDate,
        birthPlace: student.place_of_birth ?? previous.birthPlace,
        picture: student.picture ?? student.photo_url ?? previous.picture,
        pictureFile: null,
        mentionId: resolvedMentionId
          ? String(resolvedMentionId)
          : previous.mentionId,
        journeyId: resolvedJourneyId
          ? String(resolvedJourneyId)
          : previous.journeyId,
        semester: resolvedSemester || previous.semester,
        status: student.enrollment_status ?? previous.status,
        level: student.level ?? previous.level,
        enrollmentStatus: student.enrollment_status ?? previous.enrollmentStatus
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
              entry?.payment ?? entry?.payments ?? [];
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
    if (!enablePicture || !formState.pictureFile) {
      setPicturePreview(null);
      return;
    }
    const previewUrl = URL.createObjectURL(formState.pictureFile);
    setPicturePreview(previewUrl);
    return () => {
      URL.revokeObjectURL(previewUrl);
    };
  }, [enablePicture, formState.pictureFile]);

  useEffect(() => {
    if (dialogMode !== "edit") {
      lastLookupKeyRef.current = "";
      return;
    }

    const trimmed = formState.cardNumber.trim();
    if (!trimmed) {
      return;
    }

    if (enableLookup) {
      void handleStudentLookup(false);
    }
  }, [dialogMode, enableLookup, formState.cardNumber, handleStudentLookup]);

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
            {enableLookup && (
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
                      studentLookupLoading ||
                      !formState.cardNumber.trim().length
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
                  <p className="text-sm text-destructive">
                    {studentLookupError}
                  </p>
                )}
              </div>
            )}
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
                    <StudentFormInfoItem
                      label="Nom complet"
                      value={`${formState.lastName} ${formState.firstName}`}
                    />
                    <StudentFormInfoItem
                      label="Email"
                      value={formState.email}
                    />
                  </>
                )}
              </div>
              {enablePicture && (
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
                          src={
                            picturePreview ?? resolveAssetUrl(formState.picture)
                          }
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
              )}
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <StudentFormItem
              name={"Informations sur le baccalauréat et Téléphone"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={studentInformationBaccalaureate}
              classnNames="grid gap-4 sm:grid-cols-2"
            />

            <StudentFormItem
              name={"Statut social"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={studentInformationSocial}
              classnNames="grid gap-4 sm:grid-cols-2"
            />
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <StudentFormItem
              name={"Statut d'inscription"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={studentInformationRegistration}
              classnNames="grid gap-4"
            />

            {effectiveMentionOptions.length > 0 && (
              <div className="space-y-3 rounded-xl border bg-muted/20 p-5">
                <div className="flex items-center gap-2">
                  <Layers className="h-4 w-4 text-muted-foreground" />
                  <label className="text-sm font-medium">Mention</label>
                </div>
                <Select
                  value={formState.mentionId}
                  onValueChange={(value) =>
                    handleFormChange("mentionId", value)
                  }
                  disabled={isLoadingMentions}
                >
                  <SelectTrigger className="h-11">
                    <SelectValue placeholder="Sélectionner la mention" />
                  </SelectTrigger>
                  <SelectContent>
                    {effectiveMentionOptions.map((mention) => (
                      <SelectItem key={mention.id} value={mention.id}>
                        {mention.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <StudentFormItem
              name={"Coordonnées"}
              editingSections={editingSections}
              setEditingSections={setEditingSections}
              handleFormChange={handleFormChange}
              formState={formState}
              inputComponent={inputContact}
              classnNames="grid gap-4"
            />

            <StudentFormItem
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
              <StudentFormInfoItem
                label="Date de naissance"
                value={formState.birthDate}
              />
              <StudentFormInfoItem
                label="Lieu de naissance"
                value={formState.birthPlace}
              />
            </div>
          )}
            </div> */}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <StudentFormItem
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
