import { Link, useRouter, useRouterState } from "@tanstack/react-router";
import {
  BookOpenCheck,
  Bell,
  CalendarClock,
  ChevronDown,
  ChevronRight,
  FileSignature,
  FileText,
  Building2,
  FolderOpen,
  GraduationCap,
  HardDrive,
  Layers,
  LayoutDashboard,
  ListChecks,
  Banknote,
  LogOut,
  Menu,
  Moon,
  NotepadText,
  RefreshCcw,
  Route,
  Search,
  Settings,
  ShieldCheck,
  Sun,
  Trash2,
  Trophy,
  User,
  Users,
  Waypoints,
  X,
  HopOff,
  Flag,
  Home
} from "lucide-react";
import {
  type ReactNode,
  useCallback,
  useEffect,
  useMemo,
  useState
} from "react";

import { ScrollArea } from "../components/ui/scroll-area";
import { Separator } from "../components/ui/separator";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Input } from "../components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from "../components/ui/dropdown-menu";
import { cn } from "../lib/utils";
import { useAuth } from "../providers/auth-provider";
import type { AuthRole, AuthUser } from "../lib/auth-store";
import { useAvailableModels } from "../services/available-model-service";
import { clearAuthSession } from "../services/auth-service";
import { useCurrentUser } from "../services/user-service";
import { useAcademicYears } from "../services/academic-year-service";

interface NavItem {
  to: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  roles?: AuthRole[];
  badge?: string;
}

interface NavSection {
  title: string;
  items: NavItem[];
  roles?: AuthRole[];
}

