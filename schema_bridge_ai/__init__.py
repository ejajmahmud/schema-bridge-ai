"""
Schema Bridge AI
Universal tool declaration transpiler across OpenAI, Anthropic, Gemini, and MCP.
"""

from .converter import ToolDeclaration, convert_tools, convert_tool

__version__ = "0.1.0"
__all__ = ["ToolDeclaration", "convert_tools", "convert_tool"]
