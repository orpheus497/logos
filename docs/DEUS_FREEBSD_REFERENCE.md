# DEUS FreeBSD Reference

**Version:** 0.2.0
**Last Updated:** 2026-03-28
**Purpose:** Quick reference for FreeBSD-specific commands and paths used by DEUS agents

---

## System Information

| Task | Command |
|---|---|
| OS version | `freebsd-version`, `uname -r` |
| Full system info | `uname -a` |
| Hostname | `sysctl kern.hostname`, `hostname` |
| Hardware info | `sysctl hw.model`, `sysctl hw.ncpu`, `sysctl hw.physmem` |
| Device listing | `pciconf -lv`, `usbconfig list`, `devinfo -rv` |

---

## Package Management

| Task | Command |
|---|---|
| Install package | `pkg install <name>` |
| Search packages | `pkg search <name>` |
| Package info | `pkg info <name>` |
| Update repository | `pkg update` |
| Upgrade packages | `pkg upgrade` |
| Audit for CVEs | `pkg audit -F` |
| Remove package | `pkg delete <name>` |
| Autoremove orphans | `pkg autoremove` |
| Clean cache | `pkg clean -a` |
| Check integrity | `pkg check -s -a` |

**Ports tree:** `/usr/ports/` — `cd /usr/ports/category/port && make install clean`

---

## Service Management (rc.d)

| Task | Command |
|---|---|
| Start service | `service <name> start` |
| Stop service | `service <name> stop` |
| Restart service | `service <name> restart` |
| Check status | `service <name> status` |
| Enable at boot | `sysrc <name>_enable="YES"` |
| Disable at boot | `sysrc <name>_enable="NO"` |
| List enabled | `service -e` |
| List available | `service -l` |

**Script locations:**
- Base system: `/etc/rc.d/`
- Packages/ports: `/usr/local/etc/rc.d/`
- Configuration: `/etc/rc.conf` (primary), `/etc/rc.conf.local`

---

## Network Configuration

| Task | Command |
|---|---|
| Show interfaces | `ifconfig` |
| Show routes | `netstat -rn` |
| DNS config | `/etc/resolv.conf` |
| Listening ports | `sockstat -l` |
| Firewall rules (pf) | `pfctl -sr` |
| Firewall states (pf) | `pfctl -ss` |
| Firewall reload | `pfctl -f /etc/pf.conf` |
| Firewall test | `pfctl -nf /etc/pf.conf` (parse only) |

**Persistent config:** All network settings in `/etc/rc.conf`:
```
ifconfig_em0="inet 10.0.0.1 netmask 255.255.255.0"
defaultrouter="10.0.0.254"
```

---

## Filesystem & Storage

| Task | Command |
|---|---|
| Disk usage | `df -h`, `du -sh` |
| Partition management | `gpart show`, `gpart add` |
| ZFS pools | `zpool list`, `zpool status` |
| ZFS datasets | `zfs list`, `zfs get all` |
| ZFS snapshots | `zfs snapshot`, `zfs rollback` |
| ZFS send/recv | `zfs send <snap> \| zfs recv <dest>` |
| Boot environments | `bectl list`, `bectl create`, `bectl activate` |
| UFS filesystem | `newfs`, `fsck`, `tunefs` |
| Mount | `mount`, `/etc/fstab` |

---

## User & Permission Management

| Task | Command |
|---|---|
| Add user | `pw useradd <user> -m` |
| Modify user | `pw usermod <user>` |
| Delete user | `pw userdel <user> -r` |
| Add group | `pw groupadd <group>` |
| Set password | `passwd <user>` |
| Lock user | `pw lock <user>` |
| Login classes | `/etc/login.conf`, `cap_mkdb /etc/login.conf` |
| Sudo config | `visudo`, `/usr/local/etc/sudoers` |

---

## Security

