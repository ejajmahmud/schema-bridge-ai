"""
Core schema conversion logic for OpenAI, Anthropic, Gemini, and MCP.
"""

from typing import Any, Dict, List, Union
from dataclasses import dataclass


JSON_TO_GEMINI_TYPES = {
    "string": "STRING",
    "number": "NUMBER",
    "integer": "INTEGER",
    "boolean": "BOOLEAN",
    "array": "ARRAY",
    "object": "OBJECT"
}

GEMINI_TO_JSON_TYPES = {v: k for k, v in JSON_TO_GEMINI_TYPES.items()}


def transform_schema_types(schema: Any, target_flavor: str) -> Any:
    """Recursively converts type strings between JSON standard (lowercase) and Gemini (UPPERCASE)."""
    if not isinstance(schema, dict):
        return schema

    res: Dict[str, Any] = {}
    for k, v in schema.items():
        if k == "type" and isinstance(v, str):
            if target_flavor == "gemini":
                res[k] = JSON_TO_GEMINI_TYPES.get(v.lower(), v.upper())
            else:
                res[k] = GEMINI_TO_JSON_TYPES.get(v.upper(), v.lower())
        elif k == "properties" and isinstance(v, dict):
            res[k] = {prop: transform_schema_types(val, target_flavor) for prop, val in v.items()}
        elif k == "items" and isinstance(v, dict):
            res[k] = transform_schema_types(v, target_flavor)
        else:
            res[k] = v
    return res


@dataclass
class ToolDeclaration:
    name: str
    description: str
    parameters: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], source_format: str) -> "ToolDeclaration":
        source_format = source_format.lower()
        if source_format == "openai":
            # OpenAI format: {"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}
            # or direct {"name": ..., "parameters": ...}
            fn = data.get("function", data)
            return cls(
                name=fn.get("name", ""),
                description=fn.get("description", ""),
                parameters=transform_schema_types(fn.get("parameters", {}), "standard")
            )
        elif source_format == "anthropic":
            return cls(
                name=data.get("name", ""),
                description=data.get("description", ""),
                parameters=transform_schema_types(data.get("input_schema", {}), "standard")
            )
        elif source_format in ("mcp", "modelcontextprotocol"):
            return cls(
                name=data.get("name", ""),
                description=data.get("description", ""),
                parameters=transform_schema_types(data.get("inputSchema", {}), "standard")
            )
        elif source_format in ("gemini", "google"):
            # Gemini parameters can be in "parameters" with UPPERCASE types
            params = data.get("parameters", {})
            return cls(
                name=data.get("name", ""),
                description=data.get("description", ""),
                parameters=transform_schema_types(params, "standard")
            )
        else:
            raise ValueError(f"Unknown source format: {source_format}")

    def to_format(self, target_format: str) -> Dict[str, Any]:
        target_format = target_format.lower()
        if target_format == "openai":
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": transform_schema_types(self.parameters, "standard")
                }
            }
        elif target_format == "anthropic":
            return {
                "name": self.name,
                "description": self.description,
                "input_schema": transform_schema_types(self.parameters, "standard")
            }
        elif target_format in ("mcp", "modelcontextprotocol"):
            return {
                "name": self.name,
                "description": self.description,
                "inputSchema": transform_schema_types(self.parameters, "standard")
            }
        elif target_format in ("gemini", "google"):
            return {
                "name": self.name,
                "description": self.description,
                "parameters": transform_schema_types(self.parameters, "gemini")
            }
        else:
            raise ValueError(f"Unknown target format: {target_format}")


def convert_tool(tool_dict: Dict[str, Any], source_format: str, target_format: str) -> Dict[str, Any]:
    decl = ToolDeclaration.from_dict(tool_dict, source_format)
    return decl.to_format(target_format)


def convert_tools(
    tools: Union[List[Dict[str, Any]], Dict[str, Any]],
    source_format: str,
    target_format: str
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    if isinstance(tools, list):
        return [convert_tool(t, source_format, target_format) for t in tools]
    elif isinstance(tools, dict):
        # Could be {"tools": [...]} container
        if "tools" in tools and isinstance(tools["tools"], list):
            return {
                "tools": [convert_tool(t, source_format, target_format) for t in tools["tools"]]
            }
        return convert_tool(tools, source_format, target_format)
    else:
        raise TypeError("tools must be a dict or list of dicts")
