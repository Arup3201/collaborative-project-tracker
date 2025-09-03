import { createContext, useEffect, useState } from "react";

import { HttpGet } from "@/utils/http";

interface UserData {
  id: string;
  name: string;
  email: string;
}

interface AuthData {
  isLoading: boolean;
  isAuthenticated: boolean;
  setIsAuthenticated: (_: boolean) => void, 
  user: UserData | undefined;
  setUser: (_: UserData) => void
}

const AuthContext = createContext<AuthData>({
  isLoading: false,
  isAuthenticated: false,
  setIsAuthenticated: (_: boolean) => {}, 
  user: {} as UserData,
  setUser: (_: UserData) => {}
});

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserData | undefined>();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const getUser = async () => {
    setIsLoading(true);
    try {
      const data = await HttpGet("/auth/me");
      setUser({
        id: data.id,
        name: data.name,
        email: data.email,
      });
      setIsAuthenticated(true);
    } catch (err) {
      if (err instanceof Error) {
        console.error(`getUser failed with error: ${err.message}`);
        setUser(undefined);
        setIsAuthenticated(false);
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, isAuthenticated, setIsAuthenticated, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
