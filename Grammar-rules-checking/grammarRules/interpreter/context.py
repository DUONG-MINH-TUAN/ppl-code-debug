from typing import List, Optional, Dict, Set

class Context:
    def __init__(self, input_lines: List[str]):
        self.scopes = [set()]  # Stack of symbol tables
        self.function_names = set()  # Track function names
        self.errors = []  # List of errors
        self.input_lines = input_lines  # List of input lines
        self.tag_stack = []  # Stack of tags
        self.imported_hooks = set()  # Set of imported hooks
        self.variables = [{}]  # Stack of variable values
        self.hook_calls = []  # Theo dõi các lời gọi hook
        self.loop_counters = {}  # Theo dõi vòng lặp để phát hiện vô hạn
        self.execution_path = []  # Theo dõi đường dẫn thực thi

    def enter_scope(self):
        self.scopes.append(set())
        self.variables.append({})

    def exit_scope(self):
        self.scopes.pop()
        self.variables.pop()

    def declare_variable(self, name: str, line: int, value=None, initialized: bool = False) -> Optional[str]:
        if name in self.scopes[-1]:
            return f"Error at line {line}: Duplicate variable '{name}' in the same scope."
        self.scopes[-1].add(name)
        self.variables[-1][name] = {"value": value, "initialized": initialized}
        return None

    def get_variable(self, name: str, line: int):
        for scope in reversed(self.variables):
            if name in scope:
                if not scope[name]["initialized"]:
                    self.errors.append(f"Error at line {line}: Variable '{name}' used before initialization.")
                return scope[name]["value"]
        self.errors.append(f"Error at line {line}: Undefined variable '{name}'.")
        return None

    def set_variable(self, name: str, value, line: int):
        for scope in reversed(self.variables):
            if name in scope:
                scope[name]["value"] = value
                scope[name]["initialized"] = True
                return
        self.errors.append(f"Error at line {line}: Undefined variable '{name}'.")

    def track_hook_call(self, hook: str, line: int, inside_conditional: bool = False):
        if inside_conditional:
            self.errors.append(f"Error at line {line}: Hook '{hook}' called inside conditional block.")
        self.hook_calls.append((hook, line))

    def track_loop(self, loop_id: str, line: int, max_iterations: int = 1000):
        if loop_id not in self.loop_counters:
            self.loop_counters[loop_id] = 0
        self.loop_counters[loop_id] += 1
        if self.loop_counters[loop_id] > max_iterations:
            self.errors.append(f"Error at line {line}: Potential infinite loop detected at loop ID '{loop_id}'.")

    def track_function_call(self, func_name: str, line: int, max_calls: int = 1000):
        call_id = f"{func_name}_{line}"
        if call_id not in self.loop_counters:
            self.loop_counters[call_id] = 0
        self.loop_counters[call_id] += 1
        if self.loop_counters[call_id] > max_calls:
            self.errors.append(f"Warning at line {line}: Function '{func_name}' called too many times ({self.loop_counters[call_id]} calls). Potential performance issue.")

    def declare_function(self, name: str, line: int) -> Optional[str]:
        """Khai báo một function trong context."""
        if name in self.function_names:
            return f"Error at line {line}: Function '{name}' is already declared."
        self.function_names.add(name)
        return None