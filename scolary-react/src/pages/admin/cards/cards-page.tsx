import { useCallback, useEffect, useMemo, useState } from "react";
import type { Row } from "@tanstack/react-table";
import { Controller, useForm } from "react-hook-form";

import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import { Textarea } from "../../../components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "../../../components/ui/select";
import {
  DataTable,
  type ColumnDef
} from "../../../components/data-table/data-table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "../../../components/ui/dialog";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger
} from "../../../components/ui/tabs";
import { CodeEditor } from "../../../components/ui/code-editor";
import { cn } from "../../../lib/utils";
import {
  type Card,
  type CardPayload,
  useCards,
  useCreateCard,
  useUpdateCard,
  useDeleteCard,
  useRenderCardPdf,
  useUploadCardImage
} from "../../../services/card-service";
import { useMentions } from "../../../services/mention-service";
import { ConfirmDialog } from "@/components/confirm-dialog";

const cardTypes = [
  { value: "student_card", label: "Student card" },
  { value: "badge", label: "Badge" }
];

type CardFormValues = {
  name: string;
  description?: string;
  card_type: string;
  html_template: string;
  css_styles: string;
  mentionId: string;
  journeyId: string;
};

const defaultHtmlTemplate = `<div class="card">
  <h2>{{student_name}}</h2>
  <p>ID: {{student_id}}</p>
</div>`;

const defaultCss = `.card {
  width: 280px;
  border-radius: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  color: white;
  font-family: sans-serif;
}`;

const defaultFormValues: CardFormValues = {
  name: "Untitled card",
  description: "",
  card_type: "student_card",
  html_template: defaultHtmlTemplate,
  css_styles: defaultCss,
  mentionId: "",
  journeyId: ""
};

const defaultTemplateData = {
  student_name: "Jane Doe",
  student_id: "STD-2025-0001",
  registration_number: "REG-2025-042",
  program_name: "Computer Science",
  mention_name: "Informatique",
  journey_name: "L1 - Common core",
  academic_year: "2025-2026"
};

const defaultTemplateDataJson = JSON.stringify(defaultTemplateData, null, 2);

type Feedback = { type: "success" | "error"; text: string };

const apiBaseUrl =
  (() => {
    const fromEnv = import.meta.env.VITE_SCOLARY_API_URL;
    if (fromEnv) {
      try {
        const url = new URL(fromEnv);
        url.pathname = url.pathname.replace(/\/$/, "");
        return url.toString();
      } catch {
        // ignore invalid env URL
      }
    }
    if (typeof window !== "undefined" && window.location?.origin) {
      return window.location.origin;
    }
    return "";
  })() || "";

const previewBaseHref =
  apiBaseUrl ||
  (typeof window !== "undefined" && window.location?.origin
    ? window.location.origin
    : "");

