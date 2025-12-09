from typing import Any, Dict, List

from pydantic import BaseModel


class ExecutionStep(BaseModel):
    step: int
    node: str
    state: Dict[str, Any]


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = {}


class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[ExecutionStep]


class RunStateResponse(BaseModel):
    run_id: str
    state: Dict[str, Any]
    status: str
