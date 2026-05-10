import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";

// Componentes
import { Layout } from "./components/Layout";
import { Dashboard } from "./components/Dashboard";
import { ChatInterface } from "./components/ChatInterface";
import { Analytics } from "./components/Analytics";
import { Login } from "./components/Login";
import { SignUp } from "./components/SignUp";

// Auth
import { useAuth } from "./lib/auth";

// Proteção de rotas
const ProtectedRoute = () => {
  const { user } = useAuth();

  return user ? <Outlet /> : <Navigate to="/login" replace />;
};

// Rotas
export const router = createBrowserRouter([
  // Públicas
  {
    path: "/login",
    Component: Login,
  },

  {
    path: "/signup",
    Component: SignUp,
  },

  // Protegidas
  {
    path: "/",
    Component: ProtectedRoute,

    children: [
      {
        Component: Layout,

        children: [
          { index: true, Component: Dashboard },
          { path: "chat", Component: ChatInterface },
          { path: "analytics", Component: Analytics },
        ],
      },
    ],
  },
]);