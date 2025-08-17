# Coaching Supervision & Automation Platform Frontend Architecture Document

## Template and Framework Selection

This frontend architecture is designed for the Coaching Supervision & Automation Platform, building upon the backend architecture and implementing the UI/UX specifications for the Mindscribe interface. No starter template is being used - this is a custom Next.js 14 implementation optimized for the coach workflow and real-time chat refinement features.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|---------|
| 2025-08-16 | 1.0 | Initial frontend architecture based on backend architecture and UI spec | Winston (Architect) |

## Frontend Tech Stack

All technology choices align with the backend architecture document and are optimized for the coaching platform's real-time collaboration needs.

### Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-----------|
| **Framework** | Next.js | 14.1.0 | React framework with SSR/SSG | SEO optimization, built-in routing, API routes, excellent DX |
| **UI Library** | React | 18.2.0 | Component-based UI development | Industry standard, vast ecosystem, hooks API |
| **Language** | TypeScript | 5.3.3 | Type-safe JavaScript | Prevents runtime errors, excellent IDE support, self-documenting |
| **State Management** | Zustand | 4.5.0 | Lightweight state management | Simple API, TypeScript support, minimal boilerplate |
| **Routing** | Next.js Router | 14.1.0 | File-based routing | Built into Next.js, supports dynamic routes, API routes |
| **Build Tool** | Turbopack | Built-in | Next.js bundler | Faster than Webpack, built into Next.js 14 |
| **Styling** | Tailwind CSS | 3.4.1 | Utility-first CSS | Rapid development, consistent design, tree-shaking |
| **Component Library** | Shadcn/ui | Latest | Headless component library | Copy-paste components, fully customizable, Radix UI based |
| **Form Handling** | React Hook Form | 7.49.0 | Form state management | Excellent performance, built-in validation, TypeScript support |
| **Data Fetching** | TanStack Query | 5.17.0 | Server state management | Caching, background refetching, optimistic updates |
| **WebSocket** | Socket.io-client | 4.6.0 | Real-time communication | Automatic reconnection, binary support, room management |
| **Animation** | Framer Motion | 11.0.0 | Animation library | Declarative API, gesture support, layout animations |
| **Testing** | Jest + RTL | 29.7.0 / 14.2.0 | Unit and integration testing | Next.js integration, component testing, snapshot support |
| **E2E Testing** | Playwright | 1.41.0 | End-to-end testing | Cross-browser support, reliable automation |
| **Dev Tools** | ESLint + Prettier | 8.56.0 / 3.2.0 | Code quality and formatting | Consistent code style, catch errors early |

## Project Structure

