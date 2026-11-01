"""
CLI Interface for Schema Bridge AI.
"""

import argparse
import json
import sys
from .converter import convert_tools


def main():
    parser = argparse.ArgumentParser(
        prog="schema-bridge",
        description="Universal tool declaration transpiler across OpenAI, Anthropic, Gemini, and MCP"
    )
    parser.add_argument("input_file", help="Path to JSON file containing tool or array of tools")
    parser.add_argument("--from", dest="from_format", required=True, choices=["openai", "anthropic", "gemini", "mcp"], help="Source schema format")
    parser.add_argument("--to", dest="to_format", required=True, choices=["openai", "anthropic", "gemini", "mcp"], help="Target schema format")
    parser.add_argument("-o", "--output", help="Optional output JSON file (defaults to stdout)")

    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    converted = convert_tools(data, args.from_format, args.to_format)
    out_str = json.dumps(converted, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_str)
        print(f"Successfully converted tool(s) from {args.from_format} -> {args.to_format} to {args.output}")
    else:
        sys.stdout.write(out_str + "\n")


if __name__ == "__main__":
    main()
