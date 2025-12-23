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
  requiredDocuments?: { id: number; name: string }[];
};

type DocumentEditorProps = {
  requiredDocuments: { id: number; name: string }[];
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
  handleUploadDocument: (annualIndex: number, file: File | null, id_required_document?: number) => void;
  onDeleteDocument: (annualIndex: number, documentId: number) => void;
  onUpdateDocument: (
    annualIndex: number,
    documentId: number,
    payload: { name?: string; description?: string; id_required_document?: number }
  ) => void;
  setDocumentDescriptions: Dispatch<SetStateAction<Record<string, string>>>;
};

export const DocumentSummary = ({
  displayAnnualRegisters,
  requiredDocuments = []
}: DocumentSummaryProps) => (
  <div className="space-y-2">
    {displayAnnualRegisters?.map((annual, index) => (
      <div key={index} className="grid gap-3">
        {annual?.document?.length ? (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {(annual.document ?? []).slice(0, 3).map((doc, docIndex) => {
              const remaining = (annual.document?.length ?? 0) - 3;
              const showBadge = docIndex === 2 && remaining > 0;
              return (
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
                  {doc.id_required_document ? (
                    <span className="absolute left-2 top-2 z-10 rounded-full bg-background/90 px-2 py-1 text-[11px] font-semibold text-foreground shadow">
                      {requiredDocuments.find((rd) => rd.id === doc.id_required_document)?.name ??
                        "Document"}
                    </span>
                  ) : null}
                  {showBadge ? (
                    <div className="absolute right-2 top-2 rounded-full bg-foreground px-3 py-1.5 text-sm font-semibold text-background">
                      +{remaining}
                    </div>
                  ) : null}
                </a>
              );
            })}
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
  requiredDocuments,
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
  const [selectedRequiredByAnnual, setSelectedRequiredByAnnual] = useState<Record<string, number | ''>>({});
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
  const [editRequiredId, setEditRequiredId] = useState<number | ''>('');

  const openEdit = (annualIndex: number, doc: StudentDocumentState) => {
    setEditingDoc({ annualIndex, doc });
    setEditName(doc.name ?? "");
    setEditDescription(doc.description ?? "");
    setEditRequiredId(doc.id_required_document ?? '');
  };

  const closeEdit = () => {
    setEditingDoc(null);
    setEditName("");
    setEditDescription("");
    setEditRequiredId('');
  };

  const handleSaveEdit = async () => {
    if (!editingDoc?.doc?.id) {
      return;
    }
    setIsSaving(true);
    try {
      await onUpdateDocument(editingDoc.annualIndex, editingDoc.doc.id, {
        name: editName.trim() || undefined,
        description: editDescription.trim() || undefined,
        id_required_document:
          typeof editRequiredId === "number" ? editRequiredId : undefined
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
          const selectedRequiredId =
            selectedRequiredByAnnual[annualKey] ??
            (requiredDocuments[0]?.id ?? "");
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
                  Type de document requis
                </label>
                <select
                  className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm shadow-sm focus:outline-none"
                  value={selectedRequiredId}
                  onChange={(event) =>
                    setSelectedRequiredByAnnual((previous) => ({
                      ...previous,
                      [annualKey]:
                        event.target.value === "" ? "" : Number(event.target.value)
                    }))
                  }
                  disabled={!requiredDocuments.length}
                >
                  <option value="">Aucun</option>
                  {requiredDocuments.map((doc) => (
                    <option key={doc.id} value={doc.id}>
                      {doc.name}
                    </option>
                  ))}
                </select>
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
                    {doc.id_required_document ? (
                      <span className="absolute left-2 top-2 z-10 rounded-full bg-background/90 px-2 py-1 text-[11px] font-semibold text-foreground shadow">
                        {requiredDocuments.find((rd) => rd.id === doc.id_required_document)?.name ??
                          'Document'}
                      </span>
                    ) : null}
                    <div className="pointer-events-none absolute inset-0 flex items-center justify-center gap-2 opacity-0 transition-opacity group-hover:opacity-100">
                      <Button
                        type="button"
                        variant="secondary"
                        size="icon"
                        className="pointer-events-auto h-9 w-9"
                        onClick={() => openEdit(index, doc)}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="destructive"
                        size="icon"
                        className="pointer-events-auto h-9 w-9"
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
                        event.target.files?.[0] ?? null,
                        typeof selectedRequiredId === "number"
                          ? selectedRequiredId
                          : undefined
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
            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Document requis
              </label>
              <select
                className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm shadow-sm focus:outline-none"
                value={editRequiredId}
                onChange={(event) =>
                  setEditRequiredId(
                    event.target.value === "" ? "" : Number(event.target.value)
                  )
                }
              >
                <option value="">Aucun</option>
                {requiredDocuments.map((doc) => (
                  <option key={doc.id} value={doc.id}>
                    {doc.name}
                  </option>
                ))}
              </select>
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
