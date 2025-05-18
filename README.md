# PPL-DEBUGGING-PROJECT

# HookScope - Static Analysis of React Hook Dependencies

## Project Overview

**HookScope** is a static code analysis and debugging tool tailored for React applications, focusing on the `useEffect` hook. It parses JSX code to ensure compliance with dependency rules, identifying missing dependencies in `useEffect` hooks and delivering feedback through an interactive, chat-like interface. Developed for the Principles of Programming Languages (PPL) course, HookScope utilizes ANTLR for JSX parsing, integrating a modern React-based frontend with a NodeJS backend.

**Topic**: Static Analysis of React Hook Dependencies Using ANTLR-Based JSX Parsing

**Key Objectives**:

- Parse JSX code using a custom ANTLR grammar (`ReactHookAnalyzer.g4`).
- Detect variables used in `useEffect` callbacks and verify their inclusion in the dependency array.
- Provide actionable feedback (e.g., "Missing dependency 'seconds' at line 3") via a chat-like UI.
- Support analysis of multiple `useEffect` hooks within a single component.
- Offer a polished user experience with CodeMirror for code input and styled feedback.

**Example**:

```jsx
function Timer() {
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(seconds + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);
  return <div>Seconds: {seconds}</div>;
}
```

**Output**: "Missing dependency 'seconds' at line 3"

## Features

- **Dependency Checking**: Identifies missing dependencies in `useEffect` hooks with line-specific error messages.
- **Multiple Hook Support**: Analyzes all `useEffect` hooks in a component, reporting errors for each.
- **JSX Parsing**: Employs ANTLR 4.9.2 to tokenize and parse JSX syntax accurately.
- **Interactive UI**: Features a chat-like interface with CodeMirror for code input and feedback bubbles (red for errors, green for success).
- **Extensibility**: Designed to potentially support other React hooks (e.g., `useMemo`, `useCallback`).

## Technologies Used

- **Frontend**:
  - React (with Vite for fast development)
  - CodeMirror (code editor for JSX input)
  - CSS or any styling library/framework (e.g., Tailwind CSS, Bootstrap, styled-components)
- **Backend**:
  - NodeJS with Express (API to execute grammar checks)
  - Python (runs ANTLR-generated lexer/parser via `run.py`)
- **Grammar Rules**:
  - ANTLR 4.9.2 (generates lexer/parser from `ReactHookAnalyzer.g4`)
  - Custom grammar for JSX and `useEffect` dependency analysis

## Team Workflow

- **Team Size**: 3 members
- **Communication**:
  - **Group Chat**: Post project updates in the group chat. Respond within 12 hours.
  - **Online Meetings**: Conduct meetings twice weekly (mid-week and weekend) via Zoom to discuss progress and align tasks.
- **Task Updates**: Contact the project lead or relevant member for task-specific details.
- **Agile Methodology**: Follow an Agile-like approach with daily updates to track progress.
- **Progress Tracking**: Use **Notion** for task management and documentation:
  - Tasks are organized in a Kanban board (To Do, In Progress, Done) with assignees and deadlines.
  - Documentation (e.g., grammar rules, meeting notes, report drafts) is stored in Notion pages.
  - Timeline view tracks progress across the 5-week project timeline.

### Daily Update Format

Each team member provides a daily update in the following format, posted in the group chat or Notion:

```
Date: [Current Date]
- Yesterday: [Tasks worked on]
- Progress: [Percentage completed]
- Today: [Tasks planned]
- Estimate: [Time estimate for completion]
```

**Example**:

```
Date: 24/04/2025
- Yesterday: Developed grammar rules for useEffect dependency checking
- Progress: 30%
- Today: Test grammar with example components
- Estimate: 4 hours to complete
```

## Git Practices

### Branch Management

1. **Updating Code**: Regularly pull the latest code from the `main` branch to your feature branch to stay updated and check for conflicts.
2. **Merging**: After completing a task, pull the latest `main` branch and merge it into your feature branch before pushing.
3. **Pull Requests**: Create a pull request to merge your branch into `main`. Notify the project lead for review before merging.

### Commit Naming Conventions

- **Title**: Short (≤50 characters), start with a capitalized verb (e.g., "Add", "Fix", "Update").
- **Description**: Provide detailed description if necessary.
- **Avoid Abbreviations**: Use clear language.

**Commit Prefixes**:

- `fix`: Bug fixes
- `add`: New features or resources
- `update`: Updates to features, or configurations
- `remove`: Removing features or files
- `refactor`: Code refactoring
- `chore`: Maintenance tasks
- `docs`: Documentation updates
- `style`: Code style improvements
- `test`: Adding/modifying tests
- `ci`: CI/CD updates

**Example**:

```
fix: Resolve missing dependency detection in useEffect
```

## Project Deadline

- **Final Submission**: 04/06/2025

## Contributing

HookScope is an open-source project. Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Follow the Git Practices and Commit Naming Conventions outlined above.

## Additional Libraries

python-dotenv: pip install python-dotenv

## Note

This README will be updated as the project progresses. For questions, contact the project lead via the group chat or raise issues on the GitHub repository.

---

**HookScope Team, April 2025**
