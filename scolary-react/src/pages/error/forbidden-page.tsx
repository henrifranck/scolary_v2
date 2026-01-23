import { ShieldOff } from "lucide-react";
import { Link } from "@tanstack/react-router";

import { Button } from "@/components/ui/button";

export const ForbiddenPage = () => {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10 text-destructive">
        <ShieldOff className="h-8 w-8" />
      </div>
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold">Accès refusé</h1>
        <p className="max-w-xl text-sm text-muted-foreground">
          Vous n&apos;avez pas les permissions nécessaires pour consulter cette
          ressource. Si vous pensez qu&apos;il s&apos;agit d&apos;une erreur,
          contactez un administrateur.
        </p>
      </div>
      <div className="flex flex-wrap justify-center gap-3">
        <Button asChild>
          <Link to="/">Retour à l&apos;accueil</Link>
        </Button>
        <Button variant="outline" onClick={() => window.history.back()}>
          Page précédente
        </Button>
      </div>
    </div>
  );
};
