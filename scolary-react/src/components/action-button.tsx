import { Pencil, Trash2 } from "lucide-react";
import { Button } from "./ui/button";

type actionButtonProps = {
  deletingId?: string | null;
  row: any;
  handleEdit: (value: any) => void;
  setConfirmDelete: (value: any) => void;
  allowEdit?: boolean;
  allowDelete?: boolean;
};

export const ActionButton = ({
  deletingId,
  row,
  handleEdit,
  setConfirmDelete,
  allowEdit = true,
  allowDelete = true
}: actionButtonProps) => {
  const showEdit = allowEdit !== false;
  const showDelete = allowDelete !== false;

  if (!showEdit && !showDelete) {
    return null;
  }

  return (
    <div className="flex justify-end gap-2">
      {showEdit ? (
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleEdit(row.original)}
          // disabled={deletingId  && deletingId === row.original.recordId}
        >
          <Pencil className="m-1 h-4 w-4" />
        </Button>
      ) : null}
      {showDelete ? (
        <Button
          variant="outline"
          size="sm"
          className="text-destructive hover:text-destructive"
          onClick={() => setConfirmDelete(row.original)}
        >
          <Trash2 className="m-1 h-4 w-4" />
        </Button>
      ) : null}
    </div>
  );
};
