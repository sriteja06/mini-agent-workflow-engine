import uuid
from typing import Any, Dict, Optional

from app.engine.graph import Graph

# In-memory stores
GRAPHS: Dict[str, Graph] = {}
RUNS: Dict[str, Dict[str, Any]] = {}


def generate_id() -> str:
    return uuid.uuid4().hex


def save_graph(graph: Graph) -> None:
    GRAPHS[graph.id] = graph


def get_graph(graph_id: str) -> Optional[Graph]:
    return GRAPHS.get(graph_id)


def save_run(run_id: str, state: Dict[str, Any], status: str) -> None:
    RUNS[run_id] = {
        "state": state,
        "status": status,
    }


def get_run(run_id: str) -> Optional[Dict[str, Any]]:
    return RUNS.get(run_id)
