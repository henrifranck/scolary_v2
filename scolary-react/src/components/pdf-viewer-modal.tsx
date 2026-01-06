import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { resolveAssetUrl } from "@/lib/resolve-asset-url";
import { PdfStreamingViewer } from "@/modules/templates/PdfStreamingViewer";

type PdfViewerModalProps = {
  open: boolean;
  url?: string;
  urls?: string[];
  title?: string;
  onOpenChange: (open: boolean) => void;
};

export function PdfViewerModal({
  open,
  url,
  urls,
  title,
  onOpenChange
}: PdfViewerModalProps) {
  const resolvedUrls = useMemo(() => {
    const list = urls && urls.length ? urls : url ? [url] : [];
    return list
      .map((entry) => resolveAssetUrl(entry))
      .filter((entry): entry is string => Boolean(entry));
  }, [url, urls]);

  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    setActiveIndex(0);
  }, [url, urls]);

  const currentUrl = resolvedUrls[activeIndex] ?? null;
  const hasPdf = Boolean(currentUrl);

  useEffect(() => {}, [open, url, currentUrl]);

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
              onClick={() => currentUrl && window.open(currentUrl, "_blank")}
            >
              Télécharger le PDF
            </Button>
          ) : null}
        </div>

        {resolvedUrls.length > 1 ? (
          <Tabs
            value={String(activeIndex)}
            onValueChange={(value) => setActiveIndex(Number(value))}
          >
            <TabsList>
              {resolvedUrls.map((_, idx) => (
                <TabsTrigger key={idx} value={String(idx)}>
                  {idx === 0 ? "Recto" : idx === 1 ? "Verso" : `PDF ${idx + 1}`}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
        ) : null}

        <div className="flex-1">
          <ScrollArea className="h-[70vh] w-full rounded-md border bg-background">
            <div className="flex items-center justify-center p-4">
              {hasPdf ? (
                <PdfStreamingViewer
                  pdfUrl={currentUrl as string}
                  readyPage={null}
                  resetKey={currentUrl as string}
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
