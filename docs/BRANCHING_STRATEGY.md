# Branching Strategy for Mindscribe

## Overview
This document outlines the Git branching strategy for the Mindscribe project, based on a simplified Git Flow model suitable for a coaching platform development.

## Branch Types

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Protected branch, requires PR approval
- **Deployment**: Automatically deploys to production
- **Rules**: 
  - No direct commits allowed
  - All changes must come through Pull Requests
  - Requires at least 1 approval
  - All CI checks must pass

#### `develop`
- **Purpose**: Integration branch for features
- **Protection**: Protected branch, requires PR approval
- **Deployment**: Automatically deploys to staging environment
- **Rules**:
  - No direct commits allowed
  - Features merge here before going to main
  - Regular merges to main for releases

### Supporting Branches

#### Feature Branches (`feature/*`)
- **Naming**: `feature/story-number-short-description`
- **Examples**: 
  - `feature/1.1-project-setup`
  - `feature/2.3-ai-analysis-integration`
  - `feature/3.1-coach-dashboard`
- **Source**: Branch from `develop`
- **Merge**: Merge back to `develop` via PR
- **Lifespan**: Delete after merge

#### Hotfix Branches (`hotfix/*`)
- **Naming**: `hotfix/issue-description`
- **Examples**: 
  - `hotfix/database-connection-timeout`
  - `hotfix/authentication-bug`
- **Source**: Branch from `main`
- **Merge**: Merge to both `main` and `develop`
- **Lifespan**: Delete after merge

#### Release Branches (`release/*`)
- **Naming**: `release/version-number`
- **Examples**: `release/1.0.0`, `release/1.1.0`
- **Source**: Branch from `develop`
- **Merge**: Merge to `main` and back to `develop`
- **Purpose**: Final preparation for production release

## Workflow

### Feature Development
1. Create feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/1.1-project-setup
   ```

2. Develop feature with regular commits:
   ```bash
   git add .
   git commit -m "Add database models for coaching sessions"
   git push origin feature/1.1-project-setup
   ```

3. Create Pull Request to `develop`:
   - Use PR template
   - Request review from team members
   - Ensure CI passes
   - Address review feedback

4. Merge PR and delete feature branch

### Hotfix Process
1. Create hotfix branch from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-bug-fix
   ```

2. Fix the issue and test thoroughly

3. Create PRs to both `main` and `develop`

4. Deploy immediately after merge to `main`

### Release Process
1. Create release branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/1.0.0
   ```

2. Perform final testing and bug fixes

3. Update version numbers and documentation

4. Create PR to `main` for production release

5. After merge, tag the release:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

6. Merge release branch back to `develop`

## Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

### Examples
```
feat(auth): add OAuth2 authentication for coaches

Implement OAuth2 authentication flow using FastAPI-Users.
Includes login, logout, and token refresh endpoints.

Closes #23
```

```
fix(database): resolve connection pool timeout issue

Increase connection pool size and add retry logic for
database connections during high load periods.

Fixes #45
```

## Branch Protection Rules

### `main` Branch
- Require pull request reviews before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators in restrictions
- Allow force pushes: No
- Allow deletions: No

### `develop` Branch
- Require pull request reviews before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Allow force pushes: No
- Allow deletions: No

## CI/CD Integration

### Automated Checks
- **Linting**: Black, Flake8, MyPy
- **Testing**: pytest with coverage reporting
- **Security**: Bandit security scanning
- **Build**: Package building and artifact storage

### Deployment Triggers
- **Production**: Merge to `main` → Deploy to production
- **Staging**: Merge to `develop` → Deploy to staging
- **Preview**: Feature branches → Deploy to preview environment (optional)

## Best Practices

1. **Keep branches small and focused**: One feature per branch
2. **Regular syncing**: Sync with `develop` regularly to avoid conflicts
3. **Descriptive names**: Use clear, descriptive branch names
4. **Clean history**: Squash commits when merging if desired
5. **Testing**: Always run tests before creating PR
6. **Code review**: Never merge without code review
7. **Documentation**: Update docs with significant changes

## Emergency Procedures

### Critical Production Bug
1. Create hotfix branch from `main`
2. Fix issue with minimal changes
3. Fast-track review process
4. Deploy immediately
5. Monitor closely post-deployment
6. Post-mortem analysis

### Failed Deployment
1. Immediate rollback if possible
2. Create hotfix for critical issues
3. Full investigation before next deployment
4. Update deployment procedures if needed