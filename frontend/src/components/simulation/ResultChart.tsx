import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
} from 'recharts';

interface ChartProps {
  data: Array<Record<string, number | string>>;
  xKey: string;
  yKey: string;
  type?: 'line' | 'area' | 'bar';
  color?: string;
  height?: number;
  label?: string;
  unit?: string;
}

const ResultChart: React.FC<ChartProps> = ({
  data,
  xKey,
  yKey,
  type = 'line',
  color = '#3B82F6',
  height = 250,
  label,
  unit,
}) => {
  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 10, right: 10, left: 0, bottom: 0 },
    };

    switch (type) {
      case 'area':
        return (
          <AreaChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey={xKey} tick={{ fontSize: 11 }} stroke="#94A3B8" />
            <YAxis tick={{ fontSize: 11 }} stroke="#94A3B8" />
            <Tooltip
              contentStyle={{
                background: '#1E293B',
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '12px',
              }}
            />
            <Area
              type="monotone"
              dataKey={yKey}
              stroke={color}
              fill={color}
              fillOpacity={0.1}
              strokeWidth={2}
            />
          </AreaChart>
        );
      case 'bar':
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey={xKey} tick={{ fontSize: 11 }} stroke="#94A3B8" />
            <YAxis tick={{ fontSize: 11 }} stroke="#94A3B8" />
            <Tooltip
              contentStyle={{
                background: '#1E293B',
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '12px',
              }}
            />
            <Bar dataKey={yKey} fill={color} radius={[4, 4, 0, 0]} />
          </BarChart>
        );
      default:
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey={xKey} tick={{ fontSize: 11 }} stroke="#94A3B8" />
            <YAxis tick={{ fontSize: 11 }} stroke="#94A3B8" />
            <Tooltip
              contentStyle={{
                background: '#1E293B',
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '12px',
              }}
            />
            <Line
              type="monotone"
              dataKey={yKey}
              stroke={color}
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5">
      {label && (
        <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3">
          {label} {unit && <span className="text-slate-400">({unit})</span>}
        </p>
      )}
      <ResponsiveContainer width="100%" height={height}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
};

export default ResultChart;
