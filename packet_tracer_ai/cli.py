"""CLI wrapper for planning and validating Packet Tracer labs via packet-tracer-mcp."""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any


def parse_request(request: str) -> dict[str, Any]:
    """Convert common natural-language requirements to MCP planning arguments."""
    text = request.lower()
    args: dict[str, Any] = {
        "routers": 1 if re.search(r"\b(one|1)\s+router\b", text) else 2,
        "pcs_per_lan": 3,
        "switches_per_router": 1,
        "servers": 0,
        "access_points": 0,
        "has_wan": bool(re.search(r"\bwan\b|internet|branch", text)),
        "dhcp": not bool(re.search(r"\b(no|without|disable)\s+dhcp\b", text)),
        "routing": "ospf" if "ospf" in text else "eigrp" if "eigrp" in text else "rip" if re.search(r"\brip\b", text) else "static",
        "router_model": "2911",
        "switch_model": "2960-24TT",
        "template": "router_on_a_stick" if "router-on-a-stick" in text or "router on a stick" in text else "multi_lan",
        "vlans": 0,
        "dual_stack": "ipv6" in text or "dual stack" in text,
        "wireless_laptops": "wireless" in text or "wi-fi" in text or "wifi" in text,
        "deploy": False,
    }
    m = re.search(r"\b(\d+)\s+routers?\b", text)
    if m:
        args["routers"] = max(1, min(10, int(m.group(1))))
    m = re.search(r"\b(\d+)\s+(?:pcs?|computers?)\s+per\s+lan\b", text)
    if m:
        args["pcs_per_lan"] = max(0, min(50, int(m.group(1))))
    m = re.search(r"\b(\d+)\s+vlans?\b", text)
    if m:
        args["vlans"] = max(0, min(100, int(m.group(1))))
    if "single lan" in text:
        args["template"] = "single_lan"
    elif "hub and spoke" in text or "hub-spoke" in text:
        args["template"] = "hub_spoke"
    elif "three router triangle" in text:
        args["template"] = "three_router_triangle"
        args["routers"] = 3
    elif args["has_wan"]:
        args["template"] = "multi_lan_wan"
    return args


def result_text(result: Any) -> str:
    return "\n".join(getattr(item, "text", str(item)) for item in (getattr(result, "content", None) or []))


def extract_json(response: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    for index, char in enumerate(response):
        if char != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(response[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


async def run(request: str, name: str, output: str, validate_only: bool) -> int:
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        print("Missing dependency. Run: python -m pip install -e .", file=sys.stderr)
        return 2

    params = StdioServerParameters(command=sys.executable, args=["-m", "packet_tracer_mcp", "--stdio"])
    print("Request:", request)
    print("Deployment disabled; this command only plans, validates and optionally exports.")
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                planned = await session.call_tool("pt_plan_topology", arguments=parse_request(request))
                plan_output = result_text(planned)
                print("\n=== PLAN ===\n" + plan_output)
                if getattr(planned, "isError", False):
                    return 1
                plan = extract_json(plan_output)
                if plan is None:
                    print("Could not extract plan JSON safely; export skipped.", file=sys.stderr)
                    return 1
                validated = await session.call_tool("pt_validate_plan", arguments={"plan_json": json.dumps(plan)})
                validation_output = result_text(validated)
                print("\n=== VALIDATION ===\n" + validation_output)
                if getattr(validated, "isError", False):
                    print("Validation failed; export skipped.", file=sys.stderr)
                    return 1
                if validate_only:
                    print("Validate-only mode: no files exported and no devices deployed.")
                    return 0
                exported = await session.call_tool(
                    "pt_export",
                    arguments={"plan_json": json.dumps(plan), "project_name": name, "output_dir": str(Path(output))},
                )
                print("\n=== EXPORT ===\n" + result_text(exported))
                return 1 if getattr(exported, "isError", False) else 0
    except Exception as exc:
        print("Automation failed:", exc, file=sys.stderr)
        print("Verify packet-tracer-mcp is installed and starts with python -m packet_tracer_mcp --stdio.", file=sys.stderr)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan, validate and export Packet Tracer lab artifacts.")
    parser.add_argument("request", nargs="?", default="2 routers, 3 PCs per LAN, OSPF and DHCP")
    parser.add_argument("--name", default="packet-tracer-project")
    parser.add_argument("--output", default="projects")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args.request, args.name, args.output, args.validate_only)))


if __name__ == "__main__":
    main()
