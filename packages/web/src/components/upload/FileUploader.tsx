'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, X } from 'lucide-react';
import { clsx } from 'clsx';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  onFileRemove: () => void;
  selectedFile: File | null;
  disabled?: boolean;
  maxSize?: number; // in bytes
}

const FileUploader: React.FC<FileUploaderProps> = ({
  onFileSelect,
  onFileRemove,
  selectedFile,
  disabled = false,
  maxSize = 10 * 1024 * 1024, // 10MB default
}) => {
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: any[]) => {
      setError(null);
      
      if (rejectedFiles.length > 0) {
        const rejection = rejectedFiles[0];
        if (rejection.errors[0]?.code === 'file-too-large') {
          setError(`File too large. Maximum size is ${Math.round(maxSize / (1024 * 1024))}MB.`);
        } else if (rejection.errors[0]?.code === 'file-invalid-type') {
          setError('Invalid file type. Please upload .txt or .docx files only.');
        } else {
          setError('Invalid file. Please check the file and try again.');
        }
        return;
      }

      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    [onFileSelect, maxSize]
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize,
    multiple: false,
    disabled,
  });

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full">
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={clsx(
            'relative border-2 border-dashed rounded-lg p-8 transition-colors cursor-pointer',
            'flex flex-col items-center justify-center min-h-[200px]',
            {
              'border-blue-300 bg-blue-50': isDragActive && !isDragReject,
              'border-red-300 bg-red-50': isDragReject,
              'border-gray-300 hover:border-gray-400': !isDragActive && !disabled,
              'border-gray-200 bg-gray-50 cursor-not-allowed': disabled,
            }
          )}
        >
          <input {...getInputProps()} />
          
          <Upload 
            className={clsx('w-12 h-12 mb-4', {
              'text-blue-500': isDragActive && !isDragReject,
              'text-red-500': isDragReject,
              'text-gray-400': !isDragActive && !disabled,
              'text-gray-300': disabled,
            })} 
          />
          
          <div className="text-center">
            {isDragActive ? (
              isDragReject ? (
                <p className="text-red-600 font-medium">
                  File type not supported
                </p>
              ) : (
                <p className="text-blue-600 font-medium">
                  Drop the file here
                </p>
              )
            ) : (
              <>
                <p className={clsx('text-lg font-medium mb-2', {
                  'text-gray-900': !disabled,
                  'text-gray-500': disabled,
                })}>
                  Drop transcript file here
                </p>
                <p className={clsx('text-sm', {
                  'text-gray-600': !disabled,
                  'text-gray-400': disabled,
                })}>
                  or click to browse
                </p>
              </>
            )}
          </div>
          
          <div className={clsx('text-xs mt-4 text-center', {
            'text-gray-500': !disabled,
            'text-gray-400': disabled,
          })}>
            Supported formats: .txt, .docx
            <br />
            Maximum size: {Math.round(maxSize / (1024 * 1024))}MB
          </div>
        </div>
      ) : (
        <div className="border rounded-lg p-4 bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="w-8 h-8 text-blue-500" />
              <div>
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-600">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            
            {!disabled && (
              <button
                type="button"
                onClick={onFileRemove}
                className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                title="Remove file"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="mt-2 flex items-center space-x-2 text-red-600">
          <AlertCircle className="w-4 h-4" />
          <p className="text-sm">{error}</p>
        </div>
      )}
    </div>
  );
};

export default FileUploader;