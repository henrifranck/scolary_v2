import { useCallback, useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "@tanstack/react-router";
import { Pencil, Plus, Trash2 } from "lucide-react";
import { useForm } from "react-hook-form";

import {
  AcademicFilters,
  JourneyOption
} from "@/components/filters/academic-filters";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useLookupOptions } from "@/hooks/use-lookup-options";
import { Textarea } from "@/components/ui/textarea";
import { ConstituentElement } from "@/models/constituent-element";
import { ConstituentElementOffering } from "@/models/constituent-element-offering";
import { TeachingUnitOffering } from "@/models/teaching-unit-offering";
import { TeachingUnit } from "@/models/teaching-unit";
import { fetchJourneys as fetchJourneysByMention } from "@/services/inscription-service";
import { fetchConstituentElements } from "@/services/constituent-element-service";
import {
  fetchConstituentElementOfferings,
  useCreateConstituentElementOffering,
  useDeleteConstituentElementOffering,
  useUpdateConstituentElementOffering
} from "@/services/constituent-element-offering-service";
import {
  useConstituentElementOptionalGroups,
  useCreateConstituentElementOptionalGroup,
  useDeleteConstituentElementOptionalGroup,
  useUpdateConstituentElementOptionalGroup
} from "@/services/constituent-element-optional-group-service";
import { fetchTeachingUnits } from "@/services/teaching-unit-service";
import {
  fetchTeachingUnitOfferings,
  useCreateTeachingUnitOffering,
  useDeleteTeachingUnitOffering,
  useUpdateTeachingUnitOffering
} from "@/services/teaching-unit-offering-service";
import {
  useTeachingUnitOptionalGroups,
  useCreateTeachingUnitOptionalGroup,
  useDeleteTeachingUnitOptionalGroup,
  useUpdateTeachingUnitOptionalGroup
} from "@/services/teaching-unit-optional-group-service";
import { cn } from "@/lib/utils";

type OfferingFilters = {
  id_year: string;
  id_mention: string;
  id_journey: string;
  semester: string;
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
  id_journey: string;
  semester: string;
  selection_regle: string;
  id_teaching_unit_offering: string;
};

type Feedback = { type: "success" | "error"; text: string };

const semesters = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"];
const emptySelectValue = "__none__";

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
  description: "",
  id_journey: "",
  semester: "",
  selection_regle: "",
  id_teaching_unit_offering: ""
};

const resolveHeaderAcademicYear = () => {
  if (typeof window === "undefined") return "";
  const stored = window.localStorage.getItem("selected_academic_year");
  if (!stored || stored === "all") return "";
  return stored;
};

const STORAGE_KEY = "offering-management.filters";

const readStoredFilters = (): OfferingFilters | null => {
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
      return parsed as OfferingFilters;
    }
  } catch {
    return null;
  }
  return null;
};

