import { Link, useRouter, useRouterState } from '@tanstack/react-router';
import {
  BookOpenCheck,
  Bell,
  CalendarClock,
  ChevronDown,
  ChevronRight,
  FileSignature,
  Building2,
  FolderOpen,
  GraduationCap,
  HardDrive,
  Layers,
  LayoutDashboard,
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
  X
} from 'lucide-react';
import { type ReactNode, useCallback, useEffect, useState } from 'react';

import { ScrollArea } from '../components/ui/scroll-area';
import { Separator } from '../components/ui/separator';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../components/ui/dropdown-menu';
import { cn } from '../lib/utils';
import { useAuth } from '../providers/auth-provider';
import type { AuthRole, AuthUser } from '../lib/auth-store';
import { clearAuthSession } from '../services/auth-service';

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
    title: 'General',
    items: [{ to: '/', label: 'Dashboard', icon: LayoutDashboard }]
  };

  if (user?.role === 'admin') {
    return [
      generalSection,
      {
        title: 'Academic',
        roles: ['admin'],
        items: [{ to: '/admin/academic-years', label: 'Academic years', icon: GraduationCap, roles: ['admin'] }]
      },
      {
        title: 'Student',
        roles: ['admin'],
        items: [
          { to: '/user/dossier-selection', label: 'Nouveau etudians', icon: FolderOpen, roles: ['admin'] },
          { to: '/user/inscription', label: 'Inscription', icon: FileSignature, roles: ['admin'] },
          { to: '/user/re-inscription', label: 'Re-inscription', icon: RefreshCcw, roles: ['admin'] },
          { to: '/user/re-inscription-trash', label: 'Re-inscription Trash', icon: Trash2, roles: ['admin'] }
        ]
      },
      {
        title: 'User',
        roles: ['admin'],
        items: [
          { to: '/admin/users', label: 'Users', icon: Users, roles: ['admin'] },
          { to: '/admin/roles', label: 'Roles', icon: ShieldCheck, roles: ['admin'] },
          { to: '/admin/permissions', label: 'Permissions', icon: Settings, roles: ['admin'] }
        ]
      },
      {
        title: 'Service',
        roles: ['admin'],
        items: [
          { to: '/admin/mentions', label: 'Mentions', icon: Waypoints, roles: ['admin'] },
          { to: '/admin/journeys', label: 'Journeys', icon: Route, roles: ['admin'] },
          { to: '/admin/university-info', label: 'University info', icon: Building2, roles: ['admin'] },
          { to: '/admin/files', label: 'File manager', icon: HardDrive, roles: ['admin'] }
        ]
      },
      {
        title: 'Enseignant',
        roles: ['admin'],
        items: [
          { to: '/admin/teaching-unit', label: 'Teaching unit', icon: BookOpenCheck, roles: ['admin'] },
          { to: '/admin/constituent-elements', label: 'Constituent element', icon: Layers, roles: ['admin'] },
          { to: '/admin/working-time', label: 'Working time', icon: CalendarClock, roles: ['admin'] },
          { to: '/admin/groups', label: 'Group', icon: Users, roles: ['admin'] }
        ]
      }
    ];
  }

  return [
    generalSection,
    {
      title: 'Student',
      roles: ['student'],
      items: [
        { to: '/user/notes', label: 'Notes', icon: NotepadText, roles: ['student'] },
        { to: '/user/dossier-selection', label: 'Nouveau etudians', icon: FolderOpen, roles: ['student'] },
        { to: '/user/inscription', label: 'Inscription', icon: FileSignature, roles: ['student'] },
        { to: '/user/re-inscription', label: 'Re-inscription', icon: RefreshCcw, roles: ['student'] },
        { to: '/user/re-inscription-trash', label: 'Re-inscription Trash', icon: Trash2, roles: ['admin'] },
        { to: '/user/concours', label: 'Concours', icon: Trophy, roles: ['student'], badge: 'New' }
      ]
    }
  ];
};

