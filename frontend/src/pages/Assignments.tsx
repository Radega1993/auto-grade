import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Plus, 
  FileText, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Edit3,
  Download,
  Brain,
  Loader,
  Trash2,
  FileDown
} from 'lucide-react';
import { Assignment, AssignmentStatus } from '../types';
import { useAuthStore } from '../stores/authStore';
import { apiService } from '../services/api';

const Assignments: React.FC = () => {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);
  
  const { setError: setAuthError, clearError } = useAuthStore();

  useEffect(() => {
    loadAssignments();
  }, []);

  const loadAssignments = async () => {
    try {
      setLoading(true);
      clearError();
      
      const response = await apiService.getAssignments();
      setAssignments(response.data || []);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al cargar rúbricas y soluciones';
      setError(errorMessage);
      setAuthError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const getStatusInfo = (status: AssignmentStatus) => {
    switch (status) {
      case AssignmentStatus.UPLOADED:
        return { 
          color: 'blue', 
          text: 'Subida', 
          bgColor: 'bg-blue-100', 
          textColor: 'text-blue-800',
          icon: FileText
        };
      case AssignmentStatus.PROCESSING:
        return { 
          color: 'yellow', 
          text: 'Procesando', 
          bgColor: 'bg-yellow-100', 
          textColor: 'text-yellow-800',
          icon: Brain
        };
      case AssignmentStatus.AI_ANALYZED:
        return { 
          color: 'purple', 
          text: 'Analizada', 
          bgColor: 'bg-purple-100', 
          textColor: 'text-purple-800',
          icon: Brain
        };
      case AssignmentStatus.READY_FOR_EDITING:
        return { 
          color: 'green', 
          text: 'Lista para editar', 
          bgColor: 'bg-green-100', 
          textColor: 'text-green-800',
          icon: Edit3
        };
      case AssignmentStatus.FINALIZED:
        return { 
          color: 'green', 
          text: 'Finalizada', 
          bgColor: 'bg-green-100', 
          textColor: 'text-green-800',
          icon: CheckCircle
        };
      case AssignmentStatus.ERROR:
        return { 
          color: 'red', 
          text: 'Error', 
          bgColor: 'bg-red-100', 
          textColor: 'text-red-800',
          icon: AlertCircle
        };
      default:
        return { 
          color: 'gray', 
          text: 'Desconocido', 
          bgColor: 'bg-gray-100', 
          textColor: 'text-gray-800',
          icon: FileText
        };
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDeleteAssignment = async (assignmentId: string) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar esta asignación? Esta acción no se puede deshacer.')) {
      return;
    }

    try {
      setDeletingId(assignmentId);
      await apiService.deleteAssignment(assignmentId);
      setAssignments(assignments.filter(a => a.id !== assignmentId));
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al eliminar la asignación';
      setError(errorMessage);
    } finally {
      setDeletingId(null);
    }
  };

  const handleDownloadRubric = async (assignmentId: string, title: string) => {
    try {
      setDownloadingId(`rubric-${assignmentId}`);
      const blob = await apiService.downloadRubric(assignmentId);
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `rubrica_${title.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al descargar la rúbrica';
      setError(errorMessage);
    } finally {
      setDownloadingId(null);
    }
  };

  const handleDownloadSolutions = async (assignmentId: string, title: string) => {
    try {
      setDownloadingId(`solutions-${assignmentId}`);
      const blob = await apiService.downloadSolutions(assignmentId);
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `soluciones_${title.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al descargar las soluciones';
      setError(errorMessage);
    } finally {
      setDownloadingId(null);
    }
  };

  const getActionButtons = (assignment: Assignment) => {
    const statusInfo = getStatusInfo(assignment.status);
    
    switch (assignment.status) {
      case AssignmentStatus.READY_FOR_EDITING:
      case AssignmentStatus.FINALIZED:
        return (
          <div className="flex flex-wrap gap-2">
            <Link
              to={`/assignments/${assignment.id}/edit`}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200"
            >
              <Edit3 className="h-4 w-4 mr-1" />
              Editar
            </Link>
            
            {assignment.final_rubric && (
              <button
                onClick={() => handleDownloadRubric(assignment.id, assignment.title)}
                disabled={downloadingId === `rubric-${assignment.id}`}
                className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 disabled:opacity-50"
              >
                {downloadingId === `rubric-${assignment.id}` ? (
                  <Loader className="h-4 w-4 mr-1 animate-spin" />
                ) : (
                  <FileDown className="h-4 w-4 mr-1" />
                )}
                Rúbrica PDF
              </button>
            )}
            
            {assignment.final_solutions && (
              <button
                onClick={() => handleDownloadSolutions(assignment.id, assignment.title)}
                disabled={downloadingId === `solutions-${assignment.id}`}
                className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 disabled:opacity-50"
              >
                {downloadingId === `solutions-${assignment.id}` ? (
                  <Loader className="h-4 w-4 mr-1 animate-spin" />
                ) : (
                  <Download className="h-4 w-4 mr-1" />
                )}
                Soluciones PDF
              </button>
            )}
            
            <button
              onClick={() => handleDeleteAssignment(assignment.id)}
              disabled={deletingId === assignment.id}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 disabled:opacity-50"
            >
              {deletingId === assignment.id ? (
                <Loader className="h-4 w-4 mr-1 animate-spin" />
              ) : (
                <Trash2 className="h-4 w-4 mr-1" />
              )}
              Eliminar
            </button>
          </div>
        );
      default:
        return (
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-500">
              {assignment.status === AssignmentStatus.PROCESSING ? 'Procesando...' : 'Esperando...'}
            </span>
            <button
              onClick={() => handleDeleteAssignment(assignment.id)}
              disabled={deletingId === assignment.id}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 disabled:opacity-50"
            >
              {deletingId === assignment.id ? (
                <Loader className="h-4 w-4 mr-1 animate-spin" />
              ) : (
                <Trash2 className="h-4 w-4 mr-1" />
              )}
              Eliminar
            </button>
          </div>
        );
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <Loader className="animate-spin h-8 w-8 mx-auto mb-4 text-indigo-600" />
            <p className="text-gray-600">Cargando rúbricas y soluciones...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Mis Rúbricas y Soluciones</h1>
          <p className="text-gray-600 mt-2">
            Gestiona tus rúbricas y soluciones y sus correcciones automáticas
          </p>
        </div>
        <Link
          to="/assignments/new"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <Plus className="h-5 w-5 mr-2" />
          Nueva Asignación
        </Link>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md flex items-center">
          <AlertCircle className="h-5 w-5 mr-2" />
          {error}
        </div>
      )}

      {assignments.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
            <FileText className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No tienes asignaciones aún
          </h3>
          <p className="text-gray-600 mb-6">
            Comienza creando tu primera asignación para aprovechar la corrección automática con IA.
          </p>
          <Link
            to="/assignments/new"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            <Plus className="h-4 w-4 mr-2" />
            Crear Primera Asignación
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {assignments.map((assignment) => {
            const statusInfo = getStatusInfo(assignment.status);
            const StatusIcon = statusInfo.icon;

            return (
              <div key={assignment.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-medium text-gray-900">
                        {assignment.title}
                      </h3>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusInfo.bgColor} ${statusInfo.textColor}`}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {statusInfo.text}
                      </span>
                    </div>
                    
                    {assignment.description && (
                      <p className="text-gray-600 mb-3">{assignment.description}</p>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div className="flex items-center text-sm text-gray-500">
                        <Clock className="h-4 w-4 mr-2" />
                        Creada: {formatDate(assignment.created_at)}
                      </div>
                      
                      {assignment.extracted_content && (
                        <>
                          <div className="flex items-center text-sm text-gray-500">
                            <FileText className="h-4 w-4 mr-2" />
                            {assignment.extracted_content.exercises.length} ejercicios
                          </div>
                          <div className="flex items-center text-sm text-gray-500">
                            <CheckCircle className="h-4 w-4 mr-2" />
                            {assignment.extracted_content.total_points} puntos
                          </div>
                        </>
                      )}
                    </div>

                    {assignment.status === AssignmentStatus.PROCESSING && (
                      <div className="flex items-center text-sm text-yellow-600 mb-3">
                        <Loader className="animate-spin h-4 w-4 mr-2" />
                        La IA está analizando tu asignación...
                      </div>
                    )}

                    {assignment.status === AssignmentStatus.ERROR && (
                      <div className="text-sm text-red-600 mb-3">
                        Hubo un error procesando la asignación. Intenta subirla nuevamente.
                      </div>
                    )}
                  </div>

                  <div className="ml-6">
                    {getActionButtons(assignment)}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Estadísticas */}
      {assignments.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FileText className="h-8 w-8 text-indigo-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total</p>
                <p className="text-2xl font-semibold text-gray-900">{assignments.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Finalizadas</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {assignments.filter(a => a.status === AssignmentStatus.FINALIZED).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Edit3 className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">En Edición</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {assignments.filter(a => a.status === AssignmentStatus.READY_FOR_EDITING).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Brain className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Procesando</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {assignments.filter(a => a.status === AssignmentStatus.PROCESSING).length}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Assignments;
