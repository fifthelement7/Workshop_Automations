'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Upload as UploadIcon, FileText, Type } from 'lucide-react';

import FileUploader from '@/components/upload/FileUploader';
import SessionForm, { SessionFormData } from '@/components/upload/SessionForm';
import UploadProgress from '@/components/upload/UploadProgress';
import { api, ApiError } from '@/services/api';
import { UploadProgress as UploadProgressType, SessionUploadResponse } from '@/types/sessions';

type UploadMode = 'file' | 'text';

const UploadPage: React.FC = () => {
  const router = useRouter();
  
  // UI State
  const [uploadMode, setUploadMode] = useState<UploadMode>('file');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [transcriptText, setTranscriptText] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<UploadProgressType | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [sessionFormRef, setSessionFormRef] = useState<HTMLFormElement | null>(null);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError(null);
  };

  const handleFileRemove = () => {
    setSelectedFile(null);
  };

  const handleSessionFormSubmit = async (formData: SessionFormData) => {
    if (isUploading) return;

    setError(null);
    setIsUploading(true);

    try {
      // Validate upload requirements
      if (uploadMode === 'file' && !selectedFile) {
        throw new Error('Please select a file to upload');
      }
      
      if (uploadMode === 'text' && !transcriptText.trim()) {
        throw new Error('Please enter transcript text');
      }

      if (uploadMode === 'text' && transcriptText.trim().length < 100) {
        throw new Error('Transcript text must be at least 100 characters');
      }

      // Set initial progress
      setUploadProgress({
        progress: 10,
        stage: 'uploading',
        message: 'Starting upload...',
      });

      let response: SessionUploadResponse;

      if (uploadMode === 'file' && selectedFile) {
        // File upload
        setUploadProgress({
          progress: 30,
          stage: 'uploading',
          message: 'Uploading file...',
        });

        response = await api.uploadSessionFile(selectedFile, {
          session_date: formData.session_date,
          session_type: formData.session_type || undefined,
          notes: formData.notes || undefined,
        });
      } else {
        // Text upload
        setUploadProgress({
          progress: 30,
          stage: 'uploading',
          message: 'Uploading transcript...',
        });

        // Parse participants if provided
        const participants = formData.participants
          ? formData.participants.split(',').map(p => p.trim()).filter(p => p)
          : undefined;

        response = await api.uploadSessionText({
          transcript_text: transcriptText,
          session_date: formData.session_date,
          session_type: formData.session_type || undefined,
          participants,
          duration_minutes: formData.duration_minutes,
          notes: formData.notes || undefined,
        });
      }

      // Processing stage
      setUploadProgress({
        progress: 70,
        stage: 'processing',
        message: 'Processing transcript and extracting participants...',
      });

      // Simulate processing time for better UX
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Completion
      setUploadProgress({
        progress: 100,
        stage: 'completed',
        message: 'Upload completed successfully!',
      });

      // Redirect to success page after a brief delay
      setTimeout(() => {
        router.push(`/upload/success?sessionId=${response.session_id}`);
      }, 2000);

    } catch (err) {
      console.error('Upload error:', err);
      
      let errorMessage = 'An unexpected error occurred';
      
      if (err instanceof ApiError) {
        errorMessage = err.message;
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }

      setError(errorMessage);
      setUploadProgress({
        progress: 0,
        stage: 'error',
        message: 'Upload failed',
      });
    } finally {
      setIsUploading(false);
    }
  };

  const canSubmit = () => {
    if (isUploading) return false;
    
    if (uploadMode === 'file') {
      return selectedFile !== null;
    } else {
      return transcriptText.trim().length >= 100;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Upload Session Transcript
          </h1>
          <p className="text-lg text-gray-600">
            Upload your coaching session transcript for AI analysis and summary generation
          </p>
        </div>

        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          {/* Upload Mode Selector */}
          <div className="border-b border-gray-200">
            <nav className="flex">
              <button
                type="button"
                onClick={() => setUploadMode('file')}
                className={`flex-1 py-4 px-6 text-center font-medium text-sm ${
                  uploadMode === 'file'
                    ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <UploadIcon className="w-5 h-5 mx-auto mb-1" />
                Upload File
              </button>
              <button
                type="button"
                onClick={() => setUploadMode('text')}
                className={`flex-1 py-4 px-6 text-center font-medium text-sm ${
                  uploadMode === 'text'
                    ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Type className="w-5 h-5 mx-auto mb-1" />
                Paste Text
              </button>
            </nav>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left Column - Upload Content */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {uploadMode === 'file' ? 'Select Transcript File' : 'Enter Transcript Text'}
                </h3>

                {uploadMode === 'file' ? (
                  <FileUploader
                    onFileSelect={handleFileSelect}
                    onFileRemove={handleFileRemove}
                    selectedFile={selectedFile}
                    disabled={isUploading}
                  />
                ) : (
                  <div>
                    <textarea
                      value={transcriptText}
                      onChange={(e) => setTranscriptText(e.target.value)}
                      disabled={isUploading}
                      placeholder="Paste your session transcript here...

Example format:
Coach: Welcome to today's session. How are you feeling?
Client: I'm doing well, thank you. I wanted to discuss..."
                      className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 resize-vertical"
                    />
                    <div className="mt-2 flex justify-between items-center">
                      <p className="text-xs text-gray-500">
                        Minimum 100 characters required
                      </p>
                      <p className={`text-xs ${
                        transcriptText.length >= 100 ? 'text-green-600' : 'text-gray-500'
                      }`}>
                        {transcriptText.length} characters
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Right Column - Session Details */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Session Details
                </h3>
                
                <SessionForm
                  onSubmit={handleSessionFormSubmit}
                  disabled={isUploading}
                />
              </div>
            </div>

            {/* Upload Progress */}
            {uploadProgress && (
              <div className="mt-8 border-t border-gray-200 pt-6">
                <UploadProgress progress={uploadProgress} />
              </div>
            )}

            {/* Error Display */}
            {error && !uploadProgress && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            {!uploadProgress && (
              <div className="mt-8 border-t border-gray-200 pt-6">
                <button
                  type="submit"
                  form="session-form"
                  disabled={!canSubmit()}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {isUploading ? 'Uploading...' : 'Upload Session'}
                </button>
                
                {!canSubmit() && (
                  <p className="mt-2 text-sm text-gray-500 text-center">
                    {uploadMode === 'file' 
                      ? 'Please select a file to continue'
                      : 'Please enter at least 100 characters of transcript text'
                    }
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;