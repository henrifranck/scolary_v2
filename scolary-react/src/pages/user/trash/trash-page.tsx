import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import type { ColumnDef } from "@tanstack/react-table";

import { DataTable } from "@/components/data-table/data-table";
import { Button } from "@/components/ui/button";
import { ConfirmDialog } from "@/components/confirm-dialog";
import {
  fetchReinscriptionsWithMeta,
  type ReinscriptionStudent
} from "@/services/reinscription-service";
import { hardDeleteStudent, restoreStudent } from "@/services/student-service";

export const ReinscriptionTrashPage = () => {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [restoreTarget, setRestoreTarget] =
    useState<ReinscriptionStudent | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<ReinscriptionStudent | null>(
    null
  );
  const [actionError, setActionError] = useState<string | null>(null);
  const [actionLoadingId, setActionLoadingId] = useState<string | null>(null);

  const offset = (page - 1) * pageSize;

  const trashQuery = useQuery({
    queryKey: ["reinscription", "trash", { page, pageSize }],
    queryFn: () =>
      fetchReinscriptionsWithMeta({
        deletedOnly: true,
        limit: pageSize,
        offset
      })
  });

  const students = trashQuery.data?.data ?? [];
  const totalStudents = trashQuery.data?.count ?? 0;

  const handleRestore = async (student: ReinscriptionStudent) => {
    setActionError(null);
    setActionLoadingId(student.recordId);
    try {
      await restoreStudent(student.recordId);
      void trashQuery.refetch();
    } catch (error) {
      setActionError(
        error instanceof Error
          ? error.message
          : "Impossible de restaurer l'étudiant."
      );
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleHardDelete = async (student: ReinscriptionStudent) => {
    setActionError(null);
    setActionLoadingId(student.recordId);
    try {
      await hardDeleteStudent(student.recordId);
      void trashQuery.refetch();
    } catch (error) {
      setActionError(
        error instanceof Error
          ? error.message
          : "Impossible de supprimer définitivement l'étudiant."
      );
    } finally {
      setActionLoadingId(null);
    }
  };

  const columns = useMemo<ColumnDef<ReinscriptionStudent>[]>(
    () => [
      {
        accessorKey: "fullName",
        header: "Nom et prénom",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.fullName}</span>
            <span className="text-xs text-muted-foreground">
              {row.original.id}
            </span>
          </div>
        )
      },
      {
        accessorKey: "deletedAt",
        header: "Supprimé le",
        cell: ({ row }) => (
          <span className="text-xs text-muted-foreground">
            {row.original.deletedAt || "—"}
          </span>
        )
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => setRestoreTarget(row.original)}
              disabled={actionLoadingId === row.original.recordId}
            >
              Restaurer
            </Button>
            <Button
              size="sm"
              variant="destructive"
              onClick={() => setDeleteTarget(row.original)}
              disabled={actionLoadingId === row.original.recordId}
            >
              Supprimer
            </Button>
          </div>
        )
      }
    ],
    [actionLoadingId]
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-foreground">
            Corbeille étudiants
          </h1>
          <p className="text-sm text-muted-foreground">
            Gérez les étudiants supprimés.
          </p>
        </div>
      </div>
      <div className="rounded-lg border bg-background p-5 shadow-sm space-y-3">
        <DataTable
          columns={columns}
          data={students}
          searchPlaceholder="Search students"
          isLoading={trashQuery.isFetching || trashQuery.isPending}
          totalItems={totalStudents}
          page={page}
          pageSize={pageSize}
          onPageChange={setPage}
          onPageSizeChange={(nextSize) => {
            setPageSize(nextSize);
            setPage(1);
          }}
        />
        {actionError ? (
          <p className="text-sm text-destructive">{actionError}</p>
        ) : null}
      </div>

      <ConfirmDialog
        open={Boolean(restoreTarget)}
        title="Restaurer l'étudiant ?"
        description={
          restoreTarget
            ? `Restaurer ${restoreTarget.fullName} dans la liste active.`
            : undefined
        }
        confirmLabel="Restaurer"
        cancelLabel="Annuler"
        isConfirming={
          Boolean(restoreTarget) && actionLoadingId === restoreTarget?.recordId
        }
        onCancel={() => setRestoreTarget(null)}
        onConfirm={() => {
          if (restoreTarget) {
            void handleRestore(restoreTarget);
            setRestoreTarget(null);
          }
        }}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="Supprimer définitivement ?"
        description={
          deleteTarget
            ? `Cette action supprime définitivement ${deleteTarget.fullName} et ses données.`
            : undefined
        }
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        destructive
        isConfirming={
          Boolean(deleteTarget) && actionLoadingId === deleteTarget?.recordId
        }
        onCancel={() => setDeleteTarget(null)}
        onConfirm={() => {
          if (deleteTarget) {
            void handleHardDelete(deleteTarget);
            setDeleteTarget(null);
          }
        }}
      />
    </div>
  );
};
