import { Link, useRouterState } from "@tanstack/react-router";
import { useMemo } from "react";

import { Button } from "@/components/ui/button";
import { PublicHeader } from "@/components/public-header";
import { useCmsPageBySlug, usePublicCmsPages } from "@/services/cms-page-service";

const getSlugFromPath = (pathname: string) => {
  const segments = pathname.split("/").filter(Boolean);
  const raw = segments[segments.length - 1] ?? "";
  return decodeURIComponent(raw);
};

export const CmsPublicPage = () => {
  const { location } = useRouterState();
  const slug = useMemo(() => getSlugFromPath(location.pathname), [location.pathname]);
  const { data: cmsPage, isPending, isError } = useCmsPageBySlug(slug, Boolean(slug));
  const { data: homePage } = useCmsPageBySlug("home");
  const { data: cmsPagesResponse } = usePublicCmsPages();
  const cmsPages = cmsPagesResponse?.data ?? [];
  const navPages = cmsPages
    .filter(
      (page) =>
        page.slug &&
        page.slug !== "home" &&
        page.slug !== "publications" &&
        page.slug !== "working-time"
    )
    .map((page) => ({
      slug: page.slug,
      label: page.title?.trim() || page.slug
    }));
  const headerMeta = useMemo(() => {
    if (!homePage?.meta_json) {
      return {};
    }
    try {
      const parsed = JSON.parse(homePage.meta_json);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch {
      return {};
    }
  }, [homePage?.meta_json]);
  const brandSymbol = (headerMeta.brand_symbol as string) ?? "S";
  const brandName = (headerMeta.brand_name as string) ?? "Scolary";
  const brandTagline =
    (headerMeta.brand_tagline as string) ?? "Scolarite";

  const htmlContent = cmsPage?.content_json?.trim() ?? "";
  const title = cmsPage?.title ?? slug;
  const headerLinks = [
    { href: "/", label: "Accueil" },
    { href: "/pages/publications", label: "Publications" },
    { href: "/pages/working-time", label: "Horaires" },
    ...navPages.map((page) => ({
      href: `/pages/${page.slug}`,
      label: page.label
    }))
  ];

  return (
    <div
      className="min-h-screen text-foreground"
      style={{
        backgroundImage:
          "radial-gradient(circle at top, hsl(var(--background)) 0%, hsl(var(--background)) 55%, hsl(var(--muted)) 100%)"
      }}
    >
      <PublicHeader
        brandSymbol={brandSymbol}
        brandName={brandName}
        brandTagline={brandTagline}
        navItems={headerLinks}
      />

      <main className="mx-auto w-full max-w-6xl px-6 py-12">
        {isPending ? (
          <p className="text-sm text-muted-foreground">Chargement du contenu...</p>
        ) : null}
        {isError || !cmsPage ? (
          <div className="rounded-xl border bg-background p-8 shadow-sm">
            <h1 className="text-2xl font-semibold">Page introuvable</h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Cette page CMS n'est pas disponible ou n'existe pas.
            </p>
            <Button asChild className="mt-4">
              <Link to="/">Retour a l'accueil</Link>
            </Button>
          </div>
        ) : null}
        {!isPending && cmsPage ? (
          <div className="space-y-4">
            {title ? <h1 className="text-3xl font-semibold">{title}</h1> : null}
            {htmlContent ? (
              <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
            ) : (
              <p className="text-sm text-muted-foreground">
                Aucun contenu HTML pour cette page.
              </p>
            )}
          </div>
        ) : null}
      </main>
    </div>
  );
};
