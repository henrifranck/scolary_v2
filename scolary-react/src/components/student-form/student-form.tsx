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
import { fetchStudentByCardNumber } from "@/services/student-service";
import { Pencil, Layers, Eye, EyeOff } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  EditableSection,
  FormItemComponentType,
  StudentAnnualProps,
  StudentFormState,
  StudentProfile
} from "./student-form-types";
import { StudentFormItem } from "./student-form-item";
import {
  studentInformationBirth,
  studentInformationIdentity,
  studentInformationSocial,
  studentInformationPersonnel,
  enrollementFees,
  studentFatherInformation
} from "./student-form-data";
import { ReinscriptionFilters } from "@/services/reinscription-service";
import { ReinscriptionAnnualRegister } from "@/pages/user/payment/model-payment-form";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { MentionOption } from "@/models/mentions";
import { BaccalaureateSerieOption } from "@/models/baccalaureate-series";
import { useLookupOptions } from "@/hooks/use-lookup-options";

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
  registration: false,
  parentInfo: false
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
  baccalaureateOptions?: BaccalaureateSerieOption[];
  disabledEditing?: boolean;
  annualRegisterDisabled?: boolean;
  annualRegisterDisabledMessage?: string;
  registerType: string;
  newRegistration: boolean;
  onRegistrationStatusChange?: (hasRegistration: boolean) => void;
}

