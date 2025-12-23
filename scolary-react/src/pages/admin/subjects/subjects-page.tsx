import { Pencil, Trash2 } from 'lucide-react';
import { useMemo } from 'react';

import { Button } from '../../../components/ui/button';
import { DataTable, type ColumnDef } from '../../../components/data-table/data-table';

interface SubjectRow {
  id: string;
  code: string;
  label: string;
  semester: string;
  coordinator: string;
}

const mockSubjects: SubjectRow[] = [
  {
    id: 'sub-algo',
    code: 'ALGO101',
    label: 'Algorithms and data structures',
    semester: 'S1',
    coordinator: 'Dr. Sabrine T.'
  },
  {
    id: 'sub-db',
    code: 'DB204',
    label: 'Database systems',
    semester: 'S2',
    coordinator: 'Prof. Sami K.'
  },
  {
    id: 'sub-net',
    code: 'NET305',
    label: 'Network security',
    semester: 'S3',
    coordinator: 'Dr. Amine B.'
  }
];

const columns: ColumnDef<SubjectRow>[] = [
  {
    accessorKey: 'code',
    header: 'Code',
    cell: ({ row }) => <span className="font-semibold">{row.original.code}</span>
  },
  {
    accessorKey: 'label',
    header: 'Subject',
    cell: ({ row }) => (
      <div className="flex flex-col">
        <span className="font-medium">{row.original.label}</span>
        <span className="text-xs text-muted-foreground">Coordinator: {row.original.coordinator}</span>
      </div>
    )
  },
  {
    accessorKey: 'semester',
    header: 'Semester',
    cell: ({ row }) => <span className="text-sm text-muted-foreground">{row.original.semester}</span>
  },
  {
    id: 'actions',
    header: '',
    cell: ({ row }) => (
      <div className="flex justify-end gap-2">
        <Button
          size="icon"
          variant="ghost"
          onClick={() => console.info('Edit subject', row.original.id)}
          aria-label="Editer"
        >
          <Pencil className="h-4 w-4" />
        </Button>
        <Button
          size="icon"
          variant="ghost"
          onClick={() => console.info('Archive subject', row.original.id)}
          aria-label="Archiver"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    )
  }
];

export const SubjectsPage = () => {
  const data = useMemo(() => mockSubjects, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Subjects</h1>
          <p className="text-sm text-muted-foreground">
            Overview of the subjects catalogue, matching the Angular administration module.
          </p>
        </div>
        <Button size="sm">Add subject</Button>
      </div>
      <DataTable columns={columns} data={data} searchPlaceholder="Search subjects" />
    </div>
  );
};
