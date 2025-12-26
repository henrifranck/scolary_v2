import { useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import {
  CalendarDays,
  Layers,
  Users,
  GraduationCap,
  FileText,
  Clock,
  Award
} from "lucide-react";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar
} from "recharts";

import { Button } from "../../components/ui/button";
import { apiRequest } from "../../services/api-client";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
  type ChartConfig
} from "../../components/ui/chart";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "../../components/ui/select";
import { Input } from "../../components/ui/input";
import { useMentions } from "../../services/mention-service";
import { useJourneys } from "../../services/journey-service";

interface DashboardSummary {
  total_students: number;
  total_mentions: number;
  total_journeys: number;
  total_users: number;
  mention_counts: Array<{ id: number; name: string; count: number }>;
  mention_enrollments: Array<{
    academic_year_id: number;
    academic_year_name: string;
    mention_id: number;
    mention_name: string;
    count: number;
  }>;
  new_student_mention_enrollments: Array<{
    academic_year_id: number;
    academic_year_name: string;
    mention_id: number;
    mention_name: string;
    count: number;
  }>;

  age_distribution: Array<{ age: number; count: number }>;
  sex_counts: Array<{ sex: string; count: number }>;
  mention_sex_counts: Array<{
    mention_id: number;
    mention_name: string;
    sex: string;
    count: number;
  }>;
  nationality_counts: Array<{ id: number; name: string; count: number }>;
  role_counts: Array<{ role: string; count: number }>;
}

interface ChartData {
  name: string;
  value?: number;
  color?: string;
  yearId?: number;
  [key: string]: any;
}

const fetchDashboardMetrics = async (
  query?: Record<string, string | number | boolean | undefined>
): Promise<DashboardSummary> =>
  apiRequest<DashboardSummary>("/dashboard/", { query });

const buildMentionChartData = (
  mentions: DashboardSummary["mention_counts"]
): ChartData[] =>
  mentions.map((mention, index) => ({
    name: mention.name || `Mention ${mention.id}`,
    value: mention.count,
    fill: `hsl(var(--chart-${(index % 5) + 1}))`
  }));

const buildMentionTrendData = (
  enrollments:
    | DashboardSummary["mention_enrollments"]
    | DashboardSummary["new_student_mention_enrollments"]
): { data: ChartData[]; config: ChartConfig } => {
  const mentionNames = Array.from(
    new Set(
      enrollments.map(
        (enrollment) =>
          enrollment.mention_name || `Mention ${enrollment.mention_id}`
      )
    )
  );

  const yearMap = new Map<number, ChartData>();

  enrollments.forEach((enrollment) => {
    const yearLabel =
      enrollment.academic_year_name || `Année ${enrollment.academic_year_id}`;
    const mentionLabel =
      enrollment.mention_name || `Mention ${enrollment.mention_id}`;
    const existing = yearMap.get(enrollment.academic_year_id) ?? {
      name: yearLabel,
      yearId: enrollment.academic_year_id
    };

    existing[mentionLabel] = enrollment.count;
    yearMap.set(enrollment.academic_year_id, existing);
  });

  const data = Array.from(yearMap.values())
    .sort((a, b) => (a.name as string).localeCompare(b.name as string))
    .map((row) => {
      mentionNames.forEach((mentionName) => {
        if (row[mentionName] === undefined) {
          row[mentionName] = 0;
        }
      });
      return row;
    });

  const config: ChartConfig = {};
  mentionNames.forEach((mentionName, index) => {
    config[mentionName] = {
      label: mentionName,
      color: `hsl(var(--chart-${(index % 5) + 1}))`
    };
  });

  return { data, config };
};

