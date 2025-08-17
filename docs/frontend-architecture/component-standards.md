# Component Standards

## Component Template

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

## Naming Conventions

- **Components:** PascalCase (`SessionCard.tsx`)
- **Component Files:** kebab-case (`session-card.tsx`)
- **Hooks:** camelCase with `use` prefix (`useSession`)
- **Stores:** kebab-case with `-store` suffix (`auth-store.ts`)
- **API Services:** kebab-case (`sessions.ts`)
- **Types/Interfaces:** PascalCase (`SessionData`, `ApiResponse`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_FILE_SIZE`)
- **CSS Classes:** kebab-case (`session-card-wrapper`)
- **Test Files:** Same name with `.test.tsx` suffix
