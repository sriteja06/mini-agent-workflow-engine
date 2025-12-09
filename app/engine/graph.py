from typing import Any, Callable, Dict, Optional


class Graph:
    """Minimal graph representation.

    Attributes:
        id: Graph identifier.
        name: Human-friendly name.
        nodes: Mapping from node name -> Python callable (tool).
        edges: Mapping from node name -> next node name (or None for end).
        start_node: Entry node name.
    """

    def __init__(
        self,
        graph_id: str,
        name: str,
        nodes: Dict[str, Callable[[Dict[str, Any]], Any]],
        edges: Dict[str, Optional[str]],
        start_node: str,
    ) -> None:
        self.id = graph_id
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node
