import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { Save, Plus, Trash2, Edit3, Check, X } from 'lucide-react';
import { Solution } from '../../types';

interface SolutionEditorProps {
  solutions: Solution[];
  onSave: (solutions: Solution[]) => void;
  onCancel: () => void;
}

const SolutionEditor: React.FC<SolutionEditorProps> = ({ solutions, onSave, onCancel }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);

  const { control, handleSubmit, watch, setValue, reset } = useForm({
    defaultValues: {
      solutions: solutions || []
    }
  });

  const { fields, append, remove, update } = useFieldArray({
    control,
    name: 'solutions'
  });

  const watchedSolutions = watch('solutions');

  const onSubmit = (data: { solutions: Solution[] }) => {
    onSave(data.solutions);
    setIsEditing(false);
  };

  const handleEdit = (index: number) => {
    setEditingIndex(index);
    setIsEditing(true);
  };

  const handleSaveEdit = (index: number) => {
    setEditingIndex(null);
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditingIndex(null);
    setIsEditing(false);
    reset({ solutions: solutions || [] });
  };

  const addNewSolution = () => {
    const newSolution: Solution = {
      exercise_number: fields.length + 1,
      expected_answer: '',
      solution_steps: [''],
      explanation: '',
      key_concepts: []
    };
    append(newSolution);
  };

  const addSolutionStep = (solutionIndex: number) => {
    const currentSteps = watchedSolutions[solutionIndex]?.solution_steps || [];
    const newSteps = [...currentSteps, ''];
    setValue(`solutions.${solutionIndex}.solution_steps`, newSteps);
  };

  const removeSolutionStep = (solutionIndex: number, stepIndex: number) => {
    const currentSteps = watchedSolutions[solutionIndex]?.solution_steps || [];
    const newSteps = currentSteps.filter((_, index) => index !== stepIndex);
    setValue(`solutions.${solutionIndex}.solution_steps`, newSteps);
  };

  const updateSolutionStep = (solutionIndex: number, stepIndex: number, value: string) => {
    const currentSteps = watchedSolutions[solutionIndex]?.solution_steps || [];
    const newSteps = [...currentSteps];
    newSteps[stepIndex] = value;
    setValue(`solutions.${solutionIndex}.solution_steps`, newSteps);
  };

  const addKeyConcept = (solutionIndex: number) => {
    const currentConcepts = watchedSolutions[solutionIndex]?.key_concepts || [];
    const newConcepts = [...currentConcepts, ''];
    setValue(`solutions.${solutionIndex}.key_concepts`, newConcepts);
  };

  const removeKeyConcept = (solutionIndex: number, conceptIndex: number) => {
    const currentConcepts = watchedSolutions[solutionIndex]?.key_concepts || [];
    const newConcepts = currentConcepts.filter((_, index) => index !== conceptIndex);
    setValue(`solutions.${solutionIndex}.key_concepts`, newConcepts);
  };

  const updateKeyConcept = (solutionIndex: number, conceptIndex: number, value: string) => {
    const currentConcepts = watchedSolutions[solutionIndex]?.key_concepts || [];
    const newConcepts = [...currentConcepts];
    newConcepts[conceptIndex] = value;
    setValue(`solutions.${solutionIndex}.key_concepts`, newConcepts);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">Soluciones de los Ejercicios</h3>
        <div className="flex space-x-2">
          <button
            type="button"
            onClick={addNewSolution}
            className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Plus className="h-4 w-4 mr-1" />
            Nueva Solución
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {fields.map((field, index) => {
          const solution = watchedSolutions[index];
          const isCurrentlyEditing = editingIndex === index;

          return (
            <div key={field.id} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <h4 className="text-md font-medium text-gray-900">
                  Ejercicio {solution?.exercise_number || index + 1}
                </h4>
                <div className="flex space-x-2">
                  {!isCurrentlyEditing ? (
                    <button
                      type="button"
                      onClick={() => handleEdit(index)}
                      className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <Edit3 className="h-4 w-4 mr-1" />
                      Editar
                    </button>
                  ) : (
                    <div className="flex space-x-2">
                      <button
                        type="button"
                        onClick={() => handleSaveEdit(index)}
                        className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                      >
                        <Check className="h-4 w-4 mr-1" />
                        Guardar
                      </button>
                      <button
                        type="button"
                        onClick={handleCancelEdit}
                        className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        <X className="h-4 w-4 mr-1" />
                        Cancelar
                      </button>
                    </div>
                  )}
                  <button
                    type="button"
                    onClick={() => remove(index)}
                    className="inline-flex items-center px-3 py-1 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    <Trash2 className="h-4 w-4 mr-1" />
                    Eliminar
                  </button>
                </div>
              </div>

              <div className="space-y-4">
                {/* Respuesta Esperada */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Respuesta Esperada *
                  </label>
                  <textarea
                    {...control.register(`solutions.${index}.expected_answer`, {
                      required: 'La respuesta esperada es requerida'
                    })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Escribe la respuesta esperada para este ejercicio..."
                    disabled={!isCurrentlyEditing}
                  />
                </div>

                {/* Pasos de Solución */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Pasos de Solución
                    </label>
                    {isCurrentlyEditing && (
                      <button
                        type="button"
                        onClick={() => addSolutionStep(index)}
                        className="inline-flex items-center px-2 py-1 border border-transparent text-xs font-medium rounded-md text-indigo-600 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        <Plus className="h-3 w-3 mr-1" />
                        Agregar Paso
                      </button>
                    )}
                  </div>
                  <div className="space-y-2">
                    {(solution?.solution_steps || []).map((step, stepIndex) => (
                      <div key={stepIndex} className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-500 w-8">
                          {stepIndex + 1}.
                        </span>
                        <input
                          type="text"
                          value={step || ''}
                          onChange={(e) => updateSolutionStep(index, stepIndex, e.target.value)}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                          placeholder={`Paso ${stepIndex + 1} de la solución...`}
                          disabled={!isCurrentlyEditing}
                        />
                        {isCurrentlyEditing && (solution?.solution_steps || []).length > 1 && (
                          <button
                            type="button"
                            onClick={() => removeSolutionStep(index, stepIndex)}
                            className="p-1 text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Explicación */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Explicación
                  </label>
                  <textarea
                    {...control.register(`solutions.${index}.explanation`)}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Explica el razonamiento detrás de la solución..."
                    disabled={!isCurrentlyEditing}
                  />
                </div>

                {/* Conceptos Clave */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Conceptos Clave
                    </label>
                    {isCurrentlyEditing && (
                      <button
                        type="button"
                        onClick={() => addKeyConcept(index)}
                        className="inline-flex items-center px-2 py-1 border border-transparent text-xs font-medium rounded-md text-indigo-600 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        <Plus className="h-3 w-3 mr-1" />
                        Agregar Concepto
                      </button>
                    )}
                  </div>
                  <div className="space-y-2">
                    {(solution?.key_concepts || []).map((concept, conceptIndex) => (
                      <div key={conceptIndex} className="flex items-center space-x-2">
                        <input
                          type="text"
                          value={concept || ''}
                          onChange={(e) => updateKeyConcept(index, conceptIndex, e.target.value)}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                          placeholder={`Concepto clave ${conceptIndex + 1}...`}
                          disabled={!isCurrentlyEditing}
                        />
                        {isCurrentlyEditing && (
                          <button
                            type="button"
                            onClick={() => removeKeyConcept(index, conceptIndex)}
                            className="p-1 text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          );
        })}

        {fields.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">No hay soluciones definidas</p>
            <button
              type="button"
              onClick={addNewSolution}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Plus className="h-4 w-4 mr-2" />
              Crear Primera Solución
            </button>
          </div>
        )}

        {fields.length > 0 && (
          <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Save className="h-4 w-4 mr-2" />
              Guardar Todas las Soluciones
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default SolutionEditor;
