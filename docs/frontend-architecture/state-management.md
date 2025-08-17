# State Management

## Store Structure

```plaintext
src/lib/stores/
├── auth-store.ts         # Authentication state
├── session-store.ts      # Current session data
├── chat-store.ts         # Chat/refinement state
├── ui-store.ts          # UI preferences (sidebar, theme)
└── index.ts             # Store exports
```

## State Management Template

```typescript
// lib/stores/session-store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { Session, Summary } from '@/lib/types/models';

interface SessionState {
  // State
  currentSession: Session | null;
  summaries: Summary[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setCurrentSession: (session: Session | null) => void;
  setSummaries: (summaries: Summary[]) => void;
  updateSummary: (id: string, updates: Partial<Summary>) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState = {
  currentSession: null,
  summaries: [],
  isLoading: false,
  error: null,
};

export const useSessionStore = create<SessionState>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,
        
        setCurrentSession: (session) => 
          set({ currentSession: session }, false, 'setCurrentSession'),
        
        setSummaries: (summaries) => 
          set({ summaries }, false, 'setSummaries'),
        
        updateSummary: (id, updates) =>
          set((state) => ({
            summaries: state.summaries.map(s => 
              s.id === id ? { ...s, ...updates } : s
            ),
          }), false, 'updateSummary'),
        
        setLoading: (isLoading) => 
          set({ isLoading }, false, 'setLoading'),
        
        setError: (error) => 
          set({ error }, false, 'setError'),
        
        reset: () => 
          set(initialState, false, 'reset'),
      }),
      {
        name: 'session-storage',
        partialize: (state) => ({ 
          currentSession: state.currentSession 
        }),
      }
    ),
    {
      name: 'SessionStore',
    }
  )
);
```
