import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Plus, 
  FileText, 
  BarChart3, 
  Users, 
  Brain,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { useAuthStore } from '../stores/authStore';
import { UserRole } from '../types';
import { apiService } from '../services/api';
import DebugAuth from '../components/DebugAuth';

const Dashboard: React.FC = () => {
  const { user, hasRole, hasAnyRole } = useAuthStore();
  const navigate = useNavigate();

  const handleQuickAction = (link: string) => {
    navigate(link);
  };

  const getRoleDescription = (role: UserRole): string => {
    switch (role) {
      case UserRole.ADMIN:
        return 'Gestiona la plataforma, usuarios y configuración del sistema.';
      case UserRole.COORDINATOR:
        return 'Coordina profesores, gestiona rúbricas y supervisa el rendimiento académico.';
      case UserRole.TEACHER:
        return 'Crea tareas, corrige automáticamente y gestiona el progreso de tus estudiantes.';
      default:
        return 'Bienvenido a tu panel de control.';
    }
  };

  const quickActions = [
    {
      title: 'Crear Solución y Rúbrica',
      description: 'Subir documento y generar soluciones con IA',
      icon: <Brain className="h-6 w-6" />,
      link: '/assignments/new',
      color: 'bg-blue-500',
      roles: [UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN],
    },
    {
      title: 'Mis Rúbricas y Soluciones',
      description: 'Gestionar rúbricas y soluciones existentes',
      icon: <FileText className="h-6 w-6" />,
      link: '/assignments',
      color: 'bg-green-500',
      roles: [UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN],
    },
    {
      title: 'Estadísticas',
      description: 'Ver estadísticas y reportes de rendimiento',
      icon: <BarChart3 className="h-6 w-6" />,
      link: '/statistics',
      color: 'bg-purple-500',
      roles: [UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN],
    },
    {
      title: 'Gestión de Usuarios',
      description: 'Administrar usuarios y permisos',
      icon: <Users className="h-6 w-6" />,
      link: '/users',
      color: 'bg-orange-500',
      roles: [UserRole.COORDINATOR, UserRole.ADMIN],
    },
  ];

  const recentActivity = [
    {
      id: 1,
      title: 'Nueva asignación creada',
      description: 'Matemáticas - Tema 3',
      time: 'Hace 2 horas',
      type: 'success',
    },
    {
      id: 2,
      title: 'Corrección completada',
      description: '25 estudiantes evaluados',
      time: 'Hace 4 horas',
      type: 'info',
    },
    {
      id: 3,
      title: 'Usuario registrado',
      description: 'Nuevo profesor agregado',
      time: 'Ayer',
      type: 'info',
    },
  ];

  const stats = [
    {
      name: 'Asignaciones Totales',
      value: '12',
      change: '+2',
      changeType: 'positive',
      icon: <FileText className="h-5 w-5" />,
    },
    {
      name: 'Estudiantes Activos',
      value: '156',
      change: '+8',
      changeType: 'positive',
      icon: <Users className="h-5 w-5" />,
    },
    {
      name: 'Correcciones Completadas',
      value: '89',
      change: '+12',
      changeType: 'positive',
      icon: <CheckCircle className="h-5 w-5" />,
    },
    {
      name: 'Tiempo Promedio',
      value: '2.3 min',
      change: '-0.5',
      changeType: 'positive',
      icon: <Clock className="h-5 w-5" />,
    },
  ];

  const handleCheckStuckAssignments = async () => {
    try {
      const response = await apiService.checkStuckAssignments();
      if (response.stuck_assignments_fixed > 0) {
        alert(`Se marcaron ${response.stuck_assignments_fixed} asignaciones como error por timeout`);
      } else {
        alert('No se encontraron asignaciones bloqueadas');
      }
    } catch (error) {
      console.error('Error verificando asignaciones bloqueadas:', error);
      alert('Error al verificar asignaciones bloqueadas');
    }
  };

  if (!user) {
    return (
      <>
        <DebugAuth />
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Cargando...
            </h1>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <DebugAuth />
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              ¡Bienvenido, {user.first_name}!
            </h1>
            <p className="mt-2 text-gray-600">
              {getRoleDescription(user.role)}
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat) => (
              <div key={stat.name} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-indigo-100 rounded-md flex items-center justify-center">
                      {stat.icon}
                    </div>
                  </div>
                  <div className="ml-4 flex-1">
                    <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                    <div className="flex items-baseline">
                      <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                      <p className={`ml-2 text-sm font-medium ${
                        stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stat.change}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Acciones Rápidas
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {quickActions
                .filter(action => hasAnyRole(action.roles))
                .map((action) => (
                  <button
                    key={action.title}
                    onClick={() => handleQuickAction(action.link)}
                    className="bg-white rounded-lg shadow p-6 text-left hover:shadow-md transition-shadow duration-200"
                  >
                    <div className="flex items-center mb-3">
                      <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center text-white`}>
                        {action.icon}
                      </div>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      {action.title}
                    </h3>
                    <p className="text-gray-600 text-sm">
                      {action.description}
                    </p>
                  </button>
                ))}
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Recent Activity */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Actividad Reciente
                  </h2>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    {recentActivity.map((activity) => (
                      <div key={activity.id} className="flex items-start">
                        <div className="flex-shrink-0">
                          <div className={`w-2 h-2 rounded-full mt-2 ${
                            activity.type === 'info' ? 'bg-blue-500' :
                            activity.type === 'success' ? 'bg-green-500' :
                            activity.type === 'warning' ? 'bg-yellow-500' :
                            'bg-red-500'
                          }`} />
                        </div>
                        <div className="ml-3">
                          <p className="text-sm font-medium text-gray-900">
                            {activity.title}
                          </p>
                          <p className="text-sm text-gray-600">
                            {activity.description}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            {activity.time}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Getting Started */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Comenzar
                  </h2>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                      <div className="bg-blue-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                        <Brain className="h-8 w-8 text-blue-600" />
                      </div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Crear Asignación
                      </h3>
                      <p className="text-gray-600 text-sm mb-4">
                        Sube un documento y deja que la IA genere soluciones y rúbricas
                      </p>
                      <button
                        onClick={() => handleQuickAction('/assignments/new')}
                        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Comenzar
                      </button>
                    </div>

                    <div className="text-center">
                      <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                        <FileText className="h-8 w-8 text-green-600" />
                      </div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Ver Asignaciones
                      </h3>
                      <p className="text-gray-600 text-sm mb-4">
                        Gestiona tus asignaciones existentes y revisa el progreso
                      </p>
                      <button
                        onClick={() => handleQuickAction('/assignments')}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        Ver Todas
                      </button>
                    </div>

                    <div className="text-center">
                      <div className="bg-purple-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                        <TrendingUp className="h-8 w-8 text-purple-600" />
                      </div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Ver Estadísticas
                      </h3>
                      <p className="text-gray-600 text-sm mb-4">
                        Analiza el rendimiento y obtén insights valiosos
                      </p>
                      <button
                        onClick={() => handleQuickAction('/statistics')}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        Ver Reportes
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Admin Tools */}
          {hasRole(UserRole.ADMIN) && (
            <div className="mt-8">
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Herramientas de Administración
                  </h2>
                </div>
                <div className="p-6">
                  <button
                    onClick={handleCheckStuckAssignments}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    <AlertCircle className="h-4 w-4 mr-2" />
                    Verificar Asignaciones Bloqueadas
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Dashboard;
