 # AI-Powered Cisco Packet Tracer Automation

An AI-assisted automation project that connects Antigravity CLI and MCP tools with Cisco Packet Tracer to automate network lab creation and configuration.

## Project Idea

The goal is to simplify Cisco Packet Tracer lab setup by describing a network in a natural-language prompt instead of manually creating and configuring every device.

The automation workflow is designed to:
- Interpret a network lab prompt.
- Create a network topology in Cisco Packet Tracer.
- Connect the required network devices.
- Configure routers and switches according to the requested scenario.
- Generate a Packet Tracer lab that can be inspected and tested.

## Technologies

- Antigravity CLI
- Model Context Protocol (MCP)
- Cisco Packet Tracer
- Cisco IOS configuration
- PowerShell

## Example Test Scenario

To test the automation workflow, I used a prompt requesting an enterprise network with:

- VTP and VLAN management
- EtherChannel using LACP
- 802.1Q trunk links
- Router-on-a-Stick inter-VLAN routing
- DHCP configuration

This scenario is an example used to demonstrate the automation workflow; it is not the entire project.

## Project Artifacts

- `vtp_etherchannel_dhcp_topology.pkt` — generated Packet Tracer lab
- `vtp_etherchannel_dhcp.png` — topology screenshot
- `configs/` — router and switch configuration files

## Objective

Explore AI-assisted network engineering by automating repetitive Packet Tracer tasks and making network lab creation faster and easier to reproduce.
