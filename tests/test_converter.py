import unittest
from schema_bridge_ai.converter import convert_tool, convert_tools


class TestSchemaBridge(unittest.TestCase):
    def setUp(self):
        self.mcp_tool = {
            "name": "search_database",
            "description": "Searches customer records by query",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL or keyword filter"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of rows"
                    }
                },
                "required": ["query"]
            }
        }

    def test_mcp_to_openai(self):
        openai_tool = convert_tool(self.mcp_tool, "mcp", "openai")
        self.assertEqual(openai_tool["type"], "function")
        self.assertEqual(openai_tool["function"]["name"], "search_database")
        self.assertIn("properties", openai_tool["function"]["parameters"])

    def test_mcp_to_gemini(self):
        gemini_tool = convert_tool(self.mcp_tool, "mcp", "gemini")
        self.assertEqual(gemini_tool["name"], "search_database")
        # Gemini uses uppercase type names
        self.assertEqual(gemini_tool["parameters"]["type"], "OBJECT")
        self.assertEqual(gemini_tool["parameters"]["properties"]["query"]["type"], "STRING")
        self.assertEqual(gemini_tool["parameters"]["properties"]["limit"]["type"], "INTEGER")

    def test_gemini_to_anthropic(self):
        gemini_tool = convert_tool(self.mcp_tool, "mcp", "gemini")
        anthropic_tool = convert_tool(gemini_tool, "gemini", "anthropic")
        self.assertEqual(anthropic_tool["name"], "search_database")
        self.assertIn("input_schema", anthropic_tool)
        self.assertEqual(anthropic_tool["input_schema"]["type"], "object")
        self.assertEqual(anthropic_tool["input_schema"]["properties"]["query"]["type"], "string")


if __name__ == "__main__":
    unittest.main()
