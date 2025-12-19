import { useQuery } from '@tanstack/react-query';

import { Button } from '../../components/ui/button';

interface WorkingTimeSlot {
  id: string;
  label: string;
  from: string;
  to: string;
}

const fetchWorkingTime = async (): Promise<WorkingTimeSlot[]> => {
  await new Promise((resolve) => setTimeout(resolve, 250));
  return [
    { id: '1', label: 'Morning', from: '08:00', to: '12:00' },
    { id: '2', label: 'Afternoon', from: '13:00', to: '17:00' }
  ];
};

export const WorkingTimePage = () => {
  const { data } = useQuery({
    queryKey: ['admin', 'working-time'],
    queryFn: fetchWorkingTime
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Working time</h1>
          <p className="text-sm text-muted-foreground">
            Configure time slots reused in user schedules and inscriptions.
          </p>
        </div>
        <Button size="sm">Create slot</Button>
      </div>
      <div className="grid gap-3">
        {(data ?? []).map((slot) => (
          <div
            key={slot.id}
            className="flex items-center justify-between rounded-lg border bg-background px-4 py-3"
          >
            <div>
              <p className="text-sm font-medium">{slot.label}</p>
              <p className="text-xs text-muted-foreground">
                {slot.from} — {slot.to}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button size="sm" variant="outline">
                Edit
              </Button>
              <Button size="sm" variant="destructive">
                Remove
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
