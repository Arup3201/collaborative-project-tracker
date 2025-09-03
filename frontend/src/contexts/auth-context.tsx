import { createContext, useEffect, useState } from "react";

import { HttpGet } from "@/utils/http";

interface UserData {
  id: string;
  name: string;
  email: string;
}

interface AuthData {
  isAuthenticated: boolean;
  user: UserData | undefined;
  setAuth: (user: UserData, isAuthenticated: boolean) => void
}

const AuthContext = createContext<AuthData>({
  isAuthenticated: false,
  user: {} as UserData,
  setAuth: () => {}
});

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserData | undefined>();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const getUser = async () => {
    try {
      const data = await HttpGet("/auth/me");
      setUser({
        id: data.id,
        name: data.name,
        email: data.email,
      });
      setIsAuthenticated(true)
    } catch (err) {
      if (err instanceof Error) {
        console.error(`getUser failed with error: ${err.message}`);
        setUser(undefined);
        setIsAuthenticated(false);
      }
    }
  };

  useEffect(() => {
    getUser()
  }, []);

  const setAuth = (user: UserData, isAuthenticated: boolean) => {
    setUser({
        id: user.id,
        name: user.name,
        email: user.email,
    })
    setIsAuthenticated(isAuthenticated)
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, setAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
