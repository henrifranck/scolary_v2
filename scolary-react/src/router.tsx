import { Outlet, createRoute, createRouter, redirect } from '@tanstack/react-router';
import { DashboardPage } from './pages/dashboard/dashboard-page';
import { NotesPage } from './pages/user/notes/notes-page';
import { ReinscriptionPage } from './pages/user/reinscription/reinscription-page';
import { ReinscriptionTrashPage } from './pages/user/reinscription/reinscription-trash-page';
import { InscriptionPage } from './pages/user/inscription/inscription-page';
import { DossierSelectionPage } from './pages/user/dossier-selection/dossier-selection-page';
import { ConcoursPage } from './pages/user/concours/concours-page';
import { HomePage } from './pages/home/home-page';
import { CmsPublicPage } from './pages/home/cms-public-page';
import { AcademicYearsPage } from './pages/admin/academic-years-page';
import { WorkingTimePage } from './pages/admin/working-time-page';
import { UsersPage } from './pages/admin/users-page';
import { RolesPage } from './pages/admin/roles/roles-page';
import { SubjectsPage } from './pages/admin/subjects/subjects-page';
import { MentionsPage } from './pages/admin/mentions/mentions-page';
import { JourneysPage } from './pages/admin/journeys/journeys-page';
import { PermissionsPage } from './pages/admin/permissions/permissions-page';
import { UniversityInfoPage } from './pages/admin/university-info-page';
import { TeachingUnitPage } from './pages/admin/teaching-unit-page';
import { ConstituentElementsPage } from './pages/admin/constituent-elements-page';
import { GroupsPage } from './pages/admin/groups-page';
import { AvailableServicesPage } from './pages/admin/available-services/available-services-page';
import { RequiredDocumentsPage } from './pages/admin/required-documents/required-documents-page';
import { AvailableModelsPage } from './pages/admin/available-models/available-models-page';
import { FileManagerPage } from './pages/admin/files/files-page';
import { CmsManagerPage } from './pages/admin/cms/cms-manager-page';
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
  path: '/dashboard',
  component: DashboardPage,
  beforeLoad: ensureAuthenticated
});

const homeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: HomePage
});

const cmsPublicRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'pages/$slug',
  component: CmsPublicPage
});

const reinscriptionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 're-registration',
  component: ReinscriptionPage,
  beforeLoad: ensureAuthenticated
});

const reinscriptionTrashRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 're-registration-trash',
  component: ReinscriptionTrashPage,
  beforeLoad: ensureAuthenticated
});

const inscriptionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'registration',
  component: InscriptionPage,
  beforeLoad: ensureAuthenticated
});

const userNotesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'notes',
  component: NotesPage,
  beforeLoad: ensureAuthenticated
});

const dossierSelectionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'folder-selection',
  component: DossierSelectionPage,
  beforeLoad: ensureAuthenticated
});

const concoursRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'competitions',
  component: ConcoursPage,
  beforeLoad: ensureAuthenticated
});

const adminRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: 'admin',
  component: () => <Outlet />,
  beforeLoad: ensureRole('admin')
});

const adminReinscriptionRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 're-registration',
  component: ReinscriptionPage
});

const adminReinscriptionTrashRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 're-registration-trash',
  component: ReinscriptionTrashPage
});

const adminInscriptionRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'registration',
  component: InscriptionPage
});

const adminNotesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'notes',
  component: NotesPage
});

const adminDossierSelectionRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'folder-selection',
  component: DossierSelectionPage
});

const adminConcoursRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'competitions',
  component: ConcoursPage
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

const universityInfoRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'university-info',
  component: UniversityInfoPage
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

const availableServicesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'available-services',
  component: AvailableServicesPage
});

const requiredDocumentsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'required-documents',
  component: RequiredDocumentsPage
});

const availableModelsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'available-models',
  component: AvailableModelsPage
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

const cmsManagerRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: 'cms',
  component: CmsManagerPage
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
  homeRoute,
  cmsPublicRoute,
  dashboardRoute,
  userNotesRoute,
  reinscriptionRoute,
  reinscriptionTrashRoute,
  inscriptionRoute,
  dossierSelectionRoute,
  concoursRoute,
  adminRoute.addChildren([
    adminNotesRoute,
    adminDossierSelectionRoute,
    adminInscriptionRoute,
    adminReinscriptionRoute,
    adminReinscriptionTrashRoute,
    adminConcoursRoute,
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
    groupsRoute,
    availableServicesRoute,
    requiredDocumentsRoute,
    availableModelsRoute,
    universityInfoRoute,
    cmsManagerRoute
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
