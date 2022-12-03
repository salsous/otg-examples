import snappi
import dpkt
from scapy.all import *

def port_metrics_ok(api, req, packets):
    res = api.get_metrics(req)
    print(res)
    if packets == sum([m.frames_tx for m in res.port_metrics]) and packets == sum([m.frames_rx for m in res.port_metrics]):
        return True

def flow_metrics_ok(api, req, packets):
    res = api.get_metrics(req)
    print(res)
    if packets == sum([m.frames_tx for m in res.flow_metrics]) and packets == sum([m.frames_rx for m in res.flow_metrics]):
        return True

def wait_for(func, timeout=15, interval=0.2):
    """
    Keeps calling the `func` until it returns true or `timeout` occurs
    every `interval` seconds.
    """
    import time

    start = time.time()

    while time.time() - start <= timeout:
        if func():
            return True
        time.sleep(interval)

    print("Timeout occurred !")
    return False

api = snappi.api(location='https://clab-ixcb2b-ixia-c:8443', verify=False)
cfg = api.config()
# this pushes object of type `snappi.Config` to controller
api.set_config(cfg)
# this retrieves back object of type `snappi.Config` from controller
cfg = api.get_config()

# config has an attribute called `ports` which holds an iterator of type
# `snappi.PortIter`, where each item is of type `snappi.Port` (p1 and p2)
p1, p2 = cfg.ports.port(name="p1", location="eth1").port(name="p2", location="eth2")

# config has an attribute called `flows` which holds an iterator of type
# `snappi.FlowIter`, where each item is of type `snappi.Flow` (f1, f2)
f1, f2, f3 = cfg.flows.flow(name="flow p1->p2").flow(name="flow p2->p1").flow(name="scapy")

# and assign source and destination ports for each
f1.tx_rx.port.tx_name, f1.tx_rx.port.rx_name = p1.name, p2.name
f2.tx_rx.port.tx_name, f2.tx_rx.port.rx_name = p2.name, p1.name
f3.tx_rx.port.tx_name, f3.tx_rx.port.rx_name = p1.name, p2.name

# configure packet size, rate and duration for both flows
f1.size.fixed, f2.size.fixed = 128, 256
for f in cfg.flows:
    # send 1000 packets and stop
    f.duration.fixed_packets.packets = 1000
    # send 1000 packets per second
    f.rate.pps = 1000
    # allow fetching flow metrics
    f.metrics.enable = True

# configure packet with Ethernet, IPv4 and UDP headers for both flows
eth1, ip1, udp1 = f1.packet.ethernet().ipv4().udp()
eth2, ip2, udp2 = f2.packet.ethernet().ipv4().udp()

# set source and destination MAC addresses
eth1.src.value, eth1.dst.value = "00:AA:00:00:04:00", "00:AA:00:00:00:AA"
eth2.src.value, eth2.dst.value = "00:AA:00:00:00:AA", "00:AA:00:00:04:00"

# set source and destination IPv4 addresses
ip1.src.value, ip1.dst.value = "10.0.0.1", "10.0.0.2"
ip2.src.value, ip2.dst.value = "10.0.0.2", "10.0.0.1"

# set incrementing port numbers as source UDP ports
udp1.src_port.increment.start = 5000
udp1.src_port.increment.step = 2
udp1.src_port.increment.count = 10

udp2.src_port.increment.start = 6000
udp2.src_port.increment.step = 4
udp2.src_port.increment.count = 10

# assign list of port numbers as destination UDP ports
udp1.dst_port.values = [4000, 4044, 4060, 4074]
udp2.dst_port.values = [8000, 8044, 8060, 8074, 8082, 8084]

# custom flow from scapy
packet = IP(dst="10.11.12.13", src="10.11.12.14")/UDP()/DNS()
f3.packet.ethernet().custom()

eth3 = f3.packet[0]
eth3.src.value, eth3.dst.value = "00:AA:00:00:04:00", "00:AA:00:00:00:AA"

payload = f3.packet[1]
payload.bytes = packet[0].payload.build().hex()

# print resulting otg configuration
print(cfg)

# push configuration to controller
api.set_config(cfg)

# start transmitting configured flows
ts = api.transmit_state()
ts.state = ts.START
api.set_transmit_state(ts)

# create a port metrics request and filter based on port names
req = api.metrics_request()
req.flow.flow_names = [f.name for f in cfg.flows]

# fetch port metrics
res = api.get_metrics(req)

# wait for port metrics to be as expected
expected = sum([f.duration.fixed_packets.packets for f in cfg.flows])
assert wait_for(lambda: flow_metrics_ok(api, req, expected)), "Metrics validation failed!"
