import { useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import { loginUser, logoutUser } from "../redux/slices/authSlice";
import { AuthService } from "../services/AuthService";

type LoginParams = {
  access_token: string;
  refresh_token: string;
  email: string;
};

export const useAuth = () => {
  const dispatch = useAppDispatch();
  const email = useAppSelector((state) => state.auth.email);
  const [isAdmin, setIsAdmin] = useState(false);

  const doLogin = (params: LoginParams) => {
    dispatch(loginUser(params.email));
  };

  const clearAuth = () => {
    dispatch(logoutUser());
    setIsAdmin(false);
  };

  const doLogout = () => {
    new AuthService()
      .logout()
      .then(() => clearAuth())
      .catch((error) => {
        console.error("Error al cerrar sesión:", error);
        clearAuth();
      });
  };

  const loadUser = async () => {
    try {
      const user = await new AuthService().me();
      if (user.email) {
        dispatch(loginUser(user.email));
      } else {
        clearAuth();
      }
    } catch {
      clearAuth();
      console.log("Usuario no autenticado. Mostrando menú de invitado.");
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  return {
    email,
    isAdmin,
    doLogin,
    doLogout,
  };
};