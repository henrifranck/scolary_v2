import { useCallback, useEffect, useMemo, useState } from "react";
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
  Trash2
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useLookupOptions } from "@/hooks/use-lookup-options";
import { fetchJourneys as fetchJourneysByMention } from "@/services/inscription-service";
import { fetchClassrooms } from "@/services/classroom-service";
import { fetchGroups } from "@/services/group-service";
import { fetchConstituentElementOfferings } from "@/services/constituent-element-offering-service";
import { fetchConstituentElements } from "@/services/constituent-element-service";
import { fetchTeachingUnits } from "@/services/teaching-unit-service";
import {
  useCreateConstituentElementOffering,
  useDeleteConstituentElementOffering,
  useUpdateConstituentElementOffering
} from "@/services/constituent-element-offering-service";
import {
  useCreateTeachingUnitOffering,
  fetchTeachingUnitOfferings,
  useDeleteTeachingUnitOffering,
  useUpdateTeachingUnitOffering
} from "@/services/teaching-unit-offering-service";
import {
  fetchWorkingTimes,
  useCreateWorkingTime,
  useDeleteWorkingTime,
  useUpdateWorkingTime
} from "@/services/working-time-service";
import {
  WorkingSessionType,
  WorkingTime,
  WorkingTimePayload,
  WorkingTimeType
} from "@/models/working-time";
import { ConstituentElementOffering } from "@/models/constituent-element-offering";
import { Classroom } from "@/models/classroom";
import { Group } from "@/models/group";
import { TeachingUnitOffering } from "@/models/teaching-unit-offering";
import { ConstituentElement } from "@/models/constituent-element";
import { TeachingUnit } from "@/models/teaching-unit";
import {
  useConstituentElementOptionalGroups,
  useCreateConstituentElementOptionalGroup
} from "@/services/constituent-element-optional-group-service";
import {
  useTeachingUnitOptionalGroups,
  useCreateTeachingUnitOptionalGroup,
  useDeleteTeachingUnitOptionalGroup,
  useUpdateTeachingUnitOptionalGroup
} from "@/services/teaching-unit-optional-group-service";
import {
  useDeleteConstituentElementOptionalGroup,
  useUpdateConstituentElementOptionalGroup
} from "@/services/constituent-element-optional-group-service";

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

type ConstituentElementOfferingFormValues = {
  id_constituent_element: string;
  id_academic_year: string;
  weight: string;
  id_constituent_element_optional_group: string;
  id_teching_unit_offering: string;
  id_teacher: string;
};

type TeachingUnitOfferingFormValues = {
  id_teaching_unit: string;
  id_academic_year: string;
  credit: string;
  id_teaching_unit_optional_group: string;
};

type OptionalGroupFormValues = {
  name: string;
  description: string;
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
  { value: "Exam", label: "Examen" }
];
const workingTypeTabs = workingTypeOptions;

const sessionOptions: { value: WorkingSessionType; label: string }[] = [
  { value: "Normal", label: "Session normale" },
  { value: "Rattrapage", label: "Rattrapage" }
];

const defaultFormValues: WorkingTimeFormValues = {
  id_constituent_element_offering: "",
  id_classroom: "",
  id_group: "",
  working_time_type: "COURSE",
  session: "Normal",
  day: "Lundi",
  date: "",
  start: defaultStartTime,
  end: defaultEndTime
};

const defaultCEOfferingValues: ConstituentElementOfferingFormValues = {
  id_constituent_element: "",
  id_academic_year: "",
  weight: "",
  id_constituent_element_optional_group: "",
  id_teching_unit_offering: "",
  id_teacher: ""
};

const defaultTUOfferingValues: TeachingUnitOfferingFormValues = {
  id_teaching_unit: "",
  id_academic_year: "",
  credit: "",
  id_teaching_unit_optional_group: ""
};

