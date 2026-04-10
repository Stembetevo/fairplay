import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { getCurrentUser, loginUser, logoutUser, registerUser } from "../api/auth";
import type { Position, UserSummary } from "../types";

interface AuthContextValue {
  user: UserSummary | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (payload: {
    username: string;
    email: string;
    password1: string;
    preferred_position: Position;
  }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    try {
      const me = await getCurrentUser();
      setUser(me);
    } catch {
      setUser(null);
    }
  }, []);

  useEffect(() => {
    async function bootstrap() {
      await refreshUser();
      setIsLoading(false);
    }

    void bootstrap();
  }, [refreshUser]);

  const login = useCallback(async (username: string, password: string) => {
    const me = await loginUser({ username, password });
    setUser(me);
  }, []);

  const register = useCallback(
    async (payload: {
      username: string;
      email: string;
      password1: string;
      preferred_position: Position;
    }) => {
      const me = await registerUser(payload);
      setUser(me);
    },
    []
  );
  const logout = useCallback(async () => {
    await logoutUser();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, isLoading, login, register, logout, refreshUser }),
    [isLoading, login, logout, refreshUser, register, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
