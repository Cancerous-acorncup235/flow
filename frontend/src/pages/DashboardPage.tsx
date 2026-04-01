import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Activity,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Plus,
  ArrowRight,
} from 'lucide-react';

interface Simulation {
  id: string;
  name: string;
  solver: string;
  status: string;
  created_at: string;
  duration_seconds: number | null;
}

interface Stats {
  total: number;
  running: number;
  completed: number;
  failed: number;
}

const DashboardPage: React.FC = () => {
  const [simulations, setSimulations] = useState<Simulation[]>([]);
  const [stats, setStats] = useState<Stats>({ total: 0, running: 0, completed: 0, failed: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSimulations();
  }, []);

  const fetchSimulations = async () => {
    try {
      const res = await fetch('/api/v1/simulations/');
      const data = await res.json();
      setSimulations(data.simulations || []);

      const sims = data.simulations || [];
      setStats({
        total: sims.length,
        running: sims.filter((s: Simulation) => s.status === 'running').length,
        completed: sims.filter((s: Simulation) => s.status === 'completed').length,
        failed: sims.filter((s: Simulation) => s.status === 'failed').length,
      });
    } catch (err) {
      console.error('Failed to fetch simulations:', err);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { label: 'Total Simulations', value: stats.total, icon: Activity, color: 'bg-blue-50 text-blue-600' },
    { label: 'Running', value: stats.running, icon: Clock, color: 'bg-amber-50 text-amber-600' },
    { label: 'Completed', value: stats.completed, icon: CheckCircle2, color: 'bg-emerald-50 text-emerald-600' },
    { label: 'Failed', value: stats.failed, icon: AlertTriangle, color: 'bg-red-50 text-red-600' },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-500 mt-1">Engineering simulation overview</p>
        </div>
        <Link
          to="/simulations/new"
          className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium text-sm hover:bg-blue-700 transition-colors"
        >
          <Plus size={18} />
          New Simulation
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((card) => (
          <div
            key={card.label}
            className="bg-white rounded-2xl border border-slate-200 p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${card.color}`}>
                <card.icon size={20} />
              </div>
            </div>
            <p className="text-2xl font-bold text-slate-900">{card.value}</p>
            <p className="text-sm text-slate-500 mt-1">{card.label}</p>
          </div>
        ))}
      </div>

      {/* Recent Simulations */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-900">Recent Simulations</h2>
          <Link
            to="/simulations"
            className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1"
          >
            View all <ArrowRight size={14} />
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading...</div>
        ) : simulations.length === 0 ? (
          <div className="p-12 text-center">
            <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Activity size={24} className="text-slate-400" />
            </div>
            <p className="text-slate-500 font-medium">No simulations yet</p>
            <p className="text-slate-400 text-sm mt-1">
              Create your first simulation to get started
            </p>
            <Link
              to="/simulations/new"
              className="inline-flex items-center gap-2 mt-4 px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium text-sm hover:bg-blue-700 transition-colors"
            >
              <Plus size={16} />
              New Simulation
            </Link>
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                <th className="px-6 py-3">Name</th>
                <th className="px-6 py-3">Solver</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Duration</th>
                <th className="px-6 py-3">Created</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {simulations.map((sim) => (
                <tr
                  key={sim.id}
                  className="hover:bg-slate-50 cursor-pointer transition-colors"
                >
                  <td className="px-6 py-4">
                    <Link
                      to={`/simulations/${sim.id}`}
                      className="font-medium text-slate-900 hover:text-blue-600"
                    >
                      {sim.name}
                    </Link>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">{sim.solver}</td>
                  <td className="px-6 py-4">
                    <StatusBadge status={sim.status} />
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">
                    {sim.duration_seconds
                      ? `${sim.duration_seconds.toFixed(2)}s`
                      : '—'}
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">
                    {new Date(sim.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const styles: Record<string, string> = {
    created: 'bg-slate-100 text-slate-700',
    queued: 'bg-slate-100 text-slate-700',
    running: 'bg-blue-100 text-blue-700',
    completed: 'bg-emerald-100 text-emerald-700',
    failed: 'bg-red-100 text-red-700',
    cancelled: 'bg-amber-100 text-amber-700',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
        styles[status] || styles.created
      }`}
    >
      {status}
    </span>
  );
};

export default DashboardPage;