const defaultOptionalGroupValues: OptionalGroupFormValues = {
  name: "",
  description: ""
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
  working_time_type: workingTime?.working_time_type ?? "COURSE",
  session: workingTime?.session ?? "Normal",
  day: normalizeDay(workingTime?.day, workingTime?.date) ?? "Monday",
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
  day: values.day,
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
}

const WorkingTimeForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  offerings,
  classrooms,
  groups
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

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="working-time-type">
            Type de séance
          </label>
          <Select
            value={watch("working_time_type")}
            onValueChange={(value: WorkingTimeType) =>
              setValue("working_time_type", value)
            }
          >
            <SelectTrigger
              id="working-time-type"
              className={cn(
                "h-11",
                errors.working_time_type &&
                  "border-destructive text-destructive"
              )}
            >
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              {workingTypeOptions.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="working-time-session">
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

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="working-time-date">
            Date
          </label>
          <Input
            id="working-time-date"
            type="date"
            value={watch("date")}
            onChange={(event) => setValue("date", event.target.value)}
          />
        </div>
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

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="working-time-room">
            Salle (optionnel)
          </label>
          <Select
            value={watch("id_classroom") || emptySelectValue}
            onValueChange={(value) =>
              setValue("id_classroom", value === emptySelectValue ? "" : value)
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
  const createCEOffering = useCreateConstituentElementOffering();
  const createTUOffering = useCreateTeachingUnitOffering();
  const updateCEOffering = useUpdateConstituentElementOffering();
  const updateTUOffering = useUpdateTeachingUnitOffering();
  const deleteCEOffering = useDeleteConstituentElementOffering();
  const deleteTUOffering = useDeleteTeachingUnitOffering();
  const createCEOptionalGroup = useCreateConstituentElementOptionalGroup();
  const createTUOptionalGroup = useCreateTeachingUnitOptionalGroup();
  const deleteCEOptionalGroup = useDeleteConstituentElementOptionalGroup();
  const deleteTUOptionalGroup = useDeleteTeachingUnitOptionalGroup();
  const updateCEOptionalGroup = useUpdateConstituentElementOptionalGroup();
  const updateTUOptionalGroup = useUpdateTeachingUnitOptionalGroup();

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

  const [calendarType, setCalendarType] = useState<WorkingTimeType>("COURSE");

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
          value: calendarType
        });
      }

      return fetchWorkingTimes({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "constituent_element_offering.academic_year{id,name}",
          "constituent_element_offering.constituent_element{id,name,semester,color,id_journey}",
          "constituent_element_offering{id,id_academic_year,id_teching_unit_offering,id_constituent_element,id_teacher,id_constituent_element_optional_group,weight}",
          "classroom{id,name,capacity}",
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

  const constituentElementListQuery = useQuery({
    queryKey: [
      "working-time",
      "ce-list",
      filters.id_mention,
      filters.id_journey,
      filters.semester,
      filters.id_year
    ],
    queryFn: () => {
      const wheres: Array<Record<string, any>> = [];
      if (filters.id_mention) {
        wheres.push({
          key: "journey.id_mention",
          operator: "==",
          value: Number(filters.id_mention)
        });
      }
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
      return fetchConstituentElements({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "journey{id,name,abbreviation,id_mention}",
          "journey.mention{id,name}"
        ]),
        limit: 400
      });
    }
  });

  const teachingUnitListQuery = useQuery({
    queryKey: [
      "working-time",
      "tu-list",
      filters.id_mention,
      filters.id_journey,
      filters.semester,
      filters.id_year
    ],
    queryFn: () => {
      const wheres: Array<Record<string, any>> = [];
      if (filters.id_mention) {
        wheres.push({
          key: "journey.id_mention",
          operator: "==",
          value: Number(filters.id_mention)
        });
      }
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
      return fetchTeachingUnits({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "journey{id,name,abbreviation,id_mention}",
          "journey.mention{id,name}"
        ]),
        limit: 400
      });
    }
  });

  const teachingUnitOfferingQuery = useQuery({
    queryKey: [
      "working-time",
      "tu-offerings",
      filters.id_mention,
      filters.id_journey,
      filters.semester,
      filters.id_year
    ],
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
          key: "teaching_unit.journey.id_mention",
          operator: "==",
          value: Number(filters.id_mention)
        });
      }
      if (filters.id_journey) {
        wheres.push({
          key: "teaching_unit.id_journey",
          operator: "==",
          value: Number(filters.id_journey)
        });
      }
      if (filters.semester) {
        wheres.push({
          key: "teaching_unit.semester",
          operator: "==",
          value: filters.semester
        });
      }
      return fetchTeachingUnitOfferings({
        where: JSON.stringify(wheres),
        relation: JSON.stringify([
          "teaching_unit{id,name,semester,id_journey}",
          "teaching_unit.journey{id,name,abbreviation,id_mention}",
          "academic_year{id,name}"
        ]),
        limit: 400
      });
    }
  });

  const ceOptionalGroupsQuery = useConstituentElementOptionalGroups();
  const tuOptionalGroupsQuery = useTeachingUnitOptionalGroups();

  const workingTimes = workingTimeQuery.data?.data ?? [];
  const offerings = offeringsQuery.data?.data ?? [];
  const classrooms = classroomsQuery.data?.data ?? [];
  const groups = groupsQuery.data?.data ?? [];
  const [filtersCollapsed, setFiltersCollapsed] = useState(false);
  const [offeringDialogOpen, setOfferingDialogOpen] = useState(false);
  const [offeringTab, setOfferingTab] = useState<"ec" | "ue">("ec");
  const [optionalGroupDialogOpen, setOptionalGroupDialogOpen] = useState(false);
  const [optionalGroupTab, setOptionalGroupTab] = useState<"ec" | "ue">("ec");
  const [editingOptionalGroupId, setEditingOptionalGroupId] = useState<
    number | null
  >(null);
  const [manageOfferingsDialogOpen, setManageOfferingsDialogOpen] =
    useState(false);
  const [editingCEOfferingId, setEditingCEOfferingId] = useState<number | null>(
    null
  );
  const [editingTUOfferingId, setEditingTUOfferingId] = useState<number | null>(
    null
  );
  const ceForm = useForm<ConstituentElementOfferingFormValues>({
    defaultValues: defaultCEOfferingValues
  });
  const tuForm = useForm<TeachingUnitOfferingFormValues>({
    defaultValues: defaultTUOfferingValues
  });
  const optionalGroupForm = useForm<OptionalGroupFormValues>({
    defaultValues: defaultOptionalGroupValues
  });
  const ceOptions: ConstituentElement[] =
    constituentElementListQuery.data?.data ?? [];
  const tuOptions: TeachingUnit[] = teachingUnitListQuery.data?.data ?? [];
  const tuOfferingOptions: TeachingUnitOffering[] =
    teachingUnitOfferingQuery.data?.data ?? [];
  const ceOptionalGroupOptions =
    ceOptionalGroupsQuery.data?.data ?? ceOptionalGroupsQuery.data ?? [];
  const tuOptionalGroupOptions =
    tuOptionalGroupsQuery.data?.data ?? tuOptionalGroupsQuery.data ?? [];

  const resetOfferingForms = useCallback(() => {
    ceForm.reset(defaultCEOfferingValues);
    tuForm.reset(defaultTUOfferingValues);
    optionalGroupForm.reset(defaultOptionalGroupValues);
    setEditingOptionalGroupId(null);
    setEditingCEOfferingId(null);
    setEditingTUOfferingId(null);
  }, [ceForm, tuForm, optionalGroupForm]);

  const handleFiltersChange = useCallback((next: any) => {
    setFilters((prev) => ({
      ...prev,
      id_mention: next.id_mention,
      id_journey: next.id_journey,
      semester: next.semester
    }));
  }, []);

  const openCreate = () => {
    setEditing(null);
    setIsFormOpen(true);
  };

  const closeForm = useCallback(() => {
    setEditing(null);
    setIsFormOpen(false);
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

  const handleCreateCEOffering = ceForm.handleSubmit(
    async (values: ConstituentElementOfferingFormValues) => {
      const linkedUE = values.id_teching_unit_offering;
      if (!linkedUE || linkedUE === emptySelectValue) {
        ceForm.setError("id_teching_unit_offering", {
          type: "required",
          message: "L'offre UE liée est obligatoire"
        });
        return;
      }
      ceForm.clearErrors("id_teching_unit_offering");
      const payload: any = {
        id_constituent_element: values.id_constituent_element
          ? Number(values.id_constituent_element)
          : undefined,
        id_academic_year: values.id_academic_year
          ? Number(values.id_academic_year)
          : undefined,
        weight: values.weight ? Number(values.weight) : undefined,
        id_constituent_element_optional_group:
          values.id_constituent_element_optional_group
            ? Number(values.id_constituent_element_optional_group)
            : undefined,
        id_teching_unit_offering:
          linkedUE && linkedUE !== emptySelectValue
            ? Number(linkedUE)
            : undefined,
        id_teacher: values.id_teacher ? Number(values.id_teacher) : undefined
      };
      if (editingCEOfferingId) {
        await updateCEOffering.mutateAsync({
          id: editingCEOfferingId,
          payload
        });
        setFeedback({
          type: "success",
          text: "Offre EC mise à jour."
        });
      } else {
        await createCEOffering.mutateAsync(payload);
        setFeedback({
          type: "success",
          text: "Offre EC créée."
        });
      }
      resetOfferingForms();
      await offeringsQuery.refetch();
      await ceOptionalGroupsQuery.refetch();
      setOfferingDialogOpen(false);
    }
  );

  const handleCreateTUOffering = tuForm.handleSubmit(
    async (values: TeachingUnitOfferingFormValues) => {
      const payload: any = {
        id_teaching_unit: values.id_teaching_unit
          ? Number(values.id_teaching_unit)
          : undefined,
        id_academic_year: values.id_academic_year
          ? Number(values.id_academic_year)
          : undefined,
        credit: values.credit ? Number(values.credit) : undefined,
        id_teaching_unit_optional_group: values.id_teaching_unit_optional_group
          ? Number(values.id_teaching_unit_optional_group)
          : undefined
      };
      if (editingTUOfferingId) {
        await updateTUOffering.mutateAsync({
          id: editingTUOfferingId,
          payload
        });
        setFeedback({
          type: "success",
          text: "Offre UE mise à jour."
        });
      } else {
        await createTUOffering.mutateAsync(payload);
        setFeedback({
          type: "success",
          text: "Offre UE créée."
        });
      }
      resetOfferingForms();
      await teachingUnitOfferingQuery.refetch();
      await teachingUnitListQuery.refetch();
      await tuOptionalGroupsQuery.refetch();
      setOfferingDialogOpen(false);
    }
  );

  const handleCreateOptionalGroup = optionalGroupForm.handleSubmit(
    async (values: OptionalGroupFormValues) => {
      try {
        if (optionalGroupTab === "ec") {
          if (editingOptionalGroupId) {
            await updateCEOptionalGroup.mutateAsync({
              id: editingOptionalGroupId,
              payload: values
            });
          } else {
            await createCEOptionalGroup.mutateAsync(values);
          }
          await ceOptionalGroupsQuery.refetch();
        } else {
          if (editingOptionalGroupId) {
            await updateTUOptionalGroup.mutateAsync({
              id: editingOptionalGroupId,
              payload: values
            });
          } else {
            await createTUOptionalGroup.mutateAsync(values);
          }
          await tuOptionalGroupsQuery.refetch();
        }
        setFeedback({
          type: "success",
          text: editingOptionalGroupId
            ? "Groupe optionnel mis à jour."
            : "Groupe optionnel créé."
        });
        optionalGroupForm.reset(defaultOptionalGroupValues);
        setEditingOptionalGroupId(null);
        setOptionalGroupDialogOpen(false);
      } catch (error) {
        const message =
          error instanceof Error
            ? error.message
            : "Impossible de créer le groupe optionnel.";
        setFeedback({ type: "error", text: message });
      }
    }
  );

  const eventsByDay = useMemo(() => {
    const acc: Record<string, WorkingTime[]> = {};
    for (const day of daysOfWeek) {
      acc[day] = [];
    }
    workingTimes.forEach((item) => {
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
  }, [workingTimes]);

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
        <Button className="gap-2" onClick={openCreate}>
          <Plus className="h-4 w-4" />
          Ajouter un horaire
        </Button>
        <Button
          variant="outline"
          className="gap-2"
          onClick={() => {
            resetOfferingForms();
            if (filters.id_year) {
              ceForm.setValue("id_academic_year", String(filters.id_year));
              tuForm.setValue("id_academic_year", String(filters.id_year));
            }
            setOfferingDialogOpen(true);
          }}
        >
          <Plus className="h-4 w-4" />
          Ajouter une offre EC/UE
        </Button>
        <Button
          variant="outline"
          className="gap-2"
          onClick={() => {
            optionalGroupForm.reset(defaultOptionalGroupValues);
            setEditingOptionalGroupId(null);
            setOptionalGroupDialogOpen(true);
          }}
        >
          <Plus className="h-4 w-4" />
          Nouveau groupe optionnel
        </Button>
        <Button
          variant="outline"
          className="gap-2"
          onClick={() => setManageOfferingsDialogOpen(true)}
        >
          <Layers className="h-4 w-4" />
          Gérer offres
        </Button>
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
            onValueChange={(value) => setCalendarType(value as WorkingTimeType)}
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
                                      item.working_time_type ?? "cours"
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
                                <span>{item.classroom.name}</span>
                              </div>
                            ) : null}
                            <div className="flex flex-wrap items-center gap-2 text-[11px] text-muted-foreground">
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
                            </div>
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

      <Dialog open={offeringDialogOpen} onOpenChange={setOfferingDialogOpen}>
        <DialogContent className="sm:max-w-3xl">
          <DialogHeader>
            <DialogTitle>Ajouter une offre</DialogTitle>
            <DialogDescription>
              Créez rapidement une offre d&apos;élément constitutif ou
              d&apos;unité d&apos;enseignement. Tous les champs sont
              facultatifs.
            </DialogDescription>
          </DialogHeader>
          <Tabs
            value={offeringTab}
            onValueChange={(value) => setOfferingTab(value as "ec" | "ue")}
          >
            <TabsList className="grid grid-cols-2 mb-4 bg-muted">
              <TabsTrigger value="ec">Offre EC</TabsTrigger>
              <TabsTrigger value="ue">Offre UE</TabsTrigger>
            </TabsList>
          </Tabs>

          {offeringTab === "ec" ? (
            <form className="space-y-3" onSubmit={handleCreateCEOffering}>
              <div className="grid gap-3 md:grid-cols-2">
                <Select
                  value={ceForm.watch("id_constituent_element")}
                  onValueChange={(value) =>
                    ceForm.setValue("id_constituent_element", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner l'EC" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={emptySelectValue}>Aucun</SelectItem>
                    {ceOptions.map((ce) => (
                      <SelectItem key={ce.id} value={String(ce.id)}>
                        {ce.name} {ce.semester ? `· ${ce.semester}` : ""}{" "}
                        {ce.journey?.name ?? ce.journey?.abbreviation ?? ""}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Input
                  placeholder="Année académique (affichée seulement)"
                  value={
                    academicYearOptions.find(
                      (year) => year.id === ceForm.watch("id_academic_year")
                    )?.label || ""
                  }
                  disabled
                  readOnly
                />
                <Input
                  type="number"
                  placeholder="Poids"
                  {...ceForm.register("weight")}
                />
                <Select
                  value={ceForm.watch("id_constituent_element_optional_group")}
                  onValueChange={(value) =>
                    ceForm.setValue(
                      "id_constituent_element_optional_group",
                      value
                    )
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Groupe optionnel EC (facultatif)" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={emptySelectValue}>Aucun</SelectItem>
                    {ceOptionalGroupOptions.map((group: any) => (
                      <SelectItem key={group.id} value={String(group.id)}>
                        {group.name ?? `Groupe ${group.id}`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select
                  value={ceForm.watch("id_teching_unit_offering")}
                  onValueChange={(value) =>
                    ceForm.setValue("id_teching_unit_offering", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Offre UE liée (facultatif)" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={emptySelectValue}>Aucune</SelectItem>
                    {tuOfferingOptions.map((offer) => (
                      <SelectItem key={offer.id} value={String(offer.id)}>
                        {offer.teaching_unit?.name ?? "UE"}{" "}
                        {offer.teaching_unit?.semester
                          ? `· ${offer.teaching_unit.semester}`
                          : ""}{" "}
                        {offer.academic_year?.name
                          ? `· ${offer.academic_year.name}`
                          : ""}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {ceForm.formState.errors.id_teching_unit_offering ? (
                  <p className="text-xs text-destructive">
                    {ceForm.formState.errors.id_teching_unit_offering.message}
                  </p>
                ) : null}
                <Select
                  value={ceForm.watch("id_teacher")}
                  onValueChange={(value) =>
                    ceForm.setValue("id_teacher", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Enseignant (facultatif)" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={emptySelectValue}>Aucun</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex justify-end gap-2">
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setOfferingDialogOpen(false)}
                >
                  Annuler
                </Button>
                <Button type="submit" disabled={createCEOffering.isPending}>
                  {createCEOffering.isPending
                    ? "Création…"
                    : "Créer l'offre EC"}
                </Button>
              </div>
            </form>
          ) : (
            <form className="space-y-3" onSubmit={handleCreateTUOffering}>
              <div className="grid gap-3 md:grid-cols-2">
                <Select
                  value={tuForm.watch("id_teaching_unit")}
                  onValueChange={(value) =>
                    tuForm.setValue("id_teaching_unit", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner l'UE" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={emptySelectValue}>Aucune</SelectItem>
                    {tuOptions.map((tu) => (
                      <SelectItem key={tu.id} value={String(tu.id)}>
                        {tu.name} {tu.semester ? `· ${tu.semester}` : ""}{" "}
                        {tu.journey?.name ?? tu.journey?.abbreviation ?? ""}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Input
                  placeholder="Année académique (affichée seulement)"
                  value={
                    academicYearOptions.find(
                      (year) => year.id === tuForm.watch("id_academic_year")
                    )?.label || ""
                  }
                  disabled
                  readOnly
                />
                <Input
                  type="number"
                  placeholder="Crédits"
                  {...tuForm.register("credit")}
                />
                <Select
                  value={tuForm.watch("id_teaching_unit_optional_group")}
                  onValueChange={(value) =>
                    tuForm.setValue("id_teaching_unit_optional_group", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Groupe optionnel UE (facultatif)" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={emptySelectValue}>Aucun</SelectItem>
                    {tuOptionalGroupOptions.map((group: any) => (
                      <SelectItem key={group.id} value={String(group.id)}>
                        {group.name ?? `Groupe ${group.id}`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex justify-end gap-2">
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setOfferingDialogOpen(false)}
                >
                  Annuler
                </Button>
                <Button type="submit" disabled={createTUOffering.isPending}>
                  {createTUOffering.isPending
                    ? "Création…"
                    : "Créer l'offre UE"}
                </Button>
              </div>
            </form>
          )}
        </DialogContent>
      </Dialog>

      <Dialog
        open={manageOfferingsDialogOpen}
        onOpenChange={setManageOfferingsDialogOpen}
      >
        <DialogContent className="sm:max-w-4xl">
          <DialogHeader>
            <DialogTitle>Offres EC / UE</DialogTitle>
            <DialogDescription>
              Consultez, éditez ou supprimez les offres existantes.
            </DialogDescription>
          </DialogHeader>
          <Tabs defaultValue="ec">
            <TabsList className="grid grid-cols-2 bg-muted mb-4">
              <TabsTrigger value="ec">Offres EC</TabsTrigger>
              <TabsTrigger value="ue">Offres UE</TabsTrigger>
            </TabsList>
            <div className="space-y-3">
              <TabsContent value="ec" className="space-y-2">
                {(offerings ?? []).map((offer: any) => {
                  const ce = offer.constituent_element;
                  return (
                    <div
                      key={offer.id}
                      className="flex items-center justify-between rounded border bg-background px-3 py-2"
                    >
                      <div className="flex flex-col">
                        <span className="font-medium">
                          {ce?.constituent_element?.name ?? "EC"}{" "}
                          {ce?.constituent_element?.semester
                            ? `· ${ce.constituent_element.semester}`
                            : ""}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          {ce?.academic_year?.name ?? ""}{" "}
                          {ce?.constituent_element?.journey?.name ??
                            ce?.constituent_element?.journey?.abbreviation ??
                            ""}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            setOfferingDialogOpen(true);
                            setOfferingTab("ec");
                            setEditingCEOfferingId(Number(offer.id));
                            ceForm.reset({
                              id_constituent_element: ce?.constituent_element
                                ?.id
                                ? String(ce.constituent_element.id)
                                : "",
                              id_academic_year: ce?.academic_year?.id
                                ? String(ce.academic_year.id)
                                : "",
                              weight: offer.weight ? String(offer.weight) : "",
                              id_constituent_element_optional_group:
                                offer.id_constituent_element_optional_group
                                  ? String(
                                      offer.id_constituent_element_optional_group
                                    )
                                  : "",
                              id_teching_unit_offering:
                                offer.id_teching_unit_offering
                                  ? String(offer.id_teching_unit_offering)
                                  : "",
                              id_teacher: offer.id_teacher
                                ? String(offer.id_teacher)
                                : ""
                            });
                          }}
                        >
                          Éditer
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() =>
                            deleteCEOffering.mutate(Number(offer.id), {
                              onSuccess: () => {
                                offeringsQuery.refetch();
                                workingTimeQuery.refetch();
                                resetOfferingForms();
                              }
                            })
                          }
                        >
                          Supprimer
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </TabsContent>
              <TabsContent value="ue" className="space-y-2">
                {(teachingUnitOfferingQuery.data?.data ?? []).map(
                  (offer: any) => {
                    const tu = offer.teaching_unit;
                    return (
                      <div
                        key={offer.id}
                        className="flex items-center justify-between rounded border bg-background px-3 py-2"
                      >
                        <div className="flex flex-col">
                          <span className="font-medium">
                            {tu?.name ?? "UE"}{" "}
                            {tu?.semester ? `· ${tu.semester}` : ""}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {offer.academic_year?.name ?? ""}{" "}
                            {tu?.journey?.name ??
                              tu?.journey?.abbreviation ??
                              ""}
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              setOfferingDialogOpen(true);
                              setOfferingTab("ue");
                              setEditingTUOfferingId(Number(offer.id));
                              tuForm.reset({
                                id_teaching_unit: tu?.id ? String(tu.id) : "",
                                id_academic_year: offer.academic_year?.id
                                  ? String(offer.academic_year.id)
                                  : "",
                                credit: offer.credit
                                  ? String(offer.credit)
                                  : "",
                                id_teaching_unit_optional_group:
                                  offer.id_teaching_unit_optional_group
                                    ? String(
                                        offer.id_teaching_unit_optional_group
                                      )
                                    : ""
                              });
                            }}
                          >
                            Éditer
                          </Button>
                          <Button
                            size="sm"
                            variant="destructive"
                            onClick={() =>
                              deleteTUOffering.mutate(Number(offer.id), {
                                onSuccess: () => {
                                  teachingUnitOfferingQuery.refetch();
                                  workingTimeQuery.refetch();
                                  resetOfferingForms();
                                }
                              })
                            }
                          >
                            Supprimer
                          </Button>
                        </div>
                      </div>
                    );
                  }
                )}
              </TabsContent>
            </div>
          </Tabs>
        </DialogContent>
      </Dialog>

      <Dialog
        open={optionalGroupDialogOpen}
        onOpenChange={setOptionalGroupDialogOpen}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>Ajouter un groupe optionnel</DialogTitle>
            <DialogDescription>
              Créez un groupe optionnel pour une offre EC ou UE.
            </DialogDescription>
          </DialogHeader>
          <Tabs
            value={optionalGroupTab}
            onValueChange={(value) => setOptionalGroupTab(value as "ec" | "ue")}
          >
            <TabsList className="grid grid-cols-2 bg-muted mb-4">
              <TabsTrigger value="ec">Groupe EC</TabsTrigger>
              <TabsTrigger value="ue">Groupe UE</TabsTrigger>
            </TabsList>
          </Tabs>
          <form className="space-y-3" onSubmit={handleCreateOptionalGroup}>
            <Input
              placeholder="Nom du groupe"
              {...optionalGroupForm.register("name")}
            />
            <Input
              placeholder="Description"
              {...optionalGroupForm.register("description")}
            />
            <div className="rounded-md border bg-muted p-3 text-xs text-muted-foreground">
              {optionalGroupTab === "ec" ? "Listes EC :" : "Listes UE :"}
              <div className="mt-2 space-y-1">
                {(optionalGroupTab === "ec"
                  ? ceOptionalGroupOptions
                  : tuOptionalGroupOptions
                ).map((group: any) => (
                  <div
                    key={group.id}
                    className="flex items-center justify-between rounded border bg-background px-2 py-1"
                  >
                    <div className="flex flex-col">
                      <span className="font-medium text-foreground">
                        {group.name ?? `Groupe ${group.id}`}
                      </span>
                      {group.description ? (
                        <span className="text-[11px] text-muted-foreground">
                          {group.description}
                        </span>
                      ) : null}
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        size="icon"
                        variant="ghost"
                        className="h-7 w-7"
                        onClick={() => {
                          setEditingOptionalGroupId(group.id);
                          setOptionalGroupTab(
                            optionalGroupTab === "ec" ? "ec" : "ue"
                          );
                          optionalGroupForm.reset({
                            name: group.name ?? "",
                            description: group.description ?? ""
                          });
                        }}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        className="h-7 w-7 text-destructive"
                        onClick={() => {
                          if (optionalGroupTab === "ec") {
                            deleteCEOptionalGroup.mutate(Number(group.id), {
                              onSuccess: () => ceOptionalGroupsQuery.refetch()
                            });
                          } else {
                            deleteTUOptionalGroup.mutate(Number(group.id), {
                              onSuccess: () => tuOptionalGroupsQuery.refetch()
                            });
                          }
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setOptionalGroupDialogOpen(false)}
              >
                Annuler
              </Button>
              <Button
                type="submit"
                disabled={
                  createCEOptionalGroup.isPending ||
                  createTUOptionalGroup.isPending
                }
              >
                {createCEOptionalGroup.isPending ||
                createTUOptionalGroup.isPending
                  ? "Création…"
                  : "Créer le groupe"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

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
            initialValues={toFormValues(editing)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            offerings={offerings}
            classrooms={classrooms}
            groups={groups}
          />
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
    </div>
  );
};
