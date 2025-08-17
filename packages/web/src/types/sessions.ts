/**
 * TypeScript interfaces for session management.
 */

export interface SessionUploadRequest {
  transcript_text: string;
  session_date: string; // ISO date string YYYY-MM-DD
  session_type?: string;
  participants?: string[];
  duration_minutes?: number;
  notes?: string;
}

export interface SessionUploadResponse {
  session_id: string;
  status: string;
  participants_identified: string[];
  clients_created: string[];
  clients_matched: string[];
  processing_status: string;
  next_steps: string;
}

export interface FileUploadMetadata {
  session_date: string;
  session_type?: string;
  notes?: string;
}

export interface UploadProgress {
  progress: number;
  stage: 'uploading' | 'processing' | 'completed' | 'error';
  message: string;
}

export interface SessionDetails {
  session: {
    id: string;
    session_date: string;
    session_type?: string;
    duration_minutes?: number;
    processing_status: string;
    participant_count: number;
    created_at: string;
  };
  participants: Array<{
    name: string;
    email?: string;
    engagement_level?: string;
    speaking_time_seconds?: number;
  }>;
}

export interface ErrorResponse {
  error: string;
  detail: string;
  code?: string;
}