import { useMemo } from "react";

import { PublicHeader } from "@/components/public-header";
import { useCmsPageBySlug, usePublicCmsPages } from "@/services/cms-page-service";

export const PublicationsPage = () => {
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
      href: `/pages/${page.slug}`,
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
  const brandTagline = (headerMeta.brand_tagline as string) ?? "Scolarite";
  const headerLinks = [
    { href: "/", label: "Accueil" },
    { href: "/pages/publications", label: "Publications" },
    { href: "/pages/working-time", label: "Horaires" },
    ...navPages
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
      <div className="mx-auto w-full max-w-6xl px-6 py-12">
        <h1 className="text-2xl font-semibold">Publications</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Cette page affichera bientot les publications.
        </p>
      </div>
    </div>
  );
};
