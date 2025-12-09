from typing import Any, Dict, List

from app.engine.registry import ToolRegistry


async def extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    """Very simple function extractor: counts occurrences of 'def ' in the code."""
    code: str = state.get("code", "") or ""
    function_count = code.count("def ")
    return {"functions": function_count}


async def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    """Dummy complexity checker based on code length and number of functions."""
    code: str = state.get("code", "") or ""
    functions: int = state.get("functions", 1) or 1

    base_score = len(code) // 100
    complexity = max(1, min(10, base_score + functions))

    return {"complexity": complexity}


async def detect_basic_issues(state: Dict[str, Any]) -> Dict[str, Any]:
    """Detects basic smells and computes a quality score.

    Also sets '__next_node' to implement branching + looping until
    quality_score >= threshold.
    """
    code: str = state.get("code", "") or ""

    issues = 0
    issue_list: List[str] = []

    if "TODO" in code:
        issues += 1
        issue_list.append("Unresolved TODO comments found.")

    if "print(" in code:
        issues += 1
        issue_list.append("Debug prints found. Consider using logging.")

    if len(code) > 800:
        issues += 1
        issue_list.append("File is quite large. Consider splitting into modules.")

    quality_score = max(1, 10 - issues)
    threshold = state.get("threshold", 7)

    if quality_score >= threshold:
        next_node = "suggest_improvements"
    else:
        # Loop: run this node again
        next_node = "detect_basic_issues"

    return {
        "issues": issues,
        "issue_details": issue_list,
        "quality_score": quality_score,
        "__next_node": next_node,
    }


async def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest improvements based on detected issues and complexity."""
    suggestions: List[str] = []
    code: str = state.get("code", "") or ""
    complexity: int = state.get("complexity", 5)
    issues: int = state.get("issues", 0)

    if "print(" in code:
        suggestions.append("Replace print statements with a proper logger.")

    if "TODO" in code:
        suggestions.append("Resolve TODO comments or create proper tasks/tickets.")

    if len(code) > 800:
        suggestions.append("Split long files into smaller, focused modules.")

    if complexity > 7:
        suggestions.append("Refactor large functions into smaller, reusable ones.")

    if issues == 0 and complexity <= 7:
        suggestions.append("Code looks good overall. No major issues detected.")

    return {"suggestions": suggestions}


def register_code_review_tools(registry: ToolRegistry) -> None:
    """Register all tools for this workflow into the global registry."""
    registry.register("extract_functions", extract_functions)
    registry.register("check_complexity", check_complexity)
    registry.register("detect_basic_issues", detect_basic_issues)
    registry.register("suggest_improvements", suggest_improvements)