export const DashboardPage = () => {
  const [minAge, setMinAge] = useState(16);
  const [maxAge, setMaxAge] = useState(32);
  const [mentionFilter, setMentionFilter] = useState<string>("all");
  const [academicYearFilter, setAcademicYearFilter] = useState<string>("all");
  const [journeyFilter, setJourneyFilter] = useState<string>("all");
  const [headerAcademicYear, setHeaderAcademicYear] = useState<string | null>(
    () =>
      typeof window !== "undefined"
        ? window.localStorage.getItem("selected_academic_year")
        : null
  );

  const { data: mentionsData } = useMentions();
  const { data: journeysData } = useJourneys(
    mentionFilter !== "all"
      ? {
          where: JSON.stringify([
            { key: "id_mention", operator: "==", value: Number(mentionFilter) }
          ])
        }
      : undefined
  );

  const mentionOptions = useMemo(
    () => [
      { value: "all", label: "Toutes les mentions" },
      ...(mentionsData?.data ?? []).map((mention) => ({
        value: mention.id.toString(),
        label: mention.name
      }))
    ],
    [mentionsData]
  );

  const journeyOptions = useMemo(() => {
    const base = journeysData?.data ?? [];
    const filtered =
      mentionFilter === "all"
        ? base
        : base.filter(
            (journey) =>
              String((journey as any).id_mention ?? journey.mention?.id) ===
              mentionFilter
          );
    return [
      { value: "all", label: "Tous les parcours" },
      ...filtered.map((journey) => ({
        value: journey.id.toString(),
        label: journey.name
      }))
    ];
  }, [journeysData, mentionFilter]);

  useEffect(() => {
    const handleYearChange = (event: Event) => {
      const next = (event as CustomEvent<string>).detail || null;
      setHeaderAcademicYear(next);
      setAcademicYearFilter(next ?? "all");
    };
    const syncFromStorage = () => {
      if (typeof window === "undefined") return;
      const stored = window.localStorage.getItem("selected_academic_year");
      if (stored) {
        setHeaderAcademicYear(stored);
        setAcademicYearFilter(stored);
      }
    };
    window.addEventListener(
      "academicYearChanged",
      handleYearChange as EventListener
    );
    window.addEventListener("storage", syncFromStorage);
    syncFromStorage();
    return () => {
      window.removeEventListener(
        "academicYearChanged",
        handleYearChange as EventListener
      );
      window.removeEventListener("storage", syncFromStorage);
    };
  }, []);

  const {
    data: summary,
    isPending,
    refetch
  } = useQuery({
    queryKey: [
      "dashboard",
      "metrics",
      minAge,
      maxAge,
      mentionFilter,
      academicYearFilter,
      headerAcademicYear,
      journeyFilter
    ],
    queryFn: () =>
      fetchDashboardMetrics({
        min_age: minAge,
        max_age: maxAge,
        mention_id: mentionFilter !== "all" ? Number(mentionFilter) : undefined,
        academic_year_id: (() => {
          const fromFilter =
            academicYearFilter !== "all"
              ? Number(academicYearFilter)
              : undefined;
          if (fromFilter !== undefined && !Number.isNaN(fromFilter)) {
            return fromFilter;
          }
          if (headerAcademicYear && headerAcademicYear !== "all") {
            const parsed = Number(headerAcademicYear);
            return Number.isNaN(parsed) ? undefined : parsed;
          }
          return undefined;
        })(),
        journey_id: journeyFilter !== "all" ? Number(journeyFilter) : undefined
      }),
    staleTime: 60_000
  });

  const mentionChartData = summary?.mention_counts
    ? buildMentionChartData(summary.mention_counts)
    : [];

  const { data: mentionTrendData, config: mentionTrendConfig } =
    summary?.mention_enrollments
      ? buildMentionTrendData(summary.mention_enrollments)
      : { data: [] as ChartData[], config: {} as ChartConfig };

  const {
    data: newStudentmentionTrendData,
    config: newStudentmentionTrendConfig
  } = summary?.new_student_mention_enrollments
    ? buildMentionTrendData(summary.new_student_mention_enrollments)
    : { data: [] as ChartData[], config: {} as ChartConfig };

  const ageChartData = useMemo(
    () =>
      summary?.age_distribution?.map((bucket) => ({
        name: `${bucket.age}`,
        count: bucket.count
      })) ?? [],
    [summary?.age_distribution]
  );

  const ageChartConfig: ChartConfig = {
    count: { label: "Étudiants", color: "hsl(var(--chart-1))" }
  };

  const sexChartData =
    summary?.sex_counts?.map((row, index) => ({
      name: row.sex || "—",
      value: row.count,
      fill: `hsl(var(--chart-${(index % 5) + 1}))`
    })) ?? [];

  const roleChartData =
    summary?.role_counts?.map((row, index) => ({
      name: row.role || "—",
      value: row.count,
      fill: `hsl(var(--chart-${(index % 5) + 1}))`
    })) ?? [];

  const mentionSexChart = useMemo(() => {
    const rows = summary?.mention_sex_counts ?? [];
    const sexes = Array.from(new Set(rows.map((row) => row.sex || "—")));
    const mentionMap = new Map<number, ChartData>();

    rows.forEach((row) => {
      const key = row.mention_id;
      const existing = mentionMap.get(key) ?? {
        name: row.mention_name || `Mention ${row.mention_id}`,
        mentionId: row.mention_id
      };
      existing[row.sex || "—"] = row.count;
      mentionMap.set(key, existing);
    });

    const data = Array.from(mentionMap.values()).map((item) => {
      sexes.forEach((sex) => {
        if (item[sex] === undefined) {
          item[sex] = 0;
        }
      });
      return item;
    });

    const config: ChartConfig = {};
    sexes.forEach((sex, index) => {
      config[sex] = {
        label: sex,
        color: `hsl(var(--chart-${(index % 5) + 1}))`
      };
    });

    return { data, config, sexes };
  }, [summary?.mention_sex_counts]);

  const nationalityChartData =
    summary?.nationality_counts?.map((row, index) => ({
      name: row.name || `Nationalité ${row.id}`,
      value: row.count,
      fill: `hsl(var(--chart-${(index % 5) + 1}))`
    })) ?? [];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Comprehensive overview of academic metrics and student data.
          </p>
        </div>
        <Button size="sm" onClick={() => refetch()}>
          Refresh data
        </Button>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          icon={Users}
          label="Total students"
          loading={isPending}
          value={summary?.total_students ?? 0}
          trend="+0%"
        />
        <MetricCard
          icon={Layers}
          label="Total mentions"
          loading={isPending}
          value={summary?.total_mentions ?? 0}
          trend="+0%"
        />
        <MetricCard
          icon={GraduationCap}
          label="Total journeys"
          loading={isPending}
          value={summary?.total_journeys ?? 0}
          trend="+0%"
        />
        <MetricCard
          icon={FileText}
          label="Total users"
          loading={isPending}
          value={summary?.total_users ?? 0}
          trend="+0%"
        />
      </div>

      {/* Secondary Metrics */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 xl:grid-cols-3">
        <MetricCard
          icon={Clock}
          label="Avg. processing time"
          loading
          value="—"
        />
        <MetricCard icon={CalendarDays} label="Next event" loading value="—" />
      </div>

      {/* Charts Section */}
      <div className="grid gap-6 grid-cols-1 xl:grid-cols-1">
        {/* Progression par mention (5 dernières années) */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">
              Progression par mention (5 dernières années)
            </h3>
            <p className="text-sm text-muted-foreground">
              Nombre d&apos;étudiants ré-inscrits par mention et année
              universitaire (données en direct)
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {isPending ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !mentionTrendData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer config={mentionTrendConfig} className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={mentionTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                    {Object.keys(mentionTrendConfig).map((mentionKey) => (
                      <Line
                        key={mentionKey}
                        dataKey={mentionKey}
                        name={
                          mentionTrendConfig[
                            mentionKey as keyof typeof mentionTrendConfig
                          ].label
                        }
                        fill={
                          mentionTrendConfig[
                            mentionKey as keyof typeof mentionTrendConfig
                          ].color
                        }
                        stroke={
                          mentionTrendConfig[
                            mentionKey as keyof typeof mentionTrendConfig
                          ].color
                        }
                        strokeWidth={2}
                        dot={{ r: 3 }}
                        isAnimationActive={false}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>
      </div>

      {/* Gender distribution */}
      <div className="grid gap-6 grid-cols-1 xl:grid-cols-2">
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">
              Répartition par sexe et mention
            </h3>
            <p className="text-sm text-muted-foreground">
              Comparaison des mentions par sexe (filtres appliqués)
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {!summary ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !mentionSexChart.data.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer
                config={mentionSexChart.config}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={mentionSexChart.data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" tickLine={false} />
                    <YAxis allowDecimals={false} />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                    {mentionSexChart.sexes.map((sex) => (
                      <Bar
                        key={sex}
                        dataKey={sex}
                        name={mentionSexChart.config[sex].label}
                        fill={mentionSexChart.config[sex].color}
                        radius={[4, 4, 0, 0]}
                        stackId="sex"
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>

        {/* Students by Mention */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Répartition par mention</h3>
            <p className="text-sm text-muted-foreground">
              Nombre d'étudiants par mention (données en direct)
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {!summary ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !mentionChartData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer
                config={mentionChartData.reduce((acc, item) => {
                  acc[item.name] = {
                    label: item.name,
                    color: item.fill as string
                  };
                  return acc;
                }, {} as ChartConfig)}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={mentionChartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: any) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="hsl(var(--chart-1))"
                      dataKey="value"
                    >
                      {mentionChartData?.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>
      </div>

      {/* Age distribution */}
      <div className="rounded-lg border bg-background p-6 shadow-sm">
        <div className="mb-4 space-y-3">
          <div>
            <h3 className="text-lg font-semibold">Répartition par âge</h3>
            <p className="text-sm text-muted-foreground">
              Nombre d&apos;étudiants par âge (filtres mention/parcours/année
              appliqués)
            </p>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">
                Mention
              </label>
              <Select
                value={mentionFilter}
                onValueChange={(value) => {
                  setMentionFilter(value);
                  setJourneyFilter("all");
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Choisir une mention" />
                </SelectTrigger>
                <SelectContent>
                  {mentionOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">
                Parcours
              </label>
              <Select value={journeyFilter} onValueChange={setJourneyFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Choisir un parcours" />
                </SelectTrigger>
                <SelectContent>
                  {journeyOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-3">
              <label className="text-sm font-medium text-muted-foreground">
                Âge minimum
              </label>
              <Input
                type="number"
                min={0}
                value={minAge}
                onChange={(event) => setMinAge(Number(event.target.value) || 0)}
              />
            </div>

            <div className="space-y-3">
              <label className="text-sm font-medium text-muted-foreground">
                Âge maximum
              </label>
              <Input
                type="number"
                min={minAge}
                value={maxAge}
                onChange={(event) => setMaxAge(Number(event.target.value) || 0)}
              />
            </div>
          </div>
        </div>

        <div className="h-72 md:h-80 min-h-[280px]">
          {isPending ? (
            <div className="flex h-full items-center justify-center">
              <div className="text-sm text-muted-foreground">
                Loading chart...
              </div>
            </div>
          ) : !ageChartData.length ? (
            <div className="flex h-full items-center justify-center">
              <div className="text-sm text-muted-foreground">
                No data available
              </div>
            </div>
          ) : (
            <ChartContainer config={ageChartConfig} className="h-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={ageChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tickLine={false} />
                  <YAxis allowDecimals={false} />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <ChartLegend content={<ChartLegendContent />} />
                  <Bar
                    dataKey="count"
                    name={ageChartConfig.count.label}
                    fill={ageChartConfig.count.color}
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </ChartContainer>
          )}
        </div>
      </div>

      <div className="grid gap-6 grid-cols-3 xl:grid-cols-3">
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Répartition par sexe</h3>
            <p className="text-sm text-muted-foreground">
              Vue globale des étudiants par sexe (filtres appliqués)
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {!summary ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !sexChartData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer
                config={sexChartData.reduce((acc, item) => {
                  acc[item.name] = {
                    label: item.name,
                    color: item.fill as string
                  };
                  return acc;
                }, {} as ChartConfig)}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={sexChartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: any) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="hsl(var(--chart-1))"
                      dataKey="value"
                    >
                      {sexChartData?.map((entry, index) => (
                        <Cell key={`sex-cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>
        {/* Nationality distribution */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">
              Répartition par nationalité
            </h3>
            <p className="text-sm text-muted-foreground">
              Nombre d&apos;étudiants par nationalité (toutes mentions)
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {!summary ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !nationalityChartData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer
                config={nationalityChartData.reduce((acc, item) => {
                  acc[item.name] = {
                    label: item.name,
                    color: item.fill as string
                  };
                  return acc;
                }, {} as ChartConfig)}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={nationalityChartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: any) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="hsl(var(--chart-1))"
                      dataKey="value"
                    >
                      {nationalityChartData?.map((entry, index) => (
                        <Cell key={`nat-cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>

        {/* Roles distribution */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Utilisateurs par rôle</h3>
            <p className="text-sm text-muted-foreground">
              Comptes regroupés par rôle
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {!summary ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !roleChartData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer
                config={roleChartData.reduce((acc, item) => {
                  acc[item.name] = {
                    label: item.name,
                    color: item.fill as string
                  };
                  return acc;
                }, {} as ChartConfig)}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={roleChartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: any) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="hsl(var(--chart-1))"
                      dataKey="value"
                    >
                      {roleChartData?.map((entry, index) => (
                        <Cell key={`role-cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid gap-6 grid-cols-1 xl:grid-cols-1">
        {/* Progression par mention (5 dernières années) */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">
              Progression des nouveaux étudiants par mention (5 dernières
              années)
            </h3>
            <p className="text-sm text-muted-foreground">
              Nombre d&apos;étudiants inscrits par mention et année
              universitaire (données en direct)
            </p>
          </div>
          <div className="h-72 md:h-80 min-h-[280px]">
            {isPending ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  Loading chart...
                </div>
              </div>
            ) : !newStudentmentionTrendData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">
                  No data available
                </div>
              </div>
            ) : (
              <ChartContainer
                config={newStudentmentionTrendConfig}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={newStudentmentionTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <ChartLegend content={<ChartLegendContent />} />
                    {Object.keys(newStudentmentionTrendConfig).map(
                      (mentionKey) => (
                        <Line
                          key={mentionKey}
                          dataKey={mentionKey}
                          name={
                            newStudentmentionTrendConfig[
                              mentionKey as keyof typeof newStudentmentionTrendConfig
                            ].label
                          }
                          fill={
                            newStudentmentionTrendConfig[
                              mentionKey as keyof typeof newStudentmentionTrendConfig
                            ].color
                          }
                          stroke={
                            newStudentmentionTrendConfig[
                              mentionKey as keyof typeof newStudentmentionTrendConfig
                            ].color
                          }
                          strokeWidth={2}
                          dot={{ r: 3 }}
                          isAnimationActive={false}
                        />
                      )
                    )}
                  </LineChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

interface MetricCardProps {
  label: string;
  value: number | string;
  loading?: boolean;
  icon: React.ComponentType<{ className?: string }>;
  trend?: string;
}

const MetricCard = ({
  icon: Icon,
  label,
  value,
  loading,
  trend
}: MetricCardProps) => (
  <div className="rounded-xl border bg-background p-5 shadow-sm">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <p className="text-sm text-muted-foreground">{label}</p>
        <p className="mt-2 text-2xl font-semibold">{loading ? "…" : value}</p>
        {trend && (
          <p
            className={`mt-1 text-xs ${trend.startsWith("+") ? "text-green-600" : "text-red-600"}`}
          >
            {trend} from last month
          </p>
        )}
      </div>
      <Icon className="h-5 w-5 text-muted-foreground" />
    </div>
  </div>
);

interface ActivityItemProps {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  time: string;
}

const ActivityItem = ({
  icon: Icon,
  title,
  description,
  time
}: ActivityItemProps) => (
  <div className="flex items-start gap-3 rounded-lg border bg-muted/20 p-4">
    <div className="rounded-full bg-primary/10 p-2">
      <Icon className="h-4 w-4 text-primary" />
    </div>
    <div className="flex-1">
      <h4 className="text-sm font-medium">{title}</h4>
      <p className="text-xs text-muted-foreground">{description}</p>
      <p className="mt-1 text-xs text-muted-foreground">{time}</p>
    </div>
  </div>
);
