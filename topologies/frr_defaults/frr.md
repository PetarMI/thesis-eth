Empty container:

* show running-configs:

```
!
frr version 6.0.2
frr defaults traditional
hostname test-cont
log syslog informational
no ipv6 forwarding
service integrated-vtysh-config
!
line vty
!
end
```

* frr.conf

`log syslog informational`

* vtysh.conf

`service integrated-vtysh-config`

* show running-configs after pasting ospf configs:

```
Current configuration:
!
frr version 6.0.2
frr defaults traditional
hostname osboxes
no ipv6 forwarding
service integrated-vtysh-config
!
interface Fa0/0
 description "To 100.0.5.0/24"
!
interface Fa0/1
 description "To Istanbul"
 ip ospf 100 area 0
 ip ospf cost 1
!
interface Fa1/0
 description "To Sofia"
 ip ospf 100 area 0
 ip ospf cost 1
!
router ospf 100
!
line vty
!
end

```