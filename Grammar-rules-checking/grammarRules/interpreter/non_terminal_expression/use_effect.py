from typing import List, Optional, Set
from ..expression import Expression
from ..context import Context



class UseEffectExpression(Expression):
    def __init__(self, callback: Optional[Expression], deps: List[str], line: int):
        self.callback = callback
        self.deps = deps
        self.line = line

    def interpret(self, context: Context) -> None:
        # Kiểm tra hook trong điều kiện
        inside_conditional = any(path in ["if", "else"] for path in context.execution_path)
        context.track_hook_call("useEffect", self.line, inside_conditional)

        # Kiểm tra dependency
        if self.callback:
            context.execution_path.append("useEffect")
            self.callback.interpret(context)
            context.execution_path.pop()
            # Phân tích các biến được sử dụng trong callback
            used_vars = self._extract_used_vars(self.callback)
            for var in used_vars:
                if var not in self.deps:
                    context.errors.append(
                        f"Error at line {self.line}: Variable '{var}' used in useEffect but not in dependency array."
                    )

    def _extract_used_vars(self, callback: Expression) -> Set[str]:
        # Giả lập phân tích biến được sử dụng (cần mở rộng thêm)
        return set()  # Ví dụ: trả về các biến như 'x', 'y'