# TerpSearch - AI Coding Agent Instructions

## Project Overview

**TerpSearch** is a modular search application with three main components:
- **Frontend**: React 19 SPA (Create React App bootstrap)
- **Backend**: Empty/planned (structure exists but no implementation)
- **Scraping**: Empty/planned (structure exists but no implementation)

The project is in early stages with only the frontend framework initialized.

## Architecture & Component Boundaries

### Frontend (`/frontend`)
- **Framework**: React 19 with Create React App (CRA)
- **Entry Point**: `src/index.js` → renders `App` component to `#root` DOM element
- **Main Component**: `App.js` (currently empty, ready for feature development)
- **Styling**: `App.css` (empty, scoped to App component)
- **Build System**: CRA's `react-scripts` (v5.0.1)
- **Target Title**: "Terp Search" (visible in browser tab, set in `public/index.html`)

### Backend & Scraping
Currently empty directories. When implemented:
- Clarify if backend is Node.js/Python/other
- Document data models and API contract with frontend
- Define scraping data sources and pipeline

## Critical Developer Workflows

### Frontend Development

**Start development server**:
```bash
cd frontend && npm start
```
- Runs on `http://localhost:3000`
- Hot-reloads on file changes
- Opens browser automatically

**Production build**:
```bash
cd frontend && npm run build
```
- Creates optimized bundle in `frontend/build/`
- Minified with hashed filenames
- Ready for deployment

**Run tests**:
```bash
cd frontend && npm test
```
- Jest-based, runs in watch mode by default
- Uses `@testing-library/react` for component testing

## Code Structure Conventions

### React Component Patterns
- Use functional components (React 19+)
- Entry point pattern: `src/index.js` mounts root component to `#root`
- CSS modules co-located with components (e.g., `App.js` + `App.css`)

### ESLint Configuration
- Extends `react-app` and `react-app/jest` presets (CRA defaults)
- No custom overrides configured yet

### Testing
- Test library: `@testing-library/react` v16.3.0
- Assertions: `@testing-library/jest-dom` v6.9.1
- User-event simulation: `@testing-library/user-event` v13.5.0

## Key Dependencies & Versions

| Package | Version | Purpose |
|---------|---------|---------|
| `react` | ^19.2.0 | Core framework |
| `react-dom` | ^19.2.0 | DOM rendering |
| `react-scripts` | 5.0.1 | CRA build tooling |
| `@testing-library/react` | ^16.3.0 | Component testing |

## Integration Points

- **Frontend ↔ Backend**: Not yet implemented. When defining API contracts, document expected endpoints and data schemas in this file.
- **Frontend ↔ Scraping**: No visible integration yet. Clarify if scraping feeds backend or runs separately.

## Project Setup Instructions

First-time setup:
```bash
# Clone and navigate
cd frontend

# Install dependencies
npm install

# Start development
npm start
```

## Next Steps for New Contributors

1. **Expand App.js**: Build initial feature (search interface, results display, etc.)
2. **Add styles**: Populate `App.css` or introduce component-level CSS
3. **Implement backend**: Define tech stack and API contract
4. **Implement scraping**: Define data sources and pipeline
5. **Document patterns**: Update this file as new conventions emerge

---

**Last updated**: November 2025  
**Status**: Framework initialized, feature development in progress
