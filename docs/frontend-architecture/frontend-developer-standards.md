# Frontend Developer Standards

## Critical Coding Rules

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

## Quick Reference

**Common Commands:**
```bash