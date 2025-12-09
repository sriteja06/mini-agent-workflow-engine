from typing import Callable, Dict


class ToolRegistry:
    """Simple tool registry mapping tool_name -> Python function."""

    def __init__(self) -> None:
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, fn: Callable) -> None:
        self._tools[name] = fn

    def get(self, name: str) -> Callable:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def list_tools(self) -> Dict[str, Callable]:
        return dict(self._tools)


tool_registry = ToolRegistry()
