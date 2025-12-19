import { useMemo } from 'react';

import { DataTable, type ColumnDef } from '../../../components/data-table/data-table';

interface ConcoursRow {
  id: string;
  title: string;
  session: string;
  applicationStatus: 'Registered' | 'Waiting list' | 'Closed';
}

const mockConcours: ConcoursRow[] = [
  { id: 'cn-1', title: 'Engineering entrance exam', session: 'July 2024', applicationStatus: 'Registered' },
  { id: 'cn-2', title: 'IT master exam', session: 'September 2024', applicationStatus: 'Waiting list' },
  { id: 'cn-3', title: 'Business school exam', session: 'November 2024', applicationStatus: 'Closed' }
];

const columns: ColumnDef<ConcoursRow>[] = [
  {
    accessorKey: 'title',
    header: 'Competition',
    cell: ({ row }) => (
      <div className="flex flex-col">
        <span className="font-medium">{row.original.title}</span>
        <span className="text-xs text-muted-foreground">{row.original.session}</span>
      </div>
    )
  },
  {
    accessorKey: 'applicationStatus',
    header: 'Status',
    cell: ({ row }) => {
      const value = row.original.applicationStatus;
      const color =
        value === 'Registered'
          ? 'text-emerald-600'
          : value === 'Waiting list'
            ? 'text-amber-600'
            : 'text-muted-foreground';

      return <span className={`text-xs font-semibold ${color}`}>{value}</span>;
    }
  }
];

export const ConcoursPage = () => {
  const data = useMemo(() => mockConcours, []);

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Competitions & concours</h1>
        <p className="text-sm text-muted-foreground">
          Stay aligned with the concours module of the existing platform.
        </p>
      </div>
      <DataTable columns={columns} data={data} searchPlaceholder="Search concours" />
    </div>
  );
};
