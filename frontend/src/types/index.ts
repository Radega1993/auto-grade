// Tipos de usuario y autenticación
export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export enum UserRole {
  TEACHER = 'teacher',
  COORDINATOR = 'coordinator',
  ADMIN = 'admin'
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  message: string;
  user: User;
  tokens: AuthTokens;
}

export interface LoginRequest {
  email_or_username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  role?: UserRole;
}

// Tipos de asignaciones y análisis
export interface Assignment {
  id: string;
  title: string;
  description?: string;
  status: AssignmentStatus;
  teacher_id: string;
  extracted_content?: ExtractedContent;
  ai_analysis?: AIAnalysis;
  final_solutions?: Solution[];
  final_rubric?: RubricData;
  created_at: string;
  updated_at: string;
}

export enum AssignmentStatus {
  UPLOADED = 'uploaded',
  PROCESSING = 'processing',
  AI_ANALYZED = 'ai_analyzed',
  READY_FOR_EDITING = 'ready_for_editing',
  FINALIZED = 'finalized',
  ERROR = 'error'
}

export interface ExtractedContent {
  title: string;
  instructions: string;
  exercises: Exercise[];
  total_points: number;
  source_file: string;
  extraction_metadata: {
    extracted_at: string;
    content_length: number;
    exercise_count: number;
  };
}

export interface Exercise {
  number: number;
  statement: string;
  type: ExerciseType;
  points: number;
}

export enum ExerciseType {
  CALCULATION = 'calculation',
  OPEN_QUESTION = 'open_question',
  TRUE_FALSE = 'true_false',
  MULTIPLE_CHOICE = 'multiple_choice',
  FILL_BLANK = 'fill_blank',
  MIXED = 'mixed'
}

export interface AIAnalysis {
  solutions: Solution[];
  rubric: RubricData;
  ai_metadata: {
    model_used: string;
    analyzed_at: string;
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface Solution {
  exercise_number: number;
  expected_answer: string;
  solution_steps: string[];
  explanation: string;
  key_concepts: string[];
  common_mistakes: string[];
  points: number;
}

export interface RubricData {
  criteria: RubricCriterion[];
  performance_levels: PerformanceLevel[];
  total_weight: number;
  description: string;
}

export interface RubricCriterion {
  name: string;
  weight: number;
  description: string;
}

export interface PerformanceLevel {
  name: string;
  score: number;
  description: string;
}

// Tipos de correcciones
export interface Correction {
  id: string;
  assignment_id: string;
  student_name: string;
  student_file_path?: string;
  grade?: number;
  comments?: string;
  strengths?: string[];
  areas_of_improvement?: string[];
  ai_generated_percentage?: number;
  model_used?: string;
  processing_time?: number;
  created_at: string;
  updated_at: string;
}

// Tipos de rúbricas independientes
export interface Rubric {
  id: string;
  name: string;
  description?: string;
  criteria: Record<string, any>;
  created_by: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

// Tipos de API
export interface ApiResponse<T = any> {
  message?: string;
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

// Tipos para formularios
export interface AssignmentUploadForm {
  title: string;
  description: string;
  file: FileList;
}

export interface SolutionEditForm {
  exercise_number: number;
  expected_answer: string;
  solution_steps: string[];
  explanation: string;
  key_concepts: string[];
  common_mistakes: string[];
  points: number;
}

export interface RubricEditForm {
  criteria: RubricCriterion[];
  performance_levels: PerformanceLevel[];
  description: string;
}
