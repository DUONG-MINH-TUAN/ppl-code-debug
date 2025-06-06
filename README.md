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

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Python installed for the Grammar Checker.
- Ensure all project dependencies are installed by running `npm install` in the respective folders.

### Running the Project

1. **Start the Backend**:

   - Open a terminal window.
   - Navigate to the backend folder:
     cd ppl-code-debug\my-react-app\api
   - Run the backend server:
     npm start
   - The backend should now be running on port 3000 (or the port specified in your configuration). You’ll see a message like "Server running on port 3000" in the terminal.

2. **Start the Frontend**:

   - Open a new terminal window (keep the backend terminal running).
   - Navigate to the frontend folder:
     cd ppl-code-debug\my-react-app
   - Start the React development server:
     npm run dev
   - The frontend should now be running, and you’ll see a message in the terminal with a link like "http://localhost:5173/".
   - Press Ctrl + click on the link (http://localhost:5173/) to open the chat interface in your default web browser.

3. **Use the Chat Interface to Check Grammar**:
   - Once the chat interface loads, enter your JSX code into the CodeMirror editor. For example:
     ```jsx
     import { useState, useEffect } from "react";
     function App() {
       const [data, setData] = useState("");
       useEffect(() => {
         setData("Hello");
       }, []);
       return <div>{data}</div>;
     }
     ```
   - Submit the code by pressing Enter or clicking the send button.
   - The frontend will send the code to the backend, which will process it using the Grammar Checker (implemented in Python via `run.py`).
   - The response will appear in the chat interface:
     - If the code is valid, you’ll see a green feedback bubble: "Input accepted".
     - If there are errors, you’ll see a red feedback bubble with details, such as "Missing dependency 'seconds' at line 3".

### Troubleshooting

- If the backend fails to start, ensure port 3000 is not in use and check for missing dependencies (`npm install`).
- If the frontend doesn’t load, confirm you’ve run `npm install` in the `my-react-app` folder and that port 5173 is available.
- If the Grammar Checker fails (e.g., no response or errors about `run.py`), verify Python is installed and that the backend is correctly routing requests to the Python process.

## Contributing

HookScope is an open-source project. Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Follow the Git Practices and Commit Naming Conventions outlined above.

## Additional Libraries

python-dotenv: pip install python-dotenv

## Note

This README will be updated as the project progresses. For questions, contact the project lead via the group chat or raise issues on the GitHub repository.

---

**HookScope Team, April 2025**
