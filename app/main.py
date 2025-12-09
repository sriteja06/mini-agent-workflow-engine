from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from app.engine.graph import Graph
from app.engine.registry import tool_registry
from app.engine.runner import GraphRunner
from app.schemas.graph import GraphCreateRequest, GraphCreateResponse
from app.schemas.run import (
    ExecutionStep,
    GraphRunRequest,
    GraphRunResponse,
    RunStateResponse,
)
from app.storage import (
    generate_id,
    get_graph,
    get_run,
    save_graph,
    save_run,
)
from app.workflows.code_review import register_code_review_tools

app = FastAPI(
    title="Mini Agent Workflow Engine",
    description=(
        "A small workflow/graph engine with nodes, edges, "
        "shared state, branching, and looping."
    ),
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event() -> None:
    """Register built-in tools on startup."""
    register_code_review_tools(tool_registry)


@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "message": "Mini agent workflow engine is running.",
        "docs": "/docs",
    }


@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(payload: GraphCreateRequest) -> GraphCreateResponse:
    """Create a new graph definition."""
    # Resolve tools from registry
    nodes: Dict[str, Any] = {}
    for node_name, tool_name in payload.nodes.items():
        try:
            nodes[node_name] = tool_registry.get(tool_name)
        except KeyError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Tool '{tool_name}' for node '{node_name}' not found",
            ) from exc

    # Validate edges
    for src, dst in payload.edges.items():
        if src not in nodes:
            raise HTTPException(
                status_code=400,
                detail=f"Edge source node '{src}' not defined in nodes",
            )
        if dst is not None and dst not in nodes:
            raise HTTPException(
                status_code=400,
                detail=f"Edge destination node '{dst}' not defined in nodes",
            )

    if payload.start_node not in nodes:
        raise HTTPException(
            status_code=400,
            detail=f"start_node '{payload.start_node}' not defined in nodes",
        )

    graph_id = generate_id()
    graph = Graph(
        graph_id=graph_id,
        name=payload.name,
        nodes=nodes,
        edges=payload.edges,
        start_node=payload.start_node,
    )

    save_graph(graph)
    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run", response_model=GraphRunResponse)
async def run_graph(payload: GraphRunRequest) -> GraphRunResponse:
    """Run an existing graph with an initial state."""
    graph = get_graph(payload.graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")

    runner = GraphRunner(graph)
    final_state, log_items = await runner.run(payload.initial_state)

    log: list[ExecutionStep] = [
        ExecutionStep(
            step=item["step"],
            node=item["node"],
            state=item["state"],
        )
        for item in log_items
    ]

    run_id = generate_id()
    save_run(run_id, final_state, status="completed")

    return GraphRunResponse(
        run_id=run_id,
        final_state=final_state,
        log=log,
    )


@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
async def get_run_state(run_id: str) -> RunStateResponse:
    """Return the current/final state of a workflow run."""
    record = get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunStateResponse(
        run_id=run_id,
        state=record["state"],
        status=record["status"],
    )