const getNavSections = (user?: AuthUser | null): NavSection[] => {
  const generalSection: NavSection = {
    title: "General",
    items: [
      { to: "/", label: "Accueil", icon: LayoutDashboard },
      { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard }
    ]
  };

  if (user?.role === "admin") {
    return [
      generalSection,
      {
        title: "Academique",
        roles: ["admin"],
        items: [
          {
            to: "/admin/academic-years",
            label: "Academic years",
            icon: GraduationCap,
            roles: ["admin"]
          }
        ]
      },
      {
        title: "Etudiant",
        roles: ["admin"],
        items: [
          {
            to: "/admin/folder-selection",
            label: "Nouveau etudians",
            icon: FolderOpen,
            roles: ["admin"]
          },
          {
            to: "/admin/registration",
            label: "Inscription",
            icon: FileSignature,
            roles: ["admin"]
          },
          {
            to: "/admin/re-registration",
            label: "Re-inscription",
            icon: RefreshCcw,
            roles: ["admin"]
          },
          {
            to: "/admin/trash",
            label: "Trash",
            icon: Trash2,
            roles: ["admin"]
          }
        ]
      },
      {
        title: "Utilisateur",
        roles: ["admin"],
        items: [
          { to: "/admin/users", label: "Users", icon: Users, roles: ["admin"] },
          {
            to: "/admin/roles",
            label: "Roles",
            icon: ShieldCheck,
            roles: ["admin"]
          },
          {
            to: "/admin/permissions",
            label: "Permissions",
            icon: Settings,
            roles: ["admin"]
          },
          {
            to: "/admin/available-models",
            label: "Available models",
            icon: Layers,
            roles: ["admin"]
          }
        ]
      },
      {
        title: "Service",
        roles: ["admin"],
        items: [
          {
            to: "/admin/mentions",
            label: "Mentions",
            icon: Waypoints,
            roles: ["admin"]
          },
          {
            to: "/admin/journeys",
            label: "Parcours",
            icon: Route,
            roles: ["admin"]
          },
          {
            to: "/admin/available-services",
            label: "Available services",
            icon: ListChecks,
            roles: ["admin"]
          },
          {
            to: "/admin/required-documents",
            label: "Required documents",
            icon: FileText,
            roles: ["admin"]
          },
          {
            to: "/admin/enrollment-fees",
            label: "Enrollment fees",
            icon: Banknote,
            roles: ["admin"]
          },
          {
            to: "/admin/university-info",
            label: "University info",
            icon: Building2,
            roles: ["admin"]
          },
          {
            to: "/admin/files",
            label: "File manager",
            icon: HardDrive,
            roles: ["admin"]
          },

          {
            to: "/admin/baccalaureate-serie",
            label: "Serie du Baccalaureat",
            icon: HopOff,
            roles: ["admin"]
          },

          {
            to: "/admin/nationality",
            label: "Nationalité",
            icon: Flag,
            roles: ["admin"]
          },
          {
            to: "/classroom",
            label: "Salle de classe",
            icon: Home,
            roles: ["admin"]
          }
        ]
      },
      {
        title: "Contenu",
        roles: ["admin"],
        items: [
          {
            to: "/admin/cms",
            label: "Pages CMS",
            icon: FileText,
            roles: ["admin"]
          }
        ]
      },
      {
        title: "Enseignant",
        roles: ["admin"],
        items: [
          {
            to: "/admin/teaching-unit",
            label: "Teaching unit",
            icon: BookOpenCheck,
            roles: ["admin"]
          },
          {
            to: "/admin/constituent-elements",
            label: "Constituent element",
            icon: Layers,
            roles: ["admin"]
          },
          {
            to: "/admin/working-time",
            label: "Working time",
            icon: CalendarClock,
            roles: ["admin"]
          },
          { to: "/admin/groups", label: "Group", icon: Users, roles: ["admin"] }
        ]
      }
    ];
  }

  return [
    generalSection,
    {
      title: "Etudiant",
      roles: ["user"],
      items: [
        { to: "/notes", label: "Notes", icon: NotepadText, roles: ["user"] },
        {
          to: "/folder-selection",
          label: "Nouveau etudians",
          icon: FolderOpen,
          roles: ["user"]
        },
        {
          to: "/registration",
          label: "Inscription",
          icon: FileSignature,
          roles: ["user"]
        },
        {
          to: "/re-registration",
          label: "Re-inscription",
          icon: RefreshCcw,
          roles: ["user"]
        },
        {
          to: "/trash",
          label: "Trash",
          icon: Trash2,
          roles: ["admin"]
        },
        {
          to: "/competitions",
          label: "Concours",
          icon: Trophy,
          roles: ["user"],
          badge: "New"
        }
      ]
    },
    {
      title: "Service",
      roles: ["user"],
      items: [
        {
          to: "/mentions",
          label: "Mentions",
          icon: Waypoints,
          roles: ["user"]
        },
        { to: "/journeys", label: "Parcours", icon: Route, roles: ["user"] },
        {
          to: "/available-services",
          label: "Available services",
          icon: ListChecks,
          roles: ["user"]
        },
        {
          to: "/required-documents",
          label: "Required documents",
          icon: FileText,
          roles: ["user"]
        },
        {
          to: "/university-info",
          label: "University info",
          icon: Building2,
          roles: ["user"]
        },
        {
          to: "/files",
          label: "File manager",
          icon: HardDrive,
          roles: ["user"]
        },
        {
          to: "/baccalaureate-serie",
          label: "Serie du Baccalaureat",
          icon: HopOff,
          roles: ["user"]
        },
        {
          to: "/nationality",
          label: "Nationalité",
          icon: Flag,
          roles: ["user"]
        },
        {
          to: "/classroom",
          label: "Salle de classe",
          icon: Home,
          roles: ["user"]
        }
      ]
    },
    {
      title: "Academique",
      roles: ["user"],
      items: [
        {
          to: "/academic-years",
          label: "Academic years",
          icon: GraduationCap,
          roles: ["user"]
        }
      ]
    },
    {
      title: "Enseignant",
      roles: ["user"],
      items: [
        {
          to: "/teaching-unit",
          label: "Teaching unit",
          icon: BookOpenCheck,
          roles: ["user"]
        },
        {
          to: "/constituent-elements",
          label: "Constituent element",
          icon: Layers,
          roles: ["user"]
        },
        {
          to: "/working-time",
          label: "Working time",
          icon: CalendarClock,
          roles: ["user"]
        },
        { to: "/groups", label: "Group", icon: Users, roles: ["user"] }
      ]
    },
    {
      title: "Utilisateur",
      roles: ["user"],
      items: [
        { to: "/users", label: "Users", icon: Users, roles: ["user"] },
        { to: "/roles", label: "Roles", icon: ShieldCheck, roles: ["user"] },
        {
          to: "/permissions",
          label: "Permissions",
          icon: Settings,
          roles: ["user"]
        },
        {
          to: "/available-models",
          label: "Available models",
          icon: Layers,
          roles: ["user"]
        }
      ]
    },
    {
      title: "Contenu",
      roles: ["user"],
      items: [
        { to: "/cms", label: "Pages CMS", icon: FileText, roles: ["user"] }
      ]
    }
  ];
};

