# API Integration

## Service Template

```typescript
// lib/api/sessions.ts
import { apiClient } from './client';
import { Session, CreateSessionDto, UpdateSessionDto } from '@/lib/types/models';
import { ApiResponse, PaginatedResponse } from '@/lib/types/api';

export const sessionsApi = {
  // Get all sessions with pagination
  async getSessions(params?: {
    page?: number;
    limit?: number;
    coachId?: string;
    dateFrom?: string;
    dateTo?: string;
  }): Promise<PaginatedResponse<Session>> {
    const response = await apiClient.get('/sessions', { params });
    return response.data;
  },

  // Get single session by ID
  async getSession(id: string): Promise<ApiResponse<Session>> {
    const response = await apiClient.get(`/sessions/${id}`);
    return response.data;
  },

  // Create new session with transcript upload
  async createSession(data: CreateSessionDto, transcript: File): Promise<ApiResponse<Session>> {
    const formData = new FormData();
    formData.append('transcript', transcript);
    formData.append('sessionType', data.sessionType);
    formData.append('sessionDate', data.sessionDate);
    
    const response = await apiClient.post('/sessions', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get session summaries
  async getSessionSummaries(sessionId: string): Promise<ApiResponse<Summary[]>> {
    const response = await apiClient.get(`/sessions/${sessionId}/summaries`);
    return response.data;
  },

  // Approve summary
  async approveSummary(sessionId: string, summaryId: string): Promise<ApiResponse<void>> {
    const response = await apiClient.post(`/summaries/${summaryId}/approve`);
    return response.data;
  },
};

// React Query hooks
export const useSession = (id: string) => {
  return useQuery({
    queryKey: ['session', id],
    queryFn: () => sessionsApi.getSession(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useSessions = (params?: Parameters<typeof sessionsApi.getSessions>[0]) => {
  return useQuery({
    queryKey: ['sessions', params],
    queryFn: () => sessionsApi.getSessions(params),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
};
```

## API Client Configuration

```typescript
// lib/api/client.ts
import axios, { AxiosError, AxiosInstance } from 'axios';
import { toast } from '@/components/ui/use-toast';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

// Create axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;
    
    // Handle 401 - Token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    // Handle other errors
    if (error.response?.status === 429) {
      toast({
        title: 'Rate Limited',
        description: 'Too many requests. Please wait a moment.',
        variant: 'destructive',
      });
    } else if (error.response?.status === 500) {
      toast({
        title: 'Server Error',
        description: 'Something went wrong. Please try again later.',
        variant: 'destructive',
      });
    } else if (error.message === 'Network Error') {
      toast({
        title: 'Network Error',
        description: 'Please check your internet connection.',
        variant: 'destructive',
      });
    }
    
    return Promise.reject(error);
  }
);

// WebSocket configuration
export const createWebSocketConnection = (sessionId: string) => {
  const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
  const token = localStorage.getItem('access_token');
  
  return io(WS_URL, {
    auth: {
      token,
    },
    query: {
      sessionId,
    },
    transports: ['websocket'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5,
  });
};
```
