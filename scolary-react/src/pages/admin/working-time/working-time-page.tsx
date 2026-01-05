import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  Calendar as CalendarIcon,
  Clock,
  Eye,
  EyeOff,
  Filter,
  Layers,
  MapPin,
  Pencil,
  Plus,
  Trash2,
  User
} from "lucide-react";
import { useForm } from "react-hook-form";

import {
  AcademicFilters,
  JourneyOption
} from "@/components/filters/academic-filters";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useLookupOptions } from "@/hooks/use-lookup-options";
import { fetchJourneys as fetchJourneysByMention } from "@/services/inscription-service";
import { fetchClassrooms } from "@/services/classroom-service";
import { fetchGroups } from "@/services/group-service";
import { fetchConstituentElementOfferings } from "@/services/constituent-element-offering-service";
import {
  fetchWorkingTimes,
  useCreateWorkingTime,
  useDeleteWorkingTime,
  useUpdateWorkingTime
} from "@/services/working-time-service";
import {
  useExamDates,
  useCreateExamDate,
  useUpdateExamDate,
  useDeleteExamDate
} from "@/services/exam-date-service";
import { ExamDate } from "@/models/exam-date";
import {
  WorkingSessionType,
  WorkingTime,
  WorkingTimePayload,
  WorkingTimeType
} from "@/models/working-time";
import { ConstituentElementOffering } from "@/models/constituent-element-offering";
import { Classroom } from "@/models/classroom";
import { Group } from "@/models/group";

type WorkingTimeFilters = {
  id_year: string;
  id_mention: string;
  id_journey: string;
  semester: string;
};

type WorkingTimeFormValues = {
  id_constituent_element_offering: string;
  id_classroom: string;
  id_group: string;
  working_time_type: WorkingTimeType;
  session: WorkingSessionType;
  day: string;
  date: string;
  start: string;
  end: string;
};

type ExamDateFormValues = {
  id_academic_year: string;
  date_from: string;
  date_to: string;
  session: WorkingSessionType;
};

type Feedback = { type: "success" | "error"; text: string };

const semesters = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"];

// Facile à déplacer dans des paramètres/écran de configuration au besoin.
const scheduleConfig = {
  startMinutes: 7 * 60,
  endMinutes: 18 * 60,
  workingDays: ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
};

const minutesToTime = (value: number) =>
  `${String(Math.floor(value / 60)).padStart(2, "0")}:${String(value % 60).padStart(2, "0")}`;

const defaultStartTime = minutesToTime(scheduleConfig.startMinutes);
const defaultEndTime = minutesToTime(scheduleConfig.startMinutes + 120);
const minWorkingTime = minutesToTime(scheduleConfig.startMinutes);
const maxWorkingTime = minutesToTime(scheduleConfig.endMinutes);
const emptySelectValue = "__none__";

const daysOfWeek = scheduleConfig.workingDays;

const dayAliases: Record<string, string> = {
  mon: "Lundi",
  monday: "Lundi",
  lundi: "Lundi",
  tue: "Mardi",
  tuesday: "Mardi",
  mardi: "Mardi",
  wed: "Mercredi",
  wednesday: "Mercredi",
  mercredi: "Mercredi",
  thu: "Jeudi",
  thursday: "Jeudi",
  jeudi: "Jeudi",
  fri: "Vendredi",
  friday: "Vendredi",
  vendredi: "Vendredi",
  sat: "Samedi",
  saturday: "Samedi",
  samedi: "Samedi",
  sun: "Dimanche",
  sunday: "Dimanche",
  dimanche: "Dimanche"
};

const workingTypeOptions: { value: string; label: string }[] = [
  { value: "cours", label: "Cours" },
  { value: "tp", label: "Travaux pratiques" },
  { value: "td", label: "Travaux dirigés" },
  { value: "exam", label: "Examen" }
];
const workingTypeTabs = workingTypeOptions;
const workingTypeValueOptions = {
  cours: "Cours",
  tp: "Travaux pratiques",
  td: "Travaux dirigés",
  exam: "Examen"
};

const sessionOptions: { value: WorkingSessionType; label: string }[] = [
  { value: "Normal", label: "Session normale" },
  { value: "Rattrapage", label: "Rattrapage" }
];

const defaultFormValues: WorkingTimeFormValues = {
  id_constituent_element_offering: "",
  id_classroom: "",
  id_group: "",
  working_time_type: "cours",
  session: "Normal",
  day: "Lundi",
  date: "",
  start: defaultStartTime,
  end: defaultEndTime
};

const getDayFromDate = (value?: string | null) => {
  if (!value) return null;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;
  const index = parsed.getDay();
  const mapping = [
    "Dimanche",
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi"
  ];
  return mapping[index] ?? null;
};

const normalizeDay = (day?: string | null, date?: string | null) => {
  if (date) {
    const fromDate = getDayFromDate(date);
    if (fromDate) {
      return fromDate;
    }
  }

  if (!day) return null;
  const normalized = dayAliases[day.trim().toLowerCase()];
  if (normalized) return normalized;
  const direct = daysOfWeek.find(
    (entry) => entry.toLowerCase() === day.trim().toLowerCase()
  );
  return direct ?? null;
};

const normalizeWorkingTypeValue = (value?: string | null): WorkingTimeType =>
  value && ["cours", "tp", "td", "exam"].includes(value.toLowerCase())
    ? (value.toLowerCase() as WorkingTimeType)
    : ("cours" as WorkingTimeType);

const toApiWorkingTypeKey = (value?: string | null) => {
  const normalized = normalizeWorkingTypeValue(value);
  const mapping: Record<WorkingTimeType, string> = {
    cours: "COURSE",
    tp: "TP",
    td: "TD",
    exam: "EXAM"
  };
  return mapping[normalized] ?? "COURSE";
};

const timeToMinutes = (value?: string | null) => {
  if (!value) return null;
  const [hours, minutes] = value.split(":").map(Number);
  if (Number.isNaN(hours) || Number.isNaN(minutes)) return null;
  return hours * 60 + minutes;
};

const formatTime = (value?: string | null) => {
  if (!value) return "—";
  const [hours, minutes] = value.split(":");
  if (!hours || minutes === undefined) return value;
  return `${hours.padStart(2, "0")}:${minutes.padStart(2, "0")}`;
};

const formatDateLabel = (value?: string | null) => {
  if (!value) return "";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleDateString();
};

