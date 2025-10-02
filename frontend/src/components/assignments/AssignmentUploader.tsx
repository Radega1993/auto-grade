import React, { useState, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, AlertCircle, CheckCircle, Loader, X } from 'lucide-react';
import { AssignmentUploadForm } from '../../types';
import { useAuthStore } from '../../stores/authStore';
import { apiService } from '../../services/api';

const AssignmentUploader: React.FC = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { setError: setAuthError, clearError } = useAuthStore();
  
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<AssignmentUploadForm>();

  const handleFileSelect = (file: File) => {
    // Validar tipo de archivo
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
    if (!allowedTypes.includes(file.type)) {
      setError('Solo se permiten archivos PDF y Word');
      return;
    }

    // Validar tamaño (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      setError('El archivo no puede ser mayor a 10MB');
      return;
    }

    setSelectedFile(file);
    setValue('file', file as any);
    setError(null);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    setValue('file', undefined as any);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const onSubmit = async (data: AssignmentUploadForm) => {
    if (!selectedFile) {
      setError('Por favor selecciona un archivo');
      return;
    }

    setIsUploading(true);
    setError(null);
    setSuccess(null);
    clearError();

    try {
      const formData = new FormData();
      formData.append('title', data.title);
      formData.append('description', data.description);
      formData.append('file', selectedFile);

      setUploadProgress(25);

      const response = await apiService.uploadAssignment(formData);
      
      setUploadProgress(100);
      setSuccess('Asignación subida exitosamente. El análisis con IA está en proceso.');
      
      // Redirigir a la página de edición después de un breve delay
      setTimeout(() => {
        // El backend devuelve { message: '...', data: { id: '...', ... } }
        if (response.data && 'id' in response.data) {
          navigate(`/assignments/${response.data.id}/edit`);
        } else {
          navigate('/assignments');
        }
      }, 2000);

    } catch (err: any) {
      console.error('Error completo:', err);
      console.error('Error response:', err.response);
      
      const errorMessage = err.response?.data?.error || err.message || 'Error al subir la asignación';
      setError(errorMessage);
      setAuthError(errorMessage);
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const getFileIcon = (filename: string) => {
    const extension = filename.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return '📄';
      case 'docx':
      case 'doc':
        return '📝';
      default:
        return '📁';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
            <Upload className="h-6 w-6 text-indigo-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Subir Nueva Asignación
          </h2>
          <p className="text-gray-600">
            Sube un archivo PDF o Word para crear una nueva asignación con análisis automático de IA
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md flex items-center">
              <AlertCircle className="h-5 w-5 mr-2" />
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md flex items-center">
              <CheckCircle className="h-5 w-5 mr-2" />
              {success}
            </div>
          )}

          {/* Título */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Título de la Asignación *
            </label>
            <input
              {...register('title', {
                required: 'El título es requerido',
                minLength: {
                  value: 3,
                  message: 'El título debe tener al menos 3 caracteres',
                },
              })}
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Ej: Ejercicios de Matemáticas - Tema 3"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          {/* Descripción */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Descripción (Opcional)
            </label>
            <textarea
              {...register('description')}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Describe brevemente el contenido de la asignación..."
            />
          </div>

          {/* Archivo */}
          <div>
            <label htmlFor="file" className="block text-sm font-medium text-gray-700 mb-2">
              Archivo de la Asignación *
            </label>
            <div 
              className={`mt-1 flex justify-center px-6 pt-5 pb-6 border-2 ${
                isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300'
              } border-dashed rounded-md hover:border-gray-400 transition-colors`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
            >
              <div className="space-y-1 text-center">
                <FileText className="mx-auto h-12 w-12 text-gray-400" />
                <div className="flex text-sm text-gray-600">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500"
                  >
                    <span>Subir archivo</span>
                    <input
                      id="file-upload"
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf,.docx,.doc"
                      className="sr-only"
                      onChange={handleFileInputChange}
                    />
                  </label>
                  <p className="pl-1">o arrastra y suelta</p>
                </div>
                <p className="text-xs text-gray-500">
                  PDF, DOCX hasta 10MB
                </p>
              </div>
            </div>

            {/* Vista previa del archivo seleccionado */}
            {selectedFile && (
              <div className="mt-4 p-4 bg-gray-50 rounded-md flex items-center justify-between">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">{getFileIcon(selectedFile.name)}</span>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
                  </div>
                </div>
                <button 
                  type="button" 
                  onClick={removeFile} 
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            )}
          </div>

          {/* Barra de progreso */}
          {isUploading && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-gray-600">
                <span>Subiendo archivo...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          )}

          {/* Botones */}
          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => navigate('/assignments')}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isUploading || !selectedFile}
              className="flex-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isUploading ? (
                <>
                  <Loader className="animate-spin h-4 w-4 mr-2" />
                  Subiendo...
                </>
              ) : (
                'Subir Asignación'
              )}
            </button>
          </div>
        </form>

        {/* Información adicional */}
        <div className="mt-8 p-4 bg-blue-50 rounded-md">
          <h3 className="text-sm font-medium text-blue-800 mb-2">¿Qué sucede después?</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• El archivo se procesará para extraer ejercicios y enunciados</li>
            <li>• La IA analizará el contenido y generará soluciones y rúbrica</li>
            <li>• Podrás revisar y editar las soluciones y rúbrica generadas</li>
            <li>• Una vez finalizada, podrás usar la asignación para correcciones</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AssignmentUploader;
