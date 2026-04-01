import React, { useEffect, useState } from 'react';
import { Cpu, Zap, Gauge, Thermometer, Waves } from 'lucide-react';

interface Solver {
  name: string;
  type: string;
  description: string;
  speedup: string;
  use_case: string;
  available: boolean;
}

const solverIcons: Record<string, React.ElementType> = {
  fea_classic: Gauge,
  fea_neural: Zap,
  thermal_classic: Thermometer,
  thermal_neural: Zap,
  fluid_classic: Waves,
  fluid_neural: Zap,
};

const SolversPage: React.FC = () => {
  const [solvers, setSolvers] = useState<Solver[]>([]);

  useEffect(() => {
    fetch('/api/v1/solvers/')
      .then((r) => r.json())
      .then(setSolvers)
      .catch(console.error);
  }, []);

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Solvers</h1>
        <p className="text-slate-500 mt-1">
          Available simulation engines — from classical FEM to AI-accelerated Neural Operators
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {solvers.map((solver) => {
          const Icon = solverIcons[solver.type] || Cpu;
          return (
            <div
              key={solver.type}
              className={`bg-white rounded-2xl border p-6 transition-all ${
                solver.available
                  ? 'border-slate-200 hover:border-blue-200 hover:shadow-md'
                  : 'border-slate-100 opacity-60'
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                    solver.available
                      ? 'bg-blue-50 text-blue-600'
                      : 'bg-slate-100 text-slate-400'
                  }`}
                >
                  <Icon size={20} />
                </div>
                <span
                  className={`text-xs font-medium px-2.5 py-1 rounded-full ${
                    solver.available
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-slate-100 text-slate-500'
                  }`}
                >
                  {solver.available ? 'Available' : 'Coming Soon'}
                </span>
              </div>

              <h3 className="text-lg font-semibold text-slate-900 mb-1">
                {solver.name}
              </h3>
              <p className="text-sm text-slate-500 mb-3">{solver.description}</p>

              <div className="flex items-center gap-4 text-xs">
                <div className="flex items-center gap-1.5">
                  <Zap size={12} className="text-amber-500" />
                  <span className="text-slate-600 font-medium">{solver.speedup}</span>
                </div>
                <div className="text-slate-400">{solver.use_case}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Comparison Table */}
      <div className="mt-12 bg-white rounded-2xl border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100">
          <h2 className="text-lg font-semibold text-slate-900">Solver Comparison</h2>
        </div>
        <table className="w-full">
          <thead>
            <tr className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-3">Solver</th>
              <th className="px-6 py-3">Type</th>
              <th className="px-6 py-3">Speed</th>
              <th className="px-6 py-3">Accuracy</th>
              <th className="px-6 py-3">GPU Required</th>
              <th className="px-6 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            <tr>
              <td className="px-6 py-3 font-medium">FEA Classic</td>
              <td className="px-6 py-3 text-sm text-slate-500">FEM</td>
              <td className="px-6 py-3 text-sm">1x (baseline)</td>
              <td className="px-6 py-3 text-sm">High</td>
              <td className="px-6 py-3 text-sm">No</td>
              <td className="px-6 py-3"><span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full">Available</span></td>
            </tr>
            <tr>
              <td className="px-6 py-3 font-medium">FEA Neural</td>
              <td className="px-6 py-3 text-sm text-slate-500">Neural Operator</td>
              <td className="px-6 py-3 text-sm">100x</td>
              <td className="px-6 py-3 text-sm">High*</td>
              <td className="px-6 py-3 text-sm">Recommended</td>
              <td className="px-6 py-3"><span className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">Coming Soon</span></td>
            </tr>
            <tr>
              <td className="px-6 py-3 font-medium">Thermal Classic</td>
              <td className="px-6 py-3 text-sm text-slate-500">FDM</td>
              <td className="px-6 py-3 text-sm">1x (baseline)</td>
              <td className="px-6 py-3 text-sm">High</td>
              <td className="px-6 py-3 text-sm">No</td>
              <td className="px-6 py-3"><span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full">Available</span></td>
            </tr>
            <tr>
              <td className="px-6 py-3 font-medium">Fluid Classic</td>
              <td className="px-6 py-3 text-sm text-slate-500">FVM</td>
              <td className="px-6 py-3 text-sm">1x (baseline)</td>
              <td className="px-6 py-3 text-sm">High</td>
              <td className="px-6 py-3 text-sm">No</td>
              <td className="px-6 py-3"><span className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">Coming Soon</span></td>
            </tr>
          </tbody>
        </table>
        <div className="px-6 py-3 text-xs text-slate-400">
          * Neural Operator accuracy depends on training data quality
        </div>
      </div>
    </div>
  );
};

export default SolversPage;
