# Frontend Tech Stack

All technology choices align with the backend architecture document and are optimized for the coaching platform's real-time collaboration needs.

## Technology Stack Table

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
