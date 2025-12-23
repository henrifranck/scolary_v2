import { Dispatch, SetStateAction, useState } from "react";

import {
  StudentAnnualProps,
  StudentDocumentState
} from "@/components/student-form/student-form-types";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { Pencil, Trash2 } from "lucide-react";

type DocumentSummaryProps = {
  displayAnnualRegisters: Array<StudentAnnualProps>;
};

type DocumentEditorProps = {
  annualRegisterDrafts: Array<
    StudentAnnualProps & { isEditing?: boolean; isNew?: boolean }
  >;
  documentDrafts: Record<string, StudentDocumentState[]>;
  documentDescriptions: Record<string, string>;
  documentUploadError: string | null;
  documentUploadingIndex: number | null;
  getAnnualKey: (
    annual: StudentAnnualProps & { id?: number },
    index: number
  ) => string;
  handleUploadDocument: (annualIndex: number, file: File | null) => void;
  onDeleteDocument: (annualIndex: number, documentId: number) => void;
  onUpdateDocument: (
    annualIndex: number,
    documentId: number,
    payload: { name?: string; description?: string }
  ) => void;
  setDocumentDescriptions: Dispatch<SetStateAction<Record<string, string>>>;
};

export const DocumentSummary = ({
  displayAnnualRegisters
}: DocumentSummaryProps) => (
  <div className="space-y-2">
    {displayAnnualRegisters?.map((annual, index) => (
      <div key={index} className="grid gap-3">
        {annual?.document?.length ? (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {annual.document.map((doc, docIndex) => (
              <a
                key={`${index}-document-${docIndex}`}
                href={resolveAssetUrl(doc.url)}
                className="group relative aspect-square overflow-hidden rounded-lg border border-dashed bg-muted/20"
                target="_blank"
                rel="noreferrer"
              >
                <img
                  src={resolveAssetUrl(doc.url)}
                  alt={doc.name}
                  className="h-full w-full object-cover"
                />
                <div className="absolute inset-x-0 bottom-0 bg-background/80 px-2 py-1 text-xs text-foreground opacity-0 transition-opacity group-hover:opacity-100">
                  {doc.name}
                </div>
              </a>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <div className="flex aspect-square items-center justify-center rounded-lg border border-dashed bg-muted/20 text-xs text-muted-foreground">
              Aucun document
            </div>
          </div>
        )}
      </div>
    ))}
  </div>
);

export const DocumentEditor = ({
  annualRegisterDrafts,
  documentDrafts,
  documentDescriptions,
  documentUploadError,
  documentUploadingIndex,
  getAnnualKey,
  handleUploadDocument,
  onDeleteDocument,
  onUpdateDocument,
  setDocumentDescriptions
}: DocumentEditorProps) => {
  const [editingDoc, setEditingDoc] = useState<{
    annualIndex: number;
    doc: StudentDocumentState;
  } | null>(null);
  const [confirmDelete, setConfirmDelete] = useState<{
    annualIndex: number;
    docId: number;
  } | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [editName, setEditName] = useState("");
  const [editDescription, setEditDescription] = useState("");

  const openEdit = (annualIndex: number, doc: StudentDocumentState) => {
    setEditingDoc({ annualIndex, doc });
    setEditName(doc.name ?? "");
    setEditDescription(doc.description ?? "");
  };

  const closeEdit = () => {
    setEditingDoc(null);
    setEditName("");
    setEditDescription("");
  };

  const handleSaveEdit = async () => {
    if (!editingDoc?.doc?.id) {
      return;
    }
    setIsSaving(true);
    try {
      await onUpdateDocument(editingDoc.annualIndex, editingDoc.doc.id, {
        name: editName.trim() || undefined,
        description: editDescription.trim() || undefined
      });
      closeEdit();
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      {documentUploadError ? (
        <p className="text-sm text-destructive">{documentUploadError}</p>
      ) : null}
      {annualRegisterDrafts.length ? (
        annualRegisterDrafts.map((annual, index) => {
          const annualKey = getAnnualKey(annual, index);
          const docs = documentDrafts[annualKey] ?? [];
          return (
            <div
              key={`${annual.id ?? "new"}-${index}`}
              className="space-y-3 rounded-xl border bg-muted/20 p-4"
            >
              <div className="flex items-center justify-between gap-2">
                <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Ajouter les document obligatoires pour l'année{" "}
                  {annual.academic_year?.name || "Année académique"}
                </label>
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Description
                </label>
                <Textarea
                  value={documentDescriptions[annualKey] ?? ""}
                  onChange={(event) =>
                    setDocumentDescriptions((previous) => ({
                      ...previous,
                      [annualKey]: event.target.value
                    }))
                  }
                  placeholder="Description du document"
                />
              </div>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                {docs.map((doc, docIndex) => (
                  <div
                    key={`${annualKey}-doc-${docIndex}`}
                    className="group relative aspect-square overflow-hidden rounded-lg border border-dashed bg-muted/20"
                  >
                    <a
                      href={resolveAssetUrl(doc.url)}
                      className="absolute inset-0 z-0"
                      target="_blank"
                      rel="noreferrer"
                    >
                      <img
                        src={resolveAssetUrl(doc.url)}
                        alt={doc.name}
                        className="h-full w-full object-cover"
                      />
                      <div className="absolute inset-x-0 bottom-0 bg-background/80 px-2 py-1 text-xs text-foreground opacity-0 transition-opacity group-hover:opacity-100">
                        {doc.name}
                      </div>
                    </a>
                    <div className="absolute right-2 top-2 z-10 flex gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 bg-background/80"
                        onClick={() => openEdit(index, doc)}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 bg-background/80 text-destructive hover:text-destructive"
                        onClick={() =>
                          doc.id
                            ? setConfirmDelete({
                                annualIndex: index,
                                docId: doc.id
                              })
                            : null
                        }
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
                <label className="flex aspect-square cursor-pointer items-center justify-center rounded-lg border border-dashed bg-muted/10 text-sm text-muted-foreground">
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(event) =>
                      handleUploadDocument(
                        index,
                        event.target.files?.[0] ?? null
                      )
                    }
                    disabled={documentUploadingIndex === index}
                  />
                  <span className="text-2xl font-semibold">+</span>
                </label>
              </div>
            </div>
          );
        })
      ) : (
        <p className="text-sm text-muted-foreground">
          Aucun document à afficher.
        </p>
      )}
      <Dialog open={Boolean(editingDoc)} onOpenChange={closeEdit}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Modifier le document</DialogTitle>
          </DialogHeader>
          <div className="space-y-3">
            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Nom
              </label>
              <Input
                value={editName}
                onChange={(event) => setEditName(event.target.value)}
                placeholder="Nom du document"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Description
              </label>
              <Textarea
                value={editDescription}
                onChange={(event) => setEditDescription(event.target.value)}
                placeholder="Description"
              />
            </div>
          </div>
          <DialogFooter className="gap-2">
            <Button type="button" variant="ghost" onClick={closeEdit}>
              Annuler
            </Button>
            <Button type="button" onClick={handleSaveEdit} disabled={isSaving}>
              Enregistrer
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <ConfirmDialog
        open={Boolean(confirmDelete)}
        title="Supprimer le document ?"
        description="Cette action supprimera définitivement le document."
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        destructive
        onCancel={() => setConfirmDelete(null)}
        onConfirm={() => {
          if (!confirmDelete) {
            return;
          }
          onDeleteDocument(confirmDelete.annualIndex, confirmDelete.docId);
          setConfirmDelete(null);
        }}
      />
    </div>
  );
};
