# Schema Bridge AI 🌉

<p align="center">
  <img src="assets/architecture.svg" alt="Schema Bridge AI Universal Transpiler" width="100%">
</p>

<p align="center">
  <a href="https://github.com/ejajmahmud/schema-bridge-ai/releases"><img src="https://img.shields.io/github/v/release/ejajmahmud/schema-bridge-ai?color=blue&label=version" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python 3.9+"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-Compatible-10b981.svg" alt="MCP Compatible"></a>
  <a href="https://github.com/ejajmahmud/schema-bridge-ai/actions"><img src="https://img.shields.io/badge/tests-passing-brightgreen.svg" alt="Tests"></a>
</p>

**Schema Bridge AI** is a universal, lossless tool and function declaration transpiler across modern AI ecosystems:
- **Model Context Protocol (MCP)** (`inputSchema`)
- **Google Gemini** (`parameters` with uppercase types: `STRING`, `OBJECT`, `INTEGER`, etc.)
- **OpenAI** (`type: "function"`, `parameters`)
- **Anthropic Claude** (`input_schema`)

---

## ⚡ Universal Translation Topology

```mermaid
graph TD
    MCP["Model Context Protocol (MCP)<br/>inputSchema"] <--> SB(("⚡ Schema Bridge<br/>Normalization Engine"))
    GEM["Google Gemini API<br/>parameters (OBJECT, STRING)"] <--> SB
    OAI["OpenAI Tool Call<br/>function.parameters"] <--> SB
    ANT["Anthropic Claude<br/>input_schema"] <--> SB

    style SB fill:#111827,stroke:#10b981,stroke-width:3px,color:#34d399
    style MCP fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff
    style GEM fill:#1e293b,stroke:#818cf8,stroke-width:2px,color:#fff
    style OAI fill:#1e293b,stroke:#10b981,stroke-width:2px,color:#fff
    style ANT fill:#1e293b,stroke:#f59e0b,stroke-width:2px,color:#fff
```

---

## 📊 Type Mapping Matrix

| Abstract Type | Standard JSON / MCP | Google Gemini SDK | OpenAI Function | Anthropic Claude |
|---|---|---|---|---|
| String | `"type": "string"` | `"type": "STRING"` | `"type": "string"` | `"type": "string"` |
| Integer | `"type": "integer"` | `"type": "INTEGER"` | `"type": "integer"` | `"type": "integer"` |
| Float / Number | `"type": "number"` | `"type": "NUMBER"` | `"type": "number"` | `"type": "number"` |
| Boolean | `"type": "boolean"` | `"type": "BOOLEAN"` | `"type": "boolean"` | `"type": "boolean"` |
| Object | `"type": "object"` | `"type": "OBJECT"` | `"type": "object"` | `"type": "object"` |
| Array | `"type": "array"` | `"type": "ARRAY"` | `"type": "array"` | `"type": "array"` |

---

## 📦 Installation

```bash
git clone https://github.com/ejajmahmud/schema-bridge-ai.git
cd schema-bridge-ai
pip install -e .
```

---

## 🚀 Quickstart

### Python SDK

```python
from schema_bridge_ai import convert_tool

mcp_tool = {
    "name": "calculate_tax",
    "description": "Calculates sales tax",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "state": {"type": "string"}
        },
        "required": ["amount", "state"]
    }
}

# Convert MCP tool directly to Gemini format with uppercase type normalization
gemini_tool = convert_tool(mcp_tool, source_format="mcp", target_format="gemini")
print(gemini_tool)
```

### CLI Command

```bash
# Convert an MCP tool list to OpenAI format
schema-bridge tools_mcp.json --from mcp --to openai -o tools_openai.json

# Convert OpenAI functions to Gemini format
schema-bridge functions.json --from openai --to gemini -o gemini_tools.json
```

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests
```

---

## 📄 License

MIT © [Ejaj Mahmud](https://github.com/ejajmahmud)
