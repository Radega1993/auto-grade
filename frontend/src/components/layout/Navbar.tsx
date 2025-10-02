import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Menu, 
  X, 
  User, 
  LogOut, 
  Settings, 
  BookOpen, 
  BarChart3,
  Users,
  Shield
} from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { UserRole } from '../../types';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout, hasRole, hasAnyRole } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  const getRoleIcon = (role: UserRole) => {
    switch (role) {
      case UserRole.ADMIN:
        return <Shield className="h-4 w-4" />;
      case UserRole.COORDINATOR:
        return <Users className="h-4 w-4" />;
      case UserRole.TEACHER:
        return <BookOpen className="h-4 w-4" />;
      default:
        return <User className="h-4 w-4" />;
    }
  };

  const getRoleName = (role: UserRole) => {
    switch (role) {
      case UserRole.ADMIN:
        return 'Administrador';
      case UserRole.COORDINATOR:
        return 'Coordinador';
      case UserRole.TEACHER:
        return 'Profesor';
      default:
        return 'Usuario';
    }
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="flex-shrink-0 flex items-center">
              <BookOpen className="h-8 w-8 text-indigo-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">AutoGrader</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Dashboard
            </Link>
            
            {hasAnyRole([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]) && (
              <Link
                to="/assignments"
                className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Tareas
              </Link>
            )}

            {hasAnyRole([UserRole.COORDINATOR, UserRole.ADMIN]) && (
              <Link
                to="/rubrics"
                className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Rúbricas
              </Link>
            )}

            {hasRole(UserRole.ADMIN) && (
              <Link
                to="/admin"
                className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Administración
              </Link>
            )}

            <Link
              to="/profile"
              className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Perfil
            </Link>
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              {getRoleIcon(user?.role || UserRole.TEACHER)}
              <span className="text-sm text-gray-700">
                {user?.first_name} {user?.last_name}
              </span>
              <span className="text-xs text-gray-500">
                ({getRoleName(user?.role || UserRole.TEACHER)})
              </span>
            </div>
            
            <button
              onClick={handleLogout}
              className="text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium flex items-center"
            >
              <LogOut className="h-4 w-4 mr-1" />
              Cerrar Sesión
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-indigo-600 focus:outline-none focus:text-indigo-600"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-50">
            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-indigo-600 block px-3 py-2 rounded-md text-base font-medium"
              onClick={() => setIsOpen(false)}
            >
              Dashboard
            </Link>
            
            {hasAnyRole([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]) && (
              <Link
                to="/assignments"
                className="text-gray-700 hover:text-indigo-600 block px-3 py-2 rounded-md text-base font-medium"
                onClick={() => setIsOpen(false)}
              >
                Tareas
              </Link>
            )}

            {hasAnyRole([UserRole.COORDINATOR, UserRole.ADMIN]) && (
              <Link
                to="/rubrics"
                className="text-gray-700 hover:text-indigo-600 block px-3 py-2 rounded-md text-base font-medium"
                onClick={() => setIsOpen(false)}
              >
                Rúbricas
              </Link>
            )}

            {hasRole(UserRole.ADMIN) && (
              <Link
                to="/admin"
                className="text-gray-700 hover:text-indigo-600 block px-3 py-2 rounded-md text-base font-medium"
                onClick={() => setIsOpen(false)}
              >
                Administración
              </Link>
            )}

            <Link
              to="/profile"
              className="text-gray-700 hover:text-indigo-600 block px-3 py-2 rounded-md text-base font-medium"
              onClick={() => setIsOpen(false)}
            >
              Perfil
            </Link>

            <div className="border-t border-gray-200 pt-4">
              <div className="flex items-center px-3 py-2">
                {getRoleIcon(user?.role || UserRole.TEACHER)}
                <div className="ml-3">
                  <div className="text-base font-medium text-gray-800">
                    {user?.first_name} {user?.last_name}
                  </div>
                  <div className="text-sm text-gray-500">
                    {getRoleName(user?.role || UserRole.TEACHER)}
                  </div>
                </div>
              </div>
              
              <button
                onClick={handleLogout}
                className="w-full text-left text-gray-700 hover:text-red-600 block px-3 py-2 rounded-md text-base font-medium flex items-center"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
