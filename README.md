# Mini Agent Workflow Engine (AI Engineering Assignment)

This project is a minimal workflow / graph engine built with **FastAPI**.

It supports:

- Nodes as Python functions (tools) that read & modify a shared state
- Shared state as a dictionary flowing between nodes
- Edges to define execution order
- Branching & looping via a special `__next_node` key in state
- FastAPI endpoints to create and run graphs

The example workflow implemented is **Option A: Code Review Mini-Agent**:

1. `extract_functions`
2. `check_complexity`
3. `detect_basic_issues` (loops until `quality_score >= threshold`)
4. `suggest_improvements`

## How to Run

1. Create and activate a virtual environment (optional but recommended).

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI server from the project root:

```bash
uvicorn app.main:app --reload
```

4. Open the docs:

- Swagger UI: http://127.0.0.1:8000/docs
- Root: http://127.0.0.1:8000/

## Example Usage

### Create a Graph

`POST /graph/create`

Body:

```json
{
  "name": "code_review_workflow",
  "nodes": {
    "extract": "extract_functions",
    "complexity": "check_complexity",
    "detect": "detect_basic_issues",
    "suggest": "suggest_improvements"
  },
  "edges": {
    "extract": "complexity",
    "complexity": "detect",
    "detect": null,
    "suggest": null
  },
  "start_node": "extract"
}
```

### Run the Graph

`POST /graph/run`

Body:

```json
{
  "graph_id": "<graph_id_from_create>",
  "initial_state": {
    "code": "def foo():\n    print('hi')  # TODO: remove\n",
    "threshold": 7
  }
}
```

### Get Run State

`GET /graph/state/{run_id}`

Returns the final state and status.

## Possible Improvements

- WebSocket endpoint to stream logs step-by-step
- Async/background execution for long-running nodes
- Persist graphs and runs into a database (SQLite / Postgres)
- Simple UI to visualize graphs and runs
- More expressive branching conditions in the graph definition