```plaintext
coaching-platform/packages/web/
├── src/
│   ├── app/                           # Next.js 14 App Router
│   │   ├── (auth)/                    # Auth group layout
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── (dashboard)/               # Dashboard group layout
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx               # Dashboard home
│   │   │   ├── clients/
│   │   │   │   ├── page.tsx           # Clients list
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Client profile
│   │   │   ├── sessions/
│   │   │   │   ├── page.tsx           # Sessions list
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx       # Session details
│   │   │   │       └── refine/
│   │   │   │           └── page.tsx   # Chat refinement
│   │   │   ├── templates/
│   │   │   │   └── page.tsx
│   │   │   ├── follow-ups/
│   │   │   │   └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   ├── api/                       # API routes (if needed)
│   │   │   └── webhooks/
│   │   ├── layout.tsx                 # Root layout
│   │   ├── page.tsx                   # Landing page
│   │   ├── error.tsx                  # Error boundary
│   │   ├── loading.tsx                # Loading state
│   │   └── not-found.tsx              # 404 page
│   │
│   ├── components/
│   │   ├── ui/                        # Shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── form.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── table.tsx
│   │   │   ├── toast.tsx
│   │   │   └── ...
│   │   ├── layouts/
│   │   │   ├── sidebar.tsx
│   │   │   ├── header.tsx
│   │   │   └── mobile-nav.tsx
│   │   ├── features/
│   │   │   ├── sessions/
│   │   │   │   ├── session-card.tsx
│   │   │   │   ├── session-list.tsx
│   │   │   │   └── session-filters.tsx
│   │   │   ├── clients/
│   │   │   │   ├── client-card.tsx
│   │   │   │   ├── client-timeline.tsx
│   │   │   │   └── engagement-badge.tsx
│   │   │   ├── chat/
│   │   │   │   ├── chat-interface.tsx
│   │   │   │   ├── message-list.tsx
│   │   │   │   ├── message-input.tsx
│   │   │   │   └── refinement-controls.tsx
│   │   │   ├── follow-up/
│   │   │   │   ├── follow-up-generator.tsx
│   │   │   │   ├── email-preview.tsx
│   │   │   │   └── template-selector.tsx
│   │   │   └── search/
│   │   │       ├── natural-language-search.tsx
│   │   │       ├── search-results.tsx
│   │   │       └── search-filters.tsx
│   │   └── shared/
│   │       ├── loading-skeleton.tsx
│   │       ├── error-boundary.tsx
│   │       ├── empty-state.tsx
│   │       └── data-table.tsx
│   │
│   ├── lib/
│   │   ├── api/                       # API client layer
│   │   │   ├── client.ts              # Axios/fetch configuration
│   │   │   ├── auth.ts                # Auth API calls
│   │   │   ├── sessions.ts            # Sessions API
│   │   │   ├── clients.ts             # Clients API
│   │   │   ├── summaries.ts           # Summaries API
│   │   │   ├── search.ts              # Search API
│   │   │   └── websocket.ts           # WebSocket client
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── use-auth.ts
│   │   │   ├── use-session.ts
│   │   │   ├── use-chat.ts            # WebSocket chat hook
│   │   │   ├── use-search.ts
│   │   │   └── use-debounce.ts
│   │   ├── stores/                    # Zustand stores
│   │   │   ├── auth-store.ts
│   │   │   ├── session-store.ts
│   │   │   ├── chat-store.ts
│   │   │   └── ui-store.ts
│   │   ├── utils/
│   │   │   ├── cn.ts                  # Class name utility
│   │   │   ├── format.ts              # Date/number formatting
│   │   │   ├── validation.ts          # Form validation schemas
│   │   │   └── constants.ts
│   │   └── types/                     # TypeScript types
│   │       ├── api.ts                 # API response types
│   │       ├── models.ts              # Data model types
│   │       └── ui.ts                  # UI component types
│   │
│   ├── styles/
│   │   ├── globals.css                # Global styles + Tailwind
│   │   └── themes/
│   │       └── default.css            # CSS variables theme
│   │
│   └── public/
│       ├── fonts/
│       ├── images/
│       └── icons/
│
├── tests/
│   ├── unit/                          # Unit tests
│   ├── integration/                   # Integration tests
│   └── e2e/                          # Playwright tests
│
├── .env.local                         # Local environment variables
├── .env.example                       # Environment template
├── next.config.js                     # Next.js configuration
├── tailwind.config.ts                 # Tailwind configuration
├── tsconfig.json                      # TypeScript configuration
├── jest.config.js                     # Jest configuration
├── playwright.config.ts               # Playwright configuration
└── package.json
```

## Component Standards

### Component Template

```typescript
// components/features/sessions/session-card.tsx
import { FC, memo } from 'react';
import { cn } from '@/lib/utils/cn';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Session } from '@/lib/types/models';

interface SessionCardProps {
  session: Session;
  className?: string;
  onClick?: (session: Session) => void;
  isSelected?: boolean;
}

export const SessionCard: FC<SessionCardProps> = memo(({
  session,
  className,
  onClick,
  isSelected = false,
}) => {
  const handleClick = () => {
    onClick?.(session);
  };

  return (
    <Card 
      className={cn(
        'cursor-pointer transition-all hover:shadow-md',
        isSelected && 'ring-2 ring-primary',
        className
      )}
      onClick={handleClick}
    >
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">
            {session.sessionType}
          </CardTitle>
          <Badge variant={session.processingStatus === 'completed' ? 'success' : 'secondary'}>
            {session.processingStatus}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">
            {new Date(session.sessionDate).toLocaleDateString()}
          </p>
          <p className="text-sm">
            {session.participantCount} participants
          </p>
        </div>
      </CardContent>
    </Card>
  );
});

SessionCard.displayName = 'SessionCard';
```

