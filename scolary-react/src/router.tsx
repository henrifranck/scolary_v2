import {
  Outlet,
  createRoute,
  createRouter,
  redirect
} from "@tanstack/react-router";
import { DashboardPage } from "./pages/dashboard/dashboard-page";
import { NotesPage } from "./pages/user/notes/notes-page";
import { ReinscriptionPage } from "./pages/user/re-registration/re-registration-page";
import { ReinscriptionTrashPage } from "./pages/user/trash/trash-page";
import { InscriptionPage } from "./pages/user/inscription/inscription-page";
import { DossierSelectionPage } from "./pages/user/selection/selection-page";
import { ConcoursPage } from "./pages/user/concours/concours-page";
import { HomePage } from "./pages/home/home-page";
import { CmsPublicPage } from "./pages/home/cms-public-page";
import { PublicationsPage } from "./pages/home/publications-page";
import { WorkingTimePublicPage } from "./pages/home/working-time-public-page";
import { AcademicYearsPage } from "./pages/admin/academic-years/academic-years-page";
import { WorkingTimePage } from "./pages/admin/working-time/working-time-page";
import { UsersPage } from "./pages/admin/user/users-page";
import { RolesPage } from "./pages/admin/roles/roles-page";
import { SubjectsPage } from "./pages/admin/subjects/subjects-page";
import { MentionsPage } from "./pages/admin/mentions/mentions-page";
import { JourneysPage } from "./pages/admin/journeys/journeys-page";
import { PermissionsPage } from "./pages/admin/permissions/permissions-page";
import { UniversityInfoPage } from "./pages/admin/university-info/university-info-page";
import { TeachingUnitPage } from "./pages/admin/teaching-unit/teaching-unit-page";
import { ConstituentElementPage } from "./pages/admin/constituent-elements/constituent-elements-page";
import { GroupsPage } from "./pages/admin/groupe/groups-page";
import { OfferingsPage } from "./pages/admin/offering/offerings-page";
import { AvailableServicesPage } from "./pages/admin/available-services/available-services-page";
import { RequiredDocumentsPage } from "./pages/admin/required-documents/required-documents-page";
import { EnrollmentFeesPage } from "./pages/admin/enrollment-fees/enrollment-fees-page";
import { AvailableModelsPage } from "./pages/admin/available-models/available-models-page";
import { FileManagerPage } from "./pages/admin/files/files-page";
import { CmsManagerPage } from "./pages/admin/cms/cms-manager-page";
import { LoginPage } from "./pages/auth/login-page";
import { NotificationsPage } from "./pages/notifications/notifications-page";
import type { AuthRole } from "./lib/auth-store";
import type { AppRouterContext } from "./router-context";
import { Route as rootRoute } from "./routes/__root";
import { BaccalaureateSeriesPage } from "./pages/admin/baccalaureate-series/baccalaureate-series";
import { NationalitysPage } from "./pages/admin/nationality/nationality";
import { ClassroomsPage } from "./pages/admin/classroom/classroom";
import { PluggedPage } from "./pages/admin/plugged/plugged-page";
import { NotificationTemplatesPage } from "./pages/admin/notification-templates/notification-templates-page";
import { ForbiddenPage } from "./pages/error/forbidden-page";

const ensureAuthenticated = ({ context }: { context: AppRouterContext }) => {
  const { status } = context.authStore.getState();
  if (status !== "authenticated") {
    throw redirect({ to: "/auth/login", replace: true });
  }
};

const ensureRole =
  (role: AuthRole) =>
  ({ context }: { context: AppRouterContext }) => {
    const { status, user } = context.authStore.getState();
    if (status !== "authenticated" || !user) {
      throw redirect({ to: "/auth/login", replace: true });
    }

    if (user.role !== role) {
      throw redirect({ to: "/" });
    }
  };

const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/dashboard",
  component: DashboardPage,
  beforeLoad: ensureAuthenticated
});

const homeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: HomePage
});

const publicationsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "pages/publications",
  component: PublicationsPage
});

const workingTimePublicRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "pages/working-time",
  component: WorkingTimePublicPage
});

const cmsPublicRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "pages/$slug",
  component: CmsPublicPage
});

const forbiddenRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "403",
  component: ForbiddenPage
});

const notificationsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "notifications",
  component: NotificationsPage,
  beforeLoad: ensureAuthenticated
});

const reinscriptionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "re-registration",
  component: ReinscriptionPage,
  beforeLoad: ensureAuthenticated
});

const reinscriptionTrashRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "trash",
  component: ReinscriptionTrashPage,
  beforeLoad: ensureAuthenticated
});

const inscriptionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "registration",
  component: InscriptionPage,
  beforeLoad: ensureAuthenticated
});

const userNotesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "notes",
  component: NotesPage,
  beforeLoad: ensureAuthenticated
});

const dossierSelectionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "folder-selection",
  component: DossierSelectionPage,
  beforeLoad: ensureAuthenticated
});

const concoursRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "competitions",
  component: ConcoursPage,
  beforeLoad: ensureAuthenticated
});

const mentionsUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "mentions",
  component: MentionsPage,
  beforeLoad: ensureAuthenticated
});

const journeysUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "journeys",
  component: JourneysPage,
  beforeLoad: ensureAuthenticated
});

const adminRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "admin",
  component: () => <Outlet />,
  beforeLoad: ensureAuthenticated
});

const adminReinscriptionRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "re-registration",
  component: ReinscriptionPage
});

const adminReinscriptionTrashRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "trash",
  component: ReinscriptionTrashPage
});

const adminInscriptionRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "registration",
  component: InscriptionPage
});

const adminNotesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "notes",
  component: NotesPage
});

const adminDossierSelectionRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "folder-selection",
  component: DossierSelectionPage
});

const adminConcoursRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "competitions",
  component: ConcoursPage
});

const adminDashboardRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "dashboard",
  component: DashboardPage
});

const academicYearsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "academic-years",
  component: AcademicYearsPage
});

const academicYearsUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "academic-years",
  component: AcademicYearsPage,
  beforeLoad: ensureAuthenticated
});

const workingTimeRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "working-time",
  component: WorkingTimePage
});

const workingTimeUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "working-time",
  component: WorkingTimePage,
  beforeLoad: ensureAuthenticated
});

const permissionsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "permissions",
  component: PermissionsPage
});

const permissionsUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "permissions",
  component: PermissionsPage,
  beforeLoad: ensureAuthenticated
});

const universityInfoRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "university-info",
  component: UniversityInfoPage
});

const offeringsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "offerings",
  component: OfferingsPage
});

const filesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "files",
  component: FileManagerPage
});

const baccalaureateSerieRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "baccalaureate-serie",
  component: BaccalaureateSeriesPage
});

const baccalaureateSerieUserRoute = createRoute({
  getParentRoute: () => usersRoute,
  path: "baccalaureate-serie",
  component: BaccalaureateSeriesPage
});

const teachingUnitRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "teaching-unit",
  component: TeachingUnitPage
});

const teachingUnitUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "teaching-unit",
  component: TeachingUnitPage,
  beforeLoad: ensureAuthenticated
});

const constituentElementsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "constituent-elements",
  component: ConstituentElementPage
});

const constituentElementsUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "constituent-elements",
  component: ConstituentElementPage,
  beforeLoad: ensureAuthenticated
});

const groupsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "groups",
  component: GroupsPage
});

const groupsUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "groups",
  component: GroupsPage,
  beforeLoad: ensureAuthenticated
});
const pluggedRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "plugged",
  component: PluggedPage
});
const availableServicesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "available-services",
  component: AvailableServicesPage
});

const requiredDocumentsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "required-documents",
  component: RequiredDocumentsPage
});

const enrollmentFeesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "enrollment-fees",
  component: EnrollmentFeesPage
});

const availableModelsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "available-models",
  component: AvailableModelsPage
});

const availableModelsUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "available-models",
  component: AvailableModelsPage,
  beforeLoad: ensureAuthenticated
});

const usersRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "users",
  component: UsersPage
});

const usersUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "users",
  component: UsersPage,
  beforeLoad: ensureAuthenticated
});

const rolesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "roles",
  component: RolesPage
});

const rolesUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "roles",
  component: RolesPage,
  beforeLoad: ensureAuthenticated
});

const subjectsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "subjects",
  component: SubjectsPage
});

const mentionsRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "mentions",
  component: MentionsPage
});

const journeysRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "journeys",
  component: JourneysPage
});

const cmsManagerRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "cms",
  component: CmsManagerPage
});

const cmsManagerUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "cms",
  component: CmsManagerPage,
  beforeLoad: ensureAuthenticated
});

const nationalityManagerRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "nationality",
  component: NationalitysPage
});

const nationalityManagerUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "nationality",
  component: NationalitysPage,
  beforeLoad: ensureAuthenticated
});

const classroomManagerRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "classroom",
  component: ClassroomsPage
});

const notificationTemplatesRoute = createRoute({
  getParentRoute: () => adminRoute,
  path: "notification-templates",
  component: NotificationTemplatesPage,
  beforeLoad: ensureAuthenticated
});

const classroomManagerUserRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "classroom",
  component: ClassroomsPage,
  beforeLoad: ensureAuthenticated
});

const authRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "auth",
  component: () => <Outlet />
});

const loginRoute = createRoute({
  getParentRoute: () => authRoute,
  path: "login",
  component: LoginPage,
  beforeLoad: ({ context }) => {
    if (context.authStore.getState().status === "authenticated") {
      throw redirect({ to: "/" });
    }
  }
});

const routeTree = rootRoute.addChildren([
  homeRoute,
  forbiddenRoute,
  publicationsRoute,
  workingTimePublicRoute,
  cmsPublicRoute,
  notificationsRoute,
  dashboardRoute,
  userNotesRoute,
  reinscriptionRoute,
  reinscriptionTrashRoute,
  inscriptionRoute,
  dossierSelectionRoute,
  concoursRoute,
  mentionsUserRoute,
  journeysUserRoute,
  academicYearsUserRoute,
  workingTimeUserRoute,
  teachingUnitUserRoute,
  constituentElementsUserRoute,
  groupsUserRoute,
  usersUserRoute,
  rolesUserRoute,
  permissionsUserRoute,
  availableModelsUserRoute,
  cmsManagerUserRoute,
  baccalaureateSerieUserRoute,
  nationalityManagerUserRoute,
  classroomManagerUserRoute,
  adminRoute.addChildren([
    adminDashboardRoute,
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
    offeringsRoute,
    filesRoute,
    permissionsRoute,
    teachingUnitRoute,
    constituentElementsRoute,
    groupsRoute,
    pluggedRoute,
    availableServicesRoute,
    requiredDocumentsRoute,
    enrollmentFeesRoute,
    availableModelsRoute,
    universityInfoRoute,
    cmsManagerRoute,
    baccalaureateSerieRoute,
    nationalityManagerRoute,
    classroomManagerRoute,
    notificationTemplatesRoute
  ]),
  authRoute.addChildren([loginRoute])
]);

export const createAppRouter = (context: AppRouterContext) =>
  createRouter({
    context,
    routeTree
    // defaultPreload: 'intent'
  });

declare module "@tanstack/react-router" {
  interface Register {
    router: ReturnType<typeof createAppRouter>;
  }
}
