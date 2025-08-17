# Project Structure

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
