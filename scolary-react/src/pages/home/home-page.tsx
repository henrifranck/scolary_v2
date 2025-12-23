import { useMemo } from "react";

import { PublicHeader } from "@/components/public-header";
import { useCmsPageBySlug, usePublicCmsPages } from "@/services/cms-page-service";

export const HomePage = () => {
  const { data: cmsPage } = useCmsPageBySlug("home");
  const { data: cmsPagesResponse } = usePublicCmsPages();
  const cmsPages = cmsPagesResponse?.data ?? [];
  const headerMeta = useMemo(() => {
    if (!cmsPage?.meta_json) {
      return {};
    }
    try {
      const parsed = JSON.parse(cmsPage.meta_json);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch {
      return {};
    }
  }, [cmsPage?.meta_json]);
  const brandSymbol = (headerMeta.brand_symbol as string) ?? "S";
  const brandName = (headerMeta.brand_name as string) ?? "Scolary";
  const brandTagline =
    (headerMeta.brand_tagline as string) ?? "Scolarite";
  const navPages = [
    { href: "/", label: "Accueil" },
    { href: "/pages/publications", label: "Publications" },
    { href: "/pages/working-time", label: "Horaires" },
    ...cmsPages
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
      <PublicHeader
        brandSymbol={brandSymbol}
        brandName={brandName}
        brandTagline={brandTagline}
        navItems={navPages}
      />

      <main className="mx-auto w-full max-w-6xl px-6">
        {htmlContent ? (
          <div className="py-12" dangerouslySetInnerHTML={{ __html: htmlContent }} />
        ) : null}
      </main>

    </div>
  );
};
