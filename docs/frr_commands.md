#### FRR service
* `systemctl enable frr`
* `systemctl start frr`
* `systemctl status frr`
* `systemctl reload frr`
* `systemctl daemon-reload`


#### OSPF
* `ospf router-id A.B.C.D`
* `passive-interface INTERFACE`
	* no OSPF on this interface
* `network A.B.C.D/M area A.B.C.D` 
	* OSPF enabled interface
* area commands
* `ip ospf area AREA [ADDR]`
	* another way of enabling OSPF
* `ip ospf cost`	