export const StudentForm = ({
  formError,
  formState,
  setFormState,
  dialogMode,
  filters,
  enableLookup = true,
  enablePicture = true,
  mentionOptions = [],
  baccalaureateOptions = [],
  disabledEditing = false,
  annualRegisterDisabled = false,
  annualRegisterDisabledMessage,
  registerType = "REGISTRATION",
  newRegistration = false,
  onRegistrationStatusChange
}: StudentFormProps) => {
  const {
    mentionOptions: cachedMentionOptions,
    baccalaureateSerieOptions: cachedBaccalaureateOptions,
    isLoadingMentions
  } = useLookupOptions({
    includeMentions: mentionOptions.length === 0,
    includeBaccalaureateSeries: baccalaureateOptions.length === 0
  });

  const levelOptions = ["L1", "L2", "L3", "M1", "M2"];
  const effectiveMentionOptions = useMemo(
    () => (mentionOptions.length > 0 ? mentionOptions : cachedMentionOptions),
    [cachedMentionOptions, mentionOptions]
  );

  const effectiveBaccalaureateOptions = useMemo(
    () =>
      baccalaureateOptions.length > 0
        ? baccalaureateOptions
        : cachedBaccalaureateOptions,
    [baccalaureateOptions, cachedBaccalaureateOptions]
  );

  const baccalaureateSerieOptions = useMemo(
    () =>
      effectiveBaccalaureateOptions.map((option) => ({
        value: option.id,
        label: option.label
      })),
    [effectiveBaccalaureateOptions]
  );
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

  const [inputBirth] = useState<FormItemComponentType>(studentInformationBirth);
  const [inputIdentity] = useState<FormItemComponentType>(
    studentInformationIdentity
  );

  const [inputPersonal] = useState<FormItemComponentType>(
    studentInformationPersonnel
  );
  const [inputFather] = useState<FormItemComponentType>(
    studentFatherInformation
  );

  const studentInformationBaccalaureate: FormItemComponentType = {
    value: [
      {
        label: "Numéro baccalauréat",
        type: "input",
        inputType: "text",
        formKey: "baccalaureateNumber",
        placeHolder: "Numéro baccalauréat"
      },
      {
        label: "Centre baccalauréat",
        type: "input",
        inputType: "text",
        formKey: "baccalaureateCenter",
        placeHolder: "Centre d'examen"
      },
      {
        label: "Année du baccalauréat",
        type: "input",
        inputType: "date",
        formKey: "baccalaureateYear",
        placeHolder: "Année du baccalauréat"
      },
      {
        label: "Serie du baccalauréat",
        type: "select",
        inputType: "text",
        formKey: "baccalaureateSerieId",
        selectValue: "baccakaureateSerieLabel",
        options: baccalaureateSerieOptions
      }
    ],
    key: "baccalaureate",
    style: "row"
  };

  const studentInformationRegistration: FormItemComponentType = {
    value: [
      {
        label: "Statut d'inscription",
        type: "select",
        inputType: "text",
        formKey: "enrollmentStatus",
        options: [
          { value: "pending", label: "En attente" },
          { value: "selected", label: "Sélectionné(e)" },
          { value: "rejected", label: "Rejeté(e)" },
          { value: "registered", label: "Inscrit(e)" },
          { value: "former", label: "Ancien(ne)" }
        ],
        selectValue:
          formState.enrollmentStatus &&
          enrollementFees[formState.enrollmentStatus],
        placeHolder: "En attente / Sélectionné(e) / Inscrit(e)"
      },
      {
        label: "Adresse",
        type: "input",
        inputType: "text",
        formKey: "address",
        placeHolder: "Saisir l'adresse complète"
      },
      {
        label: "Addresse des parent",
        type: "input",
        inputType: "text",
        formKey: "parentAdress",
        placeHolder: "Saisir l'adresse des parents"
      }
    ],
    key: "registration",
    style: "mixte"
  };

  const [collapsed, setCollapsed] = useState(true);

  const [showField, setShowField] = useState(false);
  const isNewStudentWithoutCard =
    newRegistration && !(formState.cardNumber ?? "").trim();

  useEffect(() => {
    if (registerType === "REGISTRATION") {
      setShowField(formState.studentRecordId !== "");
    } else {
      setShowField(true);
    }
  }, [formState.studentRecordId, registerType]);

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

      if (key === "selectNumber") {
        setStudentLookupError(null);
      }
    },
    [setFormState]
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
      setFormState((previous: StudentFormState) => ({
        ...previous,
        studentRecordId: student.id
          ? String(student.id)
          : previous.studentRecordId,
        studentId:
          student.num_select ??
          (student.id ? String(student.id) : previous.studentId),
        cardNumber: student.num_carte ?? previous.cardNumber,
        selectNumber: student.num_select ?? previous.selectNumber,
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
        baccakaureateYear:
          student.year_of_baccalaureate ?? previous.baccalaureateYear,
        baccakaureateSerieId:
          student.id_baccalaureate_series ?? previous.baccalaureateSerieId,
        baccakaureateSerieLabel:
          student.baccalaureate_serie?.name ?? previous.baccakaureateSerieLabel,
        nationalityLabel:
          student.nationality?.name ?? previous.nationalityLabel,
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
        generatedLevel: student.generated_level ?? previous.generatedLevel,
        enrollmentStatus:
          student.enrollment_status ?? previous.enrollmentStatus,
        motherName: student.mother_name ?? previous.motherName,
        fatherName: student.father_name ?? previous.fatherName,
        motherJob: student.mother_job ?? previous.motherJob,
        fatherJob: student.father_job ?? previous.fatherJob,
        parentAdress: student.parent_address ?? previous.parentAdress
      }));
      setStudentLookupError(null);
    },
    [setFormState]
  );

  const handleStudentLookup = useCallback(
    async (force = false) => {
      const trimmed = newRegistration
        ? formState.selectNumber?.trim()
        : formState.cardNumber?.trim();
      if (!trimmed) {
        const message = !newRegistration
          ? "Veuillez saisir un numéro de carte."
          : "Veuillez saisir un numéro de sélection.";
        setStudentLookupError(message);
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
        console.log(newRegistration);

        const profile = await fetchStudentByCardNumber(
          filters,
          registerType,
          trimmed,
          newRegistration
        );
        const student = (profile as any).data ?? profile;

        setShowField(student.id !== undefined);
        const rawAnnual = Array.isArray(student.annual_register)
          ? student.annual_register
          : [];
        const normalizedAnnual = rawAnnual
          .map((entry: any) => {
            const payment = entry?.payment ?? entry?.payments ?? [];
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
    [
      formState.cardNumber,
      formState.selectNumber,
      populateStudentFields,
      filters,
      registerType,
      newRegistration
    ]
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

    const trimmed = formState.cardNumber?.trim();
    if (!trimmed) {
      return;
    }

    if (enableLookup) {
      void handleStudentLookup(false);
    }
  }, [dialogMode, enableLookup, formState.cardNumber, handleStudentLookup]);

  useEffect(() => {
    if (!onRegistrationStatusChange) return;
    const hasRegistration = annualRegister.some(
      (entry) =>
        Array.isArray(entry.register_semester) &&
        entry.register_semester.length > 0
    );
    onRegistrationStatusChange(hasRegistration);
  }, [annualRegister, onRegistrationStatusChange]);

  return (
    <div className="flex-1 overflow-y-auto px-6 py-4 min-h-0 overflow-y-hide">
      <div className="space-y-4">
        {formError && (
          <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-2 text-sm text-destructive">
            {formError}
          </div>
        )}
        <div className="space-y-6">
          {registerType === "REGISTRATION" && (
            <div
              className={`flex ${showField ? "justify-center" : "justify-between"} gap-4`}
            >
              <div className="rounded-xl border bg-card/80 p-5 shadow-sm space-y-5  w-[80%]">
                {enableLookup && (
                  <div className="space-y-2">
                    {newRegistration ? (
                      <>
                        <label className="text-sm font-medium text-foreground">
                          Numéro de dossier étudiant
                        </label>
                        <div className="flex flex-col gap-2 sm:flex-row">
                          <Input
                            value={formState.selectNumber}
                            onChange={(event) =>
                              handleFormChange(
                                "selectNumber",
                                event.target.value
                              )
                            }
                            placeholder="Ex: SCT-000123"
                          />
                          <Button
                            type="button"
                            onClick={() => handleStudentLookup(true)}
                            disabled={
                              studentLookupLoading ||
                              !formState.selectNumber?.trim().length
                            }
                          >
                            {studentLookupLoading
                              ? "Recherche..."
                              : "Rechercher"}
                          </Button>
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Entrez le numéro pour charger automatiquement les
                          informations enregistrées dans la base.
                        </p>
                      </>
                    ) : (
                      <>
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
                              !formState.cardNumber?.trim().length
                            }
                          >
                            {studentLookupLoading
                              ? "Recherche..."
                              : "Rechercher"}
                          </Button>
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Entrez le numéro pour charger automatiquement les
                          informations enregistrées dans la base.
                        </p>
                      </>
                    )}
                    {studentLookupError && (
                      <p className="text-sm text-destructive">
                        {studentLookupError}
                      </p>
                    )}
                  </div>
                )}
              </div>

              {showField && (
                <div className="flex justify-center w-[20%]">
                  {enablePicture && (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between gap-2"></div>
                      <div className="flex items-center gap-4">
                        <div className="relative h-36 w-36">
                          {picturePreview || formState.picture ? (
                            <img
                              src={
                                picturePreview ??
                                resolveAssetUrl(formState.picture)
                              }
                              alt="Photo étudiant"
                              className="h-36 w-36 rounded-full border object-cover"
                            />
                          ) : (
                            <div className="h-36 w-36 rounded-full border bg-muted/20" />
                          )}
                          <label
                            htmlFor={pictureInputId}
                            className={`absolute -bottom-0 -right-0 inline-flex h-8 w-8 items-center justify-center rounded-full border bg-background shadow-sm ${
                              disabledEditing
                                ? "cursor-not-allowed opacity-50"
                                : "hover:bg-muted/50 cursor-pointer"
                            }`}
                          >
                            <Pencil className="h-4 w-4" />
                          </label>
                          <input
                            id={pictureInputId}
                            type="file"
                            accept="image/*"
                            onChange={handlePictureUpload}
                            className="hidden"
                            disabled={disabledEditing}
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
          {showField && (
            <div className="grid gap-4 sm:grid-cols-1 lg:grid-cols-2">
              <div className="space-y-4">
                <StudentFormItem
                  name={"Informations personnelles"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={inputPersonal}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />

                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-2">
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
                          {effectiveMentionOptions.map(
                            (mention: MentionOption) => (
                              <SelectItem
                                key={mention.id}
                                value={mention.id.toString()}
                                className="text-upper"
                              >
                                {mention.label}
                              </SelectItem>
                            )
                          )}
                        </SelectContent>
                      </Select>
                    </div>
                  )}
                  <div className="space-y-3 rounded-xl border bg-muted/20 p-5">
                    <div className="flex items-center gap-2">
                      <Layers className="h-4 w-4 text-muted-foreground" />
                      <label className="text-sm font-medium">Niveau</label>
                    </div>
                    <Select
                      value={
                        registerType === "REGISTRATION"
                          ? !newRegistration
                            ? formState.generatedLevel
                            : formState.level
                          : formState.level
                      }
                      onValueChange={(value) =>
                        handleFormChange("level", value)
                      }
                      disabled={registerType === "REGISTRATION"}
                    >
                      <SelectTrigger className="h-11">
                        <SelectValue placeholder="Sélectionner le niveau" />
                      </SelectTrigger>
                      <SelectContent>
                        {levelOptions.map((level: string) => (
                          <SelectItem key={level} value={level}>
                            {level}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
              <div className="space-y-4 rounded-xl border bg-muted/20">
                {(annualRegisterDisabled || isNewStudentWithoutCard) && (
                  <div className="rounded-md border border-amber-200 bg-amber-50 px-4 py-2 text-sm text-amber-800">
                    {annualRegisterDisabledMessage ??
                      "Veuillez d'abord attribuer un numéro de carte avant de compléter la scolarité."}
                  </div>
                )}
                <ReinscriptionAnnualRegister
                  annualRegister={annualRegister}
                  editingSections={editingSections}
                  cardNumber={
                    registerType === "SELECTION"
                      ? formState.studentId || formState.cardNumber
                      : formState.cardNumber
                  }
                  filters={filters}
                  defaultMentionId={formState.mentionId}
                  disabledEditing={
                    disabledEditing ||
                    annualRegisterDisabled ||
                    isNewStudentWithoutCard
                  }
                  registerType={registerType}
                  onRegistrationStatusChange={onRegistrationStatusChange}
                />
              </div>
            </div>
          )}
          {showField && (
            <div className="flex justify-end">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setCollapsed(!collapsed)}
                className="gap-2"
              >
                {collapsed ? (
                  <>
                    <Eye className="h-4 w-4" />
                    Voir plus d'informations
                  </>
                ) : (
                  <>
                    <EyeOff className="h-4 w-4" />
                    Voir moins informations
                  </>
                )}
              </Button>
            </div>
          )}
          {!collapsed && (
            <>
              <div className="grid gap-6 lg:grid-cols-2">
                <StudentFormItem
                  name={"Informations sur le baccalauréat et Téléphone"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={studentInformationBaccalaureate}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />

                <StudentFormItem
                  name={"Statut social"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={studentInformationSocial}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />
              </div>

              <div className="grid gap-6 lg:grid-cols-2">
                <StudentFormItem
                  name={"Statut d'inscription et Adresse"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={studentInformationRegistration}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />

                <StudentFormItem
                  name={"Informations sur les parents"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={inputFather}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />
              </div>

              <div className="grid gap-6 lg:grid-cols-2">
                <StudentFormItem
                  name={"Informations sur la naissance et Proféssion"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={inputBirth}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />

                <StudentFormItem
                  name={"Carte d'identité"}
                  editingSections={editingSections}
                  setEditingSections={setEditingSections}
                  handleFormChange={handleFormChange}
                  formState={formState}
                  inputComponent={inputIdentity}
                  classnNames="grid gap-4 sm:grid-cols-2"
                  disabledEditing={disabledEditing}
                />
              </div>
              <div className="grid gap-6 lg:grid-cols-2"></div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
