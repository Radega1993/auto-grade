import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import Navbar from './components/layout/Navbar';
import ProtectedRoute from './components/auth/ProtectedRoute';
import { UserRole } from './types';

// Páginas
import Home from './pages/Home';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import Dashboard from './pages/Dashboard';
import Assignments from './pages/Assignments';
import AssignmentUploader from './components/assignments/AssignmentUploader';
import AssignmentEditor from './components/assignments/AssignmentEditor';

// Componentes de páginas placeholder
const Rubrics = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Gestión de Rúbricas</h1>
      <p className="text-gray-600">Esta página está en desarrollo...</p>
    </div>
  </div>
);

const Admin = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Panel de Administración</h1>
      <p className="text-gray-600">Esta página está en desarrollo...</p>
    </div>
  </div>
);

const Profile = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Perfil de Usuario</h1>
      <p className="text-gray-600">Esta página está en desarrollo...</p>
    </div>
  </div>
);

const App: React.FC = () => {
  const { isAuthenticated } = useAuthStore();

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navbar solo se muestra cuando el usuario está autenticado */}
        {isAuthenticated && <Navbar />}
        
        <Routes>
          {/* Rutas públicas */}
          <Route 
            path="/" 
            element={
              <ProtectedRoute requireAuth={false}>
                <Home />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/login" 
            element={
              <ProtectedRoute requireAuth={false}>
                {isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginForm />}
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/register" 
            element={
              <ProtectedRoute requireAuth={false}>
                {isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterForm />}
              </ProtectedRoute>
            } 
          />

          {/* Rutas protegidas */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/assignments" 
            element={
              <ProtectedRoute requiredRoles={[UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]}>
                <Assignments />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/assignments/new" 
            element={
              <ProtectedRoute requiredRoles={[UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]}>
                <AssignmentUploader />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/assignments/:id/edit" 
            element={
              <ProtectedRoute requiredRoles={[UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]}>
                <AssignmentEditor />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/rubrics" 
            element={
              <ProtectedRoute requiredRoles={[UserRole.COORDINATOR, UserRole.ADMIN]}>
                <Rubrics />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/admin/*" 
            element={
              <ProtectedRoute requiredRoles={[UserRole.ADMIN]}>
                <Admin />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } 
          />

          {/* Ruta por defecto */}
          <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/"} replace />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
