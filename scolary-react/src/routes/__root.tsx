import { Outlet, createRootRouteWithContext, useRouterState } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';

import { AppLayout } from '../layouts/app-layout';
import type { AppRouterContext } from '../router-context';

const RootComponent = () => {
  const { location } = useRouterState();
  const isAuthRoute = location.pathname.startsWith('/auth');

  return (
    <>
      {isAuthRoute ? (
        <Outlet />
      ) : (
        <AppLayout>
          <Outlet />
        </AppLayout>
      )}
      <TanStackRouterDevtools position="bottom-right" />
    </>
  );
};

export const Route = createRootRouteWithContext<AppRouterContext>()({
  component: RootComponent
});
