import { Dispatch, SetStateAction } from "react";

import {
  StudentAnnualProps,
  StudentDocumentState
} from "@/components/student-form/student-form-types";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";

type DocumentSummaryProps = {
  displayAnnualRegisters: Array<StudentAnnualProps>;
};

type DocumentEditorProps = {
  annualRegisterDrafts: Array<StudentAnnualProps & { isEditing?: boolean; isNew?: boolean }>;
  documentDrafts: Record<string, StudentDocumentState[]>;
  documentDescriptions: Record<string, string>;
  documentUploadError: string | null;
  documentUploadingIndex: number | null;
  getAnnualKey: (
    annual: StudentAnnualProps & { id?: number },
    index: number
  ) => string;
  handleUploadDocument: (annualIndex: number, file: File | null) => void;
  setDocumentDescriptions: Dispatch<
    SetStateAction<Record<string, string>>
  >;
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
  setDocumentDescriptions
}: DocumentEditorProps) => (
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
            </div>
            <div className="space-y-2">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Description
              </label>
              <input
                type="text"
                className="h-9 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={documentDescriptions[annualKey] ?? ""}
                onChange={(event) =>
                  setDocumentDescriptions((previous) => ({
                    ...previous,
                    [annualKey]: event.target.value
                  }))
                }
                placeholder="Ajouter une description"
              />
            </div>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {docs.map((doc, docIndex) => (
                <a
                  key={`${annualKey}-doc-${docIndex}`}
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
              <label className="flex aspect-square cursor-pointer items-center justify-center rounded-lg border border-dashed bg-muted/10 text-sm text-muted-foreground">
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(event) =>
                    handleUploadDocument(index, event.target.files?.[0] ?? null)
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
      <p className="text-sm text-muted-foreground">Aucun document à afficher.</p>
    )}
  </div>
);
