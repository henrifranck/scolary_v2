import { Pencil, Trash2 } from "lucide-react";
import { Button } from "./ui/button";

type actionButtonProps = {
  deletingId?: string | null;
  row: any;
  handleEdit: (value: any) => void;
  setConfirmDelete: (value: any) => void;
};

export const ActionButton = ({
  deletingId,
  row,
  handleEdit,
  setConfirmDelete
}: actionButtonProps) => {
  return (
    <div className="flex justify-end gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={() => handleEdit(row.original)}
        // disabled={deletingId  && deletingId === row.original.recordId}
      >
        <Pencil className="m-1 h-4 w-4" />
      </Button>
      <Button
        variant="outline"
        size="sm"
        className="text-destructive hover:text-destructive"
        onClick={() => setConfirmDelete(row.original)}
      >
        <Trash2 className="m-1 h-4 w-4" />
      </Button>
    </div>
  );
};