### Naming Conventions

- **Components:** PascalCase (`SessionCard.tsx`)
- **Component Files:** kebab-case (`session-card.tsx`)
- **Hooks:** camelCase with `use` prefix (`useSession`)
- **Stores:** kebab-case with `-store` suffix (`auth-store.ts`)
- **API Services:** kebab-case (`sessions.ts`)
- **Types/Interfaces:** PascalCase (`SessionData`, `ApiResponse`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_FILE_SIZE`)
- **CSS Classes:** kebab-case (`session-card-wrapper`)
- **Test Files:** Same name with `.test.tsx` suffix

## State Management

### Store Structure

```plaintext
src/lib/stores/
├── auth-store.ts         # Authentication state
├── session-store.ts      # Current session data
├── chat-store.ts         # Chat/refinement state
├── ui-store.ts          # UI preferences (sidebar, theme)
└── index.ts             # Store exports
```

### State Management Template

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

## API Integration

### Service Template

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

### API Client Configuration

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

## Routing

### Route Configuration

```typescript
// app/(dashboard)/layout.tsx
import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { Sidebar } from '@/components/layouts/sidebar';
import { Header } from '@/components/layouts/header';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession();
  
  if (!session) {
    redirect('/login');
  }
  
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}

// middleware.ts - Route protection
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token');
  const isAuthPage = request.nextUrl.pathname.startsWith('/login');
  
  if (!token && !isAuthPage) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  if (token && isAuthPage) {
    return NextResponse.redirect(new URL('/', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## Styling Guidelines

### Styling Approach

The platform uses Tailwind CSS with Shadcn/ui components for rapid development and consistent design. Custom components follow utility-first principles with occasional CSS modules for complex animations.

### Global Theme Variables

```css
/* styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Colors - Light Mode */
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    --spacing-3xl: 4rem;
    
    /* Typography */
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-mono: 'SF Mono', 'Consolas', monospace;
    
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 1.875rem;
    --text-4xl: 2.25rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
    
    /* Border Radius */
    --radius: 0.5rem;
    --radius-sm: 0.25rem;
    --radius-md: 0.375rem;
    --radius-lg: 0.5rem;
    --radius-xl: 0.75rem;
    --radius-full: 9999px;
    
    /* Animation */
    --animation-fast: 150ms;
    --animation-base: 250ms;
    --animation-slow: 350ms;
  }
  
  .dark {
    /* Colors - Dark Mode */
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer utilities {
  /* Custom utility classes */
  .animate-in {
    animation-duration: var(--animation-base);
    animation-fill-mode: both;
  }
  
  .fade-in {
    animation-name: fadeIn;
  }
  
  .slide-in-bottom {
    animation-name: slideInBottom;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideInBottom {
    from { 
      transform: translateY(10px);
      opacity: 0;
    }
    to { 
      transform: translateY(0);
      opacity: 1;
    }
  }
}
```

## Testing Requirements

### Component Test Template

```typescript
// tests/unit/components/session-card.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { SessionCard } from '@/components/features/sessions/session-card';
import { Session } from '@/lib/types/models';

// Mock data
const mockSession: Session = {
  id: '123',
  coachId: '456',
  sessionDate: '2024-01-15',
  sessionType: 'Group Workshop',
  participantCount: 12,
  processingStatus: 'completed',
  durationMinutes: 90,
  metadata: {},
};

describe('SessionCard', () => {
  it('renders session information correctly', () => {
    render(<SessionCard session={mockSession} />);
    
    expect(screen.getByText('Group Workshop')).toBeInTheDocument();
    expect(screen.getByText('12 participants')).toBeInTheDocument();
    expect(screen.getByText('completed')).toBeInTheDocument();
  });
  
  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<SessionCard session={mockSession} onClick={handleClick} />);
    
    fireEvent.click(screen.getByRole('article'));
    expect(handleClick).toHaveBeenCalledWith(mockSession);
  });
  
  it('applies selected styles when isSelected is true', () => {
    const { container } = render(
      <SessionCard session={mockSession} isSelected={true} />
    );
    
    const card = container.querySelector('.ring-2.ring-primary');
    expect(card).toBeInTheDocument();
  });
  
  it('renders processing badge with correct variant', () => {
    const processingSession = { ...mockSession, processingStatus: 'processing' };
    render(<SessionCard session={processingSession} />);
    
    const badge = screen.getByText('processing');
    expect(badge).toHaveClass('bg-secondary');
  });
});

// Integration test example
describe('SessionCard Integration', () => {
  it('integrates with session store', async () => {
    const { result } = renderHook(() => useSessionStore());
    
    render(<SessionCard session={mockSession} />);
    
    // Simulate selection
    fireEvent.click(screen.getByRole('article'));
    
    await waitFor(() => {
      expect(result.current.currentSession).toEqual(mockSession);
    });
  });
});
```

### Testing Best Practices

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions with stores and APIs
3. **E2E Tests**: Test critical user flows (session upload → refinement → approval)
4. **Coverage Goals**: Aim for 80% code coverage
5. **Test Structure**: Arrange-Act-Assert pattern
6. **Mock External Dependencies**: API calls, WebSocket connections, third-party libraries

## Environment Configuration

```bash
# .env.local - Development environment variables
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here

# Feature Flags
NEXT_PUBLIC_ENABLE_CHAT_REFINEMENT=true
NEXT_PUBLIC_ENABLE_NATURAL_SEARCH=true
NEXT_PUBLIC_ENABLE_EXPORT=true

# Analytics (optional)
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
NEXT_PUBLIC_DATADOG_CLIENT_TOKEN=

# File Upload
NEXT_PUBLIC_MAX_FILE_SIZE=52428800  # 50MB in bytes
NEXT_PUBLIC_ALLOWED_FILE_TYPES=.txt,.docx,.pdf

# WebSocket Configuration
NEXT_PUBLIC_WS_RECONNECT_DELAY=1000
NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS=5
```

## Frontend Developer Standards

### Critical Coding Rules

1. **Never use `any` type** - Always define proper TypeScript types
2. **Always handle loading and error states** - Every async operation needs loading/error UI
3. **Use React Query for server state** - Don't store API data in Zustand
4. **Memoize expensive computations** - Use `useMemo` and `React.memo` appropriately
5. **Validate all forms** - Use zod schemas with react-hook-form
6. **Sanitize user input** - Especially for rich text and file uploads
7. **Use semantic HTML** - Proper heading hierarchy and ARIA labels
8. **Implement error boundaries** - Catch and handle component errors gracefully
9. **Optimize images** - Use Next.js Image component with proper sizes
10. **Test WebSocket reconnection** - Handle connection failures gracefully
11. **Use CSS variables for theming** - Don't hardcode colors
12. **Implement proper focus management** - For modals and dynamic content
13. **Cache API responses** - Use React Query's stale-while-revalidate
14. **Debounce search inputs** - Minimum 300ms delay
15. **Lazy load heavy components** - Use dynamic imports for code splitting

### Quick Reference

**Common Commands:**
```bash
# Development
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler
npm run test         # Run unit tests
npm run test:e2e     # Run Playwright tests

# Component Generation
npx shadcn-ui@latest add [component]  # Add new UI component
```

**Key Import Patterns:**
```typescript
// Components
import { Button } from '@/components/ui/button';
import { SessionCard } from '@/components/features/sessions/session-card';

// Hooks
import { useSession } from '@/lib/hooks/use-session';
import { useSessionStore } from '@/lib/stores/session-store';

// API
import { sessionsApi } from '@/lib/api/sessions';

// Types
import type { Session } from '@/lib/types/models';

// Utils
import { cn } from '@/lib/utils/cn';
import { formatDate } from '@/lib/utils/format';
```

**File Naming Conventions:**
- Pages: `app/[route]/page.tsx`
- Components: `components/[category]/component-name.tsx`
- Hooks: `lib/hooks/use-[name].ts`
- API Services: `lib/api/[resource].ts`
- Types: `lib/types/[category].ts`
- Tests: `[file].test.tsx` or `[file].spec.tsx`

**Project-Specific Patterns:**
- WebSocket chat uses Socket.io with automatic reconnection
- All forms use react-hook-form with zod validation
- Data tables use tanstack-table with server-side pagination
- Authentication uses JWT with refresh token rotation
- File uploads go directly to S3 presigned URLs
- Natural language search uses debounced input with instant results

## Chat Refinement Interface

The chat refinement interface is the core differentiator of the platform, enabling coaches to iteratively improve AI-generated summaries through natural conversation.

### WebSocket Implementation

```typescript
// lib/hooks/use-chat.ts
import { useEffect, useRef, useState } from 'react';
import { Socket } from 'socket.io-client';
import { createWebSocketConnection } from '@/lib/api/client';
import { useChatStore } from '@/lib/stores/chat-store';

export const useChat = (sessionId: string) => {
  const socketRef = useRef<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const { addMessage, setTyping, setSummary } = useChatStore();
  
  useEffect(() => {
    // Create WebSocket connection
    socketRef.current = createWebSocketConnection(sessionId);
    
    // Connection handlers
    socketRef.current.on('connect', () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    });
    
    socketRef.current.on('disconnect', () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    });
    
    // Message handlers
    socketRef.current.on('message', (data) => {
      addMessage({
        id: data.id,
        content: data.content,
        role: data.role,
        timestamp: new Date(data.timestamp),
      });
    });
    
    socketRef.current.on('typing', (data) => {
      setTyping(data.isTyping);
    });
    
    socketRef.current.on('summary-update', (data) => {
      setSummary(data.summary);
    });
    
    // Error handling
    socketRef.current.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
    
    return () => {
      socketRef.current?.disconnect();
    };
  }, [sessionId]);
  
  const sendMessage = (content: string) => {
    socketRef.current?.emit('refine', {
      sessionId,
      content,
      timestamp: new Date().toISOString(),
    });
  };
  
  return {
    isConnected,
    sendMessage,
  };
};
```

### Performance Optimizations

1. **Virtual Scrolling** for large session lists using `@tanstack/react-virtual`
2. **Image Optimization** with Next.js Image component and responsive sizes
3. **Code Splitting** with dynamic imports for heavy components
4. **Memoization** of expensive filters and computations
5. **Debounced Search** with 300ms delay to reduce API calls
6. **Optimistic Updates** for better perceived performance
7. **Progressive Enhancement** with SSR for SEO and initial load
8. **Service Worker** for offline capability and caching

## Accessibility Implementation

- **Semantic HTML** throughout with proper heading hierarchy
- **ARIA Labels** on all interactive elements
- **Keyboard Navigation** with visible focus indicators
- **Screen Reader Support** with live regions for dynamic content
- **Color Contrast** meeting WCAG AA standards (4.5:1 ratio)
- **Responsive Design** working from 320px to 4K displays
- **Skip Links** for keyboard navigation
- **Form Labels** with clear error messages
- **Alt Text** on all images and icons
- **Focus Management** in modals and dynamic content

## Next Steps

1. **Set up development environment** with Next.js and dependencies
2. **Implement authentication flow** with JWT and refresh tokens
3. **Create base UI components** from Shadcn/ui
4. **Build WebSocket chat interface** for iterative refinement
5. **Implement session upload and processing flow**
6. **Add natural language search** with debouncing
7. **Create responsive layouts** for mobile and desktop
8. **Set up testing infrastructure** with Jest and Playwright
9. **Configure CI/CD pipeline** for automated deployment
10. **Implement monitoring** with error tracking and analytics