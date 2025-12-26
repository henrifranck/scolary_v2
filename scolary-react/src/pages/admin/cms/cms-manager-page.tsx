import { Pencil, Trash2 } from "lucide-react";
import { useCallback, useMemo, useRef, useState } from "react";

import { ConfirmDialog } from "../../../components/confirm-dialog";
import { Button } from "../../../components/ui/button";
import {
  DataTable,
  type ColumnDef
} from "../../../components/data-table/data-table";
import { Input } from "../../../components/ui/input";
import { Textarea } from "../../../components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "../../../components/ui/dialog";
import { cn } from "../../../lib/utils";
import {
  type CmsPage,
  type CmsPagePayload,
  useCmsPages,
  useCreateCmsPage,
  useDeleteCmsPage,
  useUpdateCmsPage
} from "../../../services/cms-page-service";
import { ActionButton } from "@/components/action-button";

const emptyForm: CmsPagePayload = {
  slug: "",
  title: "",
  content_json: "",
  draft_content: "",
  meta_json: "",
  status: "published"
};

type Feedback = { type: "success" | "error"; text: string };

export const CmsManagerPage = () => {
  const [selectedPage, setSelectedPage] = useState<CmsPage | null>(null);
  const [formValues, setFormValues] = useState<CmsPagePayload>(emptyForm);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isDeleteConfirmOpen, setIsDeleteConfirmOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<CmsPage | null>(null);
  const editorRef = useRef<HTMLTextAreaElement | null>(null);
  const highlightRef = useRef<HTMLPreElement | null>(null);

  const {
    data: pagesResponse,
    isPending,
    isError,
    error
  } = useCmsPages({ limit: 200 });
  const pages = pagesResponse?.data ?? [];

  const createPage = useCreateCmsPage();
  const updatePage = useUpdateCmsPage();
  const deletePage = useDeleteCmsPage();

  const selectPage = useCallback((page: CmsPage | null) => {
    setSelectedPage(page);
    setFormValues({
      slug: page?.slug ?? "",
      title: page?.title ?? "",
      content_json: page?.content_json ?? "",
      draft_content: page?.draft_content ?? page?.content_json ?? "",
      meta_json: page?.meta_json ?? "",
      status: page?.status ?? "published"
    });
  }, []);

  const handleCreateNew = useCallback(() => {
    selectPage(null);
    setIsEditorOpen(true);
  }, [selectPage, setDeleteTarget, setIsDeleteConfirmOpen]);

  const handleSave = useCallback(async () => {
    setFeedback(null);
    const contentValue = formValues.content_json ?? "";
    const metaValue = formValues.meta_json ?? "";
    const payload: CmsPagePayload = {
      slug: formValues.slug.trim(),
      title: formValues.title?.trim() || null,
      content_json: contentValue.length ? contentValue : null,
      draft_content: formValues.draft_content?.trim() || null,
      meta_json: metaValue.length ? metaValue : null,
      status: formValues.status?.trim() || "published"
    };

    if (!payload.slug) {
      setFeedback({ type: "error", text: "Le slug est requis." });
      return;
    }

    try {
      if (selectedPage?.id) {
        await updatePage.mutateAsync({ id: selectedPage.id, payload });
        setFeedback({ type: "success", text: "Page mise a jour." });
      } else {
        const created = await createPage.mutateAsync(payload);
        selectPage(created);
        setFeedback({ type: "success", text: "Page creee." });
      }
      setIsEditorOpen(true);
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Impossible d'enregistrer la page.";
      setFeedback({ type: "error", text: message });
    }
  }, [createPage, formValues, selectPage, selectedPage, updatePage]);

  const handlePublish = useCallback(async () => {
    setFeedback(null);
    const draftValue = (formValues.draft_content ?? "").trim();
    if (!draftValue) {
      setFeedback({ type: "error", text: "Le brouillon est vide." });
      return;
    }

    const basePayload: CmsPagePayload = {
      slug: formValues.slug.trim(),
      title: formValues.title?.trim() || null,
      content_json: draftValue,
      draft_content: draftValue,
      meta_json: formValues.meta_json?.trim() || null,
      status: "published"
    };

    if (!basePayload.slug) {
      setFeedback({ type: "error", text: "Le slug est requis." });
      return;
    }

    try {
      if (selectedPage?.id) {
        const updated = await updatePage.mutateAsync({
          id: selectedPage.id,
          payload: basePayload
        });
        selectPage(updated);
        setFeedback({ type: "success", text: "Page publiee." });
      } else {
        const created = await createPage.mutateAsync(basePayload);
        selectPage(created);
        setFeedback({ type: "success", text: "Page publiee." });
      }
      setIsEditorOpen(true);
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Impossible de publier la page.";
      setFeedback({ type: "error", text: message });
    }
  }, [createPage, formValues, selectPage, selectedPage, updatePage]);

  const handleDelete = useCallback(async () => {
    const target = deleteTarget ?? selectedPage;
    if (!target?.id) {
      return;
    }
    try {
      await deletePage.mutateAsync(target.id);
      if (selectedPage?.id === target.id) {
        selectPage(null);
      }
      setFeedback({ type: "success", text: "Page supprimee." });
      setIsDeleteConfirmOpen(false);
      setDeleteTarget(null);
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Impossible de supprimer la page.";
      setFeedback({ type: "error", text: message });
      setIsDeleteConfirmOpen(false);
      setDeleteTarget(null);
    }
  }, [deletePage, deleteTarget, selectPage, selectedPage]);

  const highlightHtml = useCallback((value: string) => {
    if (!value) {
      return "";
    }
    const escaped = value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    const withComments = escaped.replace(
      /(&lt;!--[\s\S]*?--&gt;)/g,
      '<span class="text-muted-foreground">$1</span>'
    );

    return withComments.replace(
      /(&lt;\/?)([A-Za-z0-9:-]+)([^&]*?)(\/?&gt;)/g,
      (_match, open, name, attrs, close) => {
        const highlightedAttrs = attrs.replace(
          /([A-Za-z0-9:-]+)(=)("[^"]*"|'[^']*')?/g,
          (_attrMatch, attrName, eq, attrValue) => {
            const valuePart = attrValue
              ? `<span class="text-emerald-600">${attrValue}</span>`
              : "";
            return `<span class="text-sky-600">${attrName}</span><span class="text-muted-foreground">${eq}</span>${valuePart}`;
          }
        );
        return `<span class="text-muted-foreground">${open}</span><span class="text-amber-600">${name}</span>${highlightedAttrs}<span class="text-muted-foreground">${close}</span>`;
      }
    );
  }, []);

  const highlightedHtml = useMemo(
    () => highlightHtml(formValues.draft_content ?? ""),
    [formValues.draft_content, highlightHtml]
  );

  const handleEdit = (row: any) => {
    selectPage(row.original);
    setIsEditorOpen(true);
  };

  const handleConfirmDelete = (row: any) => {
    setDeleteTarget(row.original);
    setIsDeleteConfirmOpen(true);
  };

  const handleEditorScroll = useCallback(
    (event: React.UIEvent<HTMLTextAreaElement>) => {
      if (!highlightRef.current) {
        return;
      }
      highlightRef.current.scrollTop = event.currentTarget.scrollTop;
      highlightRef.current.scrollLeft = event.currentTarget.scrollLeft;
    },
    []
  );

  const columns = useMemo<ColumnDef<CmsPage>[]>(() => {
    return [
      {
        accessorKey: "slug",
        header: "Slug"
      },
      {
        accessorKey: "title",
        header: "Titre"
      },
      {
        id: "draft",
        header: "Brouillon",
        cell: ({ row }) => (
          <span className="text-sm text-muted-foreground">
            {row.original.draft_content ? "Oui" : "Non"}
          </span>
        )
      },
      {
        accessorKey: "status",
        header: "Statut"
      },
      {
        id: "actions",
        header: "",
        cell: ({ row }) => (
          <div className="flex items-center justify-end gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                selectPage(row.original);
                setIsEditorOpen(true);
              }}
              aria-label="Editer"
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="text-destructive hover:text-destructive"
              onClick={() => {
                setDeleteTarget(row.original);
                setIsDeleteConfirmOpen(true);
              }}
              aria-label="Supprimer"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
          // <ActionButton
          //   row={row}
          //   setConfirmDelete={handleConfirmDelete}
          //   handleEdit={handleEdit}
          // />
        )
      }
    ];
  }, [selectPage]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">CMS</h1>
          <p className="text-sm text-muted-foreground">
            Creez et mettez a jour les pages une par une avec un apercu en temps
            reel.
          </p>
        </div>
        <Button size="sm" onClick={handleCreateNew}>
          Nouvelle page
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
            Fermer
          </button>
        </div>
      ) : null}

      <div className="space-y-4">
        <DataTable
          columns={columns}
          data={pages}
          isLoading={isPending}
          searchPlaceholder="Rechercher une page"
          emptyText={
            isError
              ? (error?.message ?? "Impossible de charger")
              : "Aucune page"
          }
          totalItems={pages.length}
          page={1}
          pageSize={pages.length || 1}
          onPageChange={() => null}
          onPageSizeChange={() => null}
        />
      </div>

      <Dialog open={isEditorOpen} onOpenChange={setIsEditorOpen}>
        <DialogContent className="flex h-[90vh] w-[100vw] max-w-none flex-col overflow-hidden">
          <DialogHeader>
            <DialogTitle>
              {selectedPage ? "Editer la page" : "Nouvelle page CMS"}
            </DialogTitle>
            <DialogDescription>
              Le contenu doit etre un div HTML avec des classes Tailwind pour le
              style.
            </DialogDescription>
          </DialogHeader>

          <div className="grid min-h-0 flex-1 gap-6 lg:grid-cols-2">
            <div className="flex min-h-0 flex-col space-y-4 overflow-hidden">
              <p className="text-sm font-semibold">Editeur HTML</p>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Slug</label>
                  <Input
                    value={formValues.slug}
                    onChange={(event) =>
                      setFormValues((prev) => ({
                        ...prev,
                        slug: event.target.value
                      }))
                    }
                    placeholder="home, platform, services"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Statut</label>
                  <Input
                    value={formValues.status ?? ""}
                    onChange={(event) =>
                      setFormValues((prev) => ({
                        ...prev,
                        status: event.target.value
                      }))
                    }
                    placeholder="published"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Titre</label>
                <Input
                  value={formValues.title ?? ""}
                  onChange={(event) =>
                    setFormValues((prev) => ({
                      ...prev,
                      title: event.target.value
                    }))
                  }
                  placeholder="Titre de la page"
                />
              </div>
              <div className="flex min-h-0 flex-col space-y-2">
                <label className="text-sm font-medium">Brouillon (HTML)</label>
                <div className="relative min-h-[320px] rounded-md border border-input bg-background">
                  <pre
                    ref={highlightRef}
                    className="pointer-events-none absolute inset-0 overflow-auto whitespace-pre-wrap break-words p-3 font-mono text-sm leading-6"
                    dangerouslySetInnerHTML={{ __html: highlightedHtml }}
                  />
                  {formValues.draft_content ? null : (
                    <div className="pointer-events-none absolute left-3 top-2 text-sm text-muted-foreground">
                      &lt;div class='space-y-8'&gt;...&lt;/div&gt;
                    </div>
                  )}
                  <Textarea
                    ref={editorRef}
                    value={formValues.draft_content ?? ""}
                    onChange={(event) =>
                      setFormValues((prev) => ({
                        ...prev,
                        draft_content: event.target.value
                      }))
                    }
                    onKeyDown={(event) => {
                      if (
                        (event.ctrlKey || event.metaKey) &&
                        event.key.toLowerCase() === "f"
                      ) {
                        event.preventDefault();
                      }
                    }}
                    onScroll={handleEditorScroll}
                    aria-label="Editeur HTML"
                    spellCheck={false}
                    className="relative z-10 min-h-[320px] border-0 bg-transparent p-3 font-mono text-sm leading-6 text-transparent caret-foreground selection:bg-primary/30 focus-visible:ring-0 focus-visible:ring-offset-0"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Meta (JSON)</label>
                <Textarea
                  value={formValues.meta_json ?? ""}
                  onChange={(event) =>
                    setFormValues((prev) => ({
                      ...prev,
                      meta_json: event.target.value
                    }))
                  }
                  placeholder='{"description":"..."}'
                  className="min-h-[120px]"
                />
              </div>
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  {selectedPage?.id ? (
                    <Button
                      variant="destructive"
                      onClick={() => {
                        setDeleteTarget(selectedPage);
                        setIsDeleteConfirmOpen(true);
                      }}
                      disabled={deletePage.isPending}
                    >
                      Supprimer
                    </Button>
                  ) : null}
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    onClick={handlePublish}
                    disabled={
                      createPage.isPending ||
                      updatePage.isPending ||
                      !(formValues.draft_content || "").trim()
                    }
                  >
                    Publier
                  </Button>
                  <Button
                    onClick={handleSave}
                    disabled={createPage.isPending || updatePage.isPending}
                  >
                    Enregistrer
                  </Button>
                </div>
              </div>
            </div>

            <div className="flex min-h-0 flex-col rounded-lg border bg-muted/20 p-4">
              <p className="text-sm font-semibold">Apercu</p>
              <div className="mt-4 min-h-0 flex-1 overflow-y-auto rounded-md border bg-background p-4">
                {formValues.draft_content ? (
                  <div
                    className="w-full"
                    dangerouslySetInnerHTML={{
                      __html: formValues.draft_content
                    }}
                  />
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Ajoutez un contenu HTML pour voir l'aperçu.
                  </p>
                )}
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={isDeleteConfirmOpen}
        title="Supprimer cette page ?"
        description="Cette action est irreversible."
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        destructive
        isConfirming={deletePage.isPending}
        onCancel={() => {
          setIsDeleteConfirmOpen(false);
          setDeleteTarget(null);
        }}
        onConfirm={handleDelete}
      />
    </div>
  );
};
