import { useEffect, useMemo, useRef, useState } from "react";
import {
  useInfiniteQuery,
  useMutation,
  useQuery,
  useQueryClient
} from "@tanstack/react-query";
import {
  ChevronsDown,
  Plus,
  RefreshCw,
  Trash2,
  FileText
} from "lucide-react";

import { AcademicFilters } from "@/components/filters/academic-filters";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useLookupOptions } from "@/hooks/use-lookup-options";
import { fetchJourneys as fetchJourneysByMention } from "@/services/inscription-service";
import {
  createGroup,
  fetchGroups,
  deleteGroup
} from "@/services/group-service";
import { CreateGroupPayload } from "@/models/group";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { fetchReinscriptionsWithMeta } from "@/services/reinscription-service";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { printStudentsListByGroup } from "@/services/print-service";

type GroupFilters = {
  id_year: string;
  id_mention: string;
  id_journey: string;
  semester: string;
};

const semesters = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"];
const STORAGE_KEY = "groups.filters";
const PAGE_SIZE = 50;

export const GroupsPage = () => {
  const { mentionOptions } = useLookupOptions({
    includeMentions: true
  });

  const resolveHeaderAcademicYear = () => {
    if (typeof window === "undefined") return "";
    const stored = window.localStorage.getItem("selected_academic_year");
    if (!stored || stored === "all") return "";
    return stored;
  };

  const readStoredFilters = (): GroupFilters | null => {
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
        return parsed as GroupFilters;
      }
    } catch {
      return null;
    }
    return null;
  };

  const [filters, setFilters] = useState<GroupFilters>(() => {
    const stored = readStoredFilters();
    return (
      stored ?? {
        id_year: resolveHeaderAcademicYear(),
        id_mention: "",
        id_journey: "",
        semester: semesters[0]
      }
    );
  });

  useEffect(() => {
    if (!mentionOptions.length) return;
    setFilters((prev) => ({
      ...prev,
      id_mention: prev.id_mention || mentionOptions[0].id
    }));
  }, [mentionOptions]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
    }
  }, [filters]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const handleYearChange = (event: Event) => {
      const detail = (event as CustomEvent<string | null>).detail;
      const nextYear =
        typeof detail === "string"
          ? detail
          : window.localStorage.getItem("selected_academic_year");
      setFilters((prev) => ({
        ...prev,
        id_year: nextYear && nextYear !== "all" ? nextYear : ""
      }));
    };
    window.addEventListener("academicYearChanged", handleYearChange);
    window.addEventListener("storage", handleYearChange);
    return () => {
      window.removeEventListener("academicYearChanged", handleYearChange);
      window.removeEventListener("storage", handleYearChange);
    };
  }, []);

  const journeyQuery = useQuery({
    queryKey: ["groups", "journeys", filters.id_mention],
    queryFn: () => fetchJourneysByMention(Number(filters.id_mention)),
    enabled: Boolean(filters.id_mention)
  });

  const journeyOptions = useMemo(
    () =>
      (journeyQuery.data ?? []).map((journey: any) => ({
        id: String(journey.id),
        label: journey.name ?? journey.abbreviation ?? `Parcours ${journey.id}`,
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
    [filters.id_mention, journeyQuery.data]
  );

  useEffect(() => {
    const firstJourney = journeyOptions[0];
    if (!firstJourney) return;
    setFilters((prev) => {
      if (prev.id_journey) return prev;
      const nextSemester =
        (firstJourney as any).semesterList?.[0] ?? prev.semester ?? semesters[0];
      return {
        ...prev,
        id_journey: firstJourney.id,
        semester: semesters.includes(nextSemester) ? nextSemester : semesters[0]
      };
    });
  }, [journeyOptions]);

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
  if (filters.id_year) {
    wheres.push({
      key: "id_academic_year",
      operator: "==",
      value: Number(filters.id_year)
    });
  }

  const groupQuery = useInfiniteQuery({
    queryKey: ["groups", filters],
    queryFn: ({ pageParam = 0 }) =>
      fetchGroups({
        where: JSON.stringify(wheres),
        relation: JSON.stringify(["journey{id,name,abbreviation,id_mention}"]),
        limit: PAGE_SIZE,
        offset: pageParam,
        academic_year_id: filters.id_year || undefined
      } as any),
    getNextPageParam: (lastPage, allPages) => {
      const totalFetched = allPages.reduce(
        (acc, page) => acc + (page.data?.length ?? 0),
        0
      );
      if (lastPage.count !== undefined && totalFetched >= (lastPage.count ?? 0)) {
        return undefined;
      }
      if (!lastPage.data?.length) return undefined;
      return totalFetched;
    },
    initialPageParam: 0
  });

  const groups = useMemo(
    () => groupQuery.data?.pages.flatMap((page) => page.data ?? []) ?? [],
    [groupQuery.data?.pages]
  );

  const totalGroups = groups.length;
  const totalStudentsFromGroups = groups.reduce(
    (acc, group) => acc + (group.student_count ?? 0),
    0
  );

  const sentinelRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!sentinelRef.current) return;
    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (entry.isIntersecting && groupQuery.hasNextPage && !groupQuery.isFetching) {
          groupQuery.fetchNextPage();
        }
      },
      { rootMargin: "120px" }
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [groupQuery.hasNextPage, groupQuery.isFetching, groupQuery.fetchNextPage]);

  const handleFiltersChange = (next: any) => {
    setFilters((prev) => ({
      ...prev,
      id_mention: next.id_mention,
      id_journey: next.id_journey,
      semester: next.semester
    }));
  };

  const { data: studentCountData, isFetching: isFetchingStudents } = useQuery({
    queryKey: ["groups", "students-count", filters],
    enabled: Boolean(filters.id_journey && filters.id_year),
    queryFn: () =>
      fetchReinscriptionsWithMeta({
        id_year: filters.id_year,
        id_mention: filters.id_mention,
        id_journey: filters.id_journey,
        semester: filters.semester,
        limit: 1,
        offset: 0
      } as any)
  });

  const totalStudents = studentCountData?.count ?? 0;

  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [groupCountInput, setGroupCountInput] = useState<number>(2);
  const [isBulkDeleteOpen, setIsBulkDeleteOpen] = useState(false);

  const maxExistingGroupNumber = useMemo(
    () =>
      groups.reduce(
        (acc, group) =>
          group.group_number !== null && group.group_number !== undefined
            ? Math.max(acc, Number(group.group_number))
            : acc,
        0
      ),
    [groups]
  );
  const maxExistingEndNumber = useMemo(
    () =>
      groups.reduce(
        (acc, group) =>
          group.end_number !== null && group.end_number !== undefined
            ? Math.max(acc, Number(group.end_number))
            : acc,
        0
      ),
    [groups]
  );

  const desiredGroups = Math.max(1, groupCountInput || 1);
  const basePerGroup =
    desiredGroups > 0 && totalStudents > 0
      ? Math.floor(totalStudents / desiredGroups)
      : 0;
  const remainder =
    desiredGroups > 0 && totalStudents > 0
      ? totalStudents % desiredGroups
      : 0;
  const totalGroupsToCreate = desiredGroups;

  const queryClient = useQueryClient();
  const createGroupMutation = useMutation({
    mutationFn: createGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["groups"] });
    }
  });
  const bulkDeleteMutation = useMutation({
    mutationFn: async (ids: number[]) => {
      await Promise.all(ids.map((id) => deleteGroup(id)));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["groups"] });
    }
  });

  const handleCreateGroups = async () => {
    if (!filters.id_journey || !filters.semester) return;
    if (!totalStudents) return;
    const groupCounts = Array.from({ length: totalGroupsToCreate }).map(
      () => basePerGroup
    );
    const bucketsToFill =
      remainder > 0 ? Math.min(remainder, totalGroupsToCreate) : 0; // spread remainder across as many groups as remainder
    for (let i = 0; i < remainder; i++) {
      const targetIndex =
        totalGroupsToCreate - 1 - (i % bucketsToFill); // distribute to last bucketsToFill groups
      groupCounts[targetIndex] = (groupCounts[targetIndex] || 0) + 1;
    }

    let currentStart = maxExistingEndNumber ? maxExistingEndNumber + 1 : 1;
    const payloads = groupCounts.map((count, index) => {
      const group_number = maxExistingGroupNumber + index + 1;
      const student_count = count;
      const start_number = currentStart;
      const end_number = Math.max(currentStart + (student_count || 0) - 1, currentStart);
      currentStart = end_number + 1;
      return {
        id_journey: Number(filters.id_journey),
        semester: filters.semester,
        group_number,
        student_count,
        start_number,
        end_number,
        id_academic_year: filters.id_year ? Number(filters.id_year) : undefined
      };
    });
    try {
      for (const payload of payloads) {
        await createGroupMutation.mutateAsync(payload);
      }
      setIsCreateOpen(false);
      setGroupCountInput(2);
      groupQuery.refetch();
    } catch (error) {
      console.error(error);
    }
  };

  const [isPrinting, setIsPrinting] = useState(false);

  const fetchAllGroupIds = async () => {
    const ids: number[] = [];
    let offset = 0;
    while (true) {
      const page = await fetchGroups({
        where: JSON.stringify(wheres),
        relation: JSON.stringify(["journey{id,name,abbreviation,id_mention}"]),
        limit: PAGE_SIZE,
        offset,
        academic_year_id: filters.id_year || undefined
      } as any);
      const pageIds =
        page.data
          ?.map((group) => Number(group.id))
          .filter((id) => !Number.isNaN(id)) ?? [];
      ids.push(...pageIds);
      const totalCount = page.count ?? ids.length;
      offset += PAGE_SIZE;
      if (!page.data?.length || ids.length >= totalCount) {
        break;
      }
    }
    return Array.from(new Set(ids));
  };

  const handleBulkDelete = async () => {
    let ids: number[] = [];
    try {
      ids = await fetchAllGroupIds();
      if (!ids.length) {
        setIsBulkDeleteOpen(false);
        return;
      }
      await bulkDeleteMutation.mutateAsync(ids);
    } catch (error) {
      console.error(error);
    } finally {
      setIsBulkDeleteOpen(false);
    }
  };

  const handlePrintByGroup = async () => {
    if (!filters.id_year || !filters.id_journey || !filters.semester) return;
    try {
      setIsPrinting(true);
      const pdf = await printStudentsListByGroup({
        idYear: filters.id_year,
        semester: filters.semester,
        journeyId: filters.id_journey
      });
      if (pdf?.url) {
        window.open(pdf.url, "_blank");
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsPrinting(false);
    }
  };

  const selectedJourneyLabel =
    journeyOptions.find((j) => j.id === filters.id_journey)?.label ?? "";

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Groupes</h1>
          <p className="text-sm text-muted-foreground">
            Gérez les groupes par parcours et semestre. Le nombre d&apos;étudiants est
            calculé selon les inscriptions du semestre.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() => groupQuery.refetch()}
          >
            <RefreshCw className={cn("h-4 w-4", groupQuery.isFetching && "animate-spin")} />
            Rafraîchir
          </Button>
          <Button
            size="sm"
            className="gap-2"
            onClick={() => setIsCreateOpen(true)}
            disabled={!filters.id_journey || !filters.semester}
          >
            <Plus className="h-4 w-4" />
            Créer des groupes
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="gap-2"
            disabled={
              !filters.id_year ||
              !filters.id_journey ||
              !filters.semester ||
              isPrinting
            }
            onClick={handlePrintByGroup}
          >
            <FileText className={cn("h-4 w-4", isPrinting && "animate-spin")} />
            Liste par groupe
          </Button>
          <Button
            size="sm"
            variant="destructive"
            className="gap-2"
            disabled={
              !filters.id_year ||
              !filters.id_journey ||
              !filters.semester ||
              bulkDeleteMutation.isPending ||
              !groups.length
            }
            onClick={() => setIsBulkDeleteOpen(true)}
          >
            <Trash2 className={cn("h-4 w-4", bulkDeleteMutation.isPending && "animate-spin")} />
            Supprimer les groupes
          </Button>
        </div>
      </div>

      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={journeyOptions}
          semesters={semesters}
          showLevel={false}
          showResetButton={false}
          showActiveFilters
          filterClassname="grid gap-4 lg:grid-cols-2"
        />
      </div>

      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2">
        <div className="rounded-lg border bg-background p-4 shadow-sm">
          <p className="text-xs text-muted-foreground">Groupes trouvés</p>
          <p className="text-2xl font-semibold">{totalGroups}</p>
        </div>
        <div className="rounded-lg border bg-background p-4 shadow-sm">
          <p className="text-xs text-muted-foreground">Étudiants (somme des groupes)</p>
          <p className="text-2xl font-semibold">{totalStudentsFromGroups}</p>
        </div>
      </div>

      <div className="rounded-lg border bg-background shadow-sm">
        <div className="flex items-center justify-between border-b px-4 py-3">
          <div>
            <p className="text-sm font-medium">
              Groupes · {filters.semester || "Semestre"}{" "}
              {journeyOptions.find((j) => j.id === filters.id_journey)?.label ?? ""}{" "}
              {totalStudents ? `(${totalStudents} étudiants)` : ""}
            </p>
            <p className="text-xs text-muted-foreground">
              {groupQuery.isFetching
                ? "Chargement..."
                : groupQuery.data?.pages?.[0]?.count
                  ? `${groupQuery.data.pages[0].count} groupe(s) au total`
                  : "Aucun groupe trouvé"}
            </p>
          </div>
        </div>
        <div className="max-h-[520px] overflow-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-muted/60 text-left">
              <tr>
                <th className="px-4 py-2 font-medium"># Groupe</th>
                <th className="px-4 py-2 font-medium">Parcours</th>
                <th className="px-4 py-2 font-medium">Semestre</th>
                <th className="px-4 py-2 font-medium">Début</th>
                <th className="px-4 py-2 font-medium">Fin</th>
                <th className="px-4 py-2 font-medium">Étudiants</th>
              </tr>
            </thead>
            <tbody>
              {groups.map((group) => (
                <tr key={group.id} className="border-b last:border-b-0">
                  <td className="px-4 py-2">
                    {group.group_number ?? "—"}
                  </td>
                  <td className="px-4 py-2">
                    {group.journey?.name ??
                      group.journey?.abbreviation ??
                      `Parcours ${group.id_journey ?? ""}`}
                  </td>
                  <td className="px-4 py-2">{group.semester ?? "—"}</td>
                  <td className="px-4 py-2">{group.start_number ?? "—"}</td>
                  <td className="px-4 py-2">{group.end_number ?? "—"}</td>
                  <td className="px-4 py-2">
                    {group.student_count !== null && group.student_count !== undefined
                      ? group.student_count
                      : "—"}
                  </td>
                </tr>
              ))}
              {!groups.length && !groupQuery.isFetching ? (
                <tr>
                  <td
                    colSpan={6}
                    className="px-4 py-6 text-center text-muted-foreground text-sm"
                  >
                    Aucun groupe pour ces filtres.
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
          <div ref={sentinelRef} className="flex items-center justify-center py-3">
            {groupQuery.hasNextPage ? (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <ChevronsDown className="h-4 w-4" />
                Charger plus en faisant défiler...
              </div>
            ) : null}
          </div>
        </div>
      </div>

      <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Créer des groupes</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="rounded-md border bg-muted p-3 text-xs text-muted-foreground space-y-1">
              <div>Parcours : {journeyOptions.find((j) => j.id === filters.id_journey)?.label ?? "N/A"}</div>
              <div>Semestre : {filters.semester}</div>
              <div>
                Étudiants inscrits :{" "}
                {isFetchingStudents ? "Calcul..." : totalStudents}
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="group-count-input">
                Nombre de groupes souhaités
              </label>
              <Input
                id="group-count-input"
                type="number"
                min={1}
                value={groupCountInput}
                onChange={(e) => setGroupCountInput(Math.max(1, Number(e.target.value) || 1))}
              />
              <p className="text-xs text-muted-foreground">
                Répartition estimée : {totalGroupsToCreate} groupe(s) ·{" "}
                {basePerGroup || "-"} étudiants/groupe
                {remainder > 0
                  ? ` (répartition du reste sur les ${Math.min(remainder, totalGroupsToCreate)} derniers groupes : ${remainder})`
                  : ""}
              </p>
            </div>
            <div className="flex items-center justify-end gap-2">
              <Button variant="ghost" onClick={() => setIsCreateOpen(false)}>
                Annuler
              </Button>
              <Button
                onClick={handleCreateGroups}
                disabled={
                  !totalStudents ||
                  createGroupMutation.isPending ||
                  isFetchingStudents
                }
              >
                {createGroupMutation.isPending ? "Création..." : "Créer"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={isBulkDeleteOpen}
        title="Supprimer les groupes"
        description={
          groups.length ? (
            <>
              Supprimer tous les groupes du semestre{" "}
              <strong>{filters.semester}</strong> pour le parcours{" "}
              <strong>{selectedJourneyLabel || "N/A"}</strong>
              {filters.id_year ? (
                <>
                  {" "}
                  de l&apos;année académique <strong>{filters.id_year}</strong>
                </>
              ) : null}
              ?
            </>
          ) : (
            "Aucun groupe correspondant à supprimer."
          )
        }
        destructive
        confirmLabel={bulkDeleteMutation.isPending ? "Suppression..." : "Supprimer"}
        isConfirming={bulkDeleteMutation.isPending}
        onCancel={() => setIsBulkDeleteOpen(false)}
        onConfirm={handleBulkDelete}
      />
    </div>
  );
};
