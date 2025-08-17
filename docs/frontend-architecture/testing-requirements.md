# Testing Requirements

## Component Test Template

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

## Testing Best Practices

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions with stores and APIs
3. **E2E Tests**: Test critical user flows (session upload → refinement → approval)
4. **Coverage Goals**: Aim for 80% code coverage
5. **Test Structure**: Arrange-Act-Assert pattern
6. **Mock External Dependencies**: API calls, WebSocket connections, third-party libraries
