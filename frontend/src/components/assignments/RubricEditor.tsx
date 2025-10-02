import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { Save, Plus, Trash2, Edit3, Check, X } from 'lucide-react';
import { Rubric } from '../../types';

interface RubricEditorProps {
  rubric: Rubric;
  onSave: (rubric: Rubric) => void;
  onCancel: () => void;
}

const RubricEditor: React.FC<RubricEditorProps> = ({ rubric, onSave, onCancel }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editingCriterion, setEditingCriterion] = useState<number | null>(null);
  const [editingLevel, setEditingLevel] = useState<{ criterionIndex: number; levelIndex: number } | null>(null);
  const [editedCriterion, setEditedCriterion] = useState<any>(null);
  const [editedLevel, setEditedLevel] = useState<any>(null);

  const { control, handleSubmit, watch, setValue, reset } = useForm({
    defaultValues: {
      criteria: rubric?.criteria || []
    }
  });

  const { fields, append, remove, update } = useFieldArray({
    control,
    name: 'criteria'
  });

  const watchedCriteria = watch('criteria');

  const onSubmit = (data: { criteria: any[] }) => {
    const updatedRubric: Rubric = {
      ...rubric,
      criteria: data.criteria,
      total_points: rubric?.total_points || 100
    };
    onSave(updatedRubric);
    setIsEditing(false);
  };

  const handleEditCriterion = (index: number) => {
    setEditingCriterion(index);
    setIsEditing(true);
    setEditedCriterion({ ...watchedCriteria[index] });
  };

  const handleSaveCriterion = (index: number) => {
    if (editedCriterion) {
      update(index, editedCriterion);
    }
    setEditingCriterion(null);
    setIsEditing(false);
    setEditedCriterion(null);
  };

  const handleCancelCriterion = () => {
    setEditingCriterion(null);
    setIsEditing(false);
    setEditedCriterion(null);
    reset({ criteria: rubric?.criteria || [] });
  };

  const handleEditLevel = (criterionIndex: number, levelIndex: number) => {
    setEditingLevel({ criterionIndex, levelIndex });
    setIsEditing(true);
    const criterion = watchedCriteria[criterionIndex];
    const level = criterion?.performance_levels?.[levelIndex];
    setEditedLevel({ ...level });
  };

  const handleSaveLevel = (criterionIndex: number, levelIndex: number) => {
    if (editedLevel) {
      const updatedCriteria = [...watchedCriteria];
      if (!updatedCriteria[criterionIndex].performance_levels) {
        updatedCriteria[criterionIndex].performance_levels = [];
      }
      updatedCriteria[criterionIndex].performance_levels[levelIndex] = editedLevel;
      setValue(`criteria.${criterionIndex}.performance_levels`, updatedCriteria[criterionIndex].performance_levels);
    }
    setEditingLevel(null);
    setIsEditing(false);
    setEditedLevel(null);
  };

  const handleCancelLevel = () => {
    setEditingLevel(null);
    setIsEditing(false);
    setEditedLevel(null);
    reset({ criteria: rubric?.criteria || [] });
  };

  const addNewCriterion = () => {
    const newCriterion = {
      name: '',
      description: '',
      weight: 0.1,
      performance_levels: [
        {
          name: 'Excelente',
          description: 'Desempeño excepcional',
          points: 10
        },
        {
          name: 'Bueno',
          description: 'Desempeño satisfactorio',
          points: 7
        },
        {
          name: 'Regular',
          description: 'Desempeño básico',
          points: 4
        },
        {
          name: 'Insuficiente',
          description: 'Desempeño por debajo del esperado',
          points: 1
        }
      ]
    };
    append(newCriterion);
  };

  const addPerformanceLevel = (criterionIndex: number) => {
    const criterion = watchedCriteria[criterionIndex];
    if (!criterion.performance_levels) {
      criterion.performance_levels = [];
    }
    const newLevel = {
      name: 'Nuevo Nivel',
      description: 'Descripción del nivel',
      points: 5
    };
    const updatedLevels = [...criterion.performance_levels, newLevel];
    setValue(`criteria.${criterionIndex}.performance_levels`, updatedLevels);
  };

  const removePerformanceLevel = (criterionIndex: number, levelIndex: number) => {
    const criterion = watchedCriteria[criterionIndex];
    if (criterion.performance_levels && criterion.performance_levels.length > 1) {
      const updatedLevels = criterion.performance_levels.filter((_, index) => index !== levelIndex);
      setValue(`criteria.${criterionIndex}.performance_levels`, updatedLevels);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">Rúbrica de Evaluación</h3>
        <div className="flex space-x-2">
          <button
            type="button"
            onClick={addNewCriterion}
            className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Plus className="h-4 w-4 mr-1" />
            Nuevo Criterio
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {fields.map((field, index) => {
          const criterion = watchedCriteria[index];
          const isCurrentlyEditing = editingCriterion === index;

          return (
            <div key={field.id} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <h4 className="text-md font-medium text-gray-900">
                  Criterio {index + 1}
                </h4>
                <div className="flex space-x-2">
                  {!isCurrentlyEditing ? (
                    <button
                      type="button"
                      onClick={() => handleEditCriterion(index)}
                      className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <Edit3 className="h-4 w-4 mr-1" />
                      Editar
                    </button>
                  ) : (
                    <div className="flex space-x-2">
                      <button
                        type="button"
                        onClick={() => handleSaveCriterion(index)}
                        className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                      >
                        <Check className="h-4 w-4 mr-1" />
                        Guardar
                      </button>
                      <button
                        type="button"
                        onClick={handleCancelCriterion}
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
                {/* Nombre del Criterio */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre del Criterio *
                  </label>
                  <input
                    {...control.register(`criteria.${index}.name`, {
                      required: 'El nombre del criterio es requerido'
                    })}
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Ej: Comprensión del problema"
                    disabled={!isCurrentlyEditing}
                  />
                </div>

                {/* Descripción del Criterio */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descripción
                  </label>
                  <textarea
                    {...control.register(`criteria.${index}.description`)}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Describe qué se evalúa en este criterio..."
                    disabled={!isCurrentlyEditing}
                  />
                </div>

                {/* Peso del Criterio */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Peso (0.0 - 1.0) *
                  </label>
                  <input
                    {...control.register(`criteria.${index}.weight`, {
                      required: 'El peso es requerido',
                      min: { value: 0, message: 'El peso debe ser mayor a 0' },
                      max: { value: 1, message: 'El peso debe ser menor a 1' }
                    })}
                    type="number"
                    step="0.1"
                    min="0"
                    max="1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="0.3"
                    disabled={!isCurrentlyEditing}
                  />
                </div>

                {/* Niveles de Desempeño */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Niveles de Desempeño
                    </label>
                    {isCurrentlyEditing && (
                      <button
                        type="button"
                        onClick={() => addPerformanceLevel(index)}
                        className="inline-flex items-center px-2 py-1 border border-transparent text-xs font-medium rounded-md text-indigo-600 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        <Plus className="h-3 w-3 mr-1" />
                        Agregar Nivel
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {(criterion?.performance_levels || []).map((level, levelIndex) => {
                      const isLevelEditing = editingLevel?.criterionIndex === index && editingLevel?.levelIndex === levelIndex;

                      return (
                        <div key={levelIndex} className="border border-gray-200 rounded-lg p-4">
                          {isLevelEditing ? (
                            <div className="space-y-3">
                              <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                  Nombre
                                </label>
                                <input
                                  type="text"
                                  value={editedLevel?.name || ''}
                                  onChange={(e) => setEditedLevel({
                                    ...editedLevel,
                                    name: e.target.value
                                  })}
                                  className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                                />
                              </div>
                              <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                  Descripción
                                </label>
                                <textarea
                                  value={editedLevel?.description || ''}
                                  onChange={(e) => setEditedLevel({
                                    ...editedLevel,
                                    description: e.target.value
                                  })}
                                  rows={2}
                                  className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                                />
                              </div>
                              <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                  Puntos
                                </label>
                                <input
                                  type="number"
                                  value={editedLevel?.points || 0}
                                  onChange={(e) => setEditedLevel({
                                    ...editedLevel,
                                    points: parseFloat(e.target.value) || 0
                                  })}
                                  className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                                />
                              </div>
                              <div className="flex space-x-2">
                                <button
                                  type="button"
                                  onClick={() => handleSaveLevel(index, levelIndex)}
                                  className="flex-1 px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700"
                                >
                                  <Check className="h-3 w-3 mx-auto" />
                                </button>
                                <button
                                  type="button"
                                  onClick={handleCancelLevel}
                                  className="flex-1 px-2 py-1 bg-gray-600 text-white text-xs rounded hover:bg-gray-700"
                                >
                                  <X className="h-3 w-3 mx-auto" />
                                </button>
                              </div>
                            </div>
                          ) : (
                            <div className="space-y-2">
                              <div className="flex justify-between items-start">
                                <h5 className="font-medium text-gray-900 text-sm">
                                  {level?.name || 'Sin nombre'}
                                </h5>
                                {isCurrentlyEditing && (
                                  <div className="flex space-x-1">
                                    <button
                                      type="button"
                                      onClick={() => handleEditLevel(index, levelIndex)}
                                      className="p-1 text-indigo-600 hover:text-indigo-800"
                                    >
                                      <Edit3 className="h-3 w-3" />
                                    </button>
                                    {(criterion?.performance_levels || []).length > 1 && (
                                      <button
                                        type="button"
                                        onClick={() => removePerformanceLevel(index, levelIndex)}
                                        className="p-1 text-red-600 hover:text-red-800"
                                      >
                                        <Trash2 className="h-3 w-3" />
                                      </button>
                                    )}
                                  </div>
                                )}
                              </div>
                              <p className="text-gray-600 text-xs">
                                {level?.description || 'Sin descripción'}
                              </p>
                              <div className="text-right">
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                  {level?.points || 0} pts
                                </span>
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          );
        })}

        {fields.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">No hay criterios definidos</p>
            <button
              type="button"
              onClick={addNewCriterion}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Plus className="h-4 w-4 mr-2" />
              Crear Primer Criterio
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
              Guardar Rúbrica
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default RubricEditor;
