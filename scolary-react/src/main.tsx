import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider } from '@tanstack/react-router';

import { createAppRouter } from './router';
import { createAuthStore } from './lib/auth-store';
import { AuthProvider } from './providers/auth-provider';
import './index.css';

const queryClient = new QueryClient();
const authStore = createAuthStore();
const router = createAppRouter({ queryClient, authStore });

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider store={authStore}>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
