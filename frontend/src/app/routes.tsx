import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";

// Importando as telas (Componentes)
import { Layout } from "./components/Layout";
import { Dashboard } from "./components/Dashboard";
import { ChatInterface } from "./components/ChatInterface";
import { Analytics } from "./components/Analytics";
import { Login } from "./components/Login";

// Importando o nosso verificador de autenticação
import { useAuth } from "./lib/auth";

// 1. Criamos o nosso "Guarda de Segurança"
const ProtectedRoute = () => {
  const { user } = useAuth();
  
  // Se o usuário existir, deixa passar (<Outlet />). 
  // Se não, redireciona para a tela de login (<Navigate />).
  return user ? <Outlet /> : <Navigate to="/login" replace />;
};

// 2. Definimos as rotas
export const router = createBrowserRouter([
  // Rota pública: Qualquer um pode acessar
  { 
    path: "/login", 
    Component: Login 
  },
  
  // Rotas protegidas: Precisam passar pelo Guarda de Segurança
  {
    path: "/",
    Component: ProtectedRoute,
    children: [
      {
        path: "",
        Component: Layout, // O Layout (Menu lateral e Topo) abraça as telas de dentro
        children: [
          { index: true, Component: Dashboard },
          { path: "chat", Component: ChatInterface },
          { path: "analytics", Component: Analytics },
        ],
      },
    ],
  },
]);