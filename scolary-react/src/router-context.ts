import type { QueryClient } from '@tanstack/react-query';

import type { AuthStore } from './lib/auth-store';

export interface AppRouterContext {
  queryClient: QueryClient;
  authStore: AuthStore;
}
