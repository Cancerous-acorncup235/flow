import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import {
  ArrowLeft,
  Play,
  Square,
  Trash2,
  Clock,
  CheckCircle2,
  AlertTriangle,
} from 'lucide-react';

interface Simulation {
  id: string;
  name: string;
  description: string;
  solver: string;
  status: string;
  geometry_format: string | null;
  parameters: Record<string, unknown>;
  result_summary: Record<string, unknown>;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  duration_seconds: number | null;
  mesh_elements: number | null;
  mesh_nodes: number | null;
}

const SimulationPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [sim, setSim] = useState<Simulation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) fetchSimulation(id);
  }, [id]);

  const fetchSimulation = async (simId: string) => {
    try {
      const res = await fetch(`/api/v1/simulations/${simId}`);
      if (!res.ok) throw new Error('Not found');
      setSim(await res.json());
    } catch {
      toast.error('Simulation not found');
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const handleRun = async () => {
    if (!id) return;
    try {
      const res = await fetch(`/api/v1/simulations/${id}/run`, { method: 'POST' });
      if (!res.ok) throw new Error('Run failed');
      const updated = await res.json();
      setSim(updated);
      toast.success('Simulation completed');
    } catch {
      toast.error('Failed to run simulation');
    }
  };

  const handleDelete = async () => {
    if (!id || !confirm('Delete this simulation?')) return;
    try {
      await fetch(`/api/v1/simulations/${id}`, { method: 'DELETE' });
      toast.success('Simulation deleted');
      navigate('/');
    } catch {
      toast.error('Failed to delete');
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading...</div>;
  if (!sim) return null;

  const statusConfig: Record<string, { icon: React.ElementType; color: string; bg: string }> = {
    created: { icon: Clock, color: 'text-slate-600', bg: 'bg-slate-100' },
    running: { icon: Clock, color: 'text-blue-600', bg: 'bg-blue-100' },
    completed: { icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-100' },
    failed: { icon: AlertTriangle, color: 'text-red-600', bg: 'bg-red-100' },
  };

  const status = statusConfig[sim.status] || statusConfig.created;
  const StatusIcon = status.icon;

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-slate-500 hover:text-slate-700 mb-6"
      >
        <ArrowLeft size={16} />
        Back to Dashboard
      </button>

      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">{sim.name}</h1>
          <p className="text-slate-500 mt-1">{sim.description || 'No description'}</p>
        </div>
        <div className="flex items-center gap-3">
          {sim.status === 'created' && (
            <button
              onClick={handleRun}
              className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium text-sm hover:bg-blue-700 transition-colors"
            >
              <Play size={16} />
              Run
            </button>
          )}
          {sim.status === 'running' && (
            <button className="flex items-center gap-2 px-5 py-2.5 bg-amber-600 text-white rounded-xl font-medium text-sm hover:bg-amber-700 transition-colors">
              <Square size={16} />
              Cancel
            </button>
          )}
          <button
            onClick={handleDelete}
            className="flex items-center gap-2 px-5 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-xl font-medium text-sm hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      {/* Status Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${status.bg}`}>
            <StatusIcon size={24} className={status.color} />
          </div>
          <div>
            <p className="text-lg font-semibold text-slate-900 capitalize">{sim.status}</p>
            <p className="text-sm text-slate-500">
              Solver: {sim.solver}
              {sim.geometry_format && ` | Format: ${sim.geometry_format}`}
            </p>
          </div>
        </div>
      </div>

      {/* Details Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <DetailCard label="Created" value={new Date(sim.created_at).toLocaleString()} />
        <DetailCard
          label="Duration"
          value={sim.duration_seconds ? `${sim.duration_seconds.toFixed(2)}s` : '—'}
        />
        <DetailCard label="Solver" value={sim.solver} />
      </div>

      {/* Results */}
      {sim.status === 'completed' && sim.result_summary && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(sim.result_summary).map(([key, value]) => (
              <div key={key} className="bg-slate-50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">
                  {key.replace(/_/g, ' ')}
                </p>
                <p className="text-lg font-semibold text-slate-900">
                  {typeof value === 'number' ? value.toFixed(4) : String(value)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const DetailCard: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="bg-white rounded-2xl border border-slate-200 p-4">
    <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{label}</p>
    <p className="text-sm font-medium text-slate-900">{value}</p>
  </div>
);

export default SimulationPage;
