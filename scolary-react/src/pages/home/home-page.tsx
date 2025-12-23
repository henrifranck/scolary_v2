import { useEffect, useState } from "react";
import { Link } from "@tanstack/react-router";
import { ArrowRight, Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useCmsPageBySlug, usePublicCmsPages } from "@/services/cms-page-service";

export const HomePage = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const { data: cmsPage } = useCmsPageBySlug("home");
  const { data: cmsPagesResponse } = usePublicCmsPages();
  const cmsPages = cmsPagesResponse?.data ?? [];
  const navPages = [
    { href: "/", label: "Accueil" },
    ...cmsPages
      .filter((page) => page.slug && page.slug !== "home")
      .map((page) => ({
        href: `/pages/${page.slug}`,
        label: page.title?.trim() || page.slug
      }))
  ];

  type HomeStat = { label: string; value: string };
  type HomeFeature = { title: string; description: string };
  type FooterNav = { label: string; href: string };
  type FooterContent = {
    about: string;
    navigation: FooterNav[];
    contact: string[];
  };

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const storedTheme = window.localStorage.getItem("theme");
    const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)")
      .matches;
    const shouldUseDark = storedTheme
      ? storedTheme === "dark"
      : Boolean(prefersDark);
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

  const defaultContent = {
    hero_badge: "Plateforme academique unifiee",
    title: "Pilotez la scolarite avec une vision claire et partagee",
    subtitle:
      "Scolary centralise les inscriptions, dossiers, paiements et documents pour offrir aux equipes une supervision fluide et securisee.",
    primary_cta_label: "Se connecter",
    secondary_cta_label: "Acceder au tableau de bord",
    stats: [
      { label: "Mentions", value: "20+" },
      { label: "Parcours", value: "80+" },
      { label: "Etudiants", value: "15k" }
    ] as HomeStat[],
    features: [
      {
        title: "Inscriptions simplifiees",
        description:
          "Automatisez les etapes administratives et reduisez les erreurs."
      },
      {
        title: "Gestion documentaire",
        description:
          "Centralisez les pieces et suivez les validations en un clic."
      },
      {
        title: "Pilotage des services",
        description:
          "Reliez les services et ajustez les droits en temps reel."
      }
    ] as HomeFeature[],
    services: [
      "Suivi des dossiers et justificatifs",
      "Calendrier des inscriptions",
      "Controle des paiements",
      "Exports et rapports institutionnels"
    ] as string[],
    contact_title: "Besoin d'informations ?",
    contact_subtitle:
      "Contactez notre equipe pour une presentation de Scolary.",
    footer: {
      about:
        "Outil de gestion academique concu pour les universites et les ecoles, avec une experience claire et moderne.",
      navigation: [
        { label: "Tableau de bord", href: "/dashboard" },
        { label: "Inscription", href: "/registration" },
        { label: "Re-inscription", href: "/re-registration" }
      ],
      contact: ["support@scolary.app", "+261 20 00 000 00"]
    } as FooterContent
  };

  const htmlContent = cmsPage?.content_json?.trim() || "";

  const content = {
    ...defaultContent,
    title: cmsPage?.title ?? defaultContent.title
  };

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
            {navPages.map((page) => (
              <Link key={page.href} to={page.href} className="hover:text-foreground">
                {page.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {isDarkMode ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </Button>
            <Button asChild>
              <Link to="/auth/login">Connexion</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl px-6">
        {htmlContent ? (
          <div className="py-12" dangerouslySetInnerHTML={{ __html: htmlContent }} />
        ) : null}
      </main>

    </div>
  );
};