| Task | Command |
|---|---|
| SUID files | `find / -perm -4000 -type f` |
| Open ports | `sockstat -l` |
| Security log | `/var/log/security` |
| Auth log | `/var/log/auth.log` |
| Securelevel | `sysctl kern.securelevel` |
| MAC framework | `mac(4)`, `mac_bsdextended`, `mac_portacl` |
| Filesystem integrity | `mtree -f /etc/mtree/` |
| Security advisories | `freebsd-update fetch`, FreeBSD-SA notices |
| Audit (BSM) | `auditd`, `/etc/security/audit_control` |

---

## Kernel & Modules

| Task | Command |
|---|---|
| Loaded modules | `kldstat` |
| Load module | `kldload <module>` |
| Unload module | `kldunload <module>` |
| Persistent modules | `/boot/loader.conf` → `module_load="YES"` |
| Kernel config | `/usr/src/sys/$(uname -m)/conf/` |
| Build custom kernel | `make buildkernel KERNCONF=CUSTOM && make installkernel` |
| Boot-time tunables | `/boot/loader.conf` |
| Runtime tunables | `sysctl`, `/etc/sysctl.conf` |
| Device hints | `/boot/device.hints` |

---

## Boot & Recovery

| Task | Command |
|---|---|
| Bootloader config | `/boot/loader.conf` |
| Boot environments | `bectl create <name>`, `bectl activate <name>` |
| Single-user mode | `boot -s` at loader prompt |
| Boot code install | `gpart bootcode -b /boot/pmbr -p /boot/gptzfsboot -i 1 <disk>` |
| EFI management | `efibootmgr` |
| Boot time | `sysctl kern.boottime` |
| Alternate kernel | `boot kernel.old` at loader prompt |

---

## Log Locations

| Log | Location |
|---|---|
| System messages | `/var/log/messages` |
| Security events | `/var/log/security` |
| Authentication | `/var/log/auth.log` |
| Mail | `/var/log/maillog` |
| Cron | `/var/log/cron` |
| Crash dumps | `/var/crash/` |
| Log rotation | `newsyslog`, `/etc/newsyslog.conf` |

---

## Jails

| Task | Command |
|---|---|
| Create jail | `jail -c name=<n> path=<p> host.hostname=<h>` |
| Config file | `/etc/jail.conf`, `/etc/jail.conf.d/` |
| Start jail | `service jail start <name>` |
| Stop jail | `service jail stop <name>` |
| List jails | `jls` |
| Enter jail | `jexec <name> /bin/sh` |
| Enable at boot | `sysrc jail_enable="YES"` |
| Resource limits | `rctl -a jail:<name>:memoryuse:deny=2G` |

---

## Performance Tools

| Tool | Purpose |
|---|---|
| `top` | Process monitoring |
| `systat` | Real-time system statistics |
| `vmstat` | Virtual memory statistics |
| `iostat` | Disk I/O statistics |
| `gstat` | GEOM I/O statistics |
| `dtrace` | Dynamic tracing (native) |
| `pmcstat` | Hardware performance counters |
| `procstat` | Process statistics |
| `ktrace`/`kdump` | System call tracing |
| `arcstat` | ZFS ARC statistics |

---

## Key FreeBSD Concepts

| Concept | Description |
|---|---|
| `/etc/rc.conf` | Centralized system configuration file |
| `/usr/local/` | Third-party software prefix (ports/packages) |
| `rc.subr` | Framework for writing rc.d service scripts |
| `pf` | Packet Filter firewall (from OpenBSD) |
| Jails | OS-level virtualization (lightweight containers) |
| ZFS | Native filesystem with snapshots, replication, boot environments |
| DTrace | Dynamic tracing framework (native, not add-on) |
| Securelevel | Kernel security level enforcement |
| Ports | Source-based package building system |

---

## Related Documents

- [OS Adaptations Guide](OS_ADAPTATIONS.md)
- [DEUS Linux Reference](DEUS_LINUX_REFERENCE.md)
