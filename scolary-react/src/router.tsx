import { Outlet, createRoute, createRouter, redirect } from '@tanstack/react-router';
import { DashboardPage } from './pages/dashboard/dashboard-page';
import { NotesPage } from './pages/user/notes/notes-page';
import { ReinscriptionPage } from './pages/user/reinscription/reinscription-page';
import { ReinscriptionTrashPage } from './pages/user/reinscription/reinscription-trash-page';
import { InscriptionPage } from './pages/user/inscription/inscription-page';
import { DossierSelectionPage } from './pages/user/dossier-selection/dossier-selection-page';
import { ConcoursPage } from './pages/user/concours/concours-page';
import { AcademicYearsPage } from './pages/admin/academic-years-page';
import { WorkingTimePage } from './pages/admin/working-time-page';
import { UsersPage } from './pages/admin/users-page';
import { RolesPage } from './pages/admin/roles/roles-page';
import { SubjectsPage } from './pages/admin/subjects/subjects-page';
import { MentionsPage } from './pages/admin/mentions/mentions-page';
import { JourneysPage } from './pages/admin/journeys/journeys-page';
import { PermissionsPage } from './pages/admin/permissions/permissions-page';
import { TeachingUnitPage } from './pages/admin/teaching-unit-page';
import { ConstituentElementsPage } from './pages/admin/constituent-elements-page';
import { GroupsPage } from './pages/admin/groups-page';
import { FileManagerPage } from './pages/admin/files/files-page';
import { LoginPage } from './pages/auth/login-page';
import type { AuthRole } from './lib/auth-store';
import type { AppRouterContext } from './router-context';
import { Route as rootRoute } from './routes/__root';

const ensureAuthenticated = ({ context }: { context: AppRouterContext }) => {
  const { status } = context.authStore.getState();
  if (status !== 'authenticated') {
    throw redirect({ to: '/auth/login', replace: true });
  }
};

const ensureRole = (role: AuthRole) => ({ context }: { context: AppRouterContext }) => {
  const { status, user } = context.authStore.getState();
  if (status !== 'authenticated' || !user) {
    throw redirect({ to: '/auth/login', replace: true });
  }

  if (user.role !== role) {
    throw redirect({ to: '/' });
  }
};

const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: DashboardPage,
  beforeLoad: ensureAuthenticated
});

const userRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'user',
  component: () => <Outlet />,
  beforeLoad: ensureAuthenticated
});

const reinscriptionRoute = createRoute({
  getParentRoute: () => userRoute,
  path: 're-inscription',
  component: ReinscriptionPage
});

const reinscriptionTrashRoute = createRoute({
  getParentRoute: () => userRoute,
  path: 're-inscription-trash',
  component: ReinscriptionTrashPage
});

const inscriptionRoute = createRoute({
  getParentRoute: () => userRoute,
  path: 'inscription',
  component: InscriptionPage
});

const userNotesRoute = createRoute({
  getParentRoute: () => userRoute,
  path: 'notes',
  component: NotesPage
});

const dossierSelectionRoute = createRoute({
  getParentRoute: () => userRoute,
  path: 'dossier-selection',
  component: DossierSelectionPage
});

const concoursRoute = createRoute({
  getParentRoute: () => userRoute,
  path: 'concours',
  component: ConcoursPage
});

const adminRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'admin',
  component: () => <Outlet />,
  beforeLoad: ensureRole('admin')
});

const academicYearsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'academic-years',
  component: AcademicYearsPage
});

const workingTimeRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'working-time',
  component: WorkingTimePage
});

const permissionsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'permissions',
  component: PermissionsPage
});


const filesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'files',
  component: FileManagerPage
});

const teachingUnitRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'teaching-unit',
  component: TeachingUnitPage
});

const constituentElementsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'constituent-elements',
  component: ConstituentElementsPage
});

const groupsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'groups',
  component: GroupsPage
});

const usersRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'users',
  component: UsersPage
});

const rolesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'roles',
  component: RolesPage
});

const subjectsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'subjects',
  component: SubjectsPage
});

const mentionsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'mentions',
  component: MentionsPage
});

const journeysRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'journeys',
  component: JourneysPage
});

const authRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'auth',
  component: () => <Outlet />
});

const loginRoute = createRoute({
  getParentRoute: () => authRoute,
  path: 'login',
  component: LoginPage,
  beforeLoad: ({ context }) => {
    if (context.authStore.getState().status === 'authenticated') {
      throw redirect({ to: '/' });
    }
  }
});

const routeTree = rootRoute.addChildren([
  dashboardRoute,
  userRoute.addChildren([
    userNotesRoute,
    reinscriptionRoute,
    reinscriptionTrashRoute,
    inscriptionRoute,
    dossierSelectionRoute,
    concoursRoute
  ]),
  adminRoute.addChildren([
    academicYearsRoute,
    workingTimeRoute,
    usersRoute,
    rolesRoute,
    subjectsRoute,
    mentionsRoute,
    journeysRoute,
    filesRoute,
    permissionsRoute,
    teachingUnitRoute,
    constituentElementsRoute,
    groupsRoute
  ]),
  authRoute.addChildren([loginRoute])
]);

export const createAppRouter = (context: AppRouterContext) =>
  createRouter({
    context,
    routeTree
    // defaultPreload: 'intent'
  });

declare module '@tanstack/react-router' {
  interface Register {
    router: ReturnType<typeof createAppRouter>;
  }
}
