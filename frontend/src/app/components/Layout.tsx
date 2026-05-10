import { useState } from "react";
import { Outlet, Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  MessageSquare,
  BarChart3,
  Menu,
  X,
  Sparkles,
  User,
  LogOut,
} from "lucide-react";
import { useAuth } from "../lib/auth";
// Use a simple public asset as placeholder (replace with real logo later)
const klabinLogo = "/favicon.svg";

export function Layout() {
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const menuItems = [
    { path: "/", icon: LayoutDashboard, label: "Dashboard" },
    { path: "/chat", icon: MessageSquare, label: "Gerador IA" },
    { path: "/analytics", icon: BarChart3, label: "Estatísticas" },
  ];

  return (
    <div className="h-screen flex bg-slate-50">
      {/* Sidebar */}
      <aside
        className={`bg-gradient-to-b from-slate-900 to-slate-800 text-white transition-all duration-300 ${
          sidebarOpen ? "w-64" : "w-20"
        } flex flex-col`}
      >
        {/* Logo & Toggle */}
        <div className="p-4 flex items-center justify-between border-b border-slate-700">
          {sidebarOpen ? (
            <>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-6 h-6" />
                </div>
                <div>
                  <h1 className="font-bold text-sm">SAP Script AI</h1>
                  <p className="text-xs text-slate-400">Klabin</p>
                </div>
              </div>
              <button
                onClick={() => setSidebarOpen(false)}
                className="p-1 hover:bg-slate-700 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </>
          ) : (
            <button
              onClick={() => setSidebarOpen(true)}
              className="p-2 hover:bg-slate-700 rounded-lg transition-colors mx-auto"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-3 rounded-xl transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-blue-600 to-purple-600 shadow-lg shadow-blue-500/50"
                    : "hover:bg-slate-700/50"
                } ${!sidebarOpen && "justify-center"}`}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && (
                  <span className="font-medium text-sm">{item.label}</span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* User Profile */}
        <div className="p-4 border-t border-slate-700">
          {sidebarOpen ? (
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-slate-600 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-slate-300" />
              </div>
              <div className="flex-1 min-w-0">
                {/* Nome dinâmico puxado do banco/token */}
                <p className="font-medium text-sm truncate text-white">
                  {user?.full_name || "Usuário Logado"}
                </p>
                {/* Mostra se é Admin ou email */}
                <p className="text-xs text-slate-400 truncate">
                  {user?.role === "admin" ? "Administrador" : "Analista"}
                </p>
              </div>
              
              {/* Botão de Sair */}
              <button 
                onClick={logout} 
                className="p-2 hover:bg-slate-700 rounded-lg text-slate-400 hover:text-red-400 transition-colors"
                title="Sair do sistema"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div 
              className="w-10 h-10 bg-slate-600 hover:bg-slate-500 cursor-pointer rounded-full flex items-center justify-center mx-auto transition-colors" 
              onClick={logout}
              title="Sair do sistema"
            >
              <LogOut className="w-5 h-5 text-slate-300" />
            </div>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <img src={klabinLogo} alt="Klabin" className="h-10" />
            <div className="border-l pl-4 hidden md:block">
              <p className="text-sm font-medium text-slate-700">
                Projeto Acadêmico - TI
              </p>
              <p className="text-xs text-slate-500">
                Record to Report | Abdul Latif
              </p>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
