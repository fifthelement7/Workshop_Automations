'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { CheckCircle, Clock, Users, ArrowRight, Upload, Home } from 'lucide-react';
import Link from 'next/link';

import { api } from '@/services/api';
import { SessionDetails } from '@/types/sessions';

const UploadSuccessPage: React.FC = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('sessionId');

  const [sessionDetails, setSessionDetails] = useState<SessionDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) {
      setError('No session ID provided');
      setLoading(false);
      return;
    }

    const fetchSessionDetails = async () => {
      try {
        const details = await api.getSession(sessionId);
        setSessionDetails(details);
      } catch (err) {
        console.error('Error fetching session details:', err);
        setError('Failed to load session details');
      } finally {
        setLoading(false);
      }
    };

    fetchSessionDetails();
  }, [sessionId]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading session details...</p>
        </div>
      </div>
    );
  }

  if (error || !sessionDetails) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="bg-red-100 rounded-full p-3 mx-auto mb-4 w-16 h-16 flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-red-600" />
          </div>
          <h1 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Session</h1>
          <p className="text-gray-600 mb-6">{error}</p>
          <Link
            href="/upload"
            className="inline-flex items-center bg-blue-600 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-700 transition-colors"
          >
            Try Again
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Success Header */}
        <div className="text-center mb-8">
          <div className="bg-green-100 rounded-full p-3 mx-auto mb-4 w-16 h-16 flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Upload Successful!
          </h1>
          <p className="text-lg text-gray-600">
            Your session transcript has been uploaded and processed
          </p>
        </div>

        {/* Session Details Card */}
        <div className="bg-white shadow-lg rounded-lg overflow-hidden mb-8">
          <div className="bg-blue-50 px-6 py-4 border-b border-blue-100">
            <h2 className="text-lg font-semibold text-blue-900">Session Details</h2>
          </div>
          
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Session Info */}
              <div>
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
                  Session Information
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 text-gray-400 mr-2" />
                    <span className="text-sm text-gray-600">Date:</span>
                    <span className="ml-2 text-sm font-medium text-gray-900">
                      {formatDate(sessionDetails.session.session_date)}
                    </span>
                  </div>
                  
                  {sessionDetails.session.session_type && (
                    <div className="flex items-center">
                      <span className="text-sm text-gray-600">Type:</span>
                      <span className="ml-2 text-sm font-medium text-gray-900 capitalize">
                        {sessionDetails.session.session_type}
                      </span>
                    </div>
                  )}
                  
                  {sessionDetails.session.duration_minutes && (
                    <div className="flex items-center">
                      <span className="text-sm text-gray-600">Duration:</span>
                      <span className="ml-2 text-sm font-medium text-gray-900">
                        {sessionDetails.session.duration_minutes} minutes
                      </span>
                    </div>
                  )}
                  
                  <div className="flex items-center">
                    <span className="text-sm text-gray-600">Session ID:</span>
                    <span className="ml-2 text-xs font-mono text-gray-700 bg-gray-100 px-2 py-1 rounded">
                      {sessionDetails.session.id}
                    </span>
                  </div>
                  
                  <div className="flex items-center">
                    <span className="text-sm text-gray-600">Created:</span>
                    <span className="ml-2 text-sm text-gray-700">
                      {formatDateTime(sessionDetails.session.created_at)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Participants */}
              <div>
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
                  Participants
                </h3>
                {sessionDetails.participants.length > 0 ? (
                  <div className="space-y-2">
                    {sessionDetails.participants.map((participant, index) => (
                      <div key={index} className="flex items-center">
                        <Users className="w-4 h-4 text-gray-400 mr-2" />
                        <span className="text-sm font-medium text-gray-900">
                          {participant.name}
                        </span>
                        {participant.email && (
                          <span className="ml-2 text-xs text-gray-500">
                            ({participant.email})
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 italic">
                    No participants identified from the transcript
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Processing Status */}
        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-gray-900">Processing Status</h3>
              <p className="text-sm text-gray-600 mt-1">
                Current status: <span className="font-medium capitalize">{sessionDetails.session.processing_status}</span>
              </p>
            </div>
            <div className="text-right">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                {sessionDetails.session.processing_status}
              </span>
            </div>
          </div>
          
          <div className="mt-4 p-4 bg-blue-50 rounded-md">
            <p className="text-sm text-blue-800">
              <strong>Next Steps:</strong> Your session is ready for AI analysis. 
              The system will automatically process the transcript to generate insights, 
              summaries, and coaching recommendations.
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/upload"
            className="inline-flex items-center justify-center bg-blue-600 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-700 transition-colors"
          >
            <Upload className="w-4 h-4 mr-2" />
            Upload Another Session
          </Link>
          
          <Link
            href="/"
            className="inline-flex items-center justify-center bg-gray-600 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-700 transition-colors"
          >
            <Home className="w-4 h-4 mr-2" />
            Go to Dashboard
          </Link>
          
          <button
            onClick={() => router.push(`/sessions/${sessionDetails.session.id}`)}
            className="inline-flex items-center justify-center border border-gray-300 bg-white text-gray-700 px-6 py-3 rounded-md font-medium hover:bg-gray-50 transition-colors"
          >
            View Session Details
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadSuccessPage;