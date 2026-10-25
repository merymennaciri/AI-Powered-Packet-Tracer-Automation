# AI-Powered Packet Tracer Automation

This repository documents the local setup and MCP connection workflow for using `packet-tracer-mcp` with Antigravity and Cisco Packet Tracer.

## What is included

- `packet_tracer_ai/` — experimental command-line wrapper.
- `tests/` and `.github/workflows/python-tests.yml` — parser tests and automated test workflow.
- `vtp_etherchannel_dhcp_topology.pkt` — existing Packet Tracer lab.
- `vtp_etherchannel_dhcp.png` — topology image.

> **Status:** the MCP connection and wrapper should be verified on the local machine. Exporting an artifact does not necessarily create or edit a native `.pkt` file.

## 1. Check prerequisites in PowerShell

Run these commands to verify the tools are available:

```powershell
python --version
python -m pip --version
git --version
node --version
npm --version
```

If a command is not recognized, install that prerequisite and reopen PowerShell.

## 2. Install the MCP server

Install the package in the Python environment you intend to use:

```powershell
python -m pip install --upgrade pip
python -m pip install packet-tracer-mcp
```

Check that the package can be launched:

```powershell
python -m packet_tracer_mcp --help
```

The MCP server uses standard input/output when launched with `--stdio`. It may wait for an MCP client rather than displaying a normal interactive prompt.

## 3. Connect it to Antigravity

In Antigravity, open its MCP settings and add an MCP server with:

- **Command:** `python`
- **Arguments:** `-m packet_tracer_mcp --stdio`

Use the same Python environment in which you installed `packet-tracer-mcp`. If Antigravity cannot find the package, configure the full path to that environment's Python executable.

Verify the configured server from PowerShell:

```powershell
agy mcp list
```

The server should appear in the list as enabled. If your Antigravity version uses a different settings screen, use its MCP server configuration UI and enter the same command and arguments.

## 4. Install this repository's wrapper

Clone the repository if it is not already on your computer, then enter the project folder:

```powershell
git clone https://github.com/merymennaciri/AI-Powered-Packet-Tracer-Automation.git
Set-Location .\AI-Powered-Packet-Tracer-Automation
python -m pip install -e .
```

If you already have the repository locally, use `Set-Location` with your existing project path instead of cloning it again.

Check the wrapper's available options:

```powershell
python -m packet_tracer_ai.cli --help
```

Example planning request:

```powershell
packet-tracer-ai "1 router, 3 VLANs, router-on-a-stick and DHCP" --name VTP-EtherChannel-DHCP --validate-only
```

To request artifact export:

```powershell
packet-tracer-ai "1 router, 3 VLANs, router-on-a-stick and DHCP" --name VTP-EtherChannel-DHCP --output projects
```

The wrapper currently uses a limited rule-based parser; review the generated plan and validation output. Do not assume the export is a native Packet Tracer project unless you verify the output.

## 5. Run tests

```powershell
python -m unittest discover -s tests -v
```

The GitHub Actions workflow at `.github/workflows/python-tests.yml` is intentionally kept in the repository.

## Troubleshooting

- **Package not found:** run `python -m pip show packet-tracer-mcp` and make sure Antigravity uses that same Python environment.
- **MCP server not listed:** check the command and arguments in Antigravity's MCP settings, then run `agy mcp list`.
- **Python command not found:** install Python, reopen PowerShell, and run `python --version`.
- **Node/npm command not found:** install Node.js and reopen PowerShell.
- **No native `.pkt` generated:** the current wrapper's export step does not guarantee native Packet Tracer file generation. The existing `.pkt` file remains a separate lab artifact.

## Existing lab

Open `vtp_etherchannel_dhcp_topology.pkt` directly in Cisco Packet Tracer to inspect the existing topology. The topology image is `vtp_etherchannel_dhcp.png`.
