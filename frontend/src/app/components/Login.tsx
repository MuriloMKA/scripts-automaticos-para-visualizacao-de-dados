import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Sparkles, Lock, Mail } from "lucide-react";
import { useAuth } from "../lib/auth";
import { authApi } from "../lib/api"; // Importamos a chamada real da API

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      // 1. Chamada real ao Backend Python
      const data = await authApi.login({ email, password });

      // 2. O 'data.user' agora vem da base de dados (com o nome real)
      // O 'data.access_token' é o passaporte para o resto do site
      login(data.user, data.access_token); 
      
      // 3. Entra no sistema
      navigate("/"); 
    } catch (err: any) {
      setError(err.message || "Erro ao conectar ao servidor. Verifique as suas credenciais.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
        
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-slate-800">SAP Script AI</h2>
          <p className="text-slate-500 text-sm mt-1">Insira as suas credenciais Klabin</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100 text-center">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">E-mail</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center"><Mail className="h-5 w-5 text-slate-400" /></div>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="utilizador@klabin.com.br" required />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Palavra-passe</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center"><Lock className="h-5 w-5 text-slate-400" /></div>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="••••••••" required />
            </div>
          </div>

          <button type="submit" disabled={isLoading} className="w-full py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-medium shadow-lg flex justify-center items-center">
            {isLoading ? "A validar..." : "Entrar no Sistema"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-600">
          Não tem conta? <Link to="/signup" className="text-blue-600 font-medium hover:underline">Registe-se aqui</Link>
        </p>
      </div>
    </div>
  );
}