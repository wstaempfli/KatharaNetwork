# Kathara Network Emulator

For the interactive exercises, we will be using Kathara, a lightweight container-based network emulation system. It leverages Docker for the setup and management of virtual network scenarios, offering a straightforward and efficient alternative to more complex tools like EVE-NG, which require complex and extensive virtualization setups. With Kathara, you can quickly create realistic lab environments while still benefiting from a wide range of configuration options. This makes it an ideal tool for both educational experiments and advanced network testing, giving you a hands-on platform to learn and explore modern networking concepts.

## Kathara Labs

In Kathara, a lab is a folder that contains all the files required to emulate a network scenario. The main components include:
- lab.conf: This file contains the network topology and device interconnection information.
- Device-Specific Files:
    - Startup File: Contains commands that execute when a device starts.
    - Device Folder: Serves as the device’s root filesystem and is mounted into the container on startup.

Example Lab File

```
LAB_DESCRIPTION="This is an example lab file."
LAB_VERSION=1.0
LAB_AUTHOR="Network Security Group"
LAB_WEB="https://netsec.ethz.ch"

# creates a device called host1
host1[0]="netA"        				# connects eth0 of host1 to the virtual network netA
host1[image]="kathara/base"         # uses the base image, containing networking tools and a Python installation 

# creates a device called host2
host2[0]="netA"        			 	# connects eth0 of host2 to the same virtual network netA
host2[1]="netB"         			# connects eth1 of host2 to the virtual network netB
host2[image]="kathara/frr"          # extends the base image, includes the FRR suite
```

**Note:** The virtual network name “netA” is simply an arbitrary label used to group devices together into the same collision domain; it does not influence any underlying network settings. Just like in real networks, where a cable doesn’t carry any inherent configuration, any configuration parameters (like IP ranges or routung information) are solely determined by the devices attached to the subnet.

## Command Overview

Kathara provides several commands to manage labs and devices. The most important commands for the labs are: 

- `kathara lstart`: Starts the lab in the current directory.
- `kathara lclean`: Cleans (stops) the lab in the current directory.
- `kathara lrestart`: Restarts the lab in the current directory.
- `kathara wipe -f`: Cleans all started labs, regardless of which directory you are currently in.

Additionally, you may find these commands useful:
- `kathara list`: Show all running Kathara devices.
- `kathara connect <device>`: Connect your terminal to a specific Kathara device.
- `kathara settings`: Adapt your system wide settings, like the terminal emulator to use.
- `kathara wipe --all`: Reset your Kathara installation; useful if you run into any persistent issues.

### What Happens When You Start a Lab

When you execute `kathara lstart`, multiple terminal windows open up - one for each device defined in your lab. In these windows, you can issue commands, configure devices, and interact with the scenario in real time.

**Important:** The containers used in Kathara are ephemeral; there is **no persistence**. Any changes made interactively (e.g., configuration changes done directly in the terminal) will be lost once the lab is stopped. To preserve your configurations, you have to implement your changes in the corresponding configuration files directly.

## Additional Tips for Setup
**Shell History:**
On startup, Kathara issues multiple startup commands. If these end up in you shell history, consider adding these commands to your shell’s history ignore list to avoid clutter.
**Terminal Windows:**
When using kathara lclean, depending on your OS and terminal emulator, configure it to automatically close windows where the session has ended. This helps prevent having multiple closed windows lingering and spamming your workspace.
**Command Aliases:**
For convenience, you might want to alias the Kathara commands in your shell’s configuration file (e.g., .bashrc or .zshrc). For example:
```bash
alias ks="kathara lstart"
alias kr="kathara lrestart"
```
Especially if you installed it as a python module:
```bash
alias kathara="python3 -m kathara"
```

## A word of Caution

Kathara is a very powerful and flexible tool, allowing you to emulate even complex networks by just using docker containers. However, since it is under active deleopment, there may be occasional unexpected behaviors. If you experience any issues, we recommend trying to reset it first using `kathara wipe --all --force`, or switching to the Python module installation for potentially improved compatibility with very specific setups. If you believe the problem is related to Kathara itself, please consider creating an issue in the GitLab Student Issues Repository.

# Introduction to FRR

## What is FRR and Why Should I Care?

### Explain It Like I'm Five

