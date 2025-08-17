/**
 * API service for communicating with the backend.
 */

import {
  SessionUploadRequest,
  SessionUploadResponse,
  SessionDetails,
} from '@/types/sessions';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string, public code?: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      error: 'Unknown error',
      detail: response.statusText,
    }));
    
    throw new ApiError(
      response.status,
      errorData.detail || errorData.error || 'Request failed',
      errorData.code
    );
  }
  
  return response.json();
}

export const api = {
  /**
   * Upload session transcript as text
   */
  async uploadSessionText(
    data: SessionUploadRequest
  ): Promise<SessionUploadResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/sessions/upload`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    return handleResponse<SessionUploadResponse>(response);
  },

  /**
   * Upload session transcript as file
   */
  async uploadSessionFile(
    file: File,
    metadata: {
      session_date: string;
      session_type?: string;
      notes?: string;
    }
  ): Promise<SessionUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_date', metadata.session_date);
    
    if (metadata.session_type) {
      formData.append('session_type', metadata.session_type);
    }
    
    if (metadata.notes) {
      formData.append('notes', metadata.notes);
    }
    
    const response = await fetch(`${API_BASE_URL}/api/v1/sessions/upload-file`, {
      method: 'POST',
      body: formData,
    });
    
    return handleResponse<SessionUploadResponse>(response);
  },

  /**
   * Get session details by ID
   */
  async getSession(sessionId: string): Promise<SessionDetails> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/sessions/${sessionId}`
    );
    
    return handleResponse<SessionDetails>(response);
  },

  /**
   * Update session status
   */
  async updateSessionStatus(
    sessionId: string,
    status: string
  ): Promise<{ session_id: string; status: string; updated: boolean }> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/sessions/${sessionId}/status`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      }
    );
    
    return handleResponse(response);
  },
};

export { ApiError };