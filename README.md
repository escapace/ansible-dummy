# ansible-dummy

Configure persistent Linux dummy interfaces with systemd-networkd.

The role allocates one IPv4 `/32` and one IPv6 `/128` per interface from the
configured address pools. Interface names start at `dummy0` and continue through
`dummy{{ dummy_number - 1 }}`.

## Variables

```yaml
dummy_number: 1
dummy_ipv4_cidr: 10.254.254.1/24
dummy_ipv6_cidr: fdb9:e835:7db0:3056::/64
```

`dummy_number` must be a positive integer. Both address pools must contain enough
addresses for the requested interfaces. The role uses the first address after
the network address for `dummy0`.

The managed host must have the `systemd-networkd` package installed. The role
checks for the package but does not enable, start, or reload
`systemd-networkd.service`. When network configuration changes, the role
notifies a handler that runs `networkctl reconfigure` at the normal handler
point near the end of the play if `systemd-networkd.service` is active. A
stopped or unavailable service remains stopped.

## Optional Ferm integration

The role has no Ferm dependency. If both `/etc/ferm/ferm.d` and
`/etc/ferm/vars.d` already exist, it installs isolation configuration for the
managed dummy interfaces and notifies a handler that restarts `ferm.service` if
it is active. It does not install or initialize Ferm.