FRR is a routing suite (collection of programs implementing routing protocols), that can turn almost any Linux machine into a router.

### Explain It Like I'm Taking Computer Networks at ETH

FRR is a free, open source, routing suite. It implements all major routing protocols used today: OSPF, IS-IS, BGP, RIP, etc. The suite is designed as a modular collection of *daemons* which run on almost any Linux machine. FRR itself is not a full router, it only implements the control plane. This means, FRR uses a combination of routing protocols to learn how packets should traverse the network, but it relies on the operating system to do the actual forwarding. This modularity allows FRR to be integrated with high performance packet forwarding (switching) chips, thus creating incredibly powerful routers based on open-source software.

### Is Learning FRR Relevant?

Yes! FRR is a popular choice for vendors who do not want to re-implement their control plane from scratch. It is the primary routing daemon in NVIDIA Cumulus Linux, a networking-focussed Linux distribution. Entire data centers are routed using only FRR! Its popularity lies not just in its performance and modularity, but also in its similarity to other major commercial router operating systems such as Cisco IOS. This allows network operators to quickly transition between working on FRR and Cisco systems without major retraining. This is also great news for you, since learning FRR now will give you an advantage if you ever choose to do a career in networking!

## FRR Architecture

Historically, routing software is made as a one-process program which provides all of the routing protocol functionalities. FRR takes a different approach. FRR is a suite of daemons that work together to build the routing table. Each major protocol is implemented in its own daemon, and these daemons talk to a middleman daemon (zebra), which is responsible for coordinating routing decisions and talking to the dataplane.

All of the FRR daemons can be managed through a single integrated user interface shell called vtysh. vtysh connects to each daemon through a UNIX domain socket and then works as a proxy for user input. In addition to being a unified interface, vtysh also provides the ability to configure all the daemons using a single configuration file (which you will edit). This avoids the overhead of maintaining a separate configuration file for each daemon.

## Getting Started with FRR
In this section, we provide you with an overview of how to work with FRR. For official up-to-date information, consult the official documentation: https://docs.frrouting.org/en/latest/
### Starting, Stopping, Restarting FRR

The labs are designed to start the relevant FRR daemons automatically. However, should you find the need to manually start, stop, or restart FRR, you can do it using the following commands:

 - **Start:**   `systemctl start frr`

 - **Stop:**    `systemctl stop frr`

 - **Restart:** `systemctl restart frr`

### FRR Configuration File

On startup, FRR reads a config file stored at `/etc/frr/frr.conf`. This config file stores the entire FRR configuration, so you can configure all FRR daemons using this one file.

#### Configuration Syntax
FRR is configured using a domain-specific language (DSL) which is structured like a tree to make configuration easy. Abstractly, you build a configuration tree - you can add new nodes (e.g., a nodes specifying a BGP neighbor), or modify nodes (e.g., setting a specific BGP feature for a neighbor).

This is best illustrated using an example. Imagine we want set up a BGP session with a neighboring AS to whom we are connected using IP `192.168.1.2`. Abstractly, we achieve this by traversing the configuration tree, entering the BGP node, adding a new node representing the newly added BGP neighbor AS. Concretely, we would execute:

    ! FRR uses exclamation marks for comments
    ! Enter the BGP Node
    router bgp <OUR AS NUMBER>
      ! Add a new node for that neighbor
      neighbor 192.168.1.2 remote-as <NEIGHBOR AS NUMBER>

That's all it takes to start a new BGP session! If we now wanted to change that neighbor's configuration by enabling *graceful-restart*, we simply traverse the configuration tree again to the neighbor's node and configure it accordingly:

    router bgp <OUR AS NUMBER>
      neighbor 192.168.1.2 remote-as <NEIGHBOR AS NUMBER> graceful-restart

Remembering all the commands is hard and in most cases not strictly necessary (though handy). Instead, you can use the FRR CLI to configure FRR, which provides convenient hints, autocompletion, and useful error messages.


### FRR CLI using VTYSH
The Very Tiny Shell (VTYSH) allows you to interact with your FRR router daemon while it's running. This is very useful to check configurations, change configurations without rebooting, and retrieving important information such as the number of BGP sessions, the state of OSPF, etc.

