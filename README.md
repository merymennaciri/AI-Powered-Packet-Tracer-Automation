# Cisco Enterprise Lab: VTP, EtherChannel (LACP) & Router-on-a-Stick DHCP

This lab was built and validated directly inside Cisco Packet Tracer via Packet Tracer MCP automation tools.

---

## 1. Topology & Hardware Overview

| Device | Model | Role / Description |
|---|---|---|
| **R1** | Cisco 2911 | Core Router & DHCP Server (Router-on-a-Stick via `Gi0/0.10`, `Gi0/0.20`, `Gi0/0.30`) |
| **SW1** | Cisco Catalyst 2960-24TT | Distribution Switch & **VTP Server** |
| **SW2** | Cisco Catalyst 2960-24TT | Intermediate Switch & **VTP Client** |
| **SW3** | Cisco Catalyst 2960-24TT | Access Switch & **VTP Client** |
| **PC1 - PC6** | Generic PC (PC-PT) | End devices obtaining IP addresses via DHCP across 3 VLANs |

---

## 2. Cabling & Port Allocation

### Trunk Links & EtherChannels
- **R1 GigabitEthernet0/0** $\leftrightarrow$ **SW1 GigabitEthernet0/1** (Straight-Through Cable, 802.1Q Trunk)
- **SW1 $\leftrightarrow$ SW2 (Port-Channel 1 - LACP Active)**:
  - `SW1 FastEthernet0/23` $\leftrightarrow$ `SW2 FastEthernet0/23` (Crossover Cable)
  - `SW1 FastEthernet0/24` $\leftrightarrow$ `SW2 FastEthernet0/24` (Crossover Cable)
- **SW2 $\leftrightarrow$ SW3 (Port-Channel 2 - LACP Active)**:
  - `SW2 FastEthernet0/21` $\leftrightarrow$ `SW3 FastEthernet0/21` (Crossover Cable)
  - `SW2 FastEthernet0/22` $\leftrightarrow$ `SW3 FastEthernet0/22` (Crossover Cable)

### Access Links & PC Assignments
| Host | Connected Switch | Port | VLAN ID | Subnet / Gateway | Assigned DHCP IP |
|---|---|---|---|---|---|
| **PC1** | SW1 | Fa0/1 | VLAN 10 (ADMIN) | 192.168.10.0/24 (GW: 192.168.10.1) | 192.168.10.11 |
| **PC2** | SW1 | Fa0/2 | VLAN 20 (IT) | 192.168.20.0/24 (GW: 192.168.20.1) | 192.168.20.11 |
| **PC3** | SW2 | Fa0/1 | VLAN 10 (ADMIN) | 192.168.10.0/24 (GW: 192.168.10.1) | 192.168.10.12 |
| **PC4** | SW2 | Fa0/2 | VLAN 30 (STUDENTS) | 192.168.30.0/24 (GW: 192.168.30.1) | 192.168.30.11 |
| **PC5** | SW3 | Fa0/1 | VLAN 20 (IT) | 192.168.20.0/24 (GW: 192.168.20.1) | 192.168.20.12 |
| **PC6** | SW3 | Fa0/2 | VLAN 30 (STUDENTS) | 192.168.30.0/24 (GW: 192.168.30.1) | 192.168.30.12 |

---

## 3. Protocol Implementation Details

### VTP (VLAN Trunking Protocol)
- **Domain**: `CCNA`
- **Password**: `cisco`
- **Version**: `2`
- **SW1**: VTP Server (creates VLANs 10, 20, 30).
- **SW2 & SW3**: VTP Clients (automatically receive and synchronize VLAN database over Po1 and Po2 trunk links).

### EtherChannel (IEEE 802.3ad / LACP)
- **Port-Channel 1**: Bundles `Fa0/23` and `Fa0/24` between SW1 and SW2 using `channel-group 1 mode active`.
- **Port-Channel 2**: Bundles `Fa0/21` and `Fa0/22` between SW2 and SW3 using `channel-group 2 mode active`.
- Configured as trunks carrying VLANs 1, 10, 20, 30.

### Inter-VLAN Routing & DHCP
- Configured Router-on-a-Stick on R1 interface `GigabitEthernet0/0`:
  - `GigabitEthernet0/0.10`: `encapsulation dot1Q 10`, IP `192.168.10.1/24`
  - `GigabitEthernet0/0.20`: `encapsulation dot1Q 20`, IP `192.168.20.1/24`
  - `GigabitEthernet0/0.30`: `encapsulation dot1Q 30`, IP `192.168.30.1/24`
- DHCP pools on R1:
  - `VLAN10_ADMIN`: `192.168.10.0/24`, Default Gateway `192.168.10.1`, DNS `8.8.8.8`
  - `VLAN20_IT`: `192.168.20.0/24`, Default Gateway `192.168.20.1`, DNS `8.8.8.8`
  - `VLAN30_STUDENTS`: `192.168.30.0/24`, Default Gateway `192.168.30.1`, DNS `8.8.8.8`