const normalizeRouteKey = (value: string) =>
  value.trim().toLowerCase().replace(/^\/+/, "");

const getPermissionEntry = (
  permissionMap: Record<string, { get?: boolean }>,
  key: string
) => {
  if (!permissionMap) {
    return null;
  }
  const normalized = normalizeRouteKey(key);
  return (
    permissionMap[normalized] ||
    permissionMap[`/${normalized}`] ||
    permissionMap[key]
  );
};

const resolvePermissionKey = (
  path: string,
  availableModels: { route_ui: string; route_api: string; name: string }[]
) => {
  const match = availableModels.find((model) => {
    const routeUi = model.route_ui?.trim();
    if (!routeUi) {
      return false;
    }
    const candidates = routeUi.startsWith("/admin/")
      ? [routeUi, routeUi.replace(/^\/admin/, "")]
      : [routeUi, `/admin${routeUi}`];
    return candidates.some(
      (candidate) => path === candidate || path.startsWith(`${candidate}/`)
    );
  });
  if (match) {
    return normalizeRouteKey(match.route_api || "");
  }
  const parts = path.split("/").filter(Boolean);
  if (!parts.length) {
    return null;
  }
  const scopeIndex = parts[0] === "admin" ? 1 : 0;
  const candidate = parts[scopeIndex] ?? "";
  return normalizeRouteKey(candidate.replace(/-/g, "_"));
};

const hasRouteUiMatch = (
  path: string,
  availableModels: { route_ui: string }[]
) => {
  if (!path || path === "/") {
    return true;
  }
  return availableModels.some((model) => {
    const routeUi = model.route_ui?.trim();
    if (!routeUi) {
      return false;
    }
    const candidates = routeUi.startsWith("/admin/")
      ? [routeUi, routeUi.replace(/^\/admin/, "")]
      : [routeUi, `/admin${routeUi}`];
    return candidates.some(
      (candidate) => path === candidate || path.startsWith(`${candidate}/`)
    );
  });
};

interface AppLayoutProps {
  children: ReactNode;
}

