import { Outlet, createRootRouteWithContext, useRouterState } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";

import { AppLayout } from "../layouts/app-layout";
import type { AppRouterContext } from "../router-context";
import { GlobalLoadingOverlay } from "@/components/global-loading-overlay";

const RootComponent = () => {
  const { location } = useRouterState();
  const isAuthRoute = location.pathname.startsWith('/auth');
  const isHomeRoute = location.pathname === '/';
  const isPublicCmsRoute = location.pathname.startsWith('/pages/');

  return (
    <>
      {isAuthRoute || isHomeRoute || isPublicCmsRoute ? (
        <Outlet />
      ) : (
        <AppLayout>
          <Outlet />
        </AppLayout>
      )}
      <GlobalLoadingOverlay />
      <TanStackRouterDevtools position="bottom-right" />
    </>
  );
};

export const Route = createRootRouteWithContext<AppRouterContext>()({
  component: RootComponent
});
