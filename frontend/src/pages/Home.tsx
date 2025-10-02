import React from 'react';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  Brain, 
  FileText, 
  BarChart3, 
  Users, 
  Shield,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const Home: React.FC = () => {
  const features = [
    {
      icon: <Brain className="h-8 w-8 text-indigo-600" />,
      title: 'Corrección Automática con IA',
      description: 'Utiliza modelos avanzados de IA para corregir tareas de forma automática y precisa.',
    },
    {
      icon: <FileText className="h-8 w-8 text-indigo-600" />,
      title: 'Múltiples Formatos',
      description: 'Soporta PDF, DOCX, TXT y más formatos de archivo para máxima flexibilidad.',
    },
    {
      icon: <BarChart3 className="h-8 w-8 text-indigo-600" />,
      title: 'Análisis Detallado',
      description: 'Obtén estadísticas, comentarios detallados y áreas de mejora específicas.',
    },
    {
      icon: <Shield className="h-8 w-8 text-indigo-600" />,
      title: 'Detección de IA',
      description: 'Identifica contenido generado por inteligencia artificial para mantener la integridad académica.',
    },
  ];

  const benefits = [
    'Ahorra tiempo en corrección de tareas',
    'Proporciona retroalimentación consistente',
    'Detecta plagio y contenido generado por IA',
    'Genera reportes detallados automáticamente',
    'Sistema de roles y permisos avanzado',
    'Interfaz intuitiva y fácil de usar',
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              <span className="block">Corrección Automática</span>
              <span className="block text-indigo-600">con Inteligencia Artificial</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              AutoGrader revoluciona la educación con corrección automática de tareas, 
              análisis detallado y detección de contenido generado por IA.
            </p>
            <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
              <div className="rounded-md shadow">
                <Link
                  to="/login"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
                >
                  Iniciar Sesión
                </Link>
              </div>
              <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
                <Link
                  to="/register"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
                >
                  Crear Cuenta
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900">
              Características Principales
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Todo lo que necesitas para una corrección eficiente y precisa
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white mx-auto">
                  {feature.icon}
                </div>
                <h3 className="mt-6 text-lg font-medium text-gray-900">
                  {feature.title}
                </h3>
                <p className="mt-2 text-base text-gray-500">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
            <div>
              <h2 className="text-3xl font-extrabold text-gray-900">
                ¿Por qué elegir AutoGrader?
              </h2>
              <p className="mt-3 text-lg text-gray-500">
                Nuestra plataforma está diseñada para simplificar y mejorar el proceso 
                de corrección de tareas, proporcionando herramientas avanzadas para educadores.
              </p>
              <div className="mt-8">
                <div className="space-y-3">
                  {benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                      <span className="text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="mt-8 lg:mt-0">
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Comienza Ahora
                </h3>
                <p className="text-gray-600 mb-6">
                  Únete a miles de educadores que ya están usando AutoGrader 
                  para mejorar su proceso de evaluación.
                </p>
                <Link
                  to="/register"
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Crear Cuenta Gratis
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-indigo-700">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            <span className="block">¿Listo para comenzar?</span>
            <span className="block text-indigo-200">
              Únete a la revolución de la corrección automática.
            </span>
          </h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
            <div className="inline-flex rounded-md shadow">
              <Link
                to="/register"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
              >
                Comenzar Ahora
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