export const AppLayout = ({ children }: AppLayoutProps) => {
  const { location } = useRouterState();
  const {
    state: { user },
    store
  } = useAuth();
  const router = useRouter();
  const { data: currentUser } = useCurrentUser(Boolean(user));
  const { data: availableModelsResponse, isPending: areModelsLoading } =
    useAvailableModels({ limit: 1000 });
  const availableModels = availableModelsResponse?.data ?? [];
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const isReinscriptionPage =
    location.pathname.startsWith("/re-registration") ||
    location.pathname.startsWith("/admin/re-registration");
  location.pathname.startsWith("/registration") ||
    location.pathname.startsWith("/admin/registration");
  location.pathname.startsWith("/selection") ||
    location.pathname.startsWith("/admin/selection");
  const { data: academicYearsData } = useAcademicYears();
  const [selectedYear, setSelectedYear] = useState<string | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [collapsedSections, setCollapsedSections] = useState<
    Record<string, boolean>
  >({});
  const isSuperuser = Boolean(user?.is_superuser);
  const permissionMap = currentUser?.permissions ?? user?.permissions ?? null;
  const shouldEnforcePermissions = Boolean(user) && !isSuperuser;
  const navSections = getNavSections(user);

  const academicYearOptions = useMemo(
    () =>
      academicYearsData?.data?.map((year) => ({
        value: String(year.id),
        label: year.name ?? `Année ${year.id}`
      })) ?? [],
    [academicYearsData]
  );

  useEffect(() => {
    const stored =
      typeof window !== "undefined"
        ? window.localStorage.getItem("selected_academic_year")
        : null;
    if (stored) {
      setSelectedYear(stored);
    }
  }, []);

  useEffect(() => {
    if (!selectedYear) {
      setSelectedYear("all");
    }
  }, [selectedYear]);

  const handleSelectYear = (value: string) => {
    setSelectedYear(value);
    if (typeof window !== "undefined") {
      window.localStorage.setItem("selected_academic_year", value);
      window.dispatchEvent(
        new CustomEvent("academicYearChanged", { detail: value })
      );
    }
  };

  const filteredNavSections = navSections
    .filter((section) => {
      if (!section.roles) {
        return true;
      }
      return user ? section.roles.includes(user.role) : false;
    })
    .map((section) => {
      const items = section.items.filter((item) => {
        if (!isSuperuser && !hasRouteUiMatch(item.to, availableModels)) {
          return false;
        }
        if (!shouldEnforcePermissions) {
          return true;
        }
        if (!permissionMap) {
          return false;
        }
        if (item.to === "/") {
          return true;
        }
        const permissionKey = resolvePermissionKey(item.to, availableModels);
        if (!permissionKey) {
          return false;
        }
        return Boolean(getPermissionEntry(permissionMap, permissionKey)?.get);
      });
      return { ...section, items };
    })
    .filter((section) => section.items.length > 0);

  const handleLogout = () => {
    clearAuthSession();
    store.logout();
    router.navigate({ to: "/auth/login" });
  };

  useEffect(() => {
    if (!currentUser || !user) {
      return;
    }
    const isSuperuser = currentUser.is_superuser ?? user.is_superuser;
    const role: AuthRole = isSuperuser ? "admin" : "user";
    const nextPermissions = currentUser.permissions ?? user.permissions ?? null;
    const samePermissions =
      JSON.stringify(user.permissions ?? null) ===
      JSON.stringify(nextPermissions);
    if (
      user.id === String(currentUser.id ?? user.id) &&
      user.is_superuser === isSuperuser &&
      samePermissions
    ) {
      return;
    }
    const nextUser: AuthUser = {
      ...user,
      id: currentUser.id ? String(currentUser.id) : user.id,
      role,
      is_superuser: isSuperuser,
      permissions: nextPermissions
    };
    store.login(nextUser);
  }, [currentUser, store, user]);

  useEffect(() => {
    if (!isReinscriptionPage || typeof window === "undefined") {
      return;
    }
    const trimmed = searchQuery.trim();
    if (!trimmed) {
      return;
    }
    const timeout = window.setTimeout(() => {
      window.dispatchEvent(
        new CustomEvent("app-search", {
          detail: { scope: "student", query: trimmed }
        })
      );
    }, 3000);
    return () => window.clearTimeout(timeout);
  }, [searchQuery, isReinscriptionPage]);

  const getRoleBadgeVariant = (role: AuthRole) => {
    return role === "admin" ? "default" : "secondary";
  };

  const toggleSection = (sectionTitle: string) => {
    setCollapsedSections((prev) => ({
      ...prev,
      [sectionTitle]: !prev[sectionTitle]
    }));
  };

  const getBreadcrumbs = () => {
    const pathSegments = location.pathname.split("/").filter(Boolean);
    const breadcrumbs = [{ label: "Home", href: "/" }];

    let currentPath = "";
    pathSegments.forEach((segment, index) => {
      currentPath += `/${segment}`;
      const isLast = index === pathSegments.length - 1;

      // Find the corresponding nav item
      const navItem = navSections
        .flatMap((section) => section.items)
        .find((item) => item.to === currentPath);

      if (navItem) {
        breadcrumbs.push({
          label: navItem.label,
          href: currentPath
        });
      }
    });

    return breadcrumbs;
  };

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    if (!user || !shouldEnforcePermissions) {
      return;
    }
    if (!permissionMap) {
      router.navigate({ to: "/" });
      return;
    }
    if (location.pathname.startsWith("/auth") || location.pathname === "/") {
      return;
    }
    const permissionKey = resolvePermissionKey(
      location.pathname,
      availableModels
    );
    if (
      !permissionKey ||
      !getPermissionEntry(permissionMap, permissionKey)?.get
    ) {
      router.navigate({ to: "/" });
    }
  }, [
    availableModels,
    location.pathname,
    permissionMap,
    router,
    shouldEnforcePermissions,
    user
  ]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    if (!user || !user.is_superuser) {
      return;
    }
    if (location.pathname.startsWith("/auth") || location.pathname === "/") {
      return;
    }
    if (location.pathname.startsWith("/admin")) {
      return;
    }
    const isKnownRoute = availableModels.some((model) => {
      const routeUi = model.route_ui?.trim();
      if (!routeUi) {
        return false;
      }
      const candidates = routeUi.startsWith("/admin/")
        ? [routeUi.replace(/^\/admin/, ""), routeUi]
        : [routeUi, `/admin${routeUi}`];
      return candidates.some(
        (candidate) =>
          location.pathname === candidate ||
          location.pathname.startsWith(`${candidate}/`)
      );
    });
    if (isKnownRoute) {
      router.navigate({ to: `/admin${location.pathname}` });
    }
  }, [availableModels, location.pathname, router, user]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    const storedTheme = window.localStorage.getItem("theme");
    const prefersDark = window.matchMedia?.(
      "(prefers-color-scheme: dark)"
    ).matches;
    const shouldUseDark = storedTheme
      ? storedTheme === "dark"
      : Boolean(prefersDark);

    setIsDarkMode(shouldUseDark);
    document.documentElement.classList.toggle("dark", shouldUseDark);
  }, []);

  const toggleTheme = useCallback(() => {
    setIsDarkMode((prev) => {
      const next = !prev;
      document.documentElement.classList.toggle("dark", next);
      window.localStorage.setItem("theme", next ? "dark" : "light");
      return next;
    });
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-muted/20 text-foreground">
      {/* Mobile menu overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/50 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 z-50 flex h-screen w-64 flex-col border-r bg-background transition-all duration-200 md:relative",
          isMobileMenuOpen ? "translate-x-0" : "-translate-x-full",
          isSidebarOpen
            ? "md:w-64 md:translate-x-0"
            : "md:w-0 md:-translate-x-full md:border-r-0"
        )}
      >
        <div className="flex h-16 items-center justify-between px-4">
          <div
            className={cn(
              "flex items-center gap-2 text-xl font-semibold",
              !isSidebarOpen && "md:hidden"
            )}
          >
            <GraduationCap className="h-6 w-6 text-primary" />
            Scolary
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="md:hidden"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        <Separator />
        <ScrollArea
          className={cn("flex-1 px-3 py-4", !isSidebarOpen && "md:hidden")}
        >
          <nav className="space-y-2">
            {filteredNavSections.map((section) => {
              const visibleItems = section.items.filter((item) => {
                if (!item.roles) {
                  return true;
                }
                return user ? item.roles.includes(user.role) : false;
              });

              if (visibleItems.length === 0) {
                return null;
              }

              const isCollapsed = collapsedSections[section.title];
              const hasActiveItem = visibleItems.some(
                (item) =>
                  location.pathname === item.to ||
                  location.pathname.startsWith(`${item.to}/`)
              );

              return (
                <div key={section.title} className="space-y-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-between px-2 py-1.5 h-auto font-medium text-muted-foreground hover:text-foreground"
                    onClick={() => toggleSection(section.title)}
                  >
                    <span className="text-xs uppercase tracking-wider">
                      {section.title}
                    </span>
                    <ChevronRight
                      className={cn(
                        "h-3 w-3 transition-transform",
                        isCollapsed ? "rotate-0" : "rotate-90"
                      )}
                    />
                  </Button>

                  {!isCollapsed && (
                    <div className="ml-2 space-y-1">
                      {visibleItems.map((item) => {
                        const Icon = item.icon;
                        const isActive =
                          location.pathname === item.to ||
                          location.pathname.startsWith(`${item.to}/`);

                        return (
                          <Link
                            key={item.to}
                            to={item.to}
                            className={cn(
                              "group flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors relative",
                              isActive
                                ? "bg-primary text-primary-foreground"
                                : "hover:bg-muted"
                            )}
                            onClick={() => setIsMobileMenuOpen(false)}
                          >
                            <Icon className="h-4 w-4" />
                            <span className="flex-1">{item.label}</span>
                            {item.badge && (
                              <Badge
                                variant="secondary"
                                className="text-xs px-1.5 py-0.5"
                              >
                                {item.badge}
                              </Badge>
                            )}
                            {isActive && (
                              <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-primary-foreground rounded-r-full" />
                            )}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </nav>
        </ScrollArea>
      </aside>

      {/* Main content */}
      <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="sticky top-0 z-40 flex h-16 items-center justify-between gap-4 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-4 shadow-sm">
          {/* Left section - Mobile menu button, breadcrumbs, and search */}
          <div className="flex items-center gap-3 flex-1">
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={() => setIsMobileMenuOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="hidden md:inline-flex"
              onClick={() => setIsSidebarOpen((prev) => !prev)}
              aria-label={isSidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
            >
              {isSidebarOpen ? (
                <Menu className="h-5 w-5" />
              ) : (
                <ChevronRight className="h-5 w-5" />
              )}
            </Button>

            {/* Breadcrumbs */}
            <nav className="hidden md:flex items-center space-x-1 text-sm">
              {getBreadcrumbs().map((breadcrumb, index) => (
                <div key={breadcrumb.href} className="flex items-center">
                  {index > 0 && (
                    <ChevronRight className="h-3 w-3 text-muted-foreground mx-1" />
                  )}
                  <Link
                    to={breadcrumb.href}
                    className={cn(
                      "text-muted-foreground hover:text-foreground transition-colors",
                      index === getBreadcrumbs().length - 1 &&
                        "text-foreground font-medium"
                    )}
                  >
                    {breadcrumb.label}
                  </Link>
                </div>
              ))}
            </nav>

            <div className="relative hidden sm:block">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-64 pl-9"
              />
            </div>
          </div>

          {/* Center section - Academic year dropdown */}
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-muted-foreground hidden sm:inline">
              Academic Year
            </span>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button size="sm" variant="outline" className="gap-1">
                  {selectedYear === "all"
                    ? "Toutes"
                    : academicYearOptions.find(
                        (year) => year.value === selectedYear
                      )?.label || "Sélectionner"}
                  <ChevronDown className="h-3 w-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuLabel>Select Academic Year</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  key="all"
                  onClick={() => handleSelectYear("all")}
                  className={cn(
                    "cursor-pointer",
                    selectedYear === "all" && "bg-accent"
                  )}
                >
                  Toutes
                </DropdownMenuItem>
                {academicYearOptions.map((year) => (
                  <DropdownMenuItem
                    key={year.value}
                    onClick={() => handleSelectYear(year.value)}
                    className={cn(
                      "cursor-pointer",
                      selectedYear === year.value && "bg-accent"
                    )}
                  >
                    {year.label}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Right section - Notifications, theme toggle, and user menu */}
          <div className="flex items-center gap-2">
            {/* Notifications */}
            <Button variant="ghost" size="sm" className="relative">
              <Bell className="h-4 w-4" />
              <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
                3
              </span>
            </Button>

            {/* Theme toggle */}
            <Button variant="ghost" size="sm" onClick={toggleTheme}>
              {isDarkMode ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </Button>

            {/* User menu */}
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    className="flex items-center gap-2 px-2"
                  >
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                      <User className="h-4 w-4 text-primary" />
                    </div>
                    <div className="hidden sm:block text-left">
                      <div className="text-sm font-medium">{user.name}</div>
                      <div className="text-xs text-muted-foreground">
                        {user.role}
                      </div>
                    </div>
                    <ChevronDown className="h-3 w-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>My Account</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <User className="mr-2 h-4 w-4" />
                    <span>Profile</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Settings className="mr-2 h-4 w-4" />
                    <span>Settings</span>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={handleLogout}
                    className="text-red-600"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : null}
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto bg-muted/30 p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
