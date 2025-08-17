'use client';

import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Calendar, Clock, FileText, Users } from 'lucide-react';

const sessionFormSchema = z.object({
  session_date: z.string().min(1, 'Session date is required'),
  session_type: z.string().optional(),
  duration_minutes: z.number().min(1).max(480).optional(),
  notes: z.string().max(1000).optional(),
  participants: z.string().optional(), // Comma-separated names
});

export type SessionFormData = z.infer<typeof sessionFormSchema>;

interface SessionFormProps {
  onSubmit: (data: SessionFormData) => void;
  disabled?: boolean;
  defaultValues?: Partial<SessionFormData>;
}

const SessionForm: React.FC<SessionFormProps> = ({
  onSubmit,
  disabled = false,
  defaultValues,
}) => {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
  } = useForm<SessionFormData>({
    resolver: zodResolver(sessionFormSchema),
    defaultValues: {
      session_date: new Date().toISOString().split('T')[0], // Today's date
      session_type: '',
      duration_minutes: undefined,
      notes: '',
      participants: '',
      ...defaultValues,
    },
  });

  const sessionTypes = [
    { value: '', label: 'Select session type (optional)' },
    { value: 'individual', label: 'Individual Coaching' },
    { value: 'group', label: 'Group Coaching' },
    { value: 'workshop', label: 'Workshop' },
    { value: 'supervision', label: 'Supervision' },
    { value: 'other', label: 'Other' },
  ];

  return (
    <form id="session-form" onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Session Date */}
      <div>
        <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
          <Calendar className="w-4 h-4" />
          <span>Session Date *</span>
        </label>
        <input
          type="date"
          {...register('session_date')}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
        />
        {errors.session_date && (
          <p className="mt-1 text-sm text-red-600">{errors.session_date.message}</p>
        )}
      </div>

      {/* Session Type */}
      <div>
        <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
          <FileText className="w-4 h-4" />
          <span>Session Type</span>
        </label>
        <select
          {...register('session_type')}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
        >
          {sessionTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>

      {/* Duration */}
      <div>
        <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
          <Clock className="w-4 h-4" />
          <span>Duration (minutes)</span>
        </label>
        <input
          type="number"
          min="1"
          max="480"
          placeholder="e.g., 60"
          {...register('duration_minutes', {
            valueAsNumber: true,
            setValueAs: (value) => value === '' ? undefined : Number(value),
          })}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
        />
        {errors.duration_minutes && (
          <p className="mt-1 text-sm text-red-600">{errors.duration_minutes.message}</p>
        )}
      </div>

      {/* Participants */}
      <div>
        <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
          <Users className="w-4 h-4" />
          <span>Participants (optional)</span>
        </label>
        <input
          type="text"
          placeholder="e.g., John Doe, Jane Smith"
          {...register('participants')}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
        />
        <p className="mt-1 text-xs text-gray-500">
          Leave blank to automatically extract from transcript. Separate multiple names with commas.
        </p>
      </div>

      {/* Notes */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Additional Notes
        </label>
        <textarea
          rows={3}
          placeholder="Any additional context about this session..."
          {...register('notes')}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:text-gray-500 resize-vertical"
        />
        {errors.notes && (
          <p className="mt-1 text-sm text-red-600">{errors.notes.message}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Maximum 1000 characters
        </p>
      </div>
    </form>
  );
};

export default SessionForm;