# AI-Powered Cisco Packet Tracer Automation

A starter automation tool for planning, validating, and exporting Cisco Packet Tracer lab artifacts through the `packet-tracer-mcp` MCP server.

## Features

- Plain-English request parser for common network lab requirements.
- MCP integration with `pt_plan_topology`, `pt_validate_plan`, and `pt_export`.
- Safe default: it does not deploy devices automatically.
- Unit tests and GitHub Actions CI.
- Keeps the existing Packet Tracer project, topology image, and `configs/` files as reference artifacts.

## Requirements

- Python 3.10+
- `packet-tracer-mcp` installed in the same Python environment
- MCP server starts with `python -m packet_tracer_mcp --stdio`

## Install

```powershell
python -m pip install -e .
```

If the shell cannot find the command, use:

```powershell
python -m packet_tracer_ai.cli --help
```

## Example: VLANs, router-on-a-stick and DHCP

```powershell
packet-tracer-ai "1 router, 3 VLANs, router-on-a-stick and DHCP" --name VTP-EtherChannel-DHCP --validate-only
```

To also request artifact export:

```powershell
packet-tracer-ai "1 router, 3 VLANs, router-on-a-stick and DHCP" --name VTP-EtherChannel-DHCP --output projects
```

The parser currently maps a limited set of common phrases to planning parameters; it is not a general-purpose LLM. Review the plan and validation output. Export behavior depends on the installed MCP server and does not guarantee a native `.pkt` file.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Existing lab artifacts

- `vtp_etherchannel_dhcp_topology.pkt` — existing Packet Tracer project
- `vtp_etherchannel_dhcp.png` — existing topology image
- `configs/R1.cfg`, `configs/SW1.cfg`, `configs/SW2.cfg`, `configs/SW3.cfg` — reference configurations

## Safety note

This project generates plans and configuration artifacts for review. Inspect and test configurations in Packet Tracer before using them elsewhere.
