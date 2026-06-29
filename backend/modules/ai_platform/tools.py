"""
Enterprise Tool Invocation Framework (EP-08).
Controlled tool execution — every tool requires explicit permission checks.
No unrestricted LLM tool access is permitted.
"""
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger("AIPlatform.Tools")


class ToolPermissionError(Exception):
    pass


class EnterpriseTool:
    """Represents a registered, permission-controlled enterprise tool."""
    def __init__(self, name: str, description: str, required_roles: List[str]):
        self.name = name
        self.description = description
        self.required_roles = set(r.upper() for r in required_roles)


class EnterpriseToolRegistry:
    """
    Controlled registry of tools the AI may invoke.
    Every tool call is:
      1. Matched to a registered tool.
      2. Permission-checked against user roles.
      3. Executed via the appropriate enterprise service.
      4. Audited.
    
    No direct database access. No shell access. No file system access.
    """

    def __init__(self):
        self._tools: Dict[str, EnterpriseTool] = {}
        self._handlers: Dict[str, Any] = {}

    def register(self, tool: EnterpriseTool, handler) -> None:
        self._tools[tool.name] = tool
        self._handlers[tool.name] = handler
        logger.info(f"Registered enterprise tool: '{tool.name}'")

    async def invoke(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        user_roles: List[str]
    ) -> Dict[str, Any]:
        tool = self._tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' is not registered.")

        # Permission check
        caller_roles = set(r.upper() for r in user_roles)
        if tool.required_roles and not (caller_roles & tool.required_roles):
            raise ToolPermissionError(
                f"User lacks required roles {tool.required_roles} to invoke tool '{tool_name}'."
            )

        handler = self._handlers[tool_name]
        logger.info(f"Invoking enterprise tool: '{tool_name}' with params {list(parameters.keys())}")

        result = await handler(**parameters)
        return {"tool": tool_name, "result": result}

    def list_tools(self, user_roles: Optional[List[str]] = None) -> List[Dict]:
        caller_roles = set(r.upper() for r in (user_roles or []))
        return [
            {
                "name": t.name,
                "description": t.description,
                "available": not t.required_roles or bool(caller_roles & t.required_roles)
            }
            for t in self._tools.values()
        ]
