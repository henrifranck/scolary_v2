import { useQuery } from '@tanstack/react-query';
import {
  CalendarDays,
  Layers,
  Users,
  GraduationCap,
  FileText,
  Clock,
  TrendingUp,
  Award
} from 'lucide-react';
import {
  BarChart,
  Bar,
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
}

interface ChartData {
  name: string;
  value: number;
  color?: string;
  [key: string]: any;
}

interface TimeSeriesData {
  month: string;
  inscriptions: number;
  graduations: number;
}

const fetchDashboardMetrics = async (): Promise<DashboardSummary> =>
  apiRequest<DashboardSummary>('/dashboard/');

const fetchEnrollmentData = async (): Promise<TimeSeriesData[]> => {
  await new Promise((resolve) => setTimeout(resolve, 300));
  return [
    { month: 'Jan', inscriptions: 45, graduations: 38 },
    { month: 'Feb', inscriptions: 52, graduations: 42 },
    { month: 'Mar', inscriptions: 48, graduations: 45 },
    { month: 'Apr', inscriptions: 61, graduations: 39 },
    { month: 'May', inscriptions: 55, graduations: 52 },
    { month: 'Jun', inscriptions: 67, graduations: 48 }
  ];
};

const fetchProgramDistribution = async (): Promise<ChartData[]> => {
  await new Promise((resolve) => setTimeout(resolve, 200));
  return [
    { name: 'Web Development', value: 120, fill: 'hsl(var(--chart-1))' },
    { name: 'Cloud & DevOps', value: 85, fill: 'hsl(var(--chart-2))' },
    { name: 'Embedded Systems', value: 65, fill: 'hsl(var(--chart-3))' },
    { name: 'Robotics', value: 45, fill: 'hsl(var(--chart-4))' },
    { name: 'Digital Marketing', value: 35, fill: 'hsl(var(--chart-5))' }
  ];
};

const enrollmentChartConfig = {
  inscriptions: {
    label: "Inscriptions",
    color: "hsl(var(--chart-1))",
  },
  graduations: {
    label: "Graduations",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

const programChartConfig = {
  "Web Development": {
    label: "Web Development",
    color: "hsl(var(--chart-1))",
  },
  "Cloud & DevOps": {
    label: "Cloud & DevOps",
    color: "hsl(var(--chart-2))",
  },
  "Embedded Systems": {
    label: "Embedded Systems",
    color: "hsl(var(--chart-3))",
  },
  "Robotics": {
    label: "Robotics",
    color: "hsl(var(--chart-4))",
  },
  "Digital Marketing": {
    label: "Digital Marketing",
    color: "hsl(var(--chart-5))",
  },
} satisfies ChartConfig;

export const DashboardPage = () => {
  const { data: summary, isPending } = useQuery({
    queryKey: ['dashboard', 'metrics'],
    queryFn: fetchDashboardMetrics,
    staleTime: 60_000
  });

  const { data: enrollmentData, isPending: enrollmentLoading } = useQuery({
    queryKey: ['dashboard', 'enrollment'],
    queryFn: fetchEnrollmentData,
    staleTime: 60_000
  });

  const { data: programData, isPending: programLoading } = useQuery({
    queryKey: ['dashboard', 'programs'],
    queryFn: fetchProgramDistribution,
    staleTime: 60_000
  });

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
          icon={TrendingUp}
          label="Completion rate"
          loading
          value="—"
          trend="+0%"
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
        {/* Enrollment Trends */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Enrollment Trends</h3>
            <p className="text-sm text-muted-foreground">
              Monthly inscriptions vs graduations
            </p>
          </div>
          <div className="h-80">
            {enrollmentLoading ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">Loading chart...</div>
              </div>
            ) : !enrollmentData || enrollmentData.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">No data available</div>
              </div>
            ) : (
              <ChartContainer config={enrollmentChartConfig} className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={enrollmentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Line
                      type="monotone"
                      dataKey="inscriptions"
                      stroke="hsl(var(--chart-1))"
                      strokeWidth={2}
                      name="Inscriptions"
                    />
                    <Line
                      type="monotone"
                      dataKey="graduations"
                      stroke="hsl(var(--chart-2))"
                      strokeWidth={2}
                      name="Graduations"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </div>
        </div>

        {/* Program Distribution */}
        <div className="rounded-lg border bg-background p-6 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Program Distribution</h3>
            <p className="text-sm text-muted-foreground">
              Students by program
            </p>
          </div>
          <div className="h-80">
            {programLoading ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">Loading chart...</div>
              </div>
            ) : !programData || programData.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <div className="text-sm text-muted-foreground">No data available</div>
              </div>
            ) : (
              <ChartContainer config={programChartConfig} className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={programData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="hsl(var(--chart-1))"
                      dataKey="value"
                    >
                      {programData?.map((entry, index) => (
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
