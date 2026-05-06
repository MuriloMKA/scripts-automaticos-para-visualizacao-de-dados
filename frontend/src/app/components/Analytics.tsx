import { useEffect, useState } from "react";
import { Calendar, TrendingUp, Clock, Users, Download } from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { fetchDashboardSummary } from "../lib/api";

const usageData = [
  { day: "Seg", scripts: 8 },
  { day: "Ter", scripts: 12 },
  { day: "Qua", scripts: 10 },
  { day: "Qui", scripts: 15 },
  { day: "Sex", scripts: 7 },
];

const typeData = [
  { name: "SQL", value: 45, color: "#3b82f6" },
  { name: "ABAP", value: 25, color: "#8b5cf6" },
  { name: "Power BI", value: 20, color: "#10b981" },
  { name: "JSON", value: 10, color: "#f59e0b" },
];

const savingsData = [
  { month: "Out", hours: 15 },
  { month: "Nov", hours: 28 },
  { month: "Dez", hours: 35 },
  { month: "Jan", hours: 42 },
  { month: "Fev", hours: 58 },
  { month: "Mar", hours: 65 },
];

export function Analytics() {
  const [scriptsGenerated, setScriptsGenerated] = useState(52);
  const [timeSavedHours, setTimeSavedHours] = useState(124);
  const [activeUsers, setActiveUsers] = useState(8);
  const [successRate, setSuccessRate] = useState(94);

  useEffect(() => {
    let mounted = true;

    fetchDashboardSummary()
      .then((data) => {
        if (!mounted) return;
        setScriptsGenerated(data.scripts_generated);
        setTimeSavedHours(data.time_saved_hours);
        setActiveUsers(data.active_users);
        setSuccessRate(data.success_rate);
      })
      .catch(() => undefined);

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Analytics</h1>
          <p className="text-slate-600">
            Acompanhe métricas e performance do sistema
          </p>
        </div>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2">
          <Download className="w-4 h-4" />
          Exportar Relatório
        </button>
      </div>

      {/* Period Selector */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Calendar className="w-5 h-5 text-slate-600" />
          <span className="text-sm font-medium text-slate-700">Período:</span>
          <select className="px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Últimos 7 dias</option>
            <option>Últimos 30 dias</option>
            <option>Últimos 3 meses</option>
            <option>Último ano</option>
          </select>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-sm bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
            Hoje
          </button>
          <button className="px-4 py-2 text-sm bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
            Esta semana
          </button>
          <button className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg">
            Este mês
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
              <TrendingUp className="w-5 h-5" />
            </div>
            <span className="text-xs bg-white/20 px-2 py-1 rounded-full backdrop-blur-sm">
              +15%
            </span>
          </div>
          <p className="text-3xl font-bold mb-1">{scriptsGenerated}</p>
          <p className="text-sm text-blue-100">Scripts gerados</p>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
              <Clock className="w-5 h-5" />
            </div>
            <span className="text-xs bg-white/20 px-2 py-1 rounded-full backdrop-blur-sm">
              -18%
            </span>
          </div>
          <p className="text-3xl font-bold mb-1">{timeSavedHours}h</p>
          <p className="text-sm text-purple-100">Tempo economizado</p>
        </div>

        <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-bold mb-1">{activeUsers}</p>
          <p className="text-sm text-green-100">Usuários ativos</p>
        </div>

        <div className="bg-gradient-to-br from-orange-600 to-orange-700 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
              <TrendingUp className="w-5 h-5" />
            </div>
            <span className="text-xs bg-white/20 px-2 py-1 rounded-full backdrop-blur-sm">
              {successRate}%
            </span>
          </div>
          <p className="text-3xl font-bold mb-1">{successRate}%</p>
          <p className="text-sm text-orange-100">Taxa de sucesso</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Usage Chart */}
        <div className="bg-white rounded-xl p-6 border border-slate-200">
          <h3 className="font-bold text-lg text-slate-800 mb-6">Uso Semanal</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={usageData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="day" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip />
              <Bar dataKey="scripts" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Type Distribution */}
        <div className="bg-white rounded-xl p-6 border border-slate-200">
          <h3 className="font-bold text-lg text-slate-800 mb-6">
            Distribuição por Tipo
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={typeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name} ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {typeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Savings Chart */}
      <div className="bg-white rounded-xl p-6 border border-slate-200">
        <div className="flex items-center justify-between mb-6">
          <h3 className="font-bold text-lg text-slate-800">
            Tempo Economizado (Horas)
          </h3>
          <div className="flex items-center gap-2 text-sm text-green-600">
            <TrendingUp className="w-4 h-4" />
            <span className="font-medium">+42% vs período anterior</span>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={savingsData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="month" stroke="#64748b" />
            <YAxis stroke="#64748b" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="hours"
              stroke="#10b981"
              strokeWidth={3}
              dot={{ fill: "#10b981", r: 6 }}
              name="Horas economizadas"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