const resolveAssetUrl = (rawPath: string) => {
  if (!rawPath || rawPath.includes("{{")) return rawPath;

  try {
    const parsed = new URL(rawPath);
    if (parsed.protocol === "http:" || parsed.protocol === "https:") {
      return parsed.toString();
    }
  } catch {
    // rawPath is relative, fall through to prefix with API base
  }

  if (!apiBaseUrl) return rawPath;

  try {
    const base = new URL(apiBaseUrl);
    base.pathname = [
      base.pathname.replace(/\/$/, ""),
      rawPath.replace(/^\//, "")
    ]
      .filter(Boolean)
      .join("/");
    return base.toString();
  } catch {
    return rawPath;
  }
};

const normalizeTemplateAssets = (template: string) => {
  if (!template || typeof DOMParser === "undefined") return template;

  try {
    const doc = new DOMParser().parseFromString(template, "text/html");
    doc.querySelectorAll("img").forEach((img) => {
      const src = img.getAttribute("src")?.trim();
      if (!src) return;
      img.setAttribute("src", resolveAssetUrl(src));
    });
    return doc.body.innerHTML || template;
  } catch {
    return template;
  }
};

const toFormValues = (card?: Card | null): CardFormValues => ({
  name: card?.name ?? "Untitled card",
  description: card?.description ?? "",
  card_type: card?.card_type ?? "student_card",
  html_template: card?.html_template ?? defaultHtmlTemplate,
  css_styles: card?.css_styles ?? defaultCss,
  mentionId: card?.id_mention ? String(card.id_mention) : "",
  journeyId: card?.id_journey ? String(card.id_journey) : ""
});

const toPayload = (values: CardFormValues): CardPayload => {
  const mentionId = Number(values.mentionId);
  const journeyId = Number(values.journeyId);

  return {
    name: values.name.trim() || "Untitled card",
    description: values.description?.trim() || undefined,
    card_type: values.card_type,
    html_template: values.html_template,
    css_styles: values.css_styles,
    id_mention:
      Number.isFinite(mentionId) && mentionId > 0 ? mentionId : undefined,
    id_journey:
      Number.isFinite(journeyId) && journeyId > 0 ? journeyId : undefined
  };
};

const formatCardTypeLabel = (value: string) =>
  cardTypes.find((type) => type.value === value)?.label ?? "Custom template";

const buildPreviewDocument = (
  card: Pick<Card, "html_template" | "css_styles">,
  cardsPerPage: number
) => {
  const layout = A4_LAYOUTS[cardsPerPage] ?? A4_LAYOUTS[4];
  const copies = Math.max(1, cardsPerPage);
  const templateWithAssets = normalizeTemplateAssets(card.html_template);

  const slotMarkup = Array.from({ length: copies })
    .map(
      () =>
        `<div class="card-slot"><div class="card-content">${templateWithAssets}</div></div>`
    )
    .join("");

  return `<!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8" />
      ${previewBaseHref ? `<base href="${previewBaseHref}/" />` : ""}
      <style>
        @page {
          size: A4;
          margin: 0;
        }
        :root {
          --page-width: ${A4_WIDTH_PX}px;
          --page-height: ${A4_HEIGHT_PX}px;
          --padding: ${A4_PADDING_PX}px;
          --gap: ${CARD_GAP_PX}px;
        }
        * {
          box-sizing: border-box;
        }
        html, body {
          margin: 0;
          padding: 0;
          width: var(--page-width);
          height: var(--page-height);
          background: #f8fafc;
        }
        body {
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .sheet {
          width: calc(var(--page-width) - (var(--padding) * 2));
          height: calc(var(--page-height) - (var(--padding) * 2));
          padding: var(--padding);
          background: white;
          border: 1px solid #e2e8f0;
          box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        }
        .print-page {
          display: grid;
          grid-template-columns: repeat(${layout.cols}, minmax(0, 1fr));
          grid-template-rows: repeat(${layout.rows}, minmax(0, 1fr));
          gap: var(--gap);
          width: 100%;
          height: 100%;
          align-items: stretch;
          justify-items: stretch;
        }
        .card-slot {
          border: 1px dashed #cbd5e1;
          background: repeating-linear-gradient(
            45deg,
            rgba(148, 163, 184, 0.07),
            rgba(148, 163, 184, 0.07) 6px,
            rgba(148, 163, 184, 0.04) 6px,
            rgba(148, 163, 184, 0.04) 12px
          );
          overflow: hidden;
          page-break-inside: avoid;
          display: flex;
          align-items: stretch;
          justify-content: stretch;
        }
        .card-slot > .card-content {
          width: 100%;
          height: 100%;
          background: white;
        }
        ${card.css_styles || ""}
      </style>
    </head>
    <body>
      <div class="sheet">
        <div class="print-page">
          ${slotMarkup}
        </div>
      </div>
    </body>
  </html>`;
};

// --- A4 + K logic -------------------------------------------------

const A4_WIDTH_PX = 794;
const A4_HEIGHT_PX = 1123;
const A4_PADDING_PX = 4; // padding externe A4
const CARD_GAP_PX = 4; // gap entre cartes

const A4_LAYOUTS: Record<
  number,
  {
    rows: number;
    cols: number;
  }
> = {
  4: { rows: 2, cols: 2 },
  6: { rows: 3, cols: 2 },
  8: { rows: 4, cols: 2 }
};

interface CardFormProps {
  mode: "create" | "edit";
  initialValues?: CardFormValues;
  isSubmitting: boolean;
  onSubmit: (values: CardFormValues) => Promise<void>;
  onCancel: () => void;
  mentionOptions: { value: string; label: string }[];
  isMentionsLoading: boolean;
  onRenderPdf: (payload: {
    html_template: string;
    css_styles: string;
    data: Record<string, unknown>;
    copies: number;
  }) => Promise<Blob>;
  isRenderingPdf: boolean;
  onUploadImage?: (file: File) => Promise<{ filename?: string; path: string }>;
  isUploadingImage?: boolean;
}

/**
 * FORM:
 * - Left: infos + Template editor (HTML/CSS tabs)
 * - Right: PDF preview + sample JSON in tabs
 */
/**
 * FORM:
 * - Left: infos + Template editor (HTML/CSS/JSON tabs)
 * - Right: full PDF preview (backend)
 */
const CardForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  mentionOptions,
  isMentionsLoading,
  onRenderPdf,
  isRenderingPdf,
  onUploadImage,
  isUploadingImage = false
}: CardFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    control,
    setValue
  } = useForm<CardFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  // editor tabs now include json
  const [editorTab, setEditorTab] = useState<"html" | "css" | "data">("html");

  const [cardsPerPage, setCardsPerPage] = useState<number>(4);
  const [sampleDataInput, setSampleDataInput] = useState<string>(
    defaultTemplateDataJson
  );
  const [sampleDataError, setSampleDataError] = useState<string | null>(null);
  const [parsedSampleData, setParsedSampleData] =
    useState<Record<string, unknown>>(defaultTemplateData);

  const [renderError, setRenderError] = useState<string | null>(null);
  const [lastPdfUrl, setLastPdfUrl] = useState<string | null>(null);
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  useEffect(() => {
    try {
      const parsed = JSON.parse(sampleDataInput);
      setParsedSampleData(parsed);
      setSampleDataError(null);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Invalid sample data JSON.";
      setSampleDataError(message);
    }
  }, [sampleDataInput]);

  useEffect(
    () => () => {
      if (lastPdfUrl) URL.revokeObjectURL(lastPdfUrl);
    },
    [lastPdfUrl]
  );

  const htmlTemplate = watch("html_template");
  const cssStyles = watch("css_styles");

  const handleRenderPdfClick = async () => {
    if (sampleDataError) {
      setRenderError(sampleDataError);
      // optionally auto-switch to JSON tab if invalid
      setEditorTab("data");
      return;
    }

    const template = typeof htmlTemplate === "string" ? htmlTemplate : "";
    const styles = typeof cssStyles === "string" ? cssStyles : "";

    if (!template.trim()) {
      setRenderError("Template is required before rendering a PDF.");
      setEditorTab("html");
      return;
    }

    try {
      setRenderError(null);
      // Save latest changes before rendering
      await handleSubmit(async (values) => {
        await onSubmit(values);
      })();

      const resolvedTemplate = normalizeTemplateAssets(template);
      const blob = await onRenderPdf({
        html_template: resolvedTemplate,
        css_styles: styles,
        data: parsedSampleData,
        copies: cardsPerPage
      });

      if (lastPdfUrl) URL.revokeObjectURL(lastPdfUrl);
      const nextUrl = URL.createObjectURL(blob);
      setLastPdfUrl(nextUrl);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to render PDF.";
      setRenderError(message);
    }
  };

  return (
    <form
      className="grid min-h-0 gap-6 lg:grid-cols-[520px_minmax(0,1fr)]"
      onSubmit={handleSubmit(onSubmit)}
    >
      {/* LEFT COLUMN: INFO + EDITOR (HTML/CSS/JSON tabs) */}
      <div className="min-w-0 space-y-4">
        <div className="space-y-4 rounded-lg border bg-muted/30 p-4">
          <details className="group rounded-lg border bg-background/60 p-3">
            <summary className="flex cursor-pointer list-none items-center justify-between">
              <div>
                <p className="text-sm font-medium">Card settings</p>
                <p className="text-xs text-muted-foreground">
                  Show or hide layout parameters.
                </p>
              </div>
              <span className="text-xs text-muted-foreground transition group-open:rotate-90">
                ▶
              </span>
            </summary>
            <div className="mt-3 space-y-4">
              <div className="w-40">
                <label className="mb-1 block text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
                  Cartes par A4
                </label>
                <Select
                  value={String(cardsPerPage)}
                  onValueChange={(value) => setCardsPerPage(Number(value))}
                >
                  <SelectTrigger className="h-8">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="4">4 par A4</SelectItem>
                    <SelectItem value="6">6 par A4</SelectItem>
                    <SelectItem value="8">8 par A4</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </details>

          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="card-name">
              Card name
            </label>
            <Input
              id="card-name"
              placeholder="ID card template"
              {...register("name", { required: "Name is required" })}
              className={cn(errors.name && "border-destructive")}
            />
            {errors.name ? (
              <p className="text-xs text-destructive">{errors.name.message}</p>
            ) : null}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="card-mention">
              Attach to mention
            </label>
            <Controller
              control={control}
              name="mentionId"
              render={({ field }) => (
                <Select
                  value={field.value || "none"}
                  onValueChange={(value) =>
                    field.onChange(value === "none" ? "" : value)
                  }
                  disabled={isMentionsLoading || mentionOptions.length === 0}
                >
                  <SelectTrigger id="card-mention">
                    <SelectValue
                      placeholder={
                        isMentionsLoading
                          ? "Loading mentions…"
                          : mentionOptions.length === 0
                            ? "No mention available"
                            : "Optional mention"
                      }
                    />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">No mention</SelectItem>
                    {mentionOptions.map((mention) => (
                      <SelectItem key={mention.value} value={mention.value}>
                        {mention.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            <p className="text-[11px] text-muted-foreground">
              Choose which mention inherits this template. Leave empty for
              global usage.
            </p>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="card-description">
              Description
            </label>
            <Textarea
              id="card-description"
              placeholder="Optional description…"
              {...register("description")}
            />
          </div>

          <div className="flex items-center justify-between gap-2 pt-2">
            <div className="flex items-center gap-2">
              <Button
                type="submit"
                variant="default"
                size="sm"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Saving…" : "Save template"}
              </Button>
              <label className="relative">
                <input
                  type="file"
                  accept="image/*"
                  className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
                  onChange={async (event) => {
                    const file = event.target.files?.[0];
                    if (!file) return;
                    try {
                      if (!onUploadImage) {
                        throw new Error("Upload not available.");
                      }
                      const uploaded = await onUploadImage(file);
                      const assetPath =
                        uploaded?.path || uploaded?.filename || "";
                      const normalized = resolveAssetUrl(assetPath);
                      if (normalized) {
                        setUploadedImages((prev) =>
                          prev.includes(normalized)
                            ? prev
                            : [...prev, normalized]
                        );
                      } else {
                        throw new Error("Upload succeeded without a path.");
                      }
                    } catch (error) {
                      const message =
                        error instanceof Error
                          ? error.message
                          : "Unable to upload image.";
                      setRenderError(message);
                    } finally {
                      event.target.value = "";
                    }
                  }}
                  disabled={!onUploadImage || isUploadingImage}
                />
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  disabled={!onUploadImage || isUploadingImage}
                >
                  {isUploadingImage ? "Uploading…" : "Upload image"}
                </Button>
              </label>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleRenderPdfClick}
                disabled={
                  isRenderingPdf || Boolean(sampleDataError) || isSubmitting
                }
              >
                {isRenderingPdf ? "Rendering…" : "Render PDF"}
              </Button>
            </div>

            {renderError ? (
              <p className="text-xs text-destructive">{renderError}</p>
            ) : null}
          </div>

          {uploadedImages.length ? (
            <div className="rounded-md border bg-background p-3">
              <p className="text-xs font-semibold text-foreground">
                Uploaded images
              </p>
              <div className="mt-2 space-y-2">
                {uploadedImages.map((path) => (
                  <div
                    key={path}
                    className="flex items-center justify-between gap-2 rounded border px-2 py-1"
                  >
                    <p className="flex-1 truncate text-xs font-medium">
                      {path}
                    </p>
                    <div className="flex items-center gap-2">
                      <Button
                        type="button"
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          const snippet = `<img src="${path}" alt="Card image" />`;
                          const current = watch("html_template") || "";
                          setValue(
                            "html_template",
                            `${current}\n${snippet}`,
                            { shouldDirty: true }
                          );
                          setEditorTab("html");
                        }}
                      >
                        Insert tag
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
              <p className="mt-2 text-[11px] text-muted-foreground">
                Insert adds an &lt;img&gt; tag referencing the uploaded asset.
              </p>
            </div>
          ) : null}
        </div>

        {/* Template + JSON tabs */}
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium">Template editor</label>
          <p className="text-xs text-muted-foreground">
            HTML / CSS / Sample JSON
          </p>
        </div>

        <Tabs
          value={editorTab}
          onValueChange={(v) => setEditorTab(v as "html" | "css" | "data")}
        >
          <TabsList className="mt-3 grid w-full grid-cols-3">
            <TabsTrigger value="html">HTML</TabsTrigger>
            <TabsTrigger value="css">CSS</TabsTrigger>
            <TabsTrigger value="data">JSON</TabsTrigger>
          </TabsList>

          <TabsContent value="html" className="mt-4">
            <Controller
              control={control}
              name="html_template"
              rules={{ required: "Template is required" }}
              render={({ field }) => (
                <CodeEditor
                  id="card-html"
                  language="html"
                  value={field.value}
                  onChange={field.onChange}
                  minHeight={360}
                  className={cn(
                    errors.html_template && "ring-2 ring-destructive"
                  )}
                />
              )}
            />
            {errors.html_template ? (
              <p className="mt-2 text-xs text-destructive">
                {errors.html_template.message}
              </p>
            ) : null}
          </TabsContent>

          <TabsContent value="css" className="mt-4">
            <Controller
              control={control}
              name="css_styles"
              rules={{ required: "Styles are required" }}
              render={({ field }) => (
                <CodeEditor
                  id="card-css"
                  language="css"
                  value={field.value}
                  onChange={field.onChange}
                  minHeight={360}
                  className={cn(errors.css_styles && "ring-2 ring-destructive")}
                />
              )}
            />
            {errors.css_styles ? (
              <p className="mt-2 text-xs text-destructive">
                {errors.css_styles.message}
              </p>
            ) : null}
          </TabsContent>

          <TabsContent value="data" className="mt-4">
            <CodeEditor
              id="card-sample-data"
              language="json"
              value={sampleDataInput}
              onChange={(value) => setSampleDataInput(value ?? "")}
              minHeight={360}
              className={cn(
                "bg-background",
                sampleDataError && "ring-2 ring-destructive"
              )}
            />
            {sampleDataError ? (
              <p className="mt-2 text-xs text-destructive">{sampleDataError}</p>
            ) : (
              <p className="mt-2 text-[11px] text-muted-foreground">
                Use placeholders like <code>{"{{ student_name }}"}</code> in
                HTML.
              </p>
            )}
          </TabsContent>
        </Tabs>
      </div>

      {/* RIGHT COLUMN: FULL PDF PREVIEW */}
      <div className="min-w-0 flex min-h-0 flex-col">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-sm font-medium">Rendered PDF preview</p>
          <p className="text-xs text-muted-foreground">
            Backend render (iframe).
          </p>
        </div>

        <div className="flex-1 min-h-0 overflow-hidden rounded-lg border bg-background">
          {lastPdfUrl ? (
            <iframe
              title="Rendered PDF"
              src={lastPdfUrl}
              className="h-full w-full"
            />
          ) : (
            <div className="flex h-full items-center justify-center p-6">
              <p className="text-sm text-muted-foreground">
                Click <strong>Render PDF</strong> to preview it here.
              </p>
            </div>
          )}
        </div>
      </div>
    </form>
  );
};

export const CardsPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingCard, setEditingCard] = useState<Card | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [cardToDelete, setCardToDelete] = useState<Card | null>(null);

  const offset = (page - 1) * pageSize;
  const {
    data: cardsResponse,
    isPending,
    isError,
    error
  } = useCards({ offset, limit: pageSize });
  const cards = cardsResponse?.data ?? [];
  const totalCards = cardsResponse?.count ?? cards.length;

  const createCard = useCreateCard();
  const updateCard = useUpdateCard();
  const deleteCard = useDeleteCard();
  const renderCardPdf = useRenderCardPdf();
  const uploadCardImage = useUploadCardImage();
  const { data: mentionsResponse, isPending: areMentionsLoading } = useMentions(
    { limit: 100 }
  );

  const mentionOptions = useMemo(
    () =>
      (mentionsResponse?.data ?? []).map((mention) => ({
        value: String(mention.id),
        label: mention.name
      })),
    [mentionsResponse]
  );

  const openCreateForm = useCallback(() => {
    setEditingCard(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((card: Card) => {
    setEditingCard(card);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setIsFormOpen(false);
    setEditingCard(null);
  }, []);

  const handleSubmit = useCallback(
    async (values: CardFormValues) => {
      const payload = toPayload(values);

      try {
        if (editingCard) {
          const updated = await updateCard.mutateAsync({
            id: editingCard.id,
            payload
          });
          setEditingCard(updated ?? editingCard);
          setFeedback({ type: "success", text: "Card updated successfully." });
        } else {
          const created = await createCard.mutateAsync(payload);
          setEditingCard(created ?? null);
          setFeedback({ type: "success", text: "Card created successfully." });
        }
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save card.";
        setFeedback({ type: "error", text: message });
      }
    },
    [createCard, editingCard, updateCard]
  );

  const handleDelete = useCallback(async () => {
    if (!cardToDelete) {
      return;
    }

    try {
      await deleteCard.mutateAsync(cardToDelete.id);
      setFeedback({ type: "success", text: "Card deleted successfully." });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete card.";
      setFeedback({ type: "error", text: message });
    } finally {
      setCardToDelete(null);
    }
  }, [cardToDelete, deleteCard]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<Card>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Card",
        cell: ({ row }) => (
          <div className="flex flex-col">
            <span className="font-medium">{row.original.name}</span>
            <span className="text-xs text-muted-foreground">
              {formatCardTypeLabel(row.original.card_type)}
            </span>
          </div>
        )
      },
      {
        id: "mention",
        header: "Mention",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.mention?.name ?? "All mentions"}
          </span>
        )
      },
      {
        id: "journey",
        header: "Journey",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.journey?.name ?? "All journeys"}
          </span>
        )
      },
      {
        id: "actions",
        header: "",
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleEdit(row.original)}
            >
              Edit
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="text-destructive hover:text-destructive"
              onClick={() => setCardToDelete(row.original)}
            >
              Delete
            </Button>
          </div>
        )
      }
    ];
  }, [handleEdit]);

  const renderCardGridItem = useCallback(
    (row: Row<Card>) => {
      const card = row.original;
      const previewDocument = buildPreviewDocument(card, 4);

      return (
        <div className="flex h-full flex-col gap-4 rounded-lg border bg-background p-4 shadow-sm">
          <div className="h-40 w-full overflow-hidden rounded-md border bg-muted/20">
            <iframe
              title={`${card.name}-preview`}
              srcDoc={previewDocument}
              className="h-full w-full"
            />
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground">{card.name}</p>
            <p className="text-xs text-muted-foreground">
              {formatCardTypeLabel(card.card_type)}
            </p>
          </div>
          <div className="space-y-1 text-xs text-muted-foreground">
            <p>Mention: {card.mention?.name ?? "All mentions"}</p>
            <p>Journey: {card.journey?.name ?? "All journeys"}</p>
          </div>
          <div className="mt-auto flex gap-2">
            <Button
              size="sm"
              variant="outline"
              className="flex-1"
              onClick={() => handleEdit(card)}
            >
              Edit
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="flex-1 text-destructive hover:text-destructive"
              onClick={() => setCardToDelete(card)}
            >
              Delete
            </Button>
          </div>
        </div>
      );
    },
    [handleEdit]
  );

  const isSubmitting = createCard.isPending || updateCard.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Cards & badges
          </h1>
          <p className="text-sm text-muted-foreground">
            Design student cards or badges and link them to mentions or
            journeys.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Create card
        </Button>
      </div>

      {feedback ? (
        <div
          className={cn(
            "flex items-start justify-between gap-4 rounded-md border px-4 py-3 text-sm",
            feedback.type === "success"
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-destructive/30 bg-destructive/10 text-destructive"
          )}
        >
          <span>{feedback.text}</span>
          <button
            className="text-xs font-medium underline"
            onClick={() => setFeedback(null)}
          >
            Dismiss
          </button>
        </div>
      ) : null}

      <Dialog
        open={isFormOpen}
        onOpenChange={(open) => {
          setIsFormOpen(open);
          if (!open) {
            setEditingCard(null);
          }
        }}
      >
        {/* WIDER MODAL + INTERNAL SCROLL */}
        <DialogContent
          className="
            w-[98vw]
            max-w-[1400px]
            h-[96vh]
            overflow-hidden
            p-0
          "
        >
          <div className="flex h-full min-h-0 flex-col">
            <DialogHeader className="border-b px-5 py-2">
              <DialogTitle>
                {editingCard ? "Edit card" : "Create new card"}
              </DialogTitle>
              <DialogDescription>
                {editingCard
                  ? "Update the template to keep printed cards in sync."
                  : "Create a card template that can be reused everywhere."}
              </DialogDescription>
            </DialogHeader>

            <div className="flex-1 min-h-0 overflow-y-auto p-5">
              <CardForm
                mode={editingCard ? "edit" : "create"}
                initialValues={toFormValues(editingCard)}
                onSubmit={handleSubmit}
                onCancel={closeForm}
                isSubmitting={isSubmitting}
                mentionOptions={mentionOptions}
                isMentionsLoading={areMentionsLoading}
                onRenderPdf={renderCardPdf.mutateAsync}
                isRenderingPdf={renderCardPdf.isPending}
                onUploadImage={uploadCardImage.mutateAsync}
                isUploadingImage={uploadCardImage.isPending}
              />
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(cardToDelete)}
        title="Delete card"
        description={
          cardToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>{cardToDelete.name}</strong>? This action cannot be
              undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteCard.isPending}
        onCancel={() => setCardToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={cards}
        isLoading={isPending}
        searchPlaceholder="Search cards"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load cards")
            : "No cards found"
        }
        enableViewToggle
        renderGridItem={renderCardGridItem}
        gridClassName="sm:grid-cols-2 xl:grid-cols-3"
        gridEmptyState={
          <div className="flex h-40 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground">
            No cards available.
          </div>
        }
        totalItems={totalCards}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
