import inspect
from typing import Any, Dict, List, Tuple

from .graph import Graph


async def _maybe_await(result: Any) -> Any:
    """Support both sync and async node functions."""
    if inspect.isawaitable(result):
        return await result
    return result


class GraphRunner:
    """Executes a Graph over a shared state dict.

    Supports:
    - Sequential edges
    - Branching via special key '__next_node' in state
    - Looping via the same mechanism (node can point back to itself or earlier nodes)
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    async def run(
        self,
        initial_state: Dict[str, Any],
        max_steps: int = 100,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        state: Dict[str, Any] = dict(initial_state)
        log: List[Dict[str, Any]] = []

        current = self.graph.start_node
        step = 0

        while current is not None:
            step += 1
            if step > max_steps:
                # Safety against infinite loops
                state["error"] = "max_steps_exceeded"
                break

            if current not in self.graph.nodes:
                state["error"] = f"Node '{current}' not found"
                break

            node_fn = self.graph.nodes[current]

            # Execute node
            result = await _maybe_await(node_fn(state))  # type: ignore[arg-type]
            if result is None:
                result = {}
            if not isinstance(result, dict):
                raise TypeError(
                    f"Node '{current}' must return a dict, got {type(result)}"
                )

            # Merge result into state
            state.update(result)

            # Log snapshot
            log.append(
                {
                    "step": step,
                    "node": current,
                    "state": dict(state),
                }
            )

            # Check for branching / looping override
            next_node = state.pop("__next_node", None)

            # If node didn't override, follow static edge
            if next_node is None:
                next_node = self.graph.edges.get(current)

            current = next_node

        return state, log
