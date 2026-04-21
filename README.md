# ETH Computer Networks — Kathara Project

Solutions for ETH Zürich's *Computer Networks* hands-on network-engineering project (Spring 2025), emulated end-to-end in Kathara on Docker with FRR routing. **Final grade: 90% (full +0.25 bonus).**

## Labs

| Lab | Topic |
|---|---|
| `01_baby_steps` | Kathara / Docker network fundamentals |
| `02_line_of_routers` | Static routing across a linear topology |
| `03_ospf` | Intra-AS routing with OSPF |
| `04_bgp` | Inter-AS routing with BGP — policy, route selection, filters |
| `05_scion` | Next-generation routing with SCION, ETH's clean-slate internet architecture |
| `06_triangle_bgp` / `06_triangle_scion` | Failure-mode comparison: BGP vs SCION under link failure |
| `07_scion_ip_gateway` | SCION ↔ IP interop through a gateway |

All configurations in FRR and standard Linux networking, emulated in Kathara-on-Docker.

## Running a lab

Each `0X_*` folder is self-contained with its own topology and `TASK.md`.

```bash
kathara lstart     # bring the topology up
kathara lclean     # tear it down
```

See [`DOCS.md`](./DOCS.md) for the full technology reference.

---

## Original project description

# Computer Networks 2025: Project Kathara

This project provides hands-on experience in network engineering through a series of interactive labs and exercises. It covers the theoretical foundations of network protocols like OSPF, BGP and SCION, and guides you through network configurations and troubleshooting scenarios you might encounter in real deployments.

# Project Structure

The project is split into two phases, each subdivided into four labs. Labs increase in complexity and are intended to be completed in sequence. Each lab is contained in its own folder and includes a `TASK.md` file with implementation assignments and questions testing your understanding.

See [`DOCS.md`](./DOCS.md) for extensive documentation about the technologies used throughout the labs.