const toFormValues = (
  workingTime?: WorkingTime | null
): WorkingTimeFormValues => ({
  id_constituent_element_offering: workingTime?.id_constituent_element_offering
    ? String(workingTime.id_constituent_element_offering)
    : "",
  id_classroom: workingTime?.id_classroom
    ? String(workingTime.id_classroom)
    : "",
  id_group: workingTime?.id_group ? String(workingTime.id_group) : "",
  working_time_type: normalizeWorkingTypeValue(workingTime?.working_time_type),
  session: workingTime?.session ?? "Normal",
  day: normalizeDay(workingTime?.day, workingTime?.date) ?? "Lundi",
  date: workingTime?.date ? workingTime.date.split("T")[0] : "",
  start: workingTime?.start ?? "08:00",
  end: workingTime?.end ?? "10:00"
});

const toPayload = (values: WorkingTimeFormValues): WorkingTimePayload => ({
  id_constituent_element_offering: Number(
    values.id_constituent_element_offering
  ),
  id_classroom: values.id_classroom ? Number(values.id_classroom) : undefined,
  id_group: values.id_group ? Number(values.id_group) : undefined,
  working_time_type: values.working_time_type,
  session: values.session,
  day: values.day || undefined,
  start: values.start,
  end: values.end,
  date: values.date ? new Date(values.date).toISOString() : undefined
});

interface WorkingTimeFormProps {
  mode: "create" | "edit";
  initialValues?: WorkingTimeFormValues;
  isSubmitting: boolean;
  offerings: ConstituentElementOffering[];
  classrooms: Classroom[];
  groups: Group[];
  onSubmit: (values: WorkingTimeFormValues) => Promise<void>;
  onCancel: () => void;
  fixedWorkingType: WorkingTimeType;
  examDateRanges?: Record<WorkingSessionType, { from: string; to: string } | null>;
  contextLabels: {
    journey: string;
    semester: string;
    year: string;
  };
}

const WorkingTimeForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  offerings,
  classrooms,
  groups,
  fixedWorkingType,
  examDateRanges,
  contextLabels
}: WorkingTimeFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    reset,
    setValue
  } = useForm<WorkingTimeFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  const dateValue = watch("date");
  const selectedOffering = watch("id_constituent_element_offering");
  const workingType = watch("working_time_type");
  const selectedSession = watch("session");
  const isExam = workingType === "exam";
  const activeExamRange =
    isExam && examDateRanges ? examDateRanges[selectedSession] ?? null : null;

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  useEffect(() => {
    if (!dateValue) return;
    const derived = getDayFromDate(dateValue);
    if (derived) {
      setValue("day", derived);
    }
  }, [dateValue, setValue]);

  useEffect(() => {
    if (selectedOffering) return;
    const first = offerings[0];
    if (first?.id) {
      setValue("id_constituent_element_offering", String(first.id));
    }
  }, [offerings, selectedOffering, setValue]);

  useEffect(() => {
    setValue("working_time_type", fixedWorkingType);
  }, [fixedWorkingType, setValue]);

  useEffect(() => {
    if (isExam) {
      setValue("id_classroom", "");
      setValue("id_group", "");
      setValue("day", "");
    } else {
      setValue("date", "");
      setValue("session", "Normal");
    }
  }, [isExam, setValue]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="rounded-md border bg-muted p-3 text-xs text-muted-foreground space-y-1">
        <div>
          Type de séance :{" "}
          {workingTypeValueOptions[workingType as keyof typeof workingTypeValueOptions] ??
            "—"}
        </div>
        <div>Parcours : {contextLabels.journey}</div>
        <div>Semestre : {contextLabels.semester}</div>
        <div>Année : {contextLabels.year}</div>
        {isExam && activeExamRange ? (
          <div>
            Plage d&apos;examen : {activeExamRange.from} → {activeExamRange.to}
          </div>
        ) : null}
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="working-time-offering">
          Élément constitutif
        </label>
        <Select
          value={watch("id_constituent_element_offering")}
          onValueChange={(value) =>
            setValue("id_constituent_element_offering", value)
          }
        >
          <SelectTrigger
            id="working-time-offering"
            className={cn(
              "h-11",
              errors.id_constituent_element_offering &&
                "border-destructive text-destructive"
            )}
          >
            <SelectValue placeholder="Select element" />
          </SelectTrigger>
          <SelectContent>
            {offerings.length ? (
              offerings.map((offering) => {
                const ce = offering.constituent_element;
                const name = ce?.name ?? "Element";
                const journey =
                  ce?.journey?.name ?? ce?.journey?.abbreviation ?? "Journey";
                const sem = ce?.semester ?? "";
                const year = offering?.academic_year?.name ?? "";
                return (
                  <SelectItem key={offering.id} value={String(offering.id)}>
                    {name} · {journey} · {sem}
                    {year ? ` · ${year}` : ""}
                  </SelectItem>
                );
              })
            ) : (
              <SelectItem value="__no_option" disabled>
                Aucun élément constitutif disponible pour ces filtres
              </SelectItem>
            )}
          </SelectContent>
        </Select>
        {errors.id_constituent_element_offering ? (
          <p className="text-xs text-destructive">
            {errors.id_constituent_element_offering.message}
          </p>
        ) : null}
      </div>

      {isExam ? (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="working-time-date">
              Date
            </label>
            <Input
              id="working-time-date"
              type="date"
              min={activeExamRange?.from}
              max={activeExamRange?.to}
              className={cn(
                errors.date && "border-destructive text-destructive"
              )}
              {...register("date", {
                validate: (val) =>
                  isExam
                    ? (() => {
                        if (!val?.trim()) {
                          return "La date est requise pour un examen";
                        }
                        if (!activeExamRange) {
                          return "Veuillez d'abord configurer une plage de dates d'examen";
                        }
                        if (val < activeExamRange.from) {
                          return `La date doit être après le ${activeExamRange.from}`;
                        }
                        if (val > activeExamRange.to) {
                          return `La date doit être avant le ${activeExamRange.to}`;
                        }
                        return true;
                      })()
                    : true
              })}
            />
            {errors.date ? (
              <p className="text-xs text-destructive">
                {errors.date.message as string}
              </p>
            ) : null}
          </div>
          <div className="space-y-2">
            <label
              className="text-sm font-medium"
              htmlFor="working-time-session"
            >
              Session
            </label>
            <Select
              value={watch("session")}
              onValueChange={(value: WorkingSessionType) =>
                setValue("session", value)
              }
            >
              <SelectTrigger id="working-time-session" className="h-11">
                <SelectValue placeholder="Select session" />
              </SelectTrigger>
              <SelectContent>
                {sessionOptions.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="working-time-day">
              Jour de la semaine
            </label>
            <Select
              value={watch("day")}
              onValueChange={(value) => setValue("day", value)}
            >
              <SelectTrigger id="working-time-day" className="h-11">
                <SelectValue placeholder="Choisir un jour" />
              </SelectTrigger>
              <SelectContent>
                {daysOfWeek.map((day) => (
                  <SelectItem key={day} value={day}>
                    {day}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="working-time-start">
            Heure de début
          </label>
          <Input
            id="working-time-start"
            type="time"
            min={minWorkingTime}
            max={maxWorkingTime}
            className={cn(
              errors.start && "border-destructive text-destructive"
            )}
            {...register("start", { required: "Start time is required" })}
          />
          {errors.start ? (
            <p className="text-xs text-destructive">{errors.start.message}</p>
          ) : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="working-time-end">
            Heure de fin
          </label>
          <Input
            id="working-time-end"
            type="time"
            min={minWorkingTime}
            max={maxWorkingTime}
            className={cn(errors.end && "border-destructive text-destructive")}
            {...register("end", { required: "End time is required" })}
          />
          {errors.end ? (
            <p className="text-xs text-destructive">{errors.end.message}</p>
          ) : null}
        </div>
      </div>

      {!isExam ? (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="working-time-room">
              Salle (optionnel)
            </label>
            <Select
              value={watch("id_classroom") || emptySelectValue}
              onValueChange={(value) =>
                setValue(
                  "id_classroom",
                  value === emptySelectValue ? "" : value
                )
              }
            >
              <SelectTrigger id="working-time-room" className="h-11">
                <SelectValue placeholder="Assigner une salle" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={emptySelectValue}>Pas de salle</SelectItem>
                {classrooms.map((room) => (
                  <SelectItem key={room.id} value={String(room.id)}>
                    {room.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="working-time-group">
              Groupe (optionnel)
            </label>
            <Select
              value={watch("id_group") || emptySelectValue}
              onValueChange={(value) =>
                setValue("id_group", value === emptySelectValue ? "" : value)
              }
            >
              <SelectTrigger id="working-time-group" className="h-11">
                <SelectValue placeholder="Associer un groupe" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={emptySelectValue}>Pas de groupe</SelectItem>
                {groups.map((group) => (
                  <SelectItem key={group.id} value={String(group.id)}>
                    {group.group_number
                      ? `Group ${group.group_number}`
                      : `Group ${group.id}`}
                    {group.semester ? ` · ${group.semester}` : ""}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      ) : null}

      <div className="flex items-center justify-end gap-2">
        <Button
          type="button"
          variant="ghost"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Annuler
        </Button>
        <Button type="submit" disabled={isSubmitting || !offerings.length}>
          {isSubmitting
            ? "Enregistrement…"
            : mode === "edit"
              ? "Enregistrer les modifications"
              : "Créer l'horaire"}
        </Button>
      </div>
    </form>
  );
};

export const WorkingTimePage = () => {
  const defaultSemester = semesters[0];
  const STORAGE_KEY = "working-time.filters";

  const createWorkingTime = useCreateWorkingTime();
  const updateWorkingTime = useUpdateWorkingTime();
  const deleteWorkingTime = useDeleteWorkingTime();
  const createExamDate = useCreateExamDate();
  const updateExamDate = useUpdateExamDate();
  const deleteExamDate = useDeleteExamDate();

  const { mentionOptions, academicYearOptions } = useLookupOptions({
    includeMentions: true,
    includeAcademicYears: true
  });

  const resolveHeaderAcademicYear = () => {
    if (typeof window === "undefined") return "";
    const stored = window.localStorage.getItem("selected_academic_year");
    if (!stored || stored === "all") return "";
    return stored;
  };

  const readStoredFilters = (): WorkingTimeFilters | null => {
    if (typeof window === "undefined") return null;
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    try {
      const parsed = JSON.parse(raw);
      if (
        parsed &&
        typeof parsed === "object" &&
        "id_mention" in parsed &&
        "id_journey" in parsed &&
        "semester" in parsed &&
        "id_year" in parsed
      ) {
        return parsed as WorkingTimeFilters;
      }
    } catch {
      return null;
    }
    return null;
  };

  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [filters, setFilters] = useState<WorkingTimeFilters>(() => {
    const stored = readStoredFilters();
    return (
      stored ?? {
        id_year: resolveHeaderAcademicYear(),
        id_mention: "",
        id_journey: "",
        semester: defaultSemester
      }
    );
  });

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editing, setEditing] = useState<WorkingTime | null>(null);
  const [workingTimeToDelete, setWorkingTimeToDelete] =
    useState<WorkingTime | null>(null);
  const [isExamDateOpen, setIsExamDateOpen] = useState(false);
  const [editingExamDate, setEditingExamDate] = useState<ExamDate | null>(
    null
  );
  const [examDateToDelete, setExamDateToDelete] = useState<ExamDate | null>(
    null
  );

  const journeyQuery = useQuery({
    queryKey: ["working-time", "journeys", filters.id_mention],
    queryFn: () => fetchJourneysByMention(Number(filters.id_mention)),
    enabled: Boolean(filters.id_mention)
  });

  const availableJourneys = useMemo(
    () =>
      (journeyQuery.data ?? []).map((journey: any) => ({
        id: String(journey.id),
        label: journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
        id_mention:
          journey.id_mention !== undefined
            ? String(journey.id_mention)
            : String(filters.id_mention),
        semesterList: Array.isArray(journey.semester_list)
          ? journey.semester_list
              .map((entry: any) =>
                typeof entry === "string"
                  ? entry
                  : (entry?.semester ?? entry?.semester_list ?? null)
              )
              .filter((sem: any): sem is string => Boolean(sem))
          : []
      })),
    [journeyQuery.data, filters.id_mention]
  );

  const allowedSemestersForJourney = useCallback(
    (journeyId?: string) => {
      const journey = availableJourneys.find((j) => j.id === journeyId);
      if (
        journey &&
        Array.isArray((journey as any).semesterList) &&
        (journey as any).semesterList.length
      ) {
        return (journey as any).semesterList as string[];
      }
      return semesters;
    },
    [availableJourneys]
  );

  useEffect(() => {
    if (!mentionOptions.length) return;
    setFilters((prev) => {
      const nextMention = prev.id_mention || mentionOptions[0].id;
      return { ...prev, id_mention: nextMention };
    });
  }, [mentionOptions]);

  useEffect(() => {
    const nextYear = resolveHeaderAcademicYear();
    setFilters((prev) => ({
      ...prev,
      id_year: nextYear
    }));
    const handleYearChange = (event: any) => {
      const detail = event?.detail;
      setFilters((prev) => ({
        ...prev,
        id_year: detail && detail !== "all" ? detail : ""
      }));
      if (typeof window !== "undefined") {
        window.localStorage.setItem(
          "selected_academic_year",
          detail && detail !== "all" ? detail : ""
        );
      }
    };
    const syncFromStorage = () => {
      setFilters((prev) => ({ ...prev, id_year: resolveHeaderAcademicYear() }));
    };
    if (typeof window !== "undefined") {
      window.addEventListener("academicYearChanged", handleYearChange as any);
      window.addEventListener("storage", syncFromStorage);
    }
    return () => {
      if (typeof window !== "undefined") {
        window.removeEventListener(
          "academicYearChanged",
          handleYearChange as any
        );
        window.removeEventListener("storage", syncFromStorage);
      }
    };
  }, []);

  useEffect(() => {
    const firstJourney = availableJourneys[0];
    if (!firstJourney) return;
    setFilters((prev) => {
      if (prev.id_journey) return prev;
      const nextSemester =
        allowedSemestersForJourney(firstJourney.id)[0] ??
        prev.semester ??
        defaultSemester;
      return {
        ...prev,
        id_journey: firstJourney.id,
        semester: semesters.includes(nextSemester)
          ? nextSemester
          : defaultSemester
      };
    });
  }, [availableJourneys, allowedSemestersForJourney, defaultSemester]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
  }, [filters]);

  const readStoredWorkingType = () => {
    if (typeof window === "undefined") return "cours" as WorkingTimeType;
    const stored = window.localStorage.getItem("working-time.calendarType");
    return normalizeWorkingTypeValue(stored);
  };

  const [calendarType, setCalendarType] =
    useState<WorkingTimeType>(readStoredWorkingType);

  const workingTimeQuery = useQuery({
    queryKey: ["working-times", { filters, calendarType }],
    queryFn: () => {
      const wheres: Array<Record<string, any>> = [];

      const offeringKeys: Array<string> = [];
      const offeringOps: Array<string> = [];
      const offeringVals: Array<string | number> = [];
      // Aggrege les filtres enfant côté API comme attendu (clé unique + opérateurs/valeurs concaténés).
      if (filters.id_year) {
        offeringKeys.push("constituent_element_offering.id_academic_year");
        offeringOps.push("==");
        offeringVals.push(Number(filters.id_year));
      }
      if (filters.id_mention) {
        offeringKeys.push(
          "constituent_element_offering.constituent_element.journey.id_mention"
        );
        offeringOps.push("==");
        offeringVals.push(Number(filters.id_mention));
      }
      if (filters.id_journey) {
        offeringKeys.push(
          "constituent_element_offering.constituent_element.id_journey"
        );
        offeringOps.push("==");
        offeringVals.push(Number(filters.id_journey));
      }
      if (filters.semester) {
        offeringKeys.push(
          "constituent_element_offering.constituent_element.semester"
        );
        offeringOps.push("==");
        offeringVals.push(filters.semester);
      }
      if (offeringKeys.length) {
        const trimmedKeys = offeringKeys.map((k) =>
          k.replace("constituent_element_offering.", "")
        );
        wheres.push({
          key: `constituent_element_offering.[${trimmedKeys.join(",")}]`,
          operator: offeringOps.join(","),
          value: offeringVals.join(",")
        });
      }
      if (calendarType) {
        wheres.push({
          key: "working_time_type",
          operator: "==",
          value: toApiWorkingTypeKey(calendarType)
        });
      }

      return fetchWorkingTimes({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "constituent_element_offering.academic_year{id,name}",
          "constituent_element_offering.constituent_element{id,name,semester,color,id_journey}",
          "constituent_element_offering{id,id_academic_year,id_teching_unit_offering,id_constituent_element,id_teacher,id_constituent_element_optional_group,weight}",
          "classroom{id,name,capacity}",
          "constituent_element_offering.teacher{id,grade,id_user}",
          "constituent_element_offering.teacher.user{id,first_name,last_name}",
          "group{id,group_number,semester,id_journey}",
          "group.journey{id,id_mention,name,abbreviation}"
        ]),
        limit: 400
      });
    }
  });

  const offeringsQuery = useQuery({
    queryKey: ["working-time", "offerings", filters],
    queryFn: () => {
      const wheres: Array<Record<string, any>> = [];
      if (filters.id_year) {
        wheres.push({
          key: "id_academic_year",
          operator: "==",
          value: Number(filters.id_year)
        });
      }
      if (filters.id_mention) {
        wheres.push({
          key: "constituent_element.journey.id_mention",
          operator: "==",
          value: Number(filters.id_mention)
        });
      }
      if (filters.id_journey) {
        wheres.push({
          key: "constituent_element.id_journey",
          operator: "==",
          value: Number(filters.id_journey)
        });
      }
      if (filters.semester) {
        wheres.push({
          key: "constituent_element.semester",
          operator: "==",
          value: filters.semester
        });
      }

      return fetchConstituentElementOfferings({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "constituent_element{id,name,semester,color,id_journey}",
          "academic_year{id,name}",
          "constituent_element.journey{id,id_mention,name,abbreviation}"
        ]),
        limit: 400
      });
    },
    enabled: Boolean(filters.id_mention && filters.id_year)
  });

  const classroomsQuery = useQuery({
    queryKey: ["working-time", "classrooms"],
    queryFn: () => fetchClassrooms({ limit: 200 })
  });

  const groupsQuery = useQuery({
    queryKey: ["working-time", "groups", filters.id_journey, filters.semester],
    queryFn: () => {
      const wheres: Array<Record<string, any>> = [];
      if (filters.id_journey) {
        wheres.push({
          key: "id_journey",
          operator: "==",
          value: Number(filters.id_journey)
        });
      }
      if (filters.semester) {
        wheres.push({
          key: "semester",
          operator: "==",
          value: filters.semester
        });
      }
      return fetchGroups({
        where: JSON.stringify(wheres),
        limit: 200
      });
    },
    enabled: Boolean(filters.id_journey)
  });

  const examDateDefaultValues = useMemo<ExamDateFormValues>(
    () => ({
      id_academic_year: filters.id_year || "",
      date_from: "",
      date_to: "",
      session: "Normal"
    }),
    [filters.id_year]
  );

  const todayDateString = useMemo(
    () => new Date().toISOString().split("T")[0],
    []
  );

  const {
    register: registerExamDate,
    handleSubmit: handleSubmitExamDate,
    reset: resetExamDate,
    formState: { errors: examDateErrors },
    watch: watchExamDate,
    setValue: setExamDateValue
  } = useForm<ExamDateFormValues>({
    defaultValues: examDateDefaultValues
  });

  useEffect(() => {
    registerExamDate("session");
  }, [registerExamDate]);

  const examDateToFormValues = useCallback(
    (examDate?: ExamDate | null): ExamDateFormValues => ({
      id_academic_year: examDate?.id_academic_year
        ? String(examDate.id_academic_year)
        : filters.id_year || "",
      date_from: examDate?.date_from
        ? examDate.date_from.split("T")[0]
        : "",
      date_to: examDate?.date_to ? examDate.date_to.split("T")[0] : "",
      session: (examDate?.session as WorkingSessionType) ?? "Normal"
    }),
    [filters.id_year]
  );

  const examDateQueryParams = useMemo(() => {
    const wheres: Array<Record<string, any>> = [];
    if (filters.id_year) {
      wheres.push({
        key: "id_academic_year",
        operator: "==",
        value: Number(filters.id_year)
      });
    }
    return {
      where: JSON.stringify(wheres),
      relation: JSON.stringify(["year{id,name}"]),
      limit: 200
    };
  }, [filters.id_year]);

  const examDatesQuery = useExamDates(examDateQueryParams);

  useEffect(() => {
    resetExamDate(
      editingExamDate
        ? examDateToFormValues(editingExamDate)
        : examDateDefaultValues
    );
  }, [
    editingExamDate,
    examDateDefaultValues,
    examDateToFormValues,
    resetExamDate
  ]);

  const offerings = offeringsQuery.data?.data ?? [];
  const classrooms = classroomsQuery.data?.data ?? [];
  const groups = groupsQuery.data?.data ?? [];
  const examDates = examDatesQuery.data?.data ?? [];
  const examDateLimitReached = (examDates?.length ?? 0) >= 2;
  const [filtersCollapsed, setFiltersCollapsed] = useState(false);
  const currentJourneyLabel =
    availableJourneys.find((journey) => journey.id === filters.id_journey)
      ?.label ?? "Parcours";
  const currentSemesterLabel = filters.semester || "Semestre";
  const currentYearLabel =
    academicYearOptions.find((year) => year.id === filters.id_year)?.label ??
    (filters.id_year ? `Année ${filters.id_year}` : "Année académique");

  const handleFiltersChange = useCallback((next: any) => {
    setFilters((prev) => ({
      ...prev,
      id_mention: next.id_mention,
      id_journey: next.id_journey,
      semester: next.semester
    }));
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem("working-time.calendarType", calendarType);
  }, [calendarType]);

  const openCreate = () => {
    setEditing(null);
    setIsFormOpen(true);
  };

  const closeForm = useCallback(() => {
    setEditing(null);
    setIsFormOpen(false);
  }, []);

  const closeExamDateModal = useCallback(() => {
    setEditingExamDate(null);
    setIsExamDateOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: WorkingTimeFormValues) => {
      try {
        if (editing) {
          await updateWorkingTime.mutateAsync({
            id: Number(editing.id),
            payload: toPayload(values)
          });
          setFeedback({
            type: "success",
            text: "Working time updated successfully."
          });
        } else {
          await createWorkingTime.mutateAsync(toPayload(values));
          setFeedback({
            type: "success",
            text: "Working time created successfully."
          });
        }
        await workingTimeQuery.refetch();
        closeForm();
      } catch (error) {
        const message =
          error instanceof Error
            ? error.message
            : "Unable to save working time.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createWorkingTime, editing, updateWorkingTime, workingTimeQuery]
  );

  const handleDelete = useCallback(async () => {
    if (!workingTimeToDelete) return;
    try {
      await deleteWorkingTime.mutateAsync(Number(workingTimeToDelete.id));
      await workingTimeQuery.refetch();
      setFeedback({
        type: "success",
        text: "Working time deleted successfully."
      });
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unable to delete working time.";
      setFeedback({ type: "error", text: message });
    } finally {
      setWorkingTimeToDelete(null);
    }
  }, [deleteWorkingTime, workingTimeQuery, workingTimeToDelete]);

  const handleExamDateSubmit = useCallback(
    async (values: ExamDateFormValues) => {
      try {
        const idYearValue = values.id_academic_year || filters.id_year;
        const payload: Partial<ExamDate> = {
          ...(idYearValue
            ? { id_academic_year: Number(idYearValue) }
            : {}),
          date_from: values.date_from || undefined,
          date_to: values.date_to || undefined,
          session: values.session
        };

        if (editingExamDate) {
          await updateExamDate.mutateAsync({
            id: Number(editingExamDate.id),
            payload
          });
          setFeedback({
            type: "success",
            text: "Date d'examen mise à jour."
          });
        } else {
          await createExamDate.mutateAsync(payload);
          setFeedback({
            type: "success",
            text: "Date d'examen créée."
          });
        }
        await examDatesQuery.refetch();
        closeExamDateModal();
      } catch (error) {
        const message =
          error instanceof Error
            ? error.message
            : "Impossible d'enregistrer la date d'examen.";
        setFeedback({ type: "error", text: message });
      }
    },
    [
      closeExamDateModal,
      createExamDate,
      editingExamDate,
      examDatesQuery,
      filters.id_year,
      updateExamDate
    ]
  );

  const handleDeleteExamDate = useCallback(async () => {
    if (!examDateToDelete) return;
    try {
      await deleteExamDate.mutateAsync(Number(examDateToDelete.id));
      await examDatesQuery.refetch();
      setFeedback({
        type: "success",
        text: "Date d'examen supprimée."
      });
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Impossible de supprimer la date d'examen.";
      setFeedback({ type: "error", text: message });
    } finally {
      setExamDateToDelete(null);
    }
  }, [deleteExamDate, examDateToDelete, examDatesQuery]);

  const computeRange = (
    entries: ExamDate[]
  ): { from: string; to: string } | null => {
    if (!entries.length) return null;
    const validDates = entries
      .map((entry) => ({
        from: entry.date_from ? new Date(entry.date_from) : null,
        to: entry.date_to ? new Date(entry.date_to) : null
      }))
      .filter((entry) => entry.from && !Number.isNaN(entry.from.getTime()));
    if (!validDates.length) return null;
    const minFrom = new Date(
      Math.min(...validDates.map((d) => (d.from as Date).getTime()))
    );
    const maxTo = new Date(
      Math.max(
        ...validDates
          .map((d) => d.to?.getTime() ?? d.from?.getTime() ?? 0)
          .filter(Boolean) as number[]
      )
    );
    if (Number.isNaN(minFrom.getTime()) || Number.isNaN(maxTo.getTime()))
      return null;
    const toISODate = (value: Date) => value.toISOString().split("T")[0];
    return {
      from: toISODate(minFrom),
      to: toISODate(maxTo)
    };
  };

  const examDateRanges = useMemo(() => {
    const bySession: Record<WorkingSessionType, { from: string; to: string } | null> = {
      Normal: null,
      Rattrapage: null
    };
    const normalEntries = examDates.filter(
      (d) => (d.session ?? "Normal") === "Normal"
    );
    const rattrapageEntries = examDates.filter(
      (d) => (d.session ?? "Normal") === "Rattrapage"
    );
    bySession.Normal = computeRange(normalEntries);
    bySession.Rattrapage = computeRange(rattrapageEntries);
    return bySession;
  }, [examDates]);

  const examDateRange = useMemo(() => {
    const ranges = Object.values(examDateRanges).filter(
      (r): r is { from: string; to: string } => Boolean(r)
    );
    if (!ranges.length) return null;
    const minFrom = ranges.reduce(
      (min, curr) => (curr.from < min ? curr.from : min),
      ranges[0].from
    );
    const maxTo = ranges.reduce(
      (max, curr) => (curr.to > max ? curr.to : max),
      ranges[0].to
    );
    return { from: minFrom, to: maxTo };
  }, [examDateRanges]);

  const filteredWorkingTimes = useMemo(() => {
    const list = workingTimeQuery.data?.data ?? [];
    if (calendarType === "exam" && examDateRange) {
      return list.filter((item) => {
        if (!item.date) return false;
        const dateOnly = item.date.split("T")[0];
        return dateOnly >= examDateRange.from && dateOnly <= examDateRange.to;
      });
    }
    return list;
  }, [calendarType, examDateRange, workingTimeQuery.data]);

  const workingTimes = filteredWorkingTimes;

  const eventsByDay = useMemo(() => {
    const acc: Record<string, WorkingTime[]> = {};
    for (const day of daysOfWeek) {
      acc[day] = [];
    }
    const list = filteredWorkingTimes;
    list.forEach((item) => {
      const day = normalizeDay(item.day, item.date);
      if (!day) return;
      acc[day] = [...(acc[day] ?? []), item];
    });
    for (const day of daysOfWeek) {
      acc[day] = (acc[day] ?? []).sort((a, b) => {
        const startA = timeToMinutes(a.start) ?? 0;
        const startB = timeToMinutes(b.start) ?? 0;
        return startA - startB;
      });
    }
    return acc;
  }, [filteredWorkingTimes]);

  const scheduleStart = scheduleConfig.startMinutes;
  const scheduleEnd = scheduleConfig.endMinutes;
  const scheduleRange = Math.max(scheduleEnd - scheduleStart, 1);
  const hoursMarkers = useMemo(() => {
    const markers: number[] = [];
    for (let minute = scheduleStart; minute <= scheduleEnd; minute += 60) {
      markers.push(minute);
    }
    return markers;
  }, [scheduleStart, scheduleEnd]);

  const isSubmitting =
    createWorkingTime.isPending || updateWorkingTime.isPending;
  const isExamDateSubmitting =
    createExamDate.isPending || updateExamDate.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Horaires de travail
          </h1>
          <p className="text-sm text-muted-foreground">
            Utilisez l&apos;année académique, la mention, le parcours et le
            semestre pour planifier les séances sur le calendrier.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            className="gap-2"
            onClick={() => setIsExamDateOpen(true)}
          >
            <CalendarIcon className="h-4 w-4" />
            Dates d&apos;examen
          </Button>
          <Button className="gap-2" onClick={openCreate}>
            <Plus className="h-4 w-4" />
            Ajouter un horaire
          </Button>
          <Button asChild variant="outline" className="gap-2">
            <Link to="/admin/offerings">
              <Layers className="h-4 w-4" />
              Gérer les offres EC/UE
            </Link>
          </Button>
        </div>
      </div>

      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3">
          {feedback ? (
            <div
              className={cn(
                "rounded-full border px-3 py-1 text-xs",
                feedback.type === "success"
                  ? "border-green-500 text-green-600"
                  : "border-destructive text-destructive"
              )}
            >
              {feedback.text}
            </div>
          ) : (
            <p className="text-xs text-muted-foreground">
              Ajustez les filtres académiques pour affiner le calendrier.
            </p>
          )}
          <Button
            variant="ghost"
            size="sm"
            className="gap-2"
            onClick={() => setFiltersCollapsed((prev) => !prev)}
          >
            <Filter className="h-4 w-4" />
            {filtersCollapsed ? (
              <>
                <Eye className="h-4 w-4" /> Afficher les filtres
              </>
            ) : (
              <>
                <EyeOff className="h-4 w-4" /> Masquer les filtres
              </>
            )}
          </Button>
        </div>

        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={availableJourneys}
          semesters={semesters}
          journeysLoading={journeyQuery.isFetching}
          showLevel={false}
          showResetButton={false}
          showActiveFilters={true}
          filterClassname="grid gap-4 lg:grid-cols-2"
          collapsed={filtersCollapsed}
          onCollapsedChange={setFiltersCollapsed}
        />
      </div>

      <div className="rounded-lg border bg-background p-5 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold">Calendrier</h2>
            <p className="text-xs text-muted-foreground">
              {workingTimes.length
                ? `Affichage de ${workingTimes.length} horaire${
                    workingTimes.length === 1 ? "" : "s"
                  }`
                : "Aucun horaire pour ces filtres"}
            </p>
          </div>
          <Tabs
            value={calendarType}
            onValueChange={(value) =>
              setCalendarType(normalizeWorkingTypeValue(value))
            }
          >
            <TabsList className="grid grid-cols-4 bg-muted">
              {workingTypeTabs.map((type) => (
                <TabsTrigger key={type.value} value={type.value}>
                  {type.label}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
          <Button variant="outline" className="gap-2" onClick={openCreate}>
            <Plus className="h-4 w-4" />
            Nouvel horaire
          </Button>
        </div>

        <div className="overflow-x-auto rounded-md border">
          <div className="min-w-[900px]">
            <div className={`grid grid-cols-${daysOfWeek.length} gap-2 p-2`}>
              {daysOfWeek.map((day) => (
                <div key={day} className="space-y-2">
                  <div className="flex items-center justify-between rounded-md bg-muted px-3 py-2">
                    <div className="flex items-center gap-2">
                      <CalendarIcon className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm font-medium">{day}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {eventsByDay[day]?.length
                        ? `${eventsByDay[day]?.length} séance${
                            (eventsByDay[day]?.length ?? 0) === 1 ? "" : "s"
                          }`
                        : "Aucune séance"}
                    </span>
                  </div>
                  <div className="relative h-[620px] rounded-lg border bg-muted/30 p-3">
                    {/* hour markers */}
                    {hoursMarkers.map((minute) => {
                      const top =
                        ((minute - scheduleStart) / scheduleRange) * 100;
                      return (
                        <div
                          key={minute}
                          className="absolute left-0 right-0 border-t border-dashed border-border text-[10px] text-muted-foreground"
                          style={{ top: `${top}%` }}
                        >
                          <span className="bg-muted/80 px-1">
                            {String(Math.floor(minute / 60)).padStart(2, "0")}
                            :00
                          </span>
                        </div>
                      );
                    })}

                    {(eventsByDay[day] ?? []).map((item) => {
                      const startMinutes =
                        timeToMinutes(item.start) ?? scheduleStart;
                      const endMinutes =
                        timeToMinutes(item.end) ??
                        Math.min(scheduleEnd, startMinutes + 90);
                      const start =
                        Math.max(startMinutes, scheduleStart) - scheduleStart;
                      const end =
                        Math.min(endMinutes, scheduleEnd) - scheduleStart;
                      const height = Math.max(
                        ((end - start) / scheduleRange) * 100,
                        6
                      );
                      const top = (start / scheduleRange) * 100;

                      const ce =
                        item.constituent_element_offering?.constituent_element;
                      const journey = ce?.journey;
                      const color = ce?.color || "var(--primary)";

                      return (
                        <div
                          key={item.id}
                          className="group absolute left-1 right-1 overflow-hidden rounded-md border bg-background shadow-sm"
                          style={{
                            top: `${top}%`,
                            height: `${height}%`,
                            borderColor: color
                          }}
                        >
                          <div
                            className="h-1 w-full"
                            style={{ backgroundColor: color }}
                          />
                          <div className="relative flex h-full flex-col gap-1 p-2">
                            <div className="flex flex-col">
                              <span className="text-xs font-semibold leading-tight w-full">
                                {ce?.name ?? "Constituent element"}
                              </span>
                            </div>
                            <div className="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity duration-150 group-hover:opacity-100">
                              <div className="flex items-center gap-2 rounded-full bg-background/85 px-2 py-1 shadow-md ring-1 ring-border pointer-events-auto">
                                <Button
                                  size="icon"
                                  variant="ghost"
                                  className="h-8 w-8"
                                  onClick={() => {
                                    setCalendarType(
                                      normalizeWorkingTypeValue(
                                        item.working_time_type
                                      )
                                    );
                                    setFilters((prev) => ({
                                      ...prev,
                                      id_journey: ce?.journey?.id
                                        ? String(ce.journey.id)
                                        : prev.id_journey,
                                      semester: ce?.semester || prev.semester,
                                      id_mention: ce?.journey?.id_mention
                                        ? String(ce.journey.id_mention)
                                        : prev.id_mention,
                                      id_year: item.constituent_element_offering
                                        ?.id_academic_year
                                        ? String(
                                            item.constituent_element_offering
                                              ?.id_academic_year
                                          )
                                        : prev.id_year
                                    }));
                                    setEditing(item);
                                    setIsFormOpen(true);
                                  }}
                                >
                                  <Pencil className="h-5 w-5" />
                                </Button>
                                <Button
                                  size="icon"
                                  variant="ghost"
                                  className="h-8 w-8 text-destructive"
                                  onClick={() => setWorkingTimeToDelete(item)}
                                >
                                  <Trash2 className="h-5 w-5" />
                                </Button>
                              </div>
                            </div>
                            <div className="flex items-center gap-2 text-[11px] text-muted-foreground">
                              <Clock className="h-3 w-3" />
                              <span>
                                {item.day ? `${item.day}, ` : ""}
                                {formatTime(item.start)} -{" "}
                                {formatTime(item.end)}
                              </span>
                            </div>
                            {item.classroom ? (
                              <div className="flex items-center gap-2 text-[11px] text-muted-foreground">
                                <MapPin className="h-3 w-3" />
                                <span>{item.classroom.name}</span>,
                                {item.constituent_element_offering?.teacher ? (
                                  <div className="flex items-center gap-2 text-[11px] text-muted-foreground">
                                    <User className="h-3 w-3" />
                                    <span>
                                      {" "}
                                      {
                                        item.constituent_element_offering
                                          .teacher.grade
                                      }{" "}
                                      {
                                        item.constituent_element_offering
                                          .teacher.user?.last_name
                                      }{" "}
                                      {
                                        item.constituent_element_offering
                                          .teacher.user?.first_name
                                      }
                                    </span>
                                  </div>
                                ) : null}
                              </div>
                            ) : null}

                            {/* <div className="flex flex-wrap items-center gap-2 text-[11px] text-muted-foreground">
                              <Layers className="h-3 w-3" />
                              <span className="rounded-full bg-muted px-2 py-0.5 text-[10px]">
                                {item.working_time_type}
                              </span>
                              {item.session ? (
                                <span className="rounded-full bg-muted px-2 py-0.5 text-[10px]">
                                  {item.session}
                                </span>
                              ) : null}
                              {item.date ? (
                                <span className="rounded-full bg-muted px-2 py-0.5 text-[10px]">
                                  {formatDateLabel(item.date)}
                                </span>
                              ) : null}
                            </div> */}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="sm:max-w-3xl">
          <DialogHeader>
            <DialogTitle>
              {editing ? "Modifier l'horaire" : "Créer un horaire"}
            </DialogTitle>
            <DialogDescription>
              Attachez les horaires à un élément constitutif pour l&apos;année,
              le parcours et le semestre sélectionnés.
            </DialogDescription>
          </DialogHeader>
          <WorkingTimeForm
            mode={editing ? "edit" : "create"}
            initialValues={
              editing
                ? toFormValues(editing)
                : { ...defaultFormValues, working_time_type: calendarType }
            }
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            offerings={offerings}
            classrooms={classrooms}
            groups={groups}
            fixedWorkingType={calendarType}
            examDateRanges={examDateRanges}
            contextLabels={{
              journey: currentJourneyLabel,
              semester: currentSemesterLabel,
              year: currentYearLabel
            }}
          />
        </DialogContent>
      </Dialog>

      <Dialog
        open={isExamDateOpen}
        onOpenChange={(open) => {
          setIsExamDateOpen(open);
          if (!open) {
            setEditingExamDate(null);
            resetExamDate(examDateDefaultValues);
          } else {
            resetExamDate(
              editingExamDate
                ? examDateToFormValues(editingExamDate)
                : examDateDefaultValues
            );
          }
        }}
      >
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle>Gérer les dates d&apos;examen</DialogTitle>
            <DialogDescription>
              Créez ou modifiez les périodes d&apos;examen pour l&apos;année
              académique sélectionnée.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="rounded-md border bg-muted p-3 text-xs text-muted-foreground space-y-1">
              <div>Année académique : {currentYearLabel}</div>
              <div>Session par défaut : {sessionOptions[0]?.label}</div>
              {examDateLimitReached ? (
                <div className="text-red-600">
                  Limite atteinte : 2 plages d&apos;examens maximum pour cette
                  année.
                </div>
              ) : null}
            </div>

            {examDateLimitReached && !editingExamDate ? null : (
              <form
                className="space-y-4"
                onSubmit={handleSubmitExamDate(handleExamDateSubmit)}
              >
                <input
                  type="hidden"
                  {...registerExamDate("id_academic_year")}
                />
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm font-medium" htmlFor="exam-date-from">
                      Date de début
                    </label>
                    <Input
                      id="exam-date-from"
                      type="date"
                      min={todayDateString}
                      className={cn(
                        examDateErrors.date_from &&
                          "border-destructive text-destructive"
                      )}
                      {...registerExamDate("date_from", {
                        required: "La date de début est obligatoire",
                        validate: (val) =>
                          val >= todayDateString ||
                          "La date de début doit être postérieure à aujourd'hui"
                      })}
                    />
                    {examDateErrors.date_from ? (
                      <p className="text-xs text-destructive">
                        {examDateErrors.date_from.message as string}
                      </p>
                    ) : null}
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium" htmlFor="exam-date-to">
                      Date de fin
                    </label>
                    <Input
                      id="exam-date-to"
                      type="date"
                      min={watchExamDate("date_from") || todayDateString}
                      className={cn(
                        examDateErrors.date_to &&
                          "border-destructive text-destructive"
                      )}
                      {...registerExamDate("date_to", {
                        required: "La date de fin est obligatoire",
                        validate: (val) => {
                          const start = watchExamDate("date_from") || todayDateString;
                          if (!val) return "La date de fin est obligatoire";
                          if (val < start)
                            return "La date de fin doit être après la date de début";
                          if (val < todayDateString)
                            return "La date de fin doit être postérieure à aujourd'hui";
                          return true;
                        }
                      })}
                    />
                    {examDateErrors.date_to ? (
                      <p className="text-xs text-destructive">
                        {examDateErrors.date_to.message as string}
                      </p>
                    ) : null}
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium" htmlFor="exam-session">
                    Session
                  </label>
                  <Select
                    value={watchExamDate("session") || "Normal"}
                    onValueChange={(value: WorkingSessionType) =>
                      setExamDateValue("session", value)
                    }
                  >
                    <SelectTrigger id="exam-session" className="h-11">
                      <SelectValue placeholder="Session" />
                    </SelectTrigger>
                    <SelectContent>
                      {sessionOptions.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center justify-end gap-2">
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={closeExamDateModal}
                    disabled={isExamDateSubmitting}
                  >
                    Fermer
                  </Button>
                  <Button
                    type="submit"
                    disabled={isExamDateSubmitting}
                  >
                    {isExamDateSubmitting
                      ? "Enregistrement…"
                      : editingExamDate
                        ? "Modifier"
                        : "Créer"}
                  </Button>
                </div>
              </form>
            )}

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-medium">Dates existantes</h4>
                <span className="text-xs text-muted-foreground">
                  {examDates.length
                    ? `${examDates.length} entrée${examDates.length > 1 ? "s" : ""}`
                    : "Aucune entrée"}
                </span>
              </div>
              <div className="space-y-2">
                {examDatesQuery.isFetching ? (
                  <p className="text-xs text-muted-foreground">Chargement…</p>
                ) : examDates.length ? (
                  examDates.map((examDate) => (
                    <div
                      key={examDate.id}
                      className="flex items-center justify-between rounded-md border p-3"
                    >
                      <div className="space-y-1 text-sm">
                        <div className="font-medium">
                          {examDate.session ?? "Session"}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {formatDateLabel(examDate.date_from)} →{" "}
                          {formatDateLabel(examDate.date_to)}
                        </div>
                        <div className="text-[11px] text-muted-foreground">
                          {examDate.year?.name ?? currentYearLabel ?? "Année"}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => setEditingExamDate(examDate)}
                        >
                          Modifier
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          className="text-destructive"
                          onClick={() => setExamDateToDelete(examDate)}
                        >
                          Supprimer
                        </Button>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-muted-foreground">
                    Aucune date d&apos;examen pour cette année académique.
                  </p>
                )}
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(workingTimeToDelete)}
        title="Supprimer l'horaire"
        description={
          workingTimeToDelete ? (
            <>
              Supprimer l&apos;horaire pour{" "}
              <strong>
                {workingTimeToDelete.constituent_element_offering
                  ?.constituent_element?.name ?? "cet élément"}
              </strong>
              ? Cette action est irréversible.
            </>
          ) : null
        }
        confirmLabel="Supprimer"
        destructive
        isConfirming={deleteWorkingTime.isPending}
        onCancel={() => setWorkingTimeToDelete(null)}
        onConfirm={handleDelete}
      />
      <ConfirmDialog
        open={Boolean(examDateToDelete)}
        title="Supprimer la date d'examen"
        description={
          examDateToDelete ? (
            <>
              Supprimer la plage d&apos;examen du{" "}
              {formatDateLabel(examDateToDelete.date_from)} au{" "}
              {formatDateLabel(examDateToDelete.date_to)} ?
            </>
          ) : null
        }
        confirmLabel="Supprimer"
        destructive
        isConfirming={deleteExamDate.isPending}
        onCancel={() => setExamDateToDelete(null)}
        onConfirm={handleDeleteExamDate}
      />
    </div>
  );
};