export const OfferingsPage = () => {
  const defaultSemester = semesters[0];
  const { mentionOptions, academicYearOptions } = useLookupOptions({
    includeMentions: true,
    includeAcademicYears: true
  });

  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [filters, setFilters] = useState<OfferingFilters>(() => {
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
  const [filtersCollapsed, setFiltersCollapsed] = useState(false);
  const [offeringDialogOpen, setOfferingDialogOpen] = useState(false);
  const [offeringTab, setOfferingTab] = useState<"ec" | "ue">("ec");
  const [optionalGroupDialogOpen, setOptionalGroupDialogOpen] = useState(false);
  const [optionalGroupTab, setOptionalGroupTab] = useState<"ec" | "ue">("ec");
  const [editingOptionalGroupId, setEditingOptionalGroupId] = useState<
    number | null
  >(null);
  const [editingCEOfferingId, setEditingCEOfferingId] = useState<number | null>(
    null
  );
  const [editingTUOfferingId, setEditingTUOfferingId] = useState<number | null>(
    null
  );

  const journeyQuery = useQuery({
    queryKey: ["offerings", "journeys", filters.id_mention],
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
  }, [allowedSemestersForJourney, availableJourneys, defaultSemester]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
  }, [filters]);

  const constituentElementListQuery = useQuery({
    queryKey: [
      "offerings",
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
      "offerings",
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

  const offeringsQuery = useQuery({
    queryKey: ["offerings", "ce-offerings", filters],
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

  const teachingUnitOfferingQuery = useQuery({
    queryKey: [
      "offerings",
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

  const ceOptionalGroupWheres = useMemo(() => {
    const wheres: Array<Record<string, any>> = [];
    const journey = filters.id_journey ? Number(filters.id_journey) : undefined;
    const semester = filters.semester || undefined;

    if (journey && semester) {
      wheres.push({
        key: "teaching_unit_offering.[teaching_unit.[id_journey,semester]]",
        operator: "==,==",
        value: `${journey},${semester}`
      });
    } else if (journey) {
      wheres.push({
        key: "teaching_unit_offering.[teaching_unit.[id_journey]]",
        operator: "==",
        value: journey
      });
    } else if (semester) {
      wheres.push({
        key: "teaching_unit_offering.[teaching_unit.[semester]]",
        operator: "==",
        value: semester
      });
    }
    return wheres;
  }, [filters.id_journey, filters.semester]);

  const tuOptionalGroupWheres = useMemo(() => {
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
    return wheres;
  }, [filters.id_journey, filters.semester]);

  const ceOptionalGroupsQuery = useConstituentElementOptionalGroups(
    ceOptionalGroupWheres.length
      ? {
          where: JSON.stringify(ceOptionalGroupWheres),
          relation: JSON.stringify([
            "teaching_unit_offering{id,credit,id_academic_year,id_teaching_unit_optional_group,id_teaching_unit}",
            "teaching_unit_offering.teaching_unit{id,name,semester,id_journey}",
            "teaching_unit_offering.academic_year{id,name}"
          ])
        }
      : {
          relation: JSON.stringify([
            "teaching_unit_offering{id,credit,id_academic_year,id_teaching_unit_optional_group,id_teaching_unit}",
            "teaching_unit_offering.teaching_unit{id,name,semester,id_journey}",
            "teaching_unit_offering.academic_year{id,name}"
          ])
        }
  );
  const tuOptionalGroupsQuery = useTeachingUnitOptionalGroups(
    tuOptionalGroupWheres.length
      ? { where: JSON.stringify(tuOptionalGroupWheres) }
      : undefined
  );
  const refetchCEOptionalGroups = ceOptionalGroupsQuery.refetch;
  const refetchTUOptionalGroups = tuOptionalGroupsQuery.refetch;

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
  const currentJourneyId =
    optionalGroupForm.watch("id_journey") || filters.id_journey;
  const currentSemester =
    optionalGroupForm.watch("semester") || filters.semester || "";
  const currentJourneyLabel =
    availableJourneys.find((journey) => journey.id === currentJourneyId)
      ?.label ?? "Non défini";

  const resetOfferingForms = useCallback(() => {
    ceForm.reset(defaultCEOfferingValues);
    tuForm.reset(defaultTUOfferingValues);
    optionalGroupForm.reset(defaultOptionalGroupValues);
    setEditingOptionalGroupId(null);
    setEditingCEOfferingId(null);
    setEditingTUOfferingId(null);
  }, [ceForm, tuForm, optionalGroupForm]);

  useEffect(() => {
    refetchCEOptionalGroups();
    refetchTUOptionalGroups();
  }, [
    refetchCEOptionalGroups,
    refetchTUOptionalGroups,
    filters.id_journey,
    filters.id_mention,
    filters.semester,
    filters.id_year
  ]);

  const handleFiltersChange = useCallback((next: any) => {
    setFilters((prev) => ({
      ...prev,
      id_mention: next.id_mention,
      id_journey: next.id_journey,
      semester: next.semester
    }));
  }, []);

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
          const payload = {
            name: values.name,
            description: values.description,
            id_teaching_unit_offering:
              values.id_teaching_unit_offering &&
              values.id_teaching_unit_offering !== emptySelectValue
                ? Number(values.id_teaching_unit_offering)
                : undefined,
            selection_regle: values.selection_regle || undefined
          };
          if (editingOptionalGroupId) {
            await updateCEOptionalGroup.mutateAsync({
              id: editingOptionalGroupId,
              payload
            });
          } else {
            await createCEOptionalGroup.mutateAsync(payload);
          }
          await ceOptionalGroupsQuery.refetch();
        } else {
          const journeyId =
            values.id_journey && values.id_journey !== emptySelectValue
              ? Number(values.id_journey)
              : filters.id_journey
                ? Number(filters.id_journey)
                : undefined;
          const semesterValue =
            values.semester && values.semester !== emptySelectValue
              ? values.semester
              : filters.semester || undefined;
          if (editingOptionalGroupId) {
            await updateTUOptionalGroup.mutateAsync({
              id: editingOptionalGroupId,
              payload: {
                name: values.name,
                id_journey: journeyId,
                semester: semesterValue,
                selection_regle: values.selection_regle || undefined
              }
            });
          } else {
            await createTUOptionalGroup.mutateAsync({
              name: values.name,
              id_journey: journeyId,
              semester: semesterValue,
              selection_regle: values.selection_regle || undefined
            });
          }
          await tuOptionalGroupsQuery.refetch();
        }
        setFeedback({
          type: "success",
          text: editingOptionalGroupId
            ? "Groupe optionnel mis à jour."
            : "Groupe optionnel créé."
        });
        optionalGroupForm.reset({
          ...defaultOptionalGroupValues,
          id_journey: filters.id_journey,
          semester: filters.semester
        });
        setEditingOptionalGroupId(null);
        // setOptionalGroupDialogOpen(false);
      } catch (error) {
        const message =
          error instanceof Error
            ? error.message
            : "Impossible de créer le groupe optionnel.";
        setFeedback({ type: "error", text: message });
      }
    }
  );

  const ceOfferings = offeringsQuery.data?.data ?? [];
  const tuOfferings = teachingUnitOfferingQuery.data?.data ?? [];

  const isSubmitting =
    createCEOffering.isPending ||
    createTUOffering.isPending ||
    createCEOptionalGroup.isPending ||
    createTUOptionalGroup.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Offres EC / UE
          </h1>
          <p className="text-sm text-muted-foreground">
            Gérez les offres d&apos;éléments constitutifs, les offres
            d&apos;unités d&apos;enseignement et leurs groupes optionnels.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button asChild variant="outline">
            <Link to="/admin/working-time">Retour aux horaires</Link>
          </Button>
          <Button
            className="gap-2"
            onClick={() => {
              resetOfferingForms();
              if (filters.id_year) {
                ceForm.setValue("id_academic_year", String(filters.id_year));
                tuForm.setValue("id_academic_year", String(filters.id_year));
              }
              setOfferingTab("ec");
              setOfferingDialogOpen(true);
            }}
          >
            <Plus className="h-4 w-4" />
            Nouvelle offre
          </Button>
          <Button
            variant="outline"
            className="gap-2"
            onClick={() => {
              optionalGroupForm.reset({
                ...defaultOptionalGroupValues,
                id_journey: filters.id_journey,
                semester: filters.semester
              });
              setEditingOptionalGroupId(null);
              setOptionalGroupDialogOpen(true);
            }}
          >
            <Plus className="h-4 w-4" />
            Nouveau groupe optionnel
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
              Ajustez les filtres académiques pour cibler les offres.
            </p>
          )}
          <Button
            variant="ghost"
            size="sm"
            className="gap-2"
            onClick={() => setFiltersCollapsed((prev) => !prev)}
          >
            {filtersCollapsed ? "Afficher les filtres" : "Masquer les filtres"}
          </Button>
        </div>

        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={availableJourneys as JourneyOption[]}
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
            <h2 className="text-lg font-semibold">Offres</h2>
            <p className="text-xs text-muted-foreground">
              Créez, éditez ou supprimez les offres EC et UE.
            </p>
          </div>
          <Button
            variant="outline"
            className="gap-2"
            onClick={() => {
              resetOfferingForms();
              if (filters.id_year) {
                ceForm.setValue("id_academic_year", String(filters.id_year));
                tuForm.setValue("id_academic_year", String(filters.id_year));
              }
              setOfferingTab("ec");
              setOfferingDialogOpen(true);
            }}
          >
            <Plus className="h-4 w-4" />
            Ajouter une offre
          </Button>
        </div>

        <Tabs defaultValue="ec">
          <TabsList className="grid grid-cols-2 bg-muted mb-4">
            <TabsTrigger value="ec">Offres EC</TabsTrigger>
            <TabsTrigger value="ue">Offres UE</TabsTrigger>
          </TabsList>
          <TabsContent value="ec" className="space-y-2">
            {ceOfferings.length ? null : (
              <p className="text-xs text-muted-foreground">
                Aucune offre EC pour ces filtres.
              </p>
            )}
            {ceOfferings.map((offer: ConstituentElementOffering) => {
              const ce = (offer as any).constituent_element;
              return (
                <div
                  key={offer.id}
                  className="flex items-center justify-between rounded border bg-background px-3 py-2"
                >
                  <div className="flex flex-col">
                    <span className="font-medium">
                      {ce?.name ?? "EC"}{" "}
                      {ce?.semester ? `· ${ce.semester}` : ""}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {(offer as any).academic_year?.name ?? ""}{" "}
                      {ce?.journey?.name ?? ce?.journey?.abbreviation ?? ""}
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
                          id_constituent_element: ce?.id ? String(ce.id) : "",
                          id_academic_year: (offer as any).academic_year?.id
                            ? String((offer as any).academic_year.id)
                            : "",
                          weight: offer.weight ? String(offer.weight) : "",
                          id_constituent_element_optional_group: (offer as any)
                            .id_constituent_element_optional_group
                            ? String(
                                (offer as any)
                                  .id_constituent_element_optional_group
                              )
                            : "",
                          id_teching_unit_offering: (offer as any)
                            .id_teching_unit_offering
                            ? String((offer as any).id_teching_unit_offering)
                            : "",
                          id_teacher: (offer as any).id_teacher
                            ? String((offer as any).id_teacher)
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
                            resetOfferingForms();
                            setFeedback({
                              type: "success",
                              text: "Offre EC supprimée."
                            });
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
            {tuOfferings.length ? null : (
              <p className="text-xs text-muted-foreground">
                Aucune offre UE pour ces filtres.
              </p>
            )}
            {tuOfferings.map((offer: any) => {
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
                      {tu?.journey?.name ?? tu?.journey?.abbreviation ?? ""}
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
                          credit: offer.credit ? String(offer.credit) : "",
                          id_teaching_unit_optional_group:
                            offer.id_teaching_unit_optional_group
                              ? String(offer.id_teaching_unit_optional_group)
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
                            resetOfferingForms();
                            setFeedback({
                              type: "success",
                              text: "Offre UE supprimée."
                            });
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
        </Tabs>
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
                  min={0}
                  max={1}
                  step="0.01"
                  {...ceForm.register("weight", {
                    min: { value: 0, message: "Le poids doit être ≥ 0" },
                    max: { value: 1, message: "Le poids doit être ≤ 1" }
                  })}
                />
                {ceForm.formState.errors.weight ? (
                  <p className="text-xs text-destructive">
                    {ceForm.formState.errors.weight.message}
                  </p>
                ) : null}
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
        open={optionalGroupDialogOpen}
        onOpenChange={setOptionalGroupDialogOpen}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>Ajouter un groupe optionnel</DialogTitle>
            <DialogDescription>
              Créez ou éditez un groupe optionnel pour une offre EC ou UE.
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
            {optionalGroupTab === "ec" ? (
              <Select
                value={optionalGroupForm.watch("id_teaching_unit_offering")}
                onValueChange={(value) =>
                  optionalGroupForm.setValue(
                    "id_teaching_unit_offering",
                    value === emptySelectValue ? "" : value
                  )
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Offre UE liée (optionnelle)" />
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
            ) : null}
            <div className="rounded-md border bg-muted p-3 text-xs text-muted-foreground">
              <div className="flex flex-col gap-1">
                <span>Parcours : {currentJourneyLabel}</span>
                <span>Semestre : {currentSemester || "N/A"}</span>
              </div>
            </div>
            <Textarea
              placeholder="Règle de sélection (optionnel)"
              {...optionalGroupForm.register("selection_regle")}
            />
            <div className="flex justify-end gap-2">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setOptionalGroupDialogOpen(false)}
              >
                Annuler
              </Button>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Création…" : "Créer le groupe"}
              </Button>
            </div>
          </form>
          <div className="mt-4 rounded-md border bg-muted p-3 text-xs text-muted-foreground">
            {optionalGroupTab === "ec" ? "Groupes EC" : "Groupes UE"}
            <div className="mt-2 space-y-2">
              {(optionalGroupTab === "ec"
                ? ceOptionalGroupOptions
                : tuOptionalGroupOptions
              ).length ? null : (
                <p className="text-[11px] text-muted-foreground">
                  Aucun groupe optionnel.
                </p>
              )}
              {(optionalGroupTab === "ec"
                ? ceOptionalGroupOptions
                : tuOptionalGroupOptions
              ).map((group: any) => (
                <div
                  key={group.id}
                  className="flex items-center justify-between rounded border bg-background px-2 py-1"
                >
                  <div className="flex flex-col gap-1">
                    <span className="font-medium text-foreground">
                      {group.name ?? `Groupe ${group.id}`}
                    </span>
                    {group.description ? (
                      <span className="text-[11px] text-muted-foreground">
                        {group.description}
                      </span>
                    ) : null}
                    <div className="flex flex-wrap gap-1 text-[11px] text-muted-foreground">
                      {group.id_teaching_unit_offering ? (
                        <span className="rounded-full bg-muted px-2 py-0.5">
                          UE liée #
                          {group.teaching_unit_offering.teaching_unit?.name ??
                            group.id_teaching_unit_offering}
                        </span>
                      ) : null}
                      {group.id_journey ? (
                        <span className="rounded-full bg-muted px-2 py-0.5">
                          {
                            availableJourneys.find(
                              (j) => j.id === String(group.id_journey)
                            )?.label
                          }
                        </span>
                      ) : null}
                      {group.semester ? (
                        <span className="rounded-full bg-muted px-2 py-0.5">
                          {group.semester}
                        </span>
                      ) : null}
                      {group.selection_regle ? (
                        <span className="rounded-full bg-muted px-2 py-0.5">
                          Règle définie
                        </span>
                      ) : null}
                    </div>
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
                          description: group.description ?? "",
                          id_teaching_unit_offering:
                            group.id_teaching_unit_offering
                              ? String(group.id_teaching_unit_offering)
                              : "",
                          id_journey: group.id_journey
                            ? String(group.id_journey)
                            : "",
                          semester: group.semester ?? "",
                          selection_regle: group.selection_regle ?? ""
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
                            onSuccess: () => {
                              ceOptionalGroupsQuery.refetch();
                              setFeedback({
                                type: "success",
                                text: "Groupe optionnel EC supprimé."
                              });
                            }
                          });
                        } else {
                          deleteTUOptionalGroup.mutate(Number(group.id), {
                            onSuccess: () => {
                              tuOptionalGroupsQuery.refetch();
                              setFeedback({
                                type: "success",
                                text: "Groupe optionnel UE supprimé."
                              });
                            }
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
        </DialogContent>
      </Dialog>
    </div>
  );
};
