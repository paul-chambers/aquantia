# -d /bin/bash

NET_DIR="/sys/class/net/"
CFG_DIR="/etc/sysconfig/network-scripts/"
IFCFG="ifcfg-"

for d in $NET_DIR/*
do
device="$(basename "$d")"
driver_path="$(readlink -f "$d/device/driver/module")"
driver="$(basename "$driver_path")"

if [ "$driver" == "atlantic" ]; then
    cfg_file="$CFG_DIR$IFCFG$device"
    if [ ! -f "$cfg_file" ]; then
        cat << EOF > "$cfg_file"
#aQuantia AQtion driver
DEVICE="$device"
BOOTPROTO=dhcp
ONBOOT=yes
EOF
fi
fi

done
