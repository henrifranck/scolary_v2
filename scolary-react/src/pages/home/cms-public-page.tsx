import { Link, useRouterState } from "@tanstack/react-router";
import { Moon, Sun } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { useCmsPageBySlug, usePublicCmsPages } from "@/services/cms-page-service";

const getSlugFromPath = (pathname: string) => {
  const segments = pathname.split("/").filter(Boolean);
  const raw = segments[segments.length - 1] ?? "";
  return decodeURIComponent(raw);
};

export const CmsPublicPage = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const { location } = useRouterState();
  const slug = useMemo(() => getSlugFromPath(location.pathname), [location.pathname]);
  const { data: cmsPage, isPending, isError } = useCmsPageBySlug(slug, Boolean(slug));
  const { data: cmsPagesResponse } = usePublicCmsPages();
  const cmsPages = cmsPagesResponse?.data ?? [];
  const navPages = cmsPages
    .filter((page) => page.slug && page.slug !== "home")
    .map((page) => ({
      slug: page.slug,
      label: page.title?.trim() || page.slug
    }));

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const storedTheme = window.localStorage.getItem("theme");
    const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
    const shouldUseDark = storedTheme ? storedTheme === "dark" : Boolean(prefersDark);
    setIsDarkMode(shouldUseDark);
    document.documentElement.classList.toggle("dark", shouldUseDark);
  }, []);

  const toggleTheme = () => {
    setIsDarkMode((prev) => {
      const next = !prev;
      document.documentElement.classList.toggle("dark", next);
      window.localStorage.setItem("theme", next ? "dark" : "light");
      return next;
    });
  };

  const htmlContent = cmsPage?.content_json?.trim() ?? "";
  const title = cmsPage?.title ?? slug;

  return (
    <div
      className="min-h-screen text-foreground"
      style={{
        backgroundImage:
          "radial-gradient(circle at top, hsl(var(--background)) 0%, hsl(var(--background)) 55%, hsl(var(--muted)) 100%)"
      }}
    >
      <header className="sticky top-0 z-40 w-full border-b bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-foreground text-background">
              S
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">
                Scolarite
              </p>
              <p className="text-base font-semibold">Scolary</p>
            </div>
          </div>

          <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
            <Link to="/" className="hover:text-foreground">
              Accueil
            </Link>
            {navPages.map((page) => (
              <Link
                key={page.slug}
                to={`/pages/${page.slug}`}
                className="hover:text-foreground"
              >
                {page.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
            <Button asChild>
              <Link to="/auth/login">Connexion</Link>
            </Button>
          </div>
        </div>
      </header>

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
