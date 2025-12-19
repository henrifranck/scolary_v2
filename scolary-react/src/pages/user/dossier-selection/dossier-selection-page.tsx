import { useCallback, useMemo, useState } from 'react';
import type { Row } from '@tanstack/react-table';

import { Button } from '../../../components/ui/button';
import {
  DataTable,
  type ColumnDef
} from '../../../components/data-table/data-table';
import {
  AcademicFilters,
  AcademicYearOption,
  type AcademicFilterValue,
  type JourneyOption,
  type MentionOption
} from '../../../components/filters/academic-filters';
import {
  useReinscriptions,
  type ReinscriptionStudent,
  type ReinscriptionStatus
} from '../../../services/reinscription-service';

const semesters = Array.from({ length: 10 }, (_, index) => `S${index + 1}`);

const mentionOptions: MentionOption[] = [
  { id: 'mention-si', label: "Systèmes d'information" },
  { id: 'mention-ese', label: 'Electronique et systèmes embarqués' },
  { id: 'mention-mkg', label: 'Marketing digital' }
];

const yearOptions: AcademicYearOption[] = [
  { id: 'year-1', label: '2024-2025' },
  { id: 'year-2', label: '2025-2026' }
];

const journeyOptions: JourneyOption[] = [
  {
    id: 'journey-dev-web',
    label: 'Licence développement web',
    mentionId: 'mention-si'
  },
  {
    id: 'journey-cloud',
    label: 'Master cloud & devops',
    mentionId: 'mention-si'
  },
  {
    id: 'journey-embedded',
    label: 'Master systèmes embarqués',
    mentionId: 'mention-ese'
  },
  {
    id: 'journey-robotics',
    label: 'Licence robotique',
    mentionId: 'mention-ese'
  },
  {
    id: 'journey-digital-market',
    label: 'Bachelor marketing digital',
    mentionId: 'mention-mkg'
  }
];

const statusStyles: Record<ReinscriptionStatus, { text: string; badge: string; dot: string }> = {
  Pending: {
    text: 'text-muted-foreground',
    badge: 'bg-slate-100 text-slate-700',
    dot: 'bg-slate-400'
  },
  'In progress': {
    text: 'text-amber-600',
    badge: 'bg-amber-100 text-amber-700',
    dot: 'bg-amber-500'
  },
  Validated: {
    text: 'text-emerald-600',
    badge: 'bg-emerald-100 text-emerald-700',
    dot: 'bg-emerald-500'
  }
};

const studentColumns: ColumnDef<ReinscriptionStudent>[] = [
  {
    accessorKey: 'fullName',
    header: 'Student',
    cell: ({ row }) => (
      <div className="flex flex-col">
        <span className="font-medium">{row.original.fullName}</span>
        <span className="text-xs text-muted-foreground">{row.original.id}</span>
      </div>
    )
  },
  {
    accessorKey: 'journeyLabel',
    header: 'Journey',
    cell: ({ row }) => (
      <div className="flex flex-col">
        <span className="text-sm font-medium">{row.original.journeyLabel}</span>
        <span className="text-xs text-muted-foreground">Semester {row.original.semester}</span>
      </div>
    )
  },
  {
    accessorKey: 'mentionLabel',
    header: 'Mention',
    cell: ({ row }) => (
      <span className="text-sm text-muted-foreground">{row.original.mentionLabel}</span>
    )
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => {
      const value = row.original.status;
      const style = statusStyles[value];
      return <span className={`text-xs font-semibold ${style.text}`}>{value}</span>;
    }
  },
  {
    accessorKey: 'lastUpdate',
    header: 'Last update',
    cell: ({ row }) => (
      <span className="text-xs text-muted-foreground">{row.original.lastUpdate}</span>
    )
  }
];

const getAvatarUrl = (fullName: string) => {
  const name = encodeURIComponent(fullName);
  return `https://ui-avatars.com/api/?name=${name}&background=random&color=fff&size=64`;
};

const renderStudentCard = (row: Row<ReinscriptionStudent>) => {
  const student = row.original;
  const statusStyle = statusStyles[student.status];

  return (
    <div className="flex h-full flex-col gap-4 rounded-lg border bg-background p-5 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <img
            src={getAvatarUrl(student.fullName)}
            alt={student.fullName}
            className="h-8 w-8 shrink-0 rounded-full"
          />
          <div>
            <p className="text-sm font-semibold leading-tight text-foreground">{student.fullName}</p>
            <p className="text-xs text-muted-foreground">{student.id}</p>
          </div>
        </div>
        <span className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium ${statusStyle.badge}`}>
          <span className={`h-1.5 w-1.5 rounded-full ${statusStyle.dot}`} />
          {student.status}
        </span>
      </div>
      <div className="space-y-2 text-sm">
        <div>
          <p className="font-medium leading-tight text-foreground">{student.journeyLabel}</p>
          <p className="text-xs text-muted-foreground">Semester {student.semester}</p>
        </div>
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>{student.mentionLabel}</span>
          <span>Last update {student.lastUpdate}</span>
        </div>
      </div>
    </div>
  );
};

export const DossierSelectionPage = () => {
  const defaultMentionId = mentionOptions[0]?.id ?? '';
  const defaultYearId = yearOptions[0]?.id ?? '';
  const defaultJourneyId =
    journeyOptions.find((journey) => journey.mentionId === defaultMentionId)?.id ?? '';
  const defaultSemester = semesters[0] ?? '';

  const [filters, setFilters] = useState<AcademicFilterValue>({
    mentionId: defaultMentionId,
    journeyId: defaultJourneyId,
    semester: defaultSemester,
    academicYearId: defaultYearId
  });
  const handleFiltersChange = useCallback((next: AcademicFilterValue) => {
    setFilters(next);
  }, []);

  const availableJourneys = useMemo(
    () => journeyOptions.filter((journey) => journey.mentionId === filters.mentionId),
    [filters.mentionId]
  );

  const { data: students = [] } = useReinscriptions(filters);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dossier selection</h1>
          <p className="text-sm text-muted-foreground">
            Filter students and track dossier selection progress.
          </p>
        </div>
        <Button size="sm">Export report</Button>
      </div>
      <div className="grid gap-4 rounded-lg border bg-background p-5 shadow-sm">
        <AcademicFilters
          value={filters}
          onChange={handleFiltersChange}
          mentionOptions={mentionOptions}
          journeyOptions={journeyOptions}
          academicYearOptions={yearOptions}
          semesters={semesters}
          showResetButton={true}
          showActiveFilters={true}
          summarySlot={
            <div className="rounded-md border bg-muted/10 p-4 text-sm text-muted-foreground">
              <div className="grid gap-2 md:grid-cols-3">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">Students matching filters:</span>
                  <span className="font-semibold text-primary">{students.length}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">Available journeys:</span>
                  <span className="font-semibold text-primary">{availableJourneys.length}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">Selected semester:</span>
                  <span className="font-semibold text-primary">{filters.semester || '—'}</span>
                </div>
              </div>
            </div>
          }
        />
        <DataTable
          columns={studentColumns}
          data={students}
          searchPlaceholder="Search students"
          enableViewToggle
          enableColumnVisibility
          renderGridItem={renderStudentCard}
          gridClassName="sm:grid-cols-2 xl:grid-cols-3"
          gridEmptyState={
            <div className="flex h-40 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground">
              No students matching filters.
            </div>
          }
        />
      </div>
    </div>
  );
};
