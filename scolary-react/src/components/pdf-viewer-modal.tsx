import { useEffect, useMemo } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { PdfStreamingViewer } from "@/modules/templates/PdfStreamingViewer";

type PdfViewerModalProps = {
  open: boolean;
  url?: string;
  title?: string;
  onOpenChange: (open: boolean) => void;
};

export function PdfViewerModal({
  open,
  url,
  title,
  onOpenChange
}: PdfViewerModalProps) {
  const resolvedUrl = useMemo(() => resolveAssetUrl(url), [url]);
  const hasPdf = Boolean(resolvedUrl);

  useEffect(() => {}, [open, url, resolvedUrl]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] max-w-5xl gap-3">
        <DialogHeader>
          <DialogTitle>{title || "Document PDF"}</DialogTitle>
          <DialogDescription>
            {hasPdf ? "Utilisez les flèches pour naviguer." : "Aucun PDF à afficher."}
          </DialogDescription>
        </DialogHeader>

        <div className="flex items-center justify-between gap-3 rounded-md border bg-muted/40 px-3 py-2">
          <div className="text-sm font-medium">
            {hasPdf ? "Document chargé" : "Aucun document"}
          </div>
          {hasPdf ? (
            <Button
              variant="outline"
              size="sm"
              onClick={() => resolvedUrl && window.open(resolvedUrl, "_blank")}
            >
              Télécharger le PDF
            </Button>
          ) : null}
        </div>

        <div className="flex-1">
          <ScrollArea className="h-[70vh] w-full rounded-md border bg-background">
            <div className="flex items-center justify-center p-4">
              {hasPdf ? (
                <PdfStreamingViewer
                  pdfUrl={resolvedUrl}
                  readyPage={null}
                  resetKey={resolvedUrl}
                />
              ) : (
                <div className="text-sm text-muted-foreground">Aucun PDF sélectionné.</div>
              )}
            </div>
          </ScrollArea>
        </div>
      </DialogContent>
    </Dialog>
  );
}
