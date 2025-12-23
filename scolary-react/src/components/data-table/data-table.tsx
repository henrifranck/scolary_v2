import { useState } from 'react';
import {
  type ColumnDef,
  type ColumnFiltersState,
  type Row,
  type SortingState,
  type VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable
} from '@tanstack/react-table';
import type { ReactNode } from 'react';
import { LayoutGrid, Rows3, Eye, EyeOff, Settings2 } from 'lucide-react';

import { Button } from '../ui/button';
import { Input } from '../ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '../ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '../../lib/utils';

interface DataTableProps<TData> {
  columns: ColumnDef<TData, any>[];
  data: TData[];
  searchPlaceholder?: string;
  emptyText?: string;
  isLoading?: boolean;
  initialVisibility?: VisibilityState;
  actionsSlot?: ReactNode;
  enableViewToggle?: boolean;
  enableColumnVisibility?: boolean;
  renderGridItem?: (row: Row<TData>) => ReactNode;
  gridEmptyState?: ReactNode;
  gridClassName?: string;
  defaultView?: 'table' | 'grid';
  totalItems?: number;
  page?: number;
  pageSize?: number;
  onPageChange?: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
  pageSizeOptions?: number[];
  showPagination?: boolean;
}

export const DataTable = <TData,>({
  columns,
  data,
  searchPlaceholder,
  emptyText = 'No data to display',
  isLoading,
  initialVisibility,
  actionsSlot,
  enableViewToggle,
  enableColumnVisibility = true,
  renderGridItem,
  gridEmptyState,
  gridClassName,
  defaultView = 'table',
  totalItems,
  page,
  pageSize,
  onPageChange,
  onPageSizeChange,
  pageSizeOptions,
  showPagination = true
}: DataTableProps<TData>) => {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>(initialVisibility ?? {});
  const canUseGridView = Boolean(enableViewToggle && renderGridItem);
  const initialViewMode: 'table' | 'grid' =
    defaultView === 'grid' && canUseGridView ? 'grid' : 'table';
  const [viewMode, setViewMode] = useState<'table' | 'grid'>(initialViewMode);

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
      columnVisibility
    },
    enableGlobalFilter: true,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize: 10
      }
    }
  });

  const filteredRowCount = table.getFilteredRowModel().rows.length;
  const visibleColumns = table.getAllLeafColumns().length || columns.length;
  const currentRows = table.getRowModel().rows;
  const isGridView = canUseGridView && viewMode === 'grid';
  const isServerPaginated =
    typeof page === 'number' &&
    typeof pageSize === 'number' &&
    typeof onPageChange === 'function' &&
    typeof onPageSizeChange === 'function';
  const pageSizeChoices = pageSizeOptions ?? [5, 10, 20, 50];

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <Input
          value={globalFilter}
          onChange={(event) => setGlobalFilter(event.target.value)}
          placeholder={searchPlaceholder ?? 'Search…'}
          className="w-full md:w-72"
        />
        <div className="flex flex-wrap items-center gap-2">
          {actionsSlot}

          {/* Column Visibility Menu */}
          {enableColumnVisibility && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm" className="gap-2">
                  <Settings2 className="h-4 w-4" />
                  Columns
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuLabel>Toggle columns</DropdownMenuLabel>
                <DropdownMenuSeparator />
                {table
                  .getAllColumns()
                  .filter((column) => column.getCanHide())
                  .map((column) => {
                    const columnDef = column.columnDef;
                    const displayName = typeof columnDef.header === 'string'
                      ? columnDef.header
                      : column.id.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());

                    return (
                      <DropdownMenuCheckboxItem
                        key={column.id}
                        className="capitalize"
                        checked={column.getIsVisible()}
                        onCheckedChange={(value: boolean) => column.toggleVisibility(!!value)}
                      >
                        {displayName}
                      </DropdownMenuCheckboxItem>
                    );
                  })}
                <DropdownMenuSeparator />
                <DropdownMenuCheckboxItem
                  checked={table.getIsAllColumnsVisible()}
                  onCheckedChange={(value: boolean) => table.toggleAllColumnsVisible(!!value)}
                >
                  Toggle all
                </DropdownMenuCheckboxItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}

          {canUseGridView ? (
            <div className="flex items-center gap-1">
              <Button
                variant={viewMode === 'table' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('table')}
                aria-pressed={viewMode === 'table'}
                aria-label="Table view"
                className="px-2"
              >
                <Rows3 className="h-4 w-4" />
                <span className="sr-only">Table view</span>
              </Button>
              <Button
                variant={viewMode === 'grid' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('grid')}
                aria-pressed={viewMode === 'grid'}
                aria-label="Grid view"
                className="px-2"
              >
                <LayoutGrid className="h-4 w-4" />
                <span className="sr-only">Grid view</span>
              </Button>
            </div>
          ) : null}

          <Button
            variant="outline"
            size="sm"
            disabled={!sorting.length}
            onClick={() => table.resetSorting()}
          >
            Reset sorting
          </Button>
          <Button
            variant="outline"
            size="sm"
            disabled={!columnFilters.length && !globalFilter}
            onClick={() => {
              table.resetColumnFilters();
              setGlobalFilter('');
            }}
          >
            Clear filters
          </Button>
        </div>
      </div>
      {isGridView ? (
        currentRows.length ? (
          <div className={cn('grid gap-4', gridClassName)}>
            {currentRows.map((row) => (
              <div key={row.id}>{renderGridItem?.(row)}</div>
            ))}
          </div>
        ) : (
          gridEmptyState ?? (
            <div className="flex h-40 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground">
              {emptyText}
            </div>
          )
        )
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    const isActions = header.column.id === 'actions';
                    return (
                      <TableHead key={header.id} className={cn(isActions && 'text-right pr-4')}>
                        {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                      </TableHead>
                    );
                  })}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell className="h-24 text-center" colSpan={visibleColumns}>
                    Loading data…
                  </TableCell>
                </TableRow>
              ) : currentRows.length ? (
                currentRows.map((row) => (
                  <TableRow key={row.id} data-state={row.getIsSelected() ? 'selected' : undefined}>
                    {row.getVisibleCells().map((cell) => {
                      const isActions = cell.column.id === 'actions';
                      return (
                        <TableCell key={cell.id} className={cn(isActions && 'text-right pr-4')}>
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell className="h-24 text-center text-sm text-muted-foreground" colSpan={visibleColumns}>
                    {emptyText}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      )}
            {showPagination !== false && (
        isServerPaginated ? (
          <div className="flex flex-col gap-3 rounded-lg border bg-background p-4 text-xs text-muted-foreground md:flex-row md:items-center md:justify-between">
            <div>
              {(() => {
                const total = totalItems ?? 0;
                if (!pageSize || pageSize <= 0) {
                  return `Showing ${currentRows.length} items`;
                }
                const start = total ? Math.min((page! - 1) * pageSize + 1, total) : currentRows.length ? 1 : 0;
                const end = total
                  ? Math.min((page! - 1) * pageSize + currentRows.length, total)
                  : currentRows.length;
                if (total) {
                  return `Showing ${start}-${end} of ${total} items (${pageSize} per page)`;
                }
                return `Showing ${currentRows.length} items (${pageSize} per page)`;
              })()}
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2">
                <span>Rows per page</span>
                <Select
                  value={String(pageSize ?? '')}
                  onValueChange={(value) => {
                    const size = Number(value);
                    onPageSizeChange?.(Number.isFinite(size) && size > 0 ? size : pageSize ?? 10);
                  }}
                >
                  <SelectTrigger className="w-20">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {pageSizeChoices.map((size) => (
                      <SelectItem key={size} value={String(size)}>
                        {size}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onPageChange?.(Math.max(1, (page ?? 1) - 1))}
                  disabled={(page ?? 1) <= 1}
                >
                  Previous
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onPageChange?.((page ?? 1) + 1)}
                  disabled={
                    totalItems
                      ? Boolean(page && pageSize && page * pageSize >= totalItems)
                      : currentRows.length < (pageSize ?? currentRows.length) || currentRows.length === 0
                  }
                >
                  Next
                </Button>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col gap-3 rounded-lg border bg-background p-4 text-xs text-muted-foreground md:flex-row md:items-center md:justify-between">
            <div>
              {(() => {
                const tablePageIndex = table.getState().pagination.pageIndex;
                const tablePageSize = table.getState().pagination.pageSize;
                if (!filteredRowCount) {
                  return 'No entries to display';
                }
                const start = tablePageIndex * tablePageSize + 1;
                const end = Math.min(start + currentRows.length - 1, filteredRowCount);
                return `Showing ${start}-${end} of ${filteredRowCount} entries (${tablePageSize} per page)`;
              })()}
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2">
                <span>Rows per page</span>
                <Select
                  value={String(table.getState().pagination.pageSize)}
                  onValueChange={(value) => {
                    const size = Number(value);
                    table.setPageSize(Number.isFinite(size) && size > 0 ? size : table.getState().pagination.pageSize);
                  }}
                >
                  <SelectTrigger className="w-20">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {pageSizeChoices.map((size) => (
                      <SelectItem key={size} value={String(size)}>
                        {size}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
                  Previous
                </Button>
                <Button variant="outline" size="sm" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
                  Next
                </Button>
              </div>
            </div>
          </div>
        )
      )}

    </div>
  );
};

export type { ColumnDef };
