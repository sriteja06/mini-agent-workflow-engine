from typing import Dict, Optional

from pydantic import BaseModel, Field


class GraphCreateRequest(BaseModel):
    """Input to /graph/create.

    nodes: mapping node_name -> tool_name (must exist in ToolRegistry)
    edges: mapping node_name -> next_node_name (or null for end)
    """

    name: str = Field(..., example="code_review_workflow")
    nodes: Dict[str, str]
    edges: Dict[str, Optional[str]]
    start_node: str = Field(..., example="extract")


class GraphCreateResponse(BaseModel):
    graph_id: str