const academicYears = [
  { value: '2024-2025', label: '2024 / 2025' },
  { value: '2023-2024', label: '2023 / 2024' },
  { value: '2022-2023', label: '2022 / 2023' }
];

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
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const isReinscriptionPage = location.pathname.startsWith('/user/re-inscription');
  const [selectedYear, setSelectedYear] = useState('2024-2025');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [collapsedSections, setCollapsedSections] = useState<Record<string, boolean>>({});
  const navSections = getNavSections(user);

  const filteredNavSections = navSections.filter((section) => {
    if (!section.roles) {
      return true;
    }
    return user ? section.roles.includes(user.role) : false;
  });

  const handleLogout = () => {
    clearAuthSession();
    store.logout();
    router.navigate({ to: '/auth/login' });
  };

  useEffect(() => {
    if (!isReinscriptionPage || typeof window === 'undefined') {
      return;
    }
    const trimmed = searchQuery.trim();
    if (!trimmed) {
      return;
    }
    const timeout = window.setTimeout(() => {
      window.dispatchEvent(
        new CustomEvent('app-search', {
          detail: { scope: 'student', query: trimmed }
        })
      );
    }, 3000);
    return () => window.clearTimeout(timeout);
  }, [searchQuery, isReinscriptionPage]);

  const getRoleBadgeVariant = (role: AuthRole) => {
    return role === 'admin' ? 'default' : 'secondary';
  };

  const toggleSection = (sectionTitle: string) => {
    setCollapsedSections(prev => ({
      ...prev,
      [sectionTitle]: !prev[sectionTitle]
    }));
  };

  const getBreadcrumbs = () => {
    const pathSegments = location.pathname.split('/').filter(Boolean);
    const breadcrumbs = [{ label: 'Home', href: '/' }];

    let currentPath = '';
    pathSegments.forEach((segment, index) => {
      currentPath += `/${segment}`;
      const isLast = index === pathSegments.length - 1;

      // Find the corresponding nav item
      const navItem = navSections
        .flatMap(section => section.items)
        .find(item => item.to === currentPath);

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
    if (typeof window === 'undefined') {
      return;
    }

    const storedTheme = window.localStorage.getItem('theme');
    const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches;
    const shouldUseDark = storedTheme ? storedTheme === 'dark' : Boolean(prefersDark);

    setIsDarkMode(shouldUseDark);
    document.documentElement.classList.toggle('dark', shouldUseDark);
  }, []);

  const toggleTheme = useCallback(() => {
    setIsDarkMode((prev) => {
      const next = !prev;
      document.documentElement.classList.toggle('dark', next);
      window.localStorage.setItem('theme', next ? 'dark' : 'light');
      return next;
    });
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-muted/20 text-foreground">
      {/* Mobile menu overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 md:hidden" onClick={() => setIsMobileMenuOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={cn(
        "fixed left-0 top-0 z-50 flex h-screen w-64 flex-col border-r bg-background transition-all duration-200 md:relative",
        isMobileMenuOpen ? "translate-x-0" : "-translate-x-full",
        isSidebarOpen ? "md:w-64 md:translate-x-0" : "md:w-0 md:-translate-x-full md:border-r-0"
      )}>
        <div className="flex h-16 items-center justify-between px-4">
          <div className={cn("flex items-center gap-2 text-xl font-semibold", !isSidebarOpen && "md:hidden")}>
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
        <ScrollArea className={cn("flex-1 px-3 py-4", !isSidebarOpen && "md:hidden")}>
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
              const hasActiveItem = visibleItems.some(item =>
                location.pathname === item.to || location.pathname.startsWith(`${item.to}/`)
              );

              return (
                <div key={section.title} className="space-y-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-between px-2 py-1.5 h-auto font-medium text-muted-foreground hover:text-foreground"
                    onClick={() => toggleSection(section.title)}
                  >
                    <span className="text-xs uppercase tracking-wider">{section.title}</span>
                    <ChevronRight className={cn(
                      "h-3 w-3 transition-transform",
                      isCollapsed ? "rotate-0" : "rotate-90"
                    )} />
                  </Button>

                  {!isCollapsed && (
                    <div className="ml-2 space-y-1">
                      {visibleItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = location.pathname === item.to || location.pathname.startsWith(`${item.to}/`);

                        return (
                          <Link
                            key={item.to}
                            to={item.to}
                            className={cn(
                              'group flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors relative',
                              isActive ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'
                            )}
                            onClick={() => setIsMobileMenuOpen(false)}
                          >
                            <Icon className="h-4 w-4" />
                            <span className="flex-1">{item.label}</span>
                            {item.badge && (
                              <Badge variant="secondary" className="text-xs px-1.5 py-0.5">
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
              {isSidebarOpen ? <Menu className="h-5 w-5" /> : <ChevronRight className="h-5 w-5" />}
            </Button>

            {/* Breadcrumbs */}
            <nav className="hidden md:flex items-center space-x-1 text-sm">
              {getBreadcrumbs().map((breadcrumb, index) => (
                <div key={breadcrumb.href} className="flex items-center">
                  {index > 0 && <ChevronRight className="h-3 w-3 text-muted-foreground mx-1" />}
                  <Link
                    to={breadcrumb.href}
                    className={cn(
                      "text-muted-foreground hover:text-foreground transition-colors",
                      index === getBreadcrumbs().length - 1 && "text-foreground font-medium"
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
            <span className="text-sm font-medium text-muted-foreground hidden sm:inline">Academic Year</span>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button size="sm" variant="outline" className="gap-1">
                  {academicYears.find(year => year.value === selectedYear)?.label || '2024 / 2025'}
                  <ChevronDown className="h-3 w-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuLabel>Select Academic Year</DropdownMenuLabel>
                <DropdownMenuSeparator />
                {academicYears.map((year) => (
                  <DropdownMenuItem
                    key={year.value}
                    onClick={() => setSelectedYear(year.value)}
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
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
            >
              {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>

            {/* User menu */}
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="flex items-center gap-2 px-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                      <User className="h-4 w-4 text-primary" />
                    </div>
                    <div className="hidden sm:block text-left">
                      <div className="text-sm font-medium">{user.name}</div>
                      <div className="text-xs text-muted-foreground">{user.role}</div>
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
                  <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : null}
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto bg-muted/30 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
};