- Excluded addresses: `.1` to `.10` on all three networks.

---

## 4. Live Verification Results

### A. VTP Status (`show vtp status` on SW1)
```text
VTP Version                     : 2
Configuration Revision          : 1
Maximum VLANs supported locally : 255
Number of existing VLANs        : 8
VTP Operating Mode              : Server
VTP Domain Name                 : CCNA
VTP Pruning Mode                : Disabled
VTP V2 Mode                     : Enabled
```

### B. EtherChannel Status (`show etherchannel summary`)
- **SW1**:
  ```text
  Group  Port-channel  Protocol    Ports
  ------+-------------+-----------+----------------------------------------------
  1      Po1(SU)           LACP   Fa0/23(P) Fa0/24(P) 
  ```
- **SW2**:
  ```text
  Group  Port-channel  Protocol    Ports
  ------+-------------+-----------+----------------------------------------------
  1      Po1(SU)           LACP   Fa0/23(P) Fa0/24(P) 
  2      Po2(SU)           LACP   Fa0/21(P) Fa0/22(P) 
  ```
- **SW3**:
  ```text
  Group  Port-channel  Protocol    Ports
  ------+-------------+-----------+----------------------------------------------
  2      Po2(SU)           LACP   Fa0/21(P) Fa0/22(P) 
  ```

### C. Trunking Status (`show interfaces trunk`)
- **SW1**: `Po1` and `Gig0/1` trunking, 802.1q, allowed VLANs `1,10,20,30`.
- **SW2**: `Po1` and `Po2` trunking, 802.1q, allowed VLANs `1,10,20,30`.
- **SW3**: `Po2` trunking, 802.1q, allowed VLANs `1,10,20,30`.

### D. DHCP Leases on R1 (`show ip dhcp binding`)
```text
IP address       Client-ID/              Lease expiration        Type
                 Hardware address
192.168.10.11    000C.85AB.2030           --                     Automatic (PC1)
192.168.10.12    0050.0F51.CCB8           --                     Automatic (PC3)
192.168.20.11    0007.EC4D.6978           --                     Automatic (PC2)
192.168.20.12    00D0.FF6C.7BA1           --                     Automatic (PC5)
192.168.30.11    000C.CFE4.20E0           --                     Automatic (PC4)
192.168.30.12    0060.5CE4.7899           --                     Automatic (PC6)
```

### E. End-to-End Ping Connectivity Tests
| Source | Destination | Path Tested | Result |
|---|---|---|---|
| **PC1 (192.168.10.11)** | **PC3 (192.168.10.12)** | Intra-VLAN 10 across SW1 $\rightarrow$ Po1 $\rightarrow$ SW2 | **4/4 (0% loss)** |
| **PC2 (192.168.20.11)** | **PC5 (192.168.20.12)** | Intra-VLAN 20 across SW1 $\rightarrow$ Po1 $\rightarrow$ SW2 $\rightarrow$ Po2 $\rightarrow$ SW3 | **4/4 (0% loss)** |
| **PC4 (192.168.30.11)** | **PC6 (192.168.30.12)** | Intra-VLAN 30 across SW2 $\rightarrow$ Po2 $\rightarrow$ SW3 | **4/4 (0% loss)** |
| **PC1 (192.168.10.11)** | **192.168.10.1 (R1)** | Host to Default Gateway | **4/4 (0% loss)** |
| **PC1 (192.168.10.11)** | **PC2 (192.168.20.11)** | Inter-VLAN Routing (VLAN 10 to VLAN 20) via R1 subinterfaces | **4/4 (0% loss)** |
| **PC1 (192.168.10.11)** | **PC4 (192.168.30.11)** | Inter-VLAN Routing (VLAN 10 to VLAN 30) via R1 & Po1 | **4/4 (0% loss)** |
| **PC6 (192.168.30.12)** | **PC1 (192.168.10.11)** | Multi-hop Inter-VLAN: SW3 $\rightarrow$ Po2 $\rightarrow$ SW2 $\rightarrow$ Po1 $\rightarrow$ SW1 $\rightarrow$ R1 | **4/4 (0% loss)** |

---

## 5. Artifacts and Project Files
- Active Packet Tracer File: [`vtp_etherchannel_dhcp_topology.pkt`](vtp_etherchannel_dhcp_topology.pkt)
- Topology Canvas Screenshot: [`vtp_etherchannel_dhcp.png`](vtp_etherchannel_dhcp.png)
- IOS Device Configurations:
  - [`configs/R1.cfg`](configs/R1.cfg)
  - [`configs/SW1.cfg`](configs/SW1.cfg)
  - [`configs/SW2.cfg`](configs/SW2.cfg)
  - [`configs/SW3.cfg`](configs/SW3.cfg)
