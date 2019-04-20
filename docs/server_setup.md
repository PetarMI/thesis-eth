### VM creation
1. Install a new vm

    ```bash
    virt-install \
       --name fuzzvm0 \
       --virt-type=kvm --hvm --ram 4096 \
       --disk size=25 \
       --vcpus 2 --os-type linux --os-variant ubuntu18.04 \
       --network bridge=virbr0 \
       --graphics none \
       --location 'http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/' \
       --extra-args='console=ttyS0'
    ```
   
2. Mount some serial ports 
    * `sudo mkdir /mnt/fz`
    * `sudo guestmount --domain fuzzvm0 --inspector /mnt/fz` 
    ```bash
       sudo ln -s /mnt/fz/lib/systemd/system/getty@.service \
       /mnt/fz/etc/systemd/system/getty.target.wants/getty@ttyS0.service
    ```
    
3. Setup ssh
    * ssh-server already installed
    * setup ssh-key
        * `ssh-copy-id -i id_rsa_<name> fuzzvm@192.168.122.204`
    * remove banner
        * in `/etc/ssh` `Banner none`
        * `service ssh restart`
        * in `/pam.d` `sudo vim sshd` and comment out stuff

4. Install docker

4. Clone machine
    * `virsh shutdown <original-vm>`
    * `virt-clone --original fuzzvm0 --name fuzzvm1 --file /var/lib/libvirt/images/fuzzvm1.qcow2`
    * `virt-sysprep --domain fuzzvm1 --enable customize,dhcp-client-state,machine-id --hostname 'fuzzvm1'`
    
5. Install weavenet plugin

### Network creation

1. Create an xml file defining the network 

    ```xml
    <network>
      <name>fuzz-net</name>
      <bridge name="br_fuzz" stp='off' macTableManager="libvirt"/>
      <mtu size="9216"/>
      <ip address="10.194.122.1" netmask="255.255.255.0">
        <dhcp>
          <range start="10.194.122.10" end="10.194.122.100" />
        </dhcp>
      </ip>
    </network>
    ```

2. Create the network

    * `virsh net-define <.xml file>`
    * `virsh net-list --all`
    * `virsh net-start <net-name>`
    * `brctl show`    
    
3. Attach Vms to network 

    * `virsh domiflist <vm-name>`
    * 
     ```
        virsh attach-interface \
          --domain <vm-name> \
          --type network \
          --source <net-name> \
          --model virtio \
          --mac <02:00:aa:0a:01:02> \
          --config --live
     ```
    * `brctl show`
    * `virsh domiflist <vm-name>`
    
4. Configure the new inerface on each VM

    * DHCP
    ```yaml
    ens5:
      dhcp: yes
    ```
    * static IP 
    ```yaml
    ens5:
      dhcp4: no
      addresses: [10.192.122.10/24]
      nameservers:
        addresses: [8.8.4.4,8.8.8.8]
    ```
    * `sudo netplan apply`
    * restart VM or network 
        * `virsh net-destroy <net-name>`
        * `virsh net=start <net-name>`