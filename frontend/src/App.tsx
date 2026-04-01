import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'sonner';
import Layout from './components/ui/Layout';
import DashboardPage from './pages/DashboardPage';
import SimulationPage from './pages/SimulationPage';
import SolversPage from './pages/SolversPage';
import NewSimulationPage from './pages/NewSimulationPage';

const App: React.FC = () => {
  return (
    <>
      <Toaster position="top-right" richColors />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/simulations" element={<DashboardPage />} />
          <Route path="/simulations/new" element={<NewSimulationPage />} />
          <Route path="/simulations/:id" element={<SimulationPage />} />
          <Route path="/solvers" element={<SolversPage />} />
        </Route>
      </Routes>
    </>
  );
};

export default App;