In your terminal, simply type `vtysh` to connect to FRR. You do not have to specify which daemon you want to connect to. When you connect using VTYSH, you are in a read-only mode (identified by the `<ROUTER-NAME>#`). This mode allows you to retrieve important data from the router using the `show` command. Typing `show ?` (the space is important) reveals all the possible options of the `show` command.

To make changes to the current configuration, you enter configuration mode by executing `configure terminal`, or `conf t` for short. Now you are in the configurtion tree of FRR. If you are not sure where to go from your current configuration node, just type `?` and FRR will show you all possible options. The questionmark also gives suggestions on how to complete a command, for example typing `r?` suggests `router`. To go back up in the tree, execute `exit`, and to leave the configuration mode entirely, execute `end`.

### FRR Logging

FRR write logs to `/var/log/frr/frr.log`. FRR can be configured with varying levels of verboseness. FRR logs are in the MRT format defined in [RFC 6396](https://datatracker.ietf.org/doc/html/rfc6396), you can find many different MRT parsers that allow you to investigate the logs.

## FRR Route Maps

When you want to implement logic in FRR, you do so using route-maps. A route-map is similar to a switch-case expressions in other programming languages. However, in FRR you do no explicitly execute the route-map - you instead _assign_ it to specific neighboring ASes. You can assign two route-maps to each neighbor, one for incoming BGP UPDATEs, and one for outgoing BGP UPDATEs.
FRR then executes the route-map for you whenever a BGP UPDATE (i) is received from a neighbor, and (ii) just before sending it out to a neighbor.

### Defining a Route Map

Let's look at a simple route-map which implements the following logic:
 - BGP UPDATE has MED value of 250 $\Rightarrow$ set MED to 200 and allow UPDATE to pass.
 - BGP UPDATE already has MED value of 200 $\Rightarrow$ allow UPDATE to pass.
 - BGP UPDATE has a different (or no) MED value
    $\Rightarrow$ drop UPDATE.

Each of these three cases is written as a separate route-map block. The order in which the blocks are executed is specified using the indices `10, 20, 30, etc`. Each block can contain (i) a `match` condition, (ii) a `set` command used to set the metric, and (iii) a final rule deciding whether the UPDATE should be accepted or denied. 

    route-map example permit 10
        match metric 250
        set metric 200
    route-map example permit 20
        match metric 200
    route-map example deny 30

### Applying a Route Map
Once you defined a route-map, you have to apply it to a neighbor, either in inbound direction (selection policy) or outbound direction (export policy).

Assume you peer with an AS 65000, and you are connected to that neighbor's BGP router on IP `192.168.1.1`. You can apply your rout-map as follows:

    ! Apply route-map called "select"
    router bgp 65000
    neighbor 192.168.1.1 route-map select in
    
    ! Apply route-map called "export"
    router bgp 65000
    neighbor 192.168.1.1 route-map export out


# Routing on a Linux-Based Machine

Your laptop routes and forwardings thousands of packets every day without you even noticing it. In this section, you learn how a Linux-based operating system performs these two essential tasks.

## Reminder: Network Protocol Stack
Before diving into IP routing specifically, let's briefly revisit at which layer in the internet IP packets are handled:

 - **Physical Layer (Layer 1):** Handles the actual electrical or optical transmission of raw bit streams. *The network interface card (NIC) handles at this layer.*
 - **Data Link Layer (Layer 2):** Responsible for node-to-node communication, typically within a local network. Ethernet operates at this layer, using MAC addresses for addressing. *The operating system handles this layer.*
 - **Network Layer (Layer 3):** This is where IP routing happens. It handles addressing and routing packets between different networks. *The operating system handles this layer.*
 - **Transport Layer (Layer 4):** Provides end-to-end communication services for applications. TCP and UDP operate here. *The operating system handles this layer, and user space programs interact with it through **sockets**.*
 - **Application Layer (Layer 5):** Where network applications and their protocols operate. *The user space handles this layer.*


## Network Interfaces
Network interfaces are the connection points between a computer's networking software and its hardware, serving as abstraction layers that enable communication between the operating system and physical or virtual network devices.

### Types of Network Interfaces

#### Physical Interfaces
Physical interfaces, such as `eth0` for ethernet cards and `wlan0` for wireless adapters, represent direct mappings to the hardware network adapters installed in a system. These interfaces abstract physical network media, whether through traditional ethernet cables or wireless radio signals, to the operating system. Each physical interface is uniquely identified by a MAC address, an assigned identifier that facilitates layer 2 communication. The interfaces operate within specific constraints defined by their underlying hardware capabilities, such as supported data rates (e.g., 1Gbps, 10Gbps) and duplex modes (half or full). Physical interfaces can be configured with multiple IP addresses, enabling them to participate in different network segments or provide various network services simultaneously.

#### Virtual Interfaces
Operating systems can create software-based virtual interfaces to enable additional networking functionality. The loopback interface (`lo`) serves as a fundamental virtual interface that facilitates internal communication within the system, allowing local processes to communicate via network protocols without utilizing physical network resources. VLAN interfaces (identified with notation like `eth0.10`) enable sophisticated network segmentation by allowing multiple logical networks to coexist on the same physical infrastructure, effectively isolating traffic while sharing physical resources. Tunnel interfaces, denoted as `tun0` or `tap0`, provide virtual endpoints for encapsulated network traffic, supporting technologies like Virtual Private Networks (VPNs) and other forms of network tunneling by creating abstract network devices that operate at either the IP level (`tun`) or ethernet level (`tap`).

### Interface Configuration

#### Addressing
Network interfaces can be configured with:
```bash
# Configure IP address
ip addr add 192.168.1.10/24 dev eth0

# Remove IP address
ip addr del 192.168.1.10/24 dev eth0
```

#### State Management
Interfaces can be enabled/disabled:
```bash
# Enable interface
ip link set eth0 up

# Disable interface
ip link set eth0 down
```

### Interface Properties
Network interfaces maintain several critical properties that define their operational characteristics and performance. The link state property indicates whether the interface is operational (up) or disabled (down), determining its ability to transmit and receive data. For ethernet interfaces, a unique Media Access Control (MAC) address is assigned, serving as a hardware-level identifier essential for Layer 2 communication within local network segments.

Each interface enforces a Maximum Transmission Unit (MTU), which specifies the largest protocol data unit that can be transmitted in a single network frame. This parameter is crucial for optimal network performance and preventing fragmentation. The interface also implements queue disciplines, sophisticated mechanisms that control how packets are queued and scheduled for transmission, enabling traffic shaping, prioritization, and congestion management.

Furthermore, interfaces maintain detailed statistics about their operation, including counters for transmitted and received packets, error conditions, dropped frames, and collisions. These metrics are invaluable for monitoring network health, troubleshooting connectivity issues, and optimizing performance through data-driven analysis.

### Interface Information
View interface details using:
```bash
# Show all interfaces
ip link show

# Show IP configuration
ip addr show

# Show interface statistics
ip -s link show
```

## IP Routing Tables
The routing table is the central data structure that determines where IP packets should be sent. In Linux, you can view routing tables using:

```bash
# Unformatted output 
route show

# Formatted, human readable output
routel
```

The latter command creates output similar to the following:

    Dst             Gateway         Prefsrc       Protocol Scope   Dev              Table
    default         138.197.176.1   192.168.1.2   static           eth0
    10.0.101.0/24   10.0.1.2        10.0.1.1      bgp              eth1             
    10.0.102.0/24   10.0.2.2        10.0.2.1      bgp              eth2             

The `routel` command's output provides a comprehensive view of the system's routing decisions. Each entry has a destination IP prefix with its network mask (`Dst`), indicating where packets should be directed. The `Dst` field is further used for longest prefix matching to determine the next hop of the routing path for outbound packets. The `Gateway` field specifies the next hop's IP address. `Prefsrc` indicates the preferred source IP address assigned to the interface for outgoing packets. This field determines the source IP a packet has when it is sent out. The `Protocol` field reveals how the route was learned (e.g., static, BGP, OSPF). `Dev` specifies which network interface should be used for forwarding, while `Table` indicates which routing table contains this particular rule.

## End-to-End Packet Processing in Linux

Linux's network stack processes packets through multiple layers, each handling specific networking functions. Let's examine how an outbound SSH connection is processed through these layers.

### Application Layer Processing
When an SSH client initiates a connection to a remote server (e.g., `ssh 192.168.1.33`), it triggers a sequence of operations starting at the application layer.

### Transport Layer Operations
The transport layer manages the end-to-end communication through socket operations and TCP state management. The SSH client creates a TCP socket via the `socket()` syscall and initiates connection to the destination (IP: 192.168.1.33, Port: 22), triggering TCP's three-way handshake. The socket interface enables bidirectional communication through `send()` and `recv()` syscalls, with TCP managing the send and receive buffers behind the scenes. Once enough bytes have accumulated in the send buffer, TCP constructs TCP segments containing the buffered data and the TCP header, and passes them to the network layer.

### Network Layer Processing 
The network layer begins by constructing the IP header, initially containing only the destination address from the socket connection. It then consults the routing table using longest prefix matching to determine the egress interface for packet transmission, the source IP address (from interface configuration), and the next-hop IP address required for layer 2 delivery.

### Data Link Layer Handling
The layer 2 subsystem encapsulates the IP packet in an appropriate frame format (e.g., Ethernet). This requires both source MAC (obtained from egress interface) and destination MAC (resolved through ARP). The Address Resolution Protocol (ARP) resolves the next-hop IP to its corresponding MAC address through broadcast requests on the local network segment. Once properly constructed, the frame is queued for transmission on the chosen network interface.

### Physical Layer Transmission
The network interface card converts the digital frame into physical signals (electrical, optical) for transmission on the medium.

# Introduction to Open Shortest Path First (OSPF)

OSPF is a link-state routing protocol that operates within a single Autonomous System. Unlike distance-vector protocols, OSPF enables routers to build a complete map of the network rather than just sharing path costs.

## Key Concepts

### Link-State Database
Each router maintains a map of the network topology. This shared view ensures consistent routing decisions across the network.

### Network and Router Hierarchy
OSPF divides networks into areas, with a backbone area (Area 0) at the center. This structure reduces routing overhead by containing topology changes within area boundaries. Routers in OSPF serve different functions based on their position in the network - some connect areas together, some connect to external networks, and others operate within a single area. To keep the lab simple, all routers are in area 0.

### Protocol Operation
OSPF operation is structured around four key processes. First, the Hello Protocol establishes and maintains relationships between neighboring routers through periodic message exchanges, enabling routers to verifying the health of connections and neighboring routers.

The Database Synchronization process follows successful neighbor discovery. During this phase, routers exchange their Link State Advertisements (LSAs) through a reliable flooding mechanism, ensuring each router obtains an identical view of the network topology. This synchronization involves a master-slave relationship where the more authoritative router shares its database with its peer.

Once the Link State Database is synchronized, routers independently execute the Shortest Path First (SPF) algorithm, an implementation of Dijkstra's algorithm. This computation considers *link costs* and network topology to determine the optimal path to every destination in the network, creating a shortest-path tree with the calculating router at the root.

Finally, the Route Installation process translates the SPF calculation results into actual forwarding entries in the router's routing table. Only the best routes, determined by lowest total path cost, are installed.

### Convergence Speed

When implementing OSPF in production networks, convergence speed tuning through hello and dead intervals requires careful consideration - aggressive timers enable fast failure detection but risk instability, while conservative settings improve stability but slow convergence. In the lab, we set very aggressive convergence times so you see how your changes take effect almost immediately. 

### Basic OSPF Configuration in FRR

Enable OSPF with Router ID:

```
router ospf
ospf router-id 10.0.0.1
```

Configure interfaces:

```
interface eth0
ip ospf area 0
ip ospf hello-interval 10
ip ospf dead-interval 40
```

For routers in multiple areas:

```
router ospf
ospf router-id 10.0.0.1
network 192.168.1.0/24 area 0
network 192.168.2.0/24 area 1
```

Verify OSPF operations:

```
show ip ospf neighbor
show ip ospf database
show ip route ospf
```


# Introduction to the Border Gateway Protocol (BGP)
BGP (Border Gateway Protocol) is the fundamental routing protocol that powers today's internet. At its core, BGP enables different networks, called Autonomous Systems (ASes), to share routing information with each other while maintaining their operational independence.

Unlike simpler routing protocols that only share distance information, BGP is a path-vector protocol. This means that when routing information is shared, it includes the complete sequence of ASes that a packet must traverse to reach its destination. This routing information is exchanged through messages called BGP UPDATEs.

A typical BGP UPDATE message contains three key components:
 - The destination IP prefix (where the traffic should go)
 - The AS path (the sequence of networks the traffic will traverse)
 - Additional attributes that influence routing decisions

While BGP's design is remarkably simple - famously first sketched on a napkin - this simplicity is also the protocol's fundamental weakness. Its expressiveness and flexibility allow for complex yet hard to verify configurations, which makes configuration errors common and difficult to debug. Moreover, BGP was designed without any built-in security mechanisms, which poses significant challenges for internet security in today's threat landscape.

## Modeling Business Relationships and Money Routing
Internet routing is fundamentally driven by economics. Operating global network infrastructure - with cables spanning continents, routers connecting regions, and constant maintenance - is expensive. Since most ASes are operated by for-profit entities, they configure their BGP policies to minimize costs and maximize revenue. In fact, ASes primarily route traffic based on business relationships rather than technical metrics like latency or bandwidth.

### Customer-Provider Relationship
In a customer-provider relationship, a customer AS pays a provider AS for transit service - the forwarding of network traffic in the name of the customer. This arrangement is fundamental to internet connectivity, as it allows smaller networks to access parts of the internet they couldn't reach directly. Since the customer AS incurs costs for sending traffic through its provider, it typically configures its BGP policies to use this paid transit only when more economical routes (like settlement free peering) aren't available. Think of it as a business arrangement where the customer pays for the provider's more extensive network reach and connectivity services.

### Settlement Free Peering Relationship

In settlement-free peering, ASes exchange traffic without charging each other. This typically occurs between networks of similar size that expect balanced traffic flows. Both ASes benefit by avoiding provider fees while maintaining direct connectivity. For example, two regional ISPs might peer to exchange their customers' traffic directly, reducing costs and latency.

### AS Tiers

The internet's hierarchical structure, induced by business relationships, is organized into three main tiers of Autonomous Systems (ASes). At the top, Tier 1 ASes (like AT&T, Lumen, and Deutsche Telekom) form the internet's backbone with global network coverage and can reach any destination without paying for transit. In the middle, Tier 2 ASes (such as Swisscom and Sunrise) operate on a (mostly) regional level, using a mix of peering arrangements with other Tier 2s and paid connections to Tier 1s for global reach. At the bottom, Tier 3 ASes, often called stub ASes, typically represent smaller entities like enterprises or institutions that primarily rely on higher-tier providers for internet connectivity, though they may establish some peering relationships for direct traffic exchange with nearby networks.

## BGP Route Selection

When an AS receives a BGP UPDATE message containing an IP prefix and its corresponding AS path, it follows a straightforward decision process. If the UPDATE does not violate any selection policy and the AS doesn't currently have a route to that IP prefix, it simply installs the new route in its routing table and advertises it according to its export policy. However, if a route to that prefix already exists, the AS must decide whether to replace it. The new route takes precedence if it either has a higher local preference value (assigned based on business relationships) or a shorter AS path length. If the new route is selected, it replaces the existing one and is then advertised according to the AS's export policy.

### BGP Selection Policy

When an AS receives BGP routes from its neighbors, it applies a selection (or import) policy to determine which routes to use. This policy acts as a filter, allowing the AS to reject undesirable routes - for example, those passing through networks known for poor performance. For accepted routes, the AS assigns a preference value called local preference, which typically reflects business relationships. Routes from customers (who pay for transit) receive the highest preference, followed by routes from peers (settlement-free exchanges), while routes from providers (to whom the AS pays) get the lowest preference. This hierarchical preference system aligns with the AS's financial interests: using customer routes generates revenue, peer routes are cost-neutral, and provider routes incur costs.

### BGP Export Policy

The BGP export policy governs which routes an AS advertises to its neighbors, primarily driven by economic considerations. When implementing export policies, ASes follow these key principles:

 - Routes learned from customers are advertised to all neighbors (providers, peers, and other customers), as this maximizes potential revenue. Customers pay for transit regardless of the traffic's source.
 - Routes learned from peers are advertised only to customers. This is because forwarding to peers does not generate any revenue while still incurring the cost of forwarding, which is compensated by billing customers.
 - Routes learned from providers are only advertised to customers. This ensures an AS does not inadvertently provide expensive transit services (which it pays for) to peers or other providers without compensation.

These export rules, often called the "valley-free" routing principle, ensure that traffic flows align with business relationships and prevent economically unfavorable routing scenarios.

# Introduction to SCION

## Overview

SCION is a future internet architecture designed to provide route control, failure isolation, and explicit trust information for end-to-end communication. Its primary goal is to deliver highly available and efficient inter-domain packet delivery — even in the presence of actively malicious entities. It can thus be considered to be a more secure, stable, and flexible successor to BGP.

## Main Concepts

### Isolation Domains (ISDs)
SCION organizes existing Autonomous Systems (ASes) into groups called Isolation Domains (ISDs). This allows SCION to route at two levels: intra-ISD (within one ISD/group of ASes), and inter-ISD (between ISDs). Changes in intra-ISD routing are not directly propagated across ISDs, which allows faults to be contained within that ISD. An ISD contains two types of ASes: (i) _core ASes_ which interconnect the ISD to other ISDs and manage cryptographic state using a so-called trust root configuration (TRC), and (ii) _non-core ASes_ which maintain most SCION services locally but still rely on core ASes for some operations.

### Trust Root Configuration (TRC)
The TRC defines the trusted root certificates and policies for an ISD. It specifies which core ASes are authorized to issue and sign certificates for other ASes and includes the cryptographic parameters used to secure path construction and inter-AS communications.

### ISD and AS Numbering
ASes in SCION are addressed using a combination of ISD identifier and AS number. The combination of 16 bit ISD identifier and 48 bit AS number is called the ISD-AS and uniquely identifies an AS. In text, an ISD-AS is written as the ISD and AS number separated by a hyphen (e.g., `42-ff00:1:f`).

### Addressing a Host in SCION
SCION's addressing scheme operates at two distinct levels: intra-AS and inter-AS. Within an AS (intra-AS), network operators can freely choose their local addressing scheme, be it IPv4, IPv6, or even MAC addresses. For communication between ASes (inter-AS), hosts are uniquely identified by their SCION address, which consists of three components: the ISD identifier, the AS number, and the host's local address within that AS. This hierarchical approach means that local addresses only need to be unique within their AS, allowing different ASes to reuse the same local identifiers without conflict.

### Core ASes
Some ASes are designated as core ASes by the TRC. These core ASes sit at the top of the intra-ISD routing hierarchy, connect customer ASes to external networks, and participate in both intra- and inter-ISD path exploration.

### Intra-ISD Routing
SCION operates on two routing levels: intra-ISD and inter-ISD. Both levels use path-segment construction beacons (PCBs) to explore network paths. A PCB is initiated by a core AS and then disseminated either within an ISD (to explore intra-ISD paths) or among core ASes (to explore core paths across different ISDs). The PCBs accumulate cryptographically protected path and forwarding information on the AS-level, and store this information in the form of hop fields (HFs). Endpoints use information from these hop fields to create end-to-end forwarding paths for data packets, which carry this information in their packet headers. This concept is called packet-carried forwarding state. The concept also supports multi-path communication among endpoints.

In the following labs, we only focus on intra-ISD routing.

## SCION Services

SCION consists of several services that work together to provide secure inter-domain routing.

*Note*: In a production environment, each of these services would run as multiple instances distributed across different physical machines to ensure high availability and fault tolerance. In our labs however, all services run on a single device for the sake of simplicity.

### Control Service
The SCION control service (`scion-control.service`) discovers SCION paths by participating in the beaconing process, signs and validates path information via the Control-Plane PKI, and acts as a recursive resolver for path and certificate data for local endpoints.

### Router Service
The SCION router (`scion-router.service`) is responsible for forwarding SCION packets. 

It reads the border_routers section of the `topology.json` file and uses the entry referring to its own `general.id` to determine the intra-AS links that this router instance is responsible for. The other router entries (“sibling routers”) define which router is responsible for which interface. This mapping is consulted during packet forwarding to determine the sibling router to which a packet transitting the AS needs to forwarded to.

Additionally, the router considers the `control_service` and `discovery_service` entries. These define the underlay addresses that the router uses to resolve anycast or multicast.

Due to the encapsulation of SCION packets, the router only uses ordinary UDP sockets as underlay and can therefore run on almost any host system without requiring any special privileges.

*Note:* SCION distinguishes between the underlay (the physical IP/UDP layer used to transport packets) and the overlay (the SCION network layer).

### Daemon Service
The SCION Daemon (`scion-daemon.service`) communicates with the control plane. It fetches, verifies, and caches path and certificate information and provides a local interface for applications to perform path lookups and obtain configuration data.

### Dispatcher Service
In earlier SCION versions, the Dispatcher (`scion-dispatcher.service`) managed a single network socket for incoming traffic and distributed packets to the appropriate applications. In newer versions of SCION (as used in our labs), each application can open its own socket directly, thus improving performance and eliminating the need for a dispatcher. To remain backwards compatible, modern SCION versions still include a so-called dispatcher shim.

### SCION IP Gateway Service
The SCION IP Gateway (SIG, `scion-ip-gateway.service`) enables non-SCION hosts to communicate via the SCION network by tunneling IP packets over SCION. It encapsulates IP packets within SCION packets and performs path lookups to select a suitable SCION path to the receiving AS. The SIG acts as a router from the perspective of the non-SCION host, whilst acting as SCION endpoint from the perspective of the SCION network. It is typically deployed inside the same AS-internal network as its non-SCION hosts, or at the edge of an enterprise network.

#### Step-by-Step Operation
Tunneling IP traffic over SCION requires a SIG at the sending and receiving AS, and involves the following steps:
1. The sending host uses its standard name resolution protocol (e.g., DNS) to retrieve the destination's IP address, and sends IP packets toward that destination IP as usual.
2. The IP packet reaches an ingress SIG in the sender’s AS.
3. Based on the destination IP address, the ingress SIG determines the SCION address (ISD-AS-endpoint address) of an egress SIG in the destination AS. To identify the egress SIG's SCION address, each SIG store a pre-configured list of partner ASes (stored in `gateway.json`), among which a SIG discovery process is performed periodically.
4. The ingress SIG encapsulates the original IP packet within one or more SCION packets and sends them to the egress SIG. In this step, a SCION path lookup may happen if no appropriate path is cached.
5. The packet is forwarded along the SCION path to the egress SIG.
6. The egress SIG receives and decapsulates the SCION packet(s) and forwards the original IP packet to its final destination host using standard IP routing.


#### SIG Traffic Rules
Each SIG requires traffic rules specified in a JSON configuration file. This configuration defines the IP prefixes to be forwarded to SIGs in remote ASes. 

A skeleton traffic rule configuration is installed with the `scion-sig` package at /etc/scion/gateway.json. This file contains a single dummy entry with placeholders. The following example illustrates how remote SIGs can be specified, in practice you need to replace `<remote_sig_AS>` with an AS ID (e.g., `1-ffaa:1:abc`) and `<remote_sig_IPnet>` with an IP network in [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing).

```json
{
    "ASes": {
        "<remote_sig_AS>": {
            "Nets": [
                "<remote_sig_IPnet>"
            ]
        }
    },
    "ConfigVersion": 9001
}
```




## Configuration

All SCION configuration files are located in `/etc/scion`. Each service has its own configuration file (for service-specific settings like logging verbosity); however, all derive their core settings from the topology.json file, which serves as the ground truth for the AS configuration.

### topology.json
The topology.json file of an AS specifies all inter-AS connections to neighboring ASes and defines the underlay IP/UDP addresses of services and routers. Both the Router and Control Service (as well as end-host applications like the Gateway) use this file for configuration.

```json
{
   "isd_as": <isd-as>,
   "attributes": [<"core">?],
   "mtu": <int>,
   "border_routers": {
      <router-id>: {
         "internal_addr": "<ip|hostname>:<port>",
         "interfaces": {
            // ... interface definitions ...
         }
      }
      // ...
   },
   "control_service": {
      <cs-id>: {
         "addr": "<ip|hostname>:<port>"
      }
      // ...
   },
   "discovery_service": {
      <ds-id>: {
         "addr": "<ip|hostname>:<port>"
      }
      // ...
   }
}
```

## SCION Networking Utilities

`scion` is a suite of command line utilities for interacting with the SCION network. Use the -h flag with each command for detailed usage information.

Command                | Description
-----------------------|------------------------------------------------------------
scion address          | Display the SCION address(es) for this host.
scion ping             | Test connectivity to a remote SCION host using SCMP echo packets.
scion showpaths        | List available paths between the local AS and a specified SCION AS.
scion traceroute       | Trace the SCION route to a remote SCION AS using SCMP traceroute.
scion version          | Display SCION version information.
