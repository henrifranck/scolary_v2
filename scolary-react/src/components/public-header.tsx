import { Link } from "@tanstack/react-router";
import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";

import { Button } from "./ui/button";

type NavItem = { href: string; label: string };

type PublicHeaderProps = {
  brandSymbol: string;
  brandName: string;
  brandTagline: string;
  navItems: NavItem[];
};

export const PublicHeader = ({
  brandSymbol,
  brandName,
  brandTagline,
  navItems
}: PublicHeaderProps) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

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

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-foreground text-background">
            {brandSymbol}
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">
              {brandTagline}
            </p>
            <p className="text-base font-semibold">{brandName}</p>
          </div>
        </div>

        <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
          {navItems.map((item) => (
            <Link key={item.href} to={item.href} className="hover:text-foreground">
              {item.label}
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
  );
};
