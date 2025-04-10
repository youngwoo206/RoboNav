#!/bin/bash
INTERFACE="wlp2s0"
ethernet_interface="eno1"
bridge_interface="br0"
sudo ip link set wlp2s0 up;
sudo ip link add br0 type bridge;
sudo ip link set dev br0 up
sudo ip link set dev eno1 up;

counter=0
while ! ip link show "$ethernet_interface" | grep -q ",UP>"; do
    if [ "$counter" -ge "150" ]; then
        echo "Timed out";
        exit 1
    fi

    ip link show "$ethernet_interface";
    sleep 1
    ((counter++))
done
counter = 0
while ! ip link show "$bridge_interface" | grep -q "state UP"; do
    if [ "$counter" -ge "150" ]; then
        echo "Timed out";
        exit 1
    fi

    ip link show "$bridge_interface";
    sleep 1
    ((counter++))
done

counter=0
while ! ip link show "$INTERFACE" | grep -q "state UP"; do
    if [ "$counter" -ge "150" ]; then
        echo "Timed out";
        exit 1
    fi

    ip link show "$INTERFACE";
    sleep 1
    ((counter++))
done
sudo ip link set dev wlp2s0 master br0
sudo ip link set dev eno1 master br0

echo "Interface $INTERFACE is up, running command..."
