import { useQuery } from '@tanstack/react-query';
import {
  CalendarDays,
  Layers,
  Users,
  GraduationCap,
  FileText,
  Clock,
  Award
} from 'lucide-react';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';

import { Button } from '../../components/ui/button';
import { apiRequest } from '../../services/api-client';
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
  type ChartConfig
} from '../../components/ui/chart';

interface DashboardSummary {
  total_students: number;
  total_mentions: number;
  total_journeys: number;
  total_users: number;
  mention_counts: Array<{ id: number; name: string; count: number }>;
  academic_year_counts: Array<{ id: number; name: string; count: number }>;
  mention_enrollments: Array<{
    academic_year_id: number;
    academic_year_name: string;
    mention_id: number;
    mention_name: string;
    count: number;
  }>;
}

interface ChartData {
  name: string;
  value?: number;
  color?: string;
  yearId?: number;
  [key: string]: any;
}

const fetchDashboardMetrics = async (): Promise<DashboardSummary> =>
  apiRequest<DashboardSummary>('/dashboard/');

const buildMentionChartData = (mentions: DashboardSummary['mention_counts']): ChartData[] =>
  mentions.map((mention, index) => ({
    name: mention.name || `Mention ${mention.id}`,
    value: mention.count,
    fill: `hsl(var(--chart-${(index % 5) + 1}))`
  }));

const buildMentionTrendData = (
  enrollments: DashboardSummary['mention_enrollments']
): { data: ChartData[]; config: ChartConfig } => {
  const mentionNames = Array.from(
    new Set(
      enrollments.map(
        (enrollment) => enrollment.mention_name || `Mention ${enrollment.mention_id}`
      )
    )
  );

  const yearMap = new Map<number, ChartData>();

  enrollments.forEach((enrollment) => {
    const yearLabel = enrollment.academic_year_name || `Année ${enrollment.academic_year_id}`;
    const mentionLabel = enrollment.mention_name || `Mention ${enrollment.mention_id}`;
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
  const { data: summary, isPending } = useQuery({
    queryKey: ['dashboard', 'metrics'],
    queryFn: fetchDashboardMetrics,
    staleTime: 60_000
  });

  const mentionChartData = summary?.mention_counts ? buildMentionChartData(summary.mention_counts) : [];
  const { data: mentionTrendData, config: mentionTrendConfig } = summary?.mention_enrollments
    ? buildMentionTrendData(summary.mention_enrollments)
    : { data: [] as ChartData[], config: {} as ChartConfig };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Comprehensive overview of academic metrics and student data.
          </p>
        </div>
        <Button size="sm">Refresh data</Button>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
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
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard
          icon={Clock}
          label="Avg. processing time"
          loading
          value="—"
        />
        <MetricCard
          icon={CalendarDays}
          label="Next event"
          loading
          value="—"
        />
      </div>

      {/* Charts Section */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Progression par mention (5 dernières années) */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Progression par mention (5 dernières années)</h3>
            <p className="text-sm text-muted-foreground">
              Nombre d&apos;étudiants inscrits par mention et année universitaire (données en direct)
            </p>
          </div>
          <div className="h-80">
            {isPending ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">Loading chart...</div>
              </div>
            ) : !mentionTrendData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">No data available</div>
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
                        name={mentionTrendConfig[mentionKey as keyof typeof mentionTrendConfig].label}
                        fill={mentionTrendConfig[mentionKey as keyof typeof mentionTrendConfig].color}
                        stroke={mentionTrendConfig[mentionKey as keyof typeof mentionTrendConfig].color}
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

        {/* Students by Mention */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Répartition par mention</h3>
            <p className="text-sm text-muted-foreground">
              Nombre d'étudiants par mention (données en direct)
            </p>
          </div>
          <div className="h-80">
            {!summary ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">Loading chart...</div>
              </div>
            ) : !mentionChartData.length ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">No data available</div>
              </div>
            ) : (
              <ChartContainer
                config={
                  mentionChartData.reduce((acc, item) => {
                    acc[item.name] = { label: item.name, color: item.fill as string };
                    return acc;
                  }, {} as ChartConfig)
                }
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={mentionChartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
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

      {/* Recent Activity */}
      <div className="rounded-lg border bg-background p-6 shadow-sm">
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Recent Activity</h3>
          <p className="text-sm text-muted-foreground">
            Latest student activities and updates
          </p>
        </div>
        <div className="space-y-3">
          <ActivityItem
            icon={Award}
            title="New graduates"
            description="15 students completed their programs this week"
            time="2 hours ago"
          />
          <ActivityItem
            icon={FileText}
            title="Applications submitted"
            description="23 new applications received today"
            time="4 hours ago"
          />
          <ActivityItem
            icon={Users}
            title="Student registrations"
            description="8 new students registered for next semester"
            time="6 hours ago"
          />
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

const MetricCard = ({ icon: Icon, label, value, loading, trend }: MetricCardProps) => (
  <div className="rounded-xl border bg-background p-5 shadow-sm">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <p className="text-sm text-muted-foreground">{label}</p>
        <p className="mt-2 text-2xl font-semibold">{loading ? '…' : value}</p>
        {trend && (
          <p className={`mt-1 text-xs ${trend.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
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

const ActivityItem = ({ icon: Icon, title, description, time }: ActivityItemProps) => (
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
