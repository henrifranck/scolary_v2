import { createContext, useContext, useMemo, useSyncExternalStore } from 'react';
import type { ReactNode } from 'react';

import type { AuthStore, AuthState } from '../lib/auth-store';

interface AuthContextValue {
  state: AuthState;
  store: AuthStore;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface AuthProviderProps {
  children: ReactNode;
  store: AuthStore;
}

export const AuthProvider = ({ children, store }: AuthProviderProps) => {
  const state = useSyncExternalStore(store.subscribe, store.getState, store.getState);

  const value = useMemo<AuthContextValue>(
    () => ({ state, store }),
    [state, store]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};
