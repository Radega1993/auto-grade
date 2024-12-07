import React, { useState } from 'react';
import axios from 'axios';

interface CorrectionResult {
    grade: number;
    comments: string;
    strengths: string[];
    areas_of_improvement: string[];
}

const AssignmentUploader: React.FC = () => {
    const [keyFile, setKeyFile] = useState < File | null > (null);
    const [studentFiles, setStudentFiles] = useState < File[] > ([]);
    const [results, setResults] = useState < CorrectionResult[] > ([]);
    const [error, setError] = useState < string | null > (null);

    const handleKeyFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) setKeyFile(file);
    };

    const handleStudentFilesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files) setStudentFiles(Array.from(files));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!keyFile || studentFiles.length === 0) {
            setError('Por favor, sube un archivo de criterios y al menos una tarea de estudiante');
            return;
        }

        const formData = new FormData();
        formData.append('key_file', keyFile);
        studentFiles.forEach(file => {
            formData.append('student_files', file);
        });

        try {
            const response = await axios.post('http://localhost:5000/api/assignments/correct', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setResults(response.data.results);
            setError(null);
        } catch (err) {
            setError('Error al corregir tareas. Por favor, inténtalo de nuevo.');
            console.error(err);
        }
    };

    return (
        <div className="max-w-md mx-auto p-4">
            <h2 className="text-2xl mb-4">Corrector Automático de Tareas</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block mb-2">Archivo de Criterios</label>
                    <input
                        type="file"
                        accept=".json"
                        onChange={handleKeyFileChange}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block mb-2">Tareas de Estudiantes</label>
                    <input
                        type="file"
                        multiple
                        onChange={handleStudentFilesChange}
                        className="w-full p-2 border rounded"
                    />
                </div>

                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                >
                    Corregir Tareas
                </button>
            </form>

            {error && (
                <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">
                    {error}
                </div>
            )}

            {results.length > 0 && (
                <div className="mt-4">
                    <h3 className="text-xl mb-2">Resultados de Corrección</h3>
                    {results.map((result, index) => (
                        <div key={index} className="mb-4 p-3 border rounded">
                            <p>Nota: <span className="font-bold">{result.grade}/10</span></p>
                            <p className="mt-2">{result.comments}</p>

                            {result.strengths.length > 0 && (
                                <div className="mt-2">
                                    <strong>Puntos Fuertes:</strong>
                                    <ul className="list-disc list-inside">
                                        {result.strengths.map((strength, idx) => (
                                            <li key={idx}>{strength}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {result.areas_of_improvement.length > 0 && (
                                <div className="mt-2">
                                    <strong>Áreas de Mejora:</strong>
                                    <ul className="list-disc list-inside">
                                        {result.areas_of_improvement.map((area, idx) => (
                                            <li key={idx}>{area}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default AssignmentUploader;