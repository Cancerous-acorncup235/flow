import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { ArrowLeft, Play, Upload } from 'lucide-react';

const SOLVERS = [
  { value: 'fea_classic', label: 'FEA Classic', desc: 'Structural analysis (FEM)' },
  { value: 'fea_neural', label: 'FEA Neural', desc: 'AI-accelerated structural (coming soon)', disabled: true },
  { value: 'thermal_classic', label: 'Thermal Classic', desc: 'Heat transfer analysis' },
  { value: 'thermal_neural', label: 'Thermal Neural', desc: 'AI-accelerated thermal (coming soon)', disabled: true },
];

const NewSimulationPage: React.FC = () => {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [solver, setSolver] = useState('fea_classic');
  const [file, setFile] = useState<File | null>(null);
  const [creating, setCreating] = useState(false);

  const handleCreate = async () => {
    if (!name.trim()) {
      toast.error('Simulation name is required');
      return;
    }

    setCreating(true);
    try {
      // Create simulation
      const res = await fetch('/api/v1/simulations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          description: description.trim(),
          solver,
          parameters: {},
        }),
      });

      if (!res.ok) throw new Error('Failed to create simulation');

      const sim = await res.json();

      // Upload geometry if provided
      if (file) {
        const formData = new FormData();
        formData.append('file', file);

        const uploadRes = await fetch(`/api/v1/simulations/${sim.id}/upload`, {
          method: 'POST',
          body: formData,
        });

        if (!uploadRes.ok) {
          toast.error('Simulation created but geometry upload failed');
        }
      }

      toast.success('Simulation created');
      navigate(`/simulations/${sim.id}`);
    } catch (err) {
      toast.error('Failed to create simulation');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-slate-500 hover:text-slate-700 mb-6"
      >
        <ArrowLeft size={16} />
        Back
      </button>

      <h1 className="text-3xl font-bold text-slate-900 mb-2">New Simulation</h1>
      <p className="text-slate-500 mb-8">Configure and create a new engineering simulation</p>

      <div className="space-y-6">
        {/* Name */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Simulation Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. bridge-beam-analysis"
            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-colors"
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the simulation..."
            rows={3}
            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-colors resize-none"
          />
        </div>

        {/* Solver Selection */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Solver
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {SOLVERS.map((s) => (
              <button
                key={s.value}
                onClick={() => !s.disabled && setSolver(s.value)}
                disabled={s.disabled}
                className={`text-left p-4 rounded-xl border-2 transition-all ${
                  solver === s.value
                    ? 'border-blue-500 bg-blue-50'
                    : s.disabled
                    ? 'border-slate-100 bg-slate-50 opacity-50 cursor-not-allowed'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <p className="font-medium text-slate-900">{s.label}</p>
                <p className="text-xs text-slate-500 mt-1">{s.desc}</p>
              </button>
            ))}
          </div>
        </div>

        {/* File Upload */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Geometry File (optional)
          </label>
          <div className="border-2 border-dashed border-slate-200 rounded-xl p-8 text-center hover:border-slate-300 transition-colors">
            <input
              type="file"
              accept=".step,.stp,.iges,.igs,.stl,.obj"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload size={32} className="mx-auto text-slate-400 mb-3" />
              {file ? (
                <p className="text-sm font-medium text-slate-700">{file.name}</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-slate-700">
                    Click to upload geometry
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    STEP, IGES, STL, or OBJ
                  </p>
                </>
              )}
            </label>
          </div>
        </div>

        {/* Submit */}
        <button
          onClick={handleCreate}
          disabled={creating || !name.trim()}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play size={18} />
          {creating ? 'Creating...' : 'Create Simulation'}
        </button>
      </div>
    </div>
  );
};

export default NewSimulationPage;
