import sys
from typing import List, Optional, Dict, Set
from interpreter.non_terminal_expression.StateSetterExpression import StateSetterExpression
from interpreter.non_terminal_expression.VariableDeclarationExpression import VariableDeclarationExpression
from interpreter.non_terminal_expression.ConsoleCommandExpression import ConsoleCommandExpression
from interpreter.non_terminal_expression.ArrowFunctionExpression import ArrowFunctionExpression
from interpreter.non_terminal_expression.ArrayExpression import ArrayExpression
from interpreter.non_terminal_expression.BinaryExpression import BinaryExpression
from interpreter.terminal_expression.ValueIndicatorExpression import ValueIndicatorExpression
from interpreter.expression import Expression

class Context:
    def __init__(self, input_lines):
        self.errors = []
        self.input_lines = input_lines
        self.current_scope = "global"
        self.symbols = {}
        self.functions = set()
        self.imported_names = set()
        self.props = set()

    def declare_function(self, name: str, line: int):
        self.functions.add(name)
        print(f"Declared function: {name} at line {line}", file=sys.stderr)

    def add_symbol(self, name: str, scope: str, var_type=None, value=None):
        if scope not in self.symbols:
            self.symbols[scope] = {}
        self.symbols[scope][name] = {"type": var_type, "value": value}
        print(f"Added symbol {name} to scope {scope} with type {var_type}, value {value}", file=sys.stderr)

    def check_symbol(self, name: str, scope: str) -> dict:
        if scope in self.symbols and name in self.symbols[scope]:
            return self.symbols[scope][name]
        if name in self.imported_names or name in self.props:
            return {"type": "imported_or_prop", "value": None}
        return None

    def add_import(self, name: str):
        self.imported_names.add(name)

    def add_prop(self, name: str):
        self.props.add(name)

    def collect_identifiers(self, expr, identifiers: set):
        if isinstance(expr, ValueIndicatorExpression):
            identifiers.add(expr.name)
        elif isinstance(expr, StateSetterExpression):
            identifiers.add(expr.state_pair[0])
            identifiers.add(expr.state_pair[1])
            if expr.initial_value:
                self.collect_identifiers(expr.initial_value, identifiers)
        elif isinstance(expr, VariableDeclarationExpression):
            identifiers.add(expr.name)
            if expr.value:
                self.collect_identifiers(expr.value, identifiers)
        elif isinstance(expr, ConsoleCommandExpression):
            if expr.arg and isinstance(expr.arg, ValueIndicatorExpression):  
                self.collect_identifiers(expr.arg, identifiers)
        elif isinstance(expr, ArrowFunctionExpression):
            for content in expr.body:
                self.collect_identifiers(content, identifiers)
        elif isinstance(expr, ArrayExpression):
            for value in expr.values:
                self.collect_identifiers(value, identifiers)
        elif isinstance(expr, BinaryExpression):
            self.collect_identifiers(expr.left, identifiers)
            self.collect_identifiers(expr.right, identifiers)
        elif isinstance(expr, (list, tuple)):
            for item in expr:
                self.collect_identifiers(item, identifiers)

    def check_hook(self, hook_type: str, line: int, scope: str, callback: Expression = None, deps: List[str] = None, initial_value: Expression = None):
        print(f"Checking hook: {hook_type} at line {line}, scope: {scope}", file=sys.stderr)
        # Allow hooks in global scope for standalone testing
        if scope != "global" and (scope[0].islower() and not scope.startswith("use")):
            self.errors.append({
                "error": f"Invalid {hook_type} call at line {line}: Hooks can only be called inside a React component or custom hook.",
                "suggestion": f"Move the {hook_type} call inside a component function or a custom hook (function starting with 'use')."
            })
        if hook_type == "useState":
            if initial_value and isinstance(initial_value, ValueIndicatorExpression):
                if not self.check_symbol(initial_value.name, scope):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} uses undefined variable '{initial_value.name}' as initial value.",
                        "suggestion": f"Ensure '{initial_value.name}' is defined or use a valid initial value (e.g., 0, null)."
                    })
        if hook_type in ["useEffect", "useCallback"] and callback and deps is not None:
            identifiers = set()
            self.collect_identifiers(callback, identifiers)
            for ident in identifiers:
                if not self.check_symbol(ident, scope):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} references undefined variable '{ident}'.",
                        "suggestion": f"Ensure '{ident}' is defined (e.g., via useState or props) before using it in {hook_type}."
                    })
                
                elif ident not in deps and ident not in self.props and ident not in self.symbols.get("global", set()):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} has missing dependency: '{ident}' is used but not in the dependency array.",
                        "suggestion": f"Add '{ident}' to the dependency array."
                    })
            
            if not deps and identifiers and not all(ident in self.symbols.get("global", set()) for ident in identifiers):
                self.errors.append({
                    "error": f"{hook_type} at line {line} uses variables {identifiers} but has an empty dependency array, which may cause stale closures.",
                    "suggestion": f"Include used variables {identifiers} in the dependency array or remove them from the {hook_type} callback."
                })
            if hook_type == "useEffect":
                has_persistent_side_effect = False
                if has_persistent_side_effect:
                    self.errors.append({
                        "error": f"{hook_type} at line {line} sets up a persistent side effect but lacks a cleanup function.",
                        "suggestion": f"Return a cleanup function from useEffect (e.g., clearInterval) to prevent memory leaks."
                    })