import { useMemo } from 'react';

import { ScrollArea } from '../../../components/ui/scroll-area';
import { Separator } from '../../../components/ui/separator';

const mockNotes = [
  {
    id: 1,
    title: 'Algorithms — group A',
    average: 14.5,
    updatedAt: '2 hours ago'
  },
  {
    id: 2,
    title: 'Database systems — group B',
    average: 11.3,
    updatedAt: 'Yesterday'
  },
  {
    id: 3,
    title: 'Network security — group C',
    average: 16.2,
    updatedAt: '3 days ago'
  }
];

export const NotesPage = () => {
  const items = useMemo(() => mockNotes, []);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Notes</h1>
        <p className="text-sm text-muted-foreground">
          This page mirrors the Angular note listing with mock data and structure.
        </p>
      </div>
      <ScrollArea className="h-[520px] rounded-xl border bg-background">
        <div className="space-y-0.5 p-4">
          {items.map((item, index) => (
            <div key={item.id}>
              <div className="flex items-center justify-between py-3">
                <div>
                  <p className="text-sm font-medium leading-none">{item.title}</p>
                  <p className="text-xs text-muted-foreground">{item.updatedAt}</p>
                </div>
                <p className="text-sm font-semibold">Average: {item.average}</p>
              </div>
              {index < items.length - 1 ? <Separator className="my-2" /> : null}
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
};
