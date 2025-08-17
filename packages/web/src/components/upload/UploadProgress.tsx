'use client';

import React from 'react';
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';
import { UploadProgress as UploadProgressType } from '@/types/sessions';

interface UploadProgressProps {
  progress: UploadProgressType;
  className?: string;
}

const UploadProgress: React.FC<UploadProgressProps> = ({
  progress,
  className,
}) => {
  const getProgressColor = () => {
    switch (progress.stage) {
      case 'uploading':
        return 'bg-blue-500';
      case 'processing':
        return 'bg-yellow-500';
      case 'completed':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getIcon = () => {
    switch (progress.stage) {
      case 'uploading':
      case 'processing':
        return <Loader2 className="w-5 h-5 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-5 h-5" />;
      case 'error':
        return <AlertCircle className="w-5 h-5" />;
      default:
        return null;
    }
  };

  const getStatusColor = () => {
    switch (progress.stage) {
      case 'uploading':
        return 'text-blue-600';
      case 'processing':
        return 'text-yellow-600';
      case 'completed':
        return 'text-green-600';
      case 'error':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className={clsx('w-full', className)}>
      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
        <div
          className={clsx(
            'h-2 rounded-full transition-all duration-300 ease-out',
            getProgressColor()
          )}
          style={{ width: `${progress.progress}%` }}
        />
      </div>

      {/* Status Info */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={getStatusColor()}>
            {getIcon()}
          </div>
          <div>
            <p className={clsx('text-sm font-medium', getStatusColor())}>
              {progress.message}
            </p>
            <p className="text-xs text-gray-500">
              {progress.progress}% complete
            </p>
          </div>
        </div>

        <div className="text-right">
          <p className={clsx('text-sm font-medium', getStatusColor())}>
            {progress.stage.charAt(0).toUpperCase() + progress.stage.slice(1)}
          </p>
        </div>
      </div>

      {/* Stage-specific details */}
      {progress.stage === 'uploading' && (
        <div className="mt-2 text-xs text-gray-500">
          Uploading transcript file...
        </div>
      )}

      {progress.stage === 'processing' && (
        <div className="mt-2 text-xs text-gray-500">
          Extracting participants and creating session record...
        </div>
      )}

      {progress.stage === 'completed' && (
        <div className="mt-2 p-3 bg-green-50 rounded-md">
          <p className="text-sm text-green-800 font-medium">Upload Complete!</p>
          <p className="text-xs text-green-600 mt-1">
            Your session has been successfully uploaded and is ready for analysis.
          </p>
        </div>
      )}

      {progress.stage === 'error' && (
        <div className="mt-2 p-3 bg-red-50 rounded-md">
          <p className="text-sm text-red-800 font-medium">Upload Failed</p>
          <p className="text-xs text-red-600 mt-1">
            Please check your file and try again. If the problem persists, contact support.
          </p>
        </div>
      )}
    </div>
  );
};

export default UploadProgress;