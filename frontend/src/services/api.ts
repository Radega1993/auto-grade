import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { useAuthStore } from '../stores/authStore';

// Tipos para las respuestas de la API
export interface ApiResponse<T = any> {
  message: string;
  data?: T;
  error?: string;
}

// Tipos para autenticación
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
}

export interface AuthResponse {
  user: {
    id: string;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    role: string;
  };
  tokens: {
    access_token: string;
    refresh_token: string;
  };
}

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para añadir el token JWT a las peticiones
    this.api.interceptors.request.use(
      (config) => {
        const token = useAuthStore.getState().getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Interceptor para manejar respuestas de error
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expirado o inválido
          useAuthStore.getState().logout();
        }
        return Promise.reject(error);
      }
    );
  }

  // Métodos de autenticación
  async login(credentials: LoginRequest): Promise<ApiResponse<AuthResponse>> {
    const response: AxiosResponse<ApiResponse<AuthResponse>> = await this.api.post('/api/auth/login', credentials);
    return response.data;
  }

  async register(userData: RegisterRequest): Promise<ApiResponse<AuthResponse>> {
    const response: AxiosResponse<ApiResponse<AuthResponse>> = await this.api.post('/api/auth/register', userData);
    return response.data;
  }

  async getProfile(): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.get('/api/auth/profile');
    return response.data;
  }

  // Métodos de asignaciones
  async getAssignments(): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.get('/api/assignments');
    return response.data;
  }

  async getAssignment(assignmentId: string): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.get(`/api/assignments/${assignmentId}`);
    return response.data;
  }

  async uploadAssignment(formData: FormData): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.post('/api/assignments/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async updateAssignment(assignmentId: string, data: any): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.put(`/api/assignments/${assignmentId}`, data);
    return response.data;
  }

  async finalizeAssignment(assignmentId: string): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.post(`/api/assignments/${assignmentId}/finalize`);
    return response.data;
  }

  async deleteAssignment(assignmentId: string): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.delete(`/api/assignments/${assignmentId}/delete`);
    return response.data;
  }

  async downloadRubric(assignmentId: string): Promise<Blob> {
    const response: AxiosResponse<Blob> = await this.api.get(`/api/assignments/${assignmentId}/download-rubric`, {
      responseType: 'blob'
    });
    return response.data;
  }

  async downloadSolutions(assignmentId: string): Promise<Blob> {
    const response: AxiosResponse<Blob> = await this.api.get(`/api/assignments/${assignmentId}/download-solutions`, {
      responseType: 'blob'
    });
    return response.data;
  }

  async checkStuckAssignments(): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.api.post('/api/assignments/check-stuck');
    return response.data;
  }
}

export const apiService = new ApiService();
