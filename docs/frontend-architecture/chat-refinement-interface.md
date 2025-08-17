# Chat Refinement Interface

The chat refinement interface is the core differentiator of the platform, enabling coaches to iteratively improve AI-generated summaries through natural conversation.

## WebSocket Implementation

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

## Performance Optimizations

1. **Virtual Scrolling** for large session lists using `@tanstack/react-virtual`
2. **Image Optimization** with Next.js Image component and responsive sizes
3. **Code Splitting** with dynamic imports for heavy components
4. **Memoization** of expensive filters and computations
5. **Debounced Search** with 300ms delay to reduce API calls
6. **Optimistic Updates** for better perceived performance
7. **Progressive Enhancement** with SSR for SEO and initial load
8. **Service Worker** for offline capability and caching
