# DEUS Linux Reference

**Version:** 0.2.0
**Last Updated:** 2026-03-28
**Purpose:** Quick reference for Linux-specific commands and paths used by DEUS agents

---

## System Information

| Task | Command |
|---|---|
| OS identification | `cat /etc/os-release`, `hostnamectl` |
| Kernel version | `uname -r`, `uname -a` |
| Distribution | `lsb_release -a` (if available) |
| Hardware info | `lshw`, `lscpu`, `lsmem` |
| Device listing | `lspci`, `lsusb`, `lsblk` |

---

## Package Management

| Distribution | Install | Search | Update | Remove |
|---|---|---|---|---|
| Debian/Ubuntu | `apt install` | `apt search` | `apt update && apt upgrade` | `apt remove` |
| RHEL/CentOS | `yum install` | `yum search` | `yum update` | `yum remove` |
| Fedora | `dnf install` | `dnf search` | `dnf upgrade` | `dnf remove` |
| Arch | `pacman -S` | `pacman -Ss` | `pacman -Syu` | `pacman -R` |

**Security updates:** `apt update && apt upgrade -s` (simulate), `yum update --security`

---

## Service Management (systemd)

| Task | Command |
|---|---|
| Start service | `systemctl start <service>` |
| Stop service | `systemctl stop <service>` |
| Restart service | `systemctl restart <service>` |
| Enable at boot | `systemctl enable <service>` |
| Disable at boot | `systemctl disable <service>` |
| Check status | `systemctl status <service>` |
| List failed | `systemctl --failed` |
| List all services | `systemctl list-units --type=service` |
| View logs | `journalctl -u <service>` |
| Boot analysis | `systemd-analyze blame` |

**Unit file locations:**
- System: `/lib/systemd/system/` (package-provided)
- Custom: `/etc/systemd/system/` (administrator overrides)

---

## Network Configuration

| Task | Command |
|---|---|
| Show interfaces | `ip addr`, `ip link` |
| Show routes | `ip route` |
| DNS config | `/etc/resolv.conf`, `systemd-resolved` |
| Listening ports | `ss -tlnp` |
| Firewall (iptables) | `iptables -L -n -v` |
| Firewall (nftables) | `nft list ruleset` |
| Firewall (ufw) | `ufw status verbose` |

**Config locations:** Netplan (`/etc/netplan/`), NetworkManager (`/etc/NetworkManager/`), systemd-networkd (`/etc/systemd/network/`)

---

## Filesystem & Storage

| Task | Command |
|---|---|
| Disk usage | `df -h`, `du -sh` |
| Block devices | `lsblk`, `blkid` |
| Partition management | `fdisk`, `gdisk`, `parted` |
| LVM | `lvcreate`, `lvextend`, `vgdisplay` |
| ZFS (if installed) | `zpool`, `zfs` (same as FreeBSD) |
| Mount | `mount`, `/etc/fstab` |
| BTRFS | `btrfs subvolume`, `btrfs filesystem` |

---

## User & Permission Management

| Task | Command |
|---|---|
| Add user | `useradd -m <user>` |
| Modify user | `usermod` |
| Delete user | `userdel -r <user>` |
| Add group | `groupadd <group>` |
| Set password | `passwd <user>` |
| Sudo config | `visudo`, `/etc/sudoers.d/` |
| File permissions | `chmod`, `chown` |
| ACLs | `setfacl`, `getfacl` |

---

## Security

| Task | Command |
|---|---|
| SUID files | `find / -perm -4000 -type f` |
| Open ports | `ss -tlnp` |
| Failed logins | `faillock --user <user>`, `journalctl -u sshd` |
| SELinux status | `sestatus`, `getenforce` |
| AppArmor status | `aa-status` |
| Audit logs | `/var/log/audit/audit.log`, `ausearch` |
| Auth logs | `/var/log/auth.log` (Debian), `/var/log/secure` (RHEL) |

---

## Kernel & Modules

| Task | Command |
|---|---|
| Loaded modules | `lsmod` |
| Load module | `modprobe <module>` |
| Module info | `modinfo <module>` |
| Persistent modules | `/etc/modules-load.d/<name>.conf` |
| Blacklist module | `/etc/modprobe.d/blacklist.conf` |
| Kernel parameters | `sysctl -a`, `/etc/sysctl.d/` |
| Kernel config | `/boot/config-$(uname -r)` |
| DKMS | `dkms status`, `dkms install` |

---

## Boot & Recovery

| Task | Command |
|---|---|
| Bootloader config | `/etc/default/grub` → `grub-mkconfig` |
| Kernel parameters | `GRUB_CMDLINE_LINUX` in `/etc/default/grub` |
| initramfs rebuild | `mkinitramfs` / `dracut` / `mkinitcpio` |
| Recovery mode | `init=/bin/bash` kernel parameter |
| EFI entries | `efibootmgr` |
| Boot analysis | `systemd-analyze`, `systemd-analyze blame` |

---

## Log Locations

| Log | Location |
|---|---|
| System journal | `journalctl` |
| Kernel messages | `journalctl -k`, `dmesg` |
| Auth/login | `/var/log/auth.log` (Debian), `/var/log/secure` (RHEL) |
| Package manager | `/var/log/apt/` (Debian), `/var/log/yum.log` (RHEL) |
| Core dumps | `/var/lib/systemd/coredump/`, `coredumpctl` |

---

## Performance Tools

| Tool | Purpose |
|---|---|
| `top` / `htop` | Process monitoring |
| `perf` | CPU profiling and tracing |
| `iostat` | Disk I/O statistics |
| `vmstat` | Virtual memory statistics |
| `sar` (sysstat) | Historical system statistics |
| `ss` | Socket statistics |
| `strace` | System call tracing |
| `bpftrace` | eBPF-based tracing |

---

## Related Documents

- [OS Adaptations Guide](OS_ADAPTATIONS.md)
- [DEUS FreeBSD Reference](DEUS_FREEBSD_REFERENCE.md)
