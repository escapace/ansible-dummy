# escapace.dummy

Configures persistent Linux dummy interfaces with systemd-networkd. It allocates
one IPv4 `/32` and one IPv6 `/128` per interface, starting at `dummy0`. The role
requires the `systemd-networkd` package but does not install, enable, or start it.

## Variables

- `dummy_number` defaults to `1`. Set a positive integer for the number of
  interfaces to configure.
- `dummy_ipv4_cidr` defaults to `10.254.254.1/24`. Supply an IPv4 CIDR with enough
  addresses for the requested interfaces, excluding the network and broadcast
  addresses.
- `dummy_ipv6_cidr` defaults to `fdb9:e835:7db0:3056::/64`. Supply an IPv6 CIDR with
  enough addresses after its network address for the requested interfaces.
- `dummy_isolation_ingress_zones` defaults to `[public]`. List existing named
  firewalld zones whose traffic must not reach the dummy addresses. Set `[]` to
  remove this role's isolation policies. `ANY` and `HOST` are not accepted as
  ingress zone names.

The role allocates the first address after each pool's network address to
`dummy0`, the next to `dummy1`, and so on. The role refuses to reduce
`dummy_number` while networkd files for higher-numbered dummy interfaces remain,
so their addresses do not silently lose isolation. Before reducing the count,
remove the obsolete interfaces and their `80-dummyN.netdev` and
`80-dummyN.network` files yourself; the role does not delete live interfaces.

When network configuration changes, the role runs `networkctl reload` only if
systemd-networkd is already running. Reloading loads the new definitions and
reconfigures affected interfaces. Stopped services remain stopped, and live
changes are skipped in Ansible check mode.

## Optional firewalld isolation

If `/etc/firewalld/policies` exists, the role requires `firewall-offline-cmd` and
manages `dummy-deny-host.xml` and `dummy-deny-fwd.xml` in that directory. Otherwise,
it skips the integration without installing firewalld or creating its directories.

The policies drop traffic from the selected ingress zones to each managed IPv4
`/32` and IPv6 `/128`, both to host services and through forwarding. They match
the incoming zone and destination address, not the zone of the dummy interface.
The role does not discover default-route interfaces, assign interfaces to zones,
or grant access to services. Choose ingress zones that represent the external
boundary; leave authorized workload and management zones outside that list.

The policies use priority `-1000`. Order conflicting grants after them.
Firewalld's earlier established/related and DNAT handling still apply. Before
writing any configuration, the role validates the existing firewalld installation
and selected zones, including in check mode. Repair invalid existing configuration
before rerunning the role. It also validates the assembled configuration before
a synchronous reload, and reloads only an already-running daemon, never in check
mode. When both firewall and network configuration change, the firewall handlers
run first.
