import { useCallback } from 'react';

export type AuthRole = 'student' | 'admin';

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: AuthRole;
  permissions?: Record<string, { get: boolean; post: boolean; put: boolean; delete: boolean }> | null;
  is_superuser?: boolean;
}

export interface AuthState {
  status: 'authenticated' | 'anonymous';
  user: AuthUser | null;
}

type Listener = (state: AuthState) => void;

const STORAGE_KEY = 'scolary-auth-state';

const readFromStorage = (): AuthState | null => {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }

    const parsed = JSON.parse(raw) as AuthState;
    if (parsed && typeof parsed === 'object' && 'status' in parsed) {
      return parsed;
    }
  } catch (error) {
    console.warn('Failed to read auth state from storage', error);
  }

  return null;
};

const writeToStorage = (state: AuthState) => {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    console.warn('Failed to persist auth state', error);
  }
};

export const createAuthStore = (initialState?: Partial<AuthState>) => {
  let state: AuthState =
    initialState && initialState.user
      ? { status: 'authenticated', user: initialState.user }
      : readFromStorage() ?? { status: 'anonymous', user: null };

  const listeners = new Set<Listener>();

  const notify = () => {
    for (const listener of listeners) {
      listener(state);
    }
  };

  const setState = (next: AuthState) => {
    state = next;
    writeToStorage(state);
    notify();
  };

  const login = (user: AuthUser) => {
    setState({ status: 'authenticated', user });
  };

  const logout = () => {
    setState({ status: 'anonymous', user: null });
  };

  const subscribe = (listener: Listener) => {
    listeners.add(listener);
    return () => listeners.delete(listener);
  };

  const getState = () => state;

  return {
    login,
    logout,
    subscribe,
    getState
  };
};

export type AuthStore = ReturnType<typeof createAuthStore>;

export const useAuthActions = (store: AuthStore) => {
  const login = useCallback(store.login, [store]);
  const logout = useCallback(store.logout, [store]);

  return { login, logout };
};
