import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import type { ColumnDef } from "@tanstack/react-table";

import { DataTable } from "@/components/data-table/data-table";
import { Button } from "@/components/ui/button";
import { ConfirmDialog } from "@/components/confirm-dialog";
import {
  hardDeleteStudentById,
  restoreStudentById,
  fetchTrashedStudents,
  type TrashStudent
} from "@/services/trash-service";
import { StudentProfile } from "@/components/student-form/student-form-types";

const formatDeletedAt = (deletedAt?: string) => {
  if (!deletedAt) return "—";
  const date = new Date(deletedAt);
  if (Number.isNaN(date.getTime())) return "—";

  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
};

export const ReinscriptionTrashPage = () => {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [restoreTarget, setRestoreTarget] = useState<TrashStudent | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<TrashStudent | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [actionLoadingId, setActionLoadingId] = useState<string | null>(null);

  const offset = (page - 1) * pageSize;

  const trashQuery = useQuery({
    queryKey: ["trash", { page, pageSize }],
    queryFn: () =>
      fetchTrashedStudents({
        limit: pageSize,
        offset
      })
  });

  const students = trashQuery.data?.data ?? [];
  const totalStudents = trashQuery.data?.count ?? 0;

  const handleRestore = async (student: TrashStudent) => {
    setActionError(null);
    const targetId = student.recordId;
    console.log(student);

    setActionLoadingId(targetId);
    try {
      await restoreStudentById(targetId);
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

  const handleHardDelete = async (student: TrashStudent) => {
    setActionError(null);
    const targetId = student.recordId;
    setActionLoadingId(targetId);
    try {
      await hardDeleteStudentById(targetId);
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

  const columns = useMemo<ColumnDef<TrashStudent>[]>(
    () => [
      {
        accessorKey: "fullName",
        header: "Nom et prénom",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.fullName}</span>
            <span className="text-xs text-muted-foreground">
              {row.original.cardNumber ||
                row.original.numSelect ||
                row.original.recordId}
            </span>
          </div>
        )
      },
      {
        accessorKey: "deletedAt",
        header: "Supprimé le",
        cell: ({ row }) => (
          <span className="text-xs text-muted-foreground">
            {formatDeletedAt(row.original.deletedAt)}
          </span>
        )
      },
      {
        accessorKey: "mention",
        header: "Mention",
        cell: ({ row }) => (
          <span className="text-xs text-muted-foreground">
            {row.original.mention || "—"}
          </span>
        )
      },

      {
        accessorKey: "level",
        header: "Niveau",
        cell: ({ row }) => (
          <span className="text-xs text-muted-foreground">
            {row.original.level || "—"}
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
