import React, { useEffect, useState } from 'react';
import { Activity } from 'lucide-react';

interface HealthData {
  status: string;
  version: string;
  gpu_available: boolean;
  active_simulations: number;
}

const HealthBadge: React.FC = () => {
  const [health, setHealth] = useState<HealthData | null>(null);

  useEffect(() => {
    const check = async () => {
      try {
        const res = await fetch('/api/v1/health');
        setHealth(await res.json());
      } catch {
        setHealth(null);
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  if (!health) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-50 text-red-600 text-xs font-medium">
        <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
        Offline
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-600 text-xs font-medium">
      <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
      API v{health.version}
      {health.gpu_available && (
        <span className="text-blue-600 ml-1">GPU</span>
      )}
    </div>
  );
};

export default HealthBadge;
