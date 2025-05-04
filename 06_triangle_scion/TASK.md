# Lab 06-2: The Triangle Problem in SCION

As you had experienced in the previous lab, performing even simple traffic engineering operations in BGP can require intricate and fragile BGP attribute tuning. In this lab, you will now see how SCION elegantly supports traffic engineering natively.

You will work on the same triangle topology, but with SCION ASes replacing BGP ASes. For your convenience, the lab is already correctly configured, so no further configuration changes are necessary. Instead, you take the view of a host in the AS scion1, and you have to identify the bad link and route around it, all while using tools provided by SCION.

![06_triangle_scion](./06_triangle_scion.png)

## Tasks

 - **Q1:** How were you able to identify the bad link with high latency? Include the exact SCION commands (including any command line flags) you used.
 - **A1:** \<WRITE YOUR ANSWER HERE\> 
 - **Q2:** SCION provides fine-grained path control to end hosts, whereas in the BGP internet hosts have no control over which paths traffic is routed. Compare both approaches by providing a list of trade-offs for each approach.
 - **A2:** \<WRITE YOUR ANSWER HERE\> 
