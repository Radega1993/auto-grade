import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Save, 
  Download, 
  CheckCircle, 
  AlertCircle, 
  Loader,
  Edit3,
  FileText,
  Brain,
  Target
} from 'lucide-react';
import { Assignment, Solution, RubricData, AssignmentStatus } from '../../types';
import { useAuthStore } from '../../stores/authStore';
import { apiService } from '../../services/api';
import SolutionEditor from './SolutionEditor';
import RubricEditor from './RubricEditor';

const AssignmentEditor: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [assignment, setAssignment] = useState<Assignment | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'solutions' | 'rubric'>('solutions');
  
  const { setError: setAuthError, clearError } = useAuthStore();

  useEffect(() => {
    if (id) {
      loadAssignment();
    }
  }, [id]);

  const loadAssignment = async () => {
    try {
      setLoading(true);
      clearError();
      
      const response = await apiService.getAssignment(id!);
      setAssignment(response.data);
      
      // Si está en procesamiento, recargar cada 5 segundos
      if (response.data.status === AssignmentStatus.PROCESSING) {
        setTimeout(loadAssignment, 5000);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al cargar la asignación';
      setError(errorMessage);
      setAuthError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSolutions = async (solutions: Solution[]) => {
    try {
      setSaving(true);
      await apiService.updateAssignmentSolutions(id!, solutions);
      
      setAssignment(prev => prev ? { ...prev, final_solutions: solutions } : null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al guardar soluciones';
      setError(errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const handleSaveRubric = async (rubric: RubricData) => {
    try {
      setSaving(true);
      await apiService.updateAssignmentRubric(id!, rubric);
      
      setAssignment(prev => prev ? { ...prev, final_rubric: rubric } : null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al guardar rúbrica';
      setError(errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const handleFinalize = async () => {
    try {
      setSaving(true);
      await apiService.finalizeAssignment(id!);
      
      setAssignment(prev => prev ? { ...prev, status: AssignmentStatus.FINALIZED } : null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al finalizar asignación';
      setError(errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await apiService.downloadAssignment(id!);
      // TODO: Implementar descarga real del PDF
      console.log('Descarga preparada:', response.data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Error al preparar descarga';
      setError(errorMessage);
    }
  };

  const getStatusInfo = (status: AssignmentStatus) => {
    switch (status) {
      case AssignmentStatus.UPLOADED:
        return { color: 'blue', text: 'Archivo subido', icon: FileText };
      case AssignmentStatus.PROCESSING:
        return { color: 'yellow', text: 'Procesando con IA', icon: Brain };
      case AssignmentStatus.READY_FOR_EDITING:
        return { color: 'green', text: 'Listo para editar', icon: Edit3 };
      case AssignmentStatus.FINALIZED:
        return { color: 'green', text: 'Finalizada', icon: CheckCircle };
      case AssignmentStatus.ERROR:
        return { color: 'red', text: 'Error', icon: AlertCircle };
      default:
        return { color: 'gray', text: 'Desconocido', icon: FileText };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="animate-spin h-8 w-8 text-indigo-600 mx-auto mb-4" />
          <p className="text-gray-600">Cargando asignación...</p>
        </div>
      </div>
    );
  }

  if (!assignment) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-8 w-8 text-red-600 mx-auto mb-4" />
          <p className="text-gray-600">Asignación no encontrada</p>
          <button
            onClick={() => navigate('/assignments')}
            className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Volver a asignaciones
          </button>
        </div>
      </div>
    );
  }

  const statusInfo = getStatusInfo(assignment.status);
  const StatusIcon = statusInfo.icon;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/assignments')}
                className="p-2 text-gray-400 hover:text-gray-600"
              >
                <ArrowLeft className="h-5 w-5" />
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{assignment.title}</h1>
                {assignment.description && (
                  <p className="text-gray-600 mt-1">{assignment.description}</p>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className={`flex items-center px-3 py-1 rounded-full text-sm font-medium bg-${statusInfo.color}-100 text-${statusInfo.color}-800`}>
                <StatusIcon className="h-4 w-4 mr-2" />
                {statusInfo.text}
              </div>
              
              {assignment.status === AssignmentStatus.FINALIZED && (
                <button
                  onClick={handleDownload}
                  className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Descargar PDF
                </button>
              )}
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md flex items-center">
            <AlertCircle className="h-5 w-5 mr-2" />
            {error}
          </div>
        )}

        {/* Contenido extraído */}
        {assignment.extracted_content && (
          <div className="mb-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Contenido Extraído</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="font-medium text-gray-900">Ejercicios</h3>
                <p className="text-2xl font-bold text-indigo-600">
                  {assignment.extracted_content.exercises.length}
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="font-medium text-gray-900">Puntos Totales</h3>
                <p className="text-2xl font-bold text-indigo-600">
                  {assignment.extracted_content.total_points}
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="font-medium text-gray-900">Archivo</h3>
                <p className="text-sm text-gray-600 truncate">
                  {assignment.extracted_content.source_file.split('/').pop()}
                </p>
              </div>
            </div>
            
            {assignment.extracted_content.instructions && (
              <div className="mb-4">
                <h3 className="font-medium text-gray-900 mb-2">Instrucciones</h3>
                <p className="text-gray-700 bg-gray-50 p-3 rounded-md">
                  {assignment.extracted_content.instructions}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Tabs */}
        {assignment.status === AssignmentStatus.READY_FOR_EDITING || assignment.status === AssignmentStatus.FINALIZED ? (
          <div className="bg-white rounded-lg shadow">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8 px-6">
                <button
                  onClick={() => setActiveTab('solutions')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'solutions'
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Soluciones ({assignment.final_solutions?.length || 0})
                </button>
                <button
                  onClick={() => setActiveTab('rubric')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'rubric'
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Rúbrica
                </button>
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'solutions' && (
                <SolutionEditor
                  solutions={assignment.final_solutions || []}
                  exercises={assignment.extracted_content?.exercises || []}
                  onSave={handleSaveSolutions}
                  saving={saving}
                />
              )}

              {activeTab === 'rubric' && (
                <RubricEditor
                  rubric={assignment.final_rubric}
                  onSave={handleSaveRubric}
                  saving={saving}
                />
              )}
            </div>

            {/* Botones de acción */}
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-between">
              <button
                onClick={() => navigate('/assignments')}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Volver
              </button>
              
              {assignment.status === AssignmentStatus.READY_FOR_EDITING && (
                <button
                  onClick={handleFinalize}
                  disabled={saving}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center"
                >
                  {saving ? (
                    <Loader className="animate-spin h-4 w-4 mr-2" />
                  ) : (
                    <CheckCircle className="h-4 w-4 mr-2" />
                  )}
                  Finalizar Asignación
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100 mb-4">
              <StatusIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {assignment.status === AssignmentStatus.PROCESSING ? 'Procesando con IA...' : 'Esperando procesamiento'}
            </h3>
            <p className="text-gray-600 mb-4">
              {assignment.status === AssignmentStatus.PROCESSING 
                ? 'La IA está analizando tu asignación y generando soluciones y rúbrica. Esto puede tomar unos minutos.'
                : 'Tu asignación está en cola para ser procesada por la IA.'
              }
            </p>
            {assignment.status === AssignmentStatus.PROCESSING && (
              <div className="flex justify-center">
                <Loader className="animate-spin h-6 w-6 text-indigo-600" />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AssignmentEditor;